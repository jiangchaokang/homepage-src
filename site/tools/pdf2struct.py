#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf2struct.py —— 规则性文本型 PDF(非扫描件) -> 「图片 + 文本」结构化 JSON

输出:
  output/images/*.png|jpg      每张嵌入图片独立文件
  output/pages/page_XXX.json   每页结构化结果
  output/document.json         全量结果
  output/document.md           按阅读顺序还原的图文混排预览
  python3 pdf2struct.py "RL.pdf" -o output

内置脱敏: 公司名/版权声明/作者/导出日期/部门号/邮箱/重复页眉页脚/重复 LOGO 全部过滤。

用法: python3 pdf2struct.py input.pdf -o output
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:                                    # PyMuPDF >= 1.24 推荐 import 名
    import pymupdf
except ModuleNotFoundError:             # 兼容旧版
    import fitz as pymupdf              # type: ignore

LOG = logging.getLogger("pdf2struct")


# ============================== 0. 常量 =====================================
def _flag(name: str, default: int) -> int:
    return int(getattr(pymupdf, name, default))


# 保留连字/空白 + CJK 不插伪空格 + 裁到 mediabox；不含 PRESERVE_IMAGES(图片单独处理)
TEXT_FLAGS = (
    _flag("TEXT_PRESERVE_LIGATURES", 1)
    | _flag("TEXT_PRESERVE_WHITESPACE", 2)
    | _flag("TEXT_INHIBIT_SPACES", 8)
    | _flag("TEXT_MEDIABOX_CLIP", 64)
)
BOLD_BIT = 1 << 4                       # span["flags"] bit4 = bold
CJK = r"\u2e80-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef"
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\u200b-\u200f\u202a-\u202e\ufeff\u00ad]")
_BOLD_NAME = re.compile(r"bold|black|heavy|semib|demi", re.I)


# ============================== 1. 脱敏规则 ==================================
# ① 命中即整行丢弃（公司/版权/作者/导出信息等）
DROP_RULES: list[re.Pattern] = [re.compile(p, re.I) for p in (
    r"\bcopyright\b|©",
    r"all\s+rights\s+reserved",
    r"industrial\s+property\s+rights",
    r"regarding\s+any\s+disposal",
    r"robert\s*bosch|\bbosch\b|\bRB[A-Z]{2}\b",     # 公司名（如需保留句子可移到 MASK_RULES）
    r"docupedia",
    r"^\s*(author|作者|owner|editor)\s*[:：]",
    r"^\s*(date|日期|exported?|导出)\s*[:：]",
    r"^\s*\d{1,2}[-/][A-Za-z]{3}[-/]\d{2,4}(\s+\d{1,2}:\d{2}(:\d{2})?)?\s*$",
    r"\b(confidential|internal\s+use\s+only|company\s+restricted)\b",
)]
# ② 命中即掩码（保留其余正文）
MASK_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL]"),
    (re.compile(r"https?://\S+", re.I), "[URL]"),
    (re.compile(r"\b[A-Z]{2,3}-[A-Z]{2,3}(?:/[A-Z0-9]+(?:-[A-Z0-9]+)*)+\b"), "[DEPT]"),
    (re.compile(r"\b(bosch|docupedia)\w*\b", re.I), "[COMPANY]"),
]


def clean_text(s: str) -> str:
    s = _CTRL.sub("", s)
    return re.sub(r"[ \t\u3000]{2,}", " ", s).strip()


def redact(s: str) -> str | None:
    """返回脱敏后的文本；None 表示整行应丢弃。"""
    for rx in DROP_RULES:
        if rx.search(s):
            return None
    for rx, rep in MASK_RULES:
        s = rx.sub(rep, s)
    # 掩码后只剩占位符/标点 -> 无信息量，丢弃
    if not re.sub(r"\[[A-Z_]+\]|[\W_]+", "", s, flags=re.UNICODE):
        return None
    return s.strip() or None


def load_extra_rules(path: str | None) -> None:
    """rules.json: {"drop": ["正则", ...], "mask": [["正则","替换"], ...]}"""
    if not path:
        return
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    DROP_RULES.extend(re.compile(p, re.I) for p in cfg.get("drop", []))
    MASK_RULES.extend((re.compile(p, re.I), r) for p, r in cfg.get("mask", []))


def norm_key(s: str) -> str:
    """页眉/页脚模板归一化：数字 -> #，便于跨页比对（"Xxx 3 | 18" == "Xxx 7 | 18"）"""
    return re.sub(r"\s+", " ", re.sub(r"\d+", "#", s)).strip().lower()


# ============================== 2. 配置 & 数据结构 ===========================
@dataclass
class Cfg:
    out_dir: Path
    dpi: int = 200                # 内联图/解码失败时的裁剪渲染分辨率
    min_img_pt: float = 20.0      # 版面上小于该尺寸(pt)的图视为装饰线，丢弃
    min_img_px: int = 16          # 像素太小同样丢弃
    y_tol: float = 6.0            # 阅读顺序：同一行带的 y 容差(pt)
    heading_ratio: float = 1.15   # 标题字号阈值 = 正文字号 * ratio
    band: float = 0.12            # 页眉/页脚判定带（页高比例）
    boiler_ratio: float = 0.5     # 跨页重复率阈值（页眉页脚 / LOGO）
    keep_breaks: bool = False     # 段内是否保留换行
    redact: bool = True
    drop_repeated_images: bool = True


@dataclass
class Line:
    text: str
    bbox: tuple
    size: float
    max_size: float
    font: str
    bold: bool


# ============================== 3. 页眉页脚模板识别 ==========================
def detect_boilerplate(doc, pages: list[int], cfg: Cfg) -> set[str]:
    if len(pages) < 2:
        return set()
    counter: Counter = Counter()
    for pno in pages:
        page = doc[pno]
        h = page.rect.height or 1.0
        keys = set()
        for x0, y0, x1, y1, txt, _no, btype in page.get_text("blocks"):
            if btype != 0:
                continue
            if not (y1 <= h * cfg.band or y0 >= h * (1 - cfg.band)):
                continue
            for ln in txt.splitlines():
                k = norm_key(clean_text(ln))
                if k:
                    keys.add(k)
        counter.update(keys)
    thr = max(2, round(len(pages) * cfg.boiler_ratio))
    return {k for k, v in counter.items() if v >= thr}


# ============================== 4. 文本抽取 ==================================
def _span_style(sp: dict) -> tuple[float, str, bool]:
    font = sp.get("font", "") or ""
    bold = bool(int(sp.get("flags", 0)) & BOLD_BIT) or bool(_BOLD_NAME.search(font))
    return round(float(sp.get("size", 0.0)), 1), font, bold


def extract_page_lines(page, cfg: Cfg, boiler: set[str]) -> list[list[Line]]:
    """返回「PDF 原生 block -> 行列表」，已完成清洗/脱敏/页眉页脚剔除。"""
    h = page.rect.height or 1.0
    out: list[list[Line]] = []
    for blk in page.get_text("dict", flags=TEXT_FLAGS).get("blocks", []):
        if blk.get("type", 0) != 0:
            continue
        lines: list[Line] = []
        for ln in blk.get("lines", []):
            spans = [s for s in ln.get("spans", []) if (s.get("text") or "").strip()]
            if not spans:
                continue
            text = clean_text("".join(s["text"] for s in spans))
            if not text:
                continue
            bbox = tuple(round(float(v), 2) for v in ln["bbox"])
            in_band = bbox[3] <= h * cfg.band or bbox[1] >= h * (1 - cfg.band)
            if in_band and norm_key(text) in boiler:      # 重复页眉/页脚
                continue
            if cfg.redact:
                red = redact(text)
                if red is None:
                    continue
                text = red
            styles = [_span_style(s) for s in spans]
            w = [max(len(s["text"].strip()), 1) for s in spans]
            size = max({st[0] for st in styles},
                       key=lambda z: sum(wi for st, wi in zip(styles, w) if st[0] == z))
            font = Counter(st[1] for st in styles).most_common(1)[0][0]
            bold = sum(wi for st, wi in zip(styles, w) if st[2]) * 2 >= sum(w)
            lines.append(Line(text, bbox, size, max(st[0] for st in styles), font, bold))
        if lines:
            lines.sort(key=lambda l: (l.bbox[1], l.bbox[0]))
            out.append(lines)
    return out


def group_lines(lines: list[Line], gap_factor: float = 1.8) -> list[list[Line]]:
    """同一 PDF block 内按「样式突变 / 行距突变」再切分，避免标题与正文粘连。"""
    groups: list[list[Line]] = []
    for ln in lines:
        if groups:
            prev = groups[-1][-1]
            same = abs(ln.size - prev.size) < 0.6 and ln.bold == prev.bold
            lh = max(prev.bbox[3] - prev.bbox[1], ln.bbox[3] - ln.bbox[1], 1.0)
            if same and (ln.bbox[1] - prev.bbox[3]) <= gap_factor * lh:
                groups[-1].append(ln)
                continue
        groups.append([ln])
    return groups


def join_lines(lines: list[Line], keep_breaks: bool) -> str:
    if keep_breaks:
        return "\n".join(l.text for l in lines)
    out = ""
    for t in (l.text for l in lines):
        if not out:
            out = t
        elif out.endswith("-") and re.match(r"[a-z]", t):        # 英文断词
            out = out[:-1] + t
        elif re.search(f"[{CJK}]$", out) or re.match(f"[{CJK}]", t):   # 中文不加空格
            out += t
        else:
            out += " " + t
    return out


_NUM_HEAD = re.compile(rf"^(第[一二三四五六七八九十百]+[章节篇]|\d+(\.\d+){{0,3}})[\s、.:：)]")


def is_heading(text: str, size: float, bold: bool, body: float, cfg: Cfg) -> bool:
    t = text.strip()
    if not t or len(t) > 120 or "\n" in t:
        return False
    if size >= body * cfg.heading_ratio:
        return True
    if _NUM_HEAD.match(t) and len(t) <= 80 and (bold or size >= body):
        return True
    if bold and size >= body - 0.1 and len(t) <= 60 and not t.endswith(("。", ".", "，", ",", "；", ";")):
        return True
    return False


def make_text_block(group: list[Line], pno: int, idx: int, cfg: Cfg, body: float) -> dict:
    w = [max(len(l.text), 1) for l in group]
    size = round(sum(l.size * wi for l, wi in zip(group, w)) / sum(w), 1)
    max_size = round(max(l.max_size for l in group), 1)
    bold = sum(wi for l, wi in zip(group, w) if l.bold) * 2 >= sum(w)
    text = join_lines(group, cfg.keep_breaks)
    return {
        "id": f"p{pno:03d}_t{idx:02d}",
        "type": "text",
        "content": text,
        "bbox": [min(l.bbox[0] for l in group), min(l.bbox[1] for l in group),
                 max(l.bbox[2] for l in group), max(l.bbox[3] for l in group)],
        "font": Counter(l.font for l in group).most_common(1)[0][0],
        "font_size": size,
        "max_font_size": max_size,
        "bold": bold,
        "is_heading": is_heading(text, max_size, bold, body, cfg),
        "heading_level": None,          # 稍后按全局字号排名回填
        "line_count": len(group),
        "char_count": len(text),
    }


# ============================== 5. 图片抽取 ==================================
def decode_image(doc, xref: int) -> tuple[bytes | None, str | None]:
    """优先原始字节(JPG/PNG 零损失)；CMYK / 带透明蒙版则转 PNG。"""
    try:
        info = doc.extract_image(xref)
    except Exception:
        return None, None
    if not info or not info.get("image"):
        return None, None
    ext = str(info.get("ext", "png")).lower()
    smask = int(info.get("smask", 0) or 0)
    ncomp = int(info.get("colorspace", 3) or 3)
    if not smask and ncomp <= 3 and ext in ("png", "jpeg", "jpg"):
        return info["image"], ("jpg" if ext.startswith("jp") else "png")
    try:
        pix = pymupdf.Pixmap(doc, xref)
        if pix.colorspace and pix.colorspace.n == 4:                  # CMYK -> RGB
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        if smask:
            try:
                pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(doc, smask))  # 合并 alpha
            except Exception:
                pass
        return pix.tobytes("png"), "png"
    except Exception:
        return None, None


def extract_page_images(doc, page, pno: int, cfg: Cfg, st: dict) -> list[dict]:
    try:
        infos = page.get_image_info(xrefs=True)          # 真实绘制位置(含内联图)
    except Exception:
        infos = [{"bbox": tuple(b[:4]), "xref": 0} for b in page.get_text("blocks") if b[6] == 1]

    blocks, seen, idx = [], set(), 0
    for info in infos:
        rect = pymupdf.Rect(info["bbox"]) & page.rect
        if rect.is_empty or rect.width < cfg.min_img_pt or rect.height < cfg.min_img_pt:
            continue
        xref = int(info.get("xref", 0) or 0)
        px, py = int(info.get("width", 0) or 0), int(info.get("height", 0) or 0)
        if px and py and (px < cfg.min_img_px or py < cfg.min_img_px):
            continue
        sig = (xref, round(rect.x0), round(rect.y0), round(rect.x1), round(rect.y1))
        if sig in seen:                                   # 同位置重复绘制
            continue
        seen.add(sig)

        data, ext = decode_image(doc, xref) if xref else (None, None)
        if data is None:                                  # 内联图/异常 -> 裁剪渲染
            data, ext = page.get_pixmap(clip=rect, dpi=cfg.dpi).tobytes("png"), "png"

        digest = hashlib.sha1(data).hexdigest()
        rel = st["by_hash"].get(digest)
        idx += 1
        if rel is None:                                   # 相同图片全局只落一份盘
            rel = f"images/p{pno:03d}_img{idx:02d}.{ext}"
            (cfg.out_dir / rel).write_bytes(data)
            st["by_hash"][digest] = rel
        st["pages_of_hash"].setdefault(digest, set()).add(pno)

        blocks.append({
            "id": f"p{pno:03d}_i{idx:02d}",
            "type": "image",
            "content": rel,                               # 相对 output/ 的路径
            "bbox": [round(rect.x0, 2), round(rect.y0, 2), round(rect.x1, 2), round(rect.y1, 2)],
            "xref": xref,
            "pixel_size": [px, py],
            "format": ext,
            "bytes": len(data),
            "sha1": digest,
        })
    return blocks


# ============================== 6. 阅读顺序 ==================================
def reading_order(items: list[dict], y_tol: float) -> list[dict]:
    """先按 y0 聚成行带(容差 y_tol)，带内再按 x0 从左到右。"""
    items = sorted(items, key=lambda it: (it["bbox"][1], it["bbox"][0]))
    ordered, row = [], []
    for it in items:
        if row and it["bbox"][1] - row[0]["bbox"][1] > y_tol:
            ordered += sorted(row, key=lambda x: x["bbox"][0])
            row = []
        row.append(it)
    ordered += sorted(row, key=lambda x: x["bbox"][0])
    return ordered


# ============================== 7. 主流程 ====================================
def parse_pdf(pdf: Path, cfg: Cfg, page_sel: set[int] | None, password: str | None) -> dict:
    doc = pymupdf.open(pdf)
    if doc.needs_pass and not doc.authenticate(password or ""):
        raise SystemExit("PDF 已加密，请用 --password 提供口令")

    pages = [i for i in range(doc.page_count) if page_sel is None or (i + 1) in page_sel]
    (cfg.out_dir / "images").mkdir(parents=True, exist_ok=True)
    (cfg.out_dir / "pages").mkdir(parents=True, exist_ok=True)

    boiler = detect_boilerplate(doc, pages, cfg)
    LOG.info("页眉/页脚模板 %d 条已识别并过滤", len(boiler))

    # --- Phase A: 抽取原料 -------------------------------------------------
    st = {"by_hash": {}, "pages_of_hash": {}}
    raw: list[tuple] = []
    for pno in pages:
        page = doc[pno]
        groups = extract_page_lines(page, cfg, boiler)
        images = extract_page_images(doc, page, pno + 1, cfg, st)
        if not groups and images:
            LOG.warning("第 %d 页无可选文本，疑似扫描页（本工具面向文本型 PDF，需 OCR）", pno + 1)
        raw.append((pno, page.rect, page.rotation, groups, images))

    # --- Phase B: 全局统计（正文字号 / LOGO 判定）--------------------------
    cnt: Counter = Counter()
    for _p, _r, _rot, groups, _im in raw:
        for g in groups:
            for l in g:
                cnt[l.size] += max(len(l.text), 1)
    body = cnt.most_common(1)[0][0] if cnt else 10.0
    LOG.info("正文字号推定为 %.1f pt", body)

    logos: set[str] = set()
    if cfg.drop_repeated_images and len(pages) >= 3:
        thr = max(3, round(len(pages) * cfg.boiler_ratio))
        logos = {h for h, ps in st["pages_of_hash"].items() if len(ps) >= thr}
    for h in logos:                                       # 删除疑似 LOGO/水印文件
        f = cfg.out_dir / st["by_hash"][h]
        f.unlink(missing_ok=True)
        LOG.info("已过滤跨页重复图片（疑似 LOGO/水印）: %s", f.name)

    # --- Phase C: 组装 -----------------------------------------------------
    pages_out, heading_sizes = [], set()
    for pno, rect, rot, groups, images in raw:
        tblocks: list[dict] = []
        for g in groups:
            for sub in group_lines(g):
                tblocks.append(make_text_block(sub, pno + 1, len(tblocks) + 1, cfg, body))
        iblocks = [b for b in images if b["sha1"] not in logos]
        heading_sizes |= {b["max_font_size"] for b in tblocks if b["is_heading"]}
        pages_out.append({
            "page": pno + 1,
            "size": {"width": round(rect.width, 2), "height": round(rect.height, 2)},
            "rotation": rot,
            "text_blocks": tblocks,
            "image_blocks": iblocks,
        })

    levels = {s: min(i + 1, 6) for i, s in enumerate(sorted(heading_sizes, reverse=True))}
    for p in pages_out:
        for b in p["text_blocks"]:
            if b["is_heading"]:
                b["heading_level"] = levels.get(b["max_font_size"], 6)
        merged = reading_order(p["text_blocks"] + p["image_blocks"], cfg.y_tol)
        p["content_order"] = [{
            "order": i,
            "type": b["type"],
            "content": b["content"],
            "bbox": b["bbox"],
            "ref": b["id"],
            **({"is_heading": b["is_heading"], "heading_level": b["heading_level"],
                "font_size": b["font_size"]} if b["type"] == "text"
               else {"pixel_size": b["pixel_size"], "format": b["format"]}),
        } for i, b in enumerate(merged)]

    meta = {}
    for k, v in (doc.metadata or {}).items():
        if not v or k in ("author", "producer", "creator", "keywords", "subject"):
            continue                                       # 直接丢弃可能含企业信息的字段
        rv = redact(clean_text(str(v))) if cfg.redact else str(v)
        if rv:
            meta[k] = rv

    doc.close()
    return {
        "source_file": (redact(pdf.name) or "document.pdf") if cfg.redact else pdf.name,
        "page_count": len(pages_out),
        "body_font_size": body,
        "engine": f"PyMuPDF {getattr(pymupdf, '__version__', '?')}",
        "redacted": cfg.redact,
        "metadata": meta,
        "pages": pages_out,
    }


def write_outputs(res: dict, cfg: Cfg, pretty: bool) -> None:
    ind = 2 if pretty else None
    for p in res["pages"]:
        (cfg.out_dir / "pages" / f"page_{p['page']:03d}.json").write_text(
            json.dumps(p, ensure_ascii=False, indent=ind), encoding="utf-8")
    (cfg.out_dir / "document.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=ind), encoding="utf-8")

    md = []
    for p in res["pages"]:
        md.append(f"<!-- ===== page {p['page']} ===== -->")
        for it in p["content_order"]:
            if it["type"] == "image":
                md.append(f"![{Path(it['content']).name}]({it['content']})")
            elif it.get("is_heading"):
                md.append("#" * (it.get("heading_level") or 2) + " " + it["content"])
            else:
                md.append(it["content"])
        md.append("")
    (cfg.out_dir / "document.md").write_text("\n\n".join(md), encoding="utf-8")


def parse_pages(expr: str | None) -> set[int] | None:
    if not expr:
        return None
    out: set[int] = set()
    for part in expr.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="文本型 PDF -> 图文结构化 JSON（内置脱敏）")
    ap.add_argument("pdf", help="输入 PDF（文字可选中）")
    ap.add_argument("-o", "--out", default="output", help="输出目录，默认 output")
    ap.add_argument("--pages", help='页码筛选，如 "1-5,8"')
    ap.add_argument("--password", help="加密 PDF 口令")
    ap.add_argument("--rules", help="追加脱敏规则 JSON")
    ap.add_argument("--dpi", type=int, default=200, help="内联图裁剪渲染 DPI，默认 200")
    ap.add_argument("--min-img-pt", type=float, default=20.0, help="最小图片版面尺寸(pt)")
    ap.add_argument("--y-tol", type=float, default=6.0, help="阅读顺序行带容差(pt)")
    ap.add_argument("--heading-ratio", type=float, default=1.15, help="标题字号倍数阈值")
    ap.add_argument("--keep-linebreaks", action="store_true", help="段内保留换行")
    ap.add_argument("--keep-repeated-images", action="store_true", help="不过滤跨页重复图片")
    ap.add_argument("--no-redact", action="store_true", help="关闭脱敏（不推荐）")
    ap.add_argument("--compact", action="store_true", help="JSON 不缩进")
    a = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    pdf = Path(a.pdf).expanduser().resolve()
    if not pdf.is_file():
        LOG.error("文件不存在: %s", pdf)
        return 2
    load_extra_rules(a.rules)

    cfg = Cfg(out_dir=Path(a.out).expanduser().resolve(), dpi=a.dpi, min_img_pt=a.min_img_pt,
              y_tol=a.y_tol, heading_ratio=a.heading_ratio, keep_breaks=a.keep_linebreaks,
              redact=not a.no_redact, drop_repeated_images=not a.keep_repeated_images)

    res = parse_pdf(pdf, cfg, parse_pages(a.pages), a.password)
    write_outputs(res, cfg, pretty=not a.compact)

    nt = sum(len(p["text_blocks"]) for p in res["pages"])
    ni = sum(len(p["image_blocks"]) for p in res["pages"])
    nh = sum(1 for p in res["pages"] for b in p["text_blocks"] if b["is_heading"])
    LOG.info("完成: %d 页 / 文本块 %d(标题 %d) / 图片 %d 张 -> %s",
             res["page_count"], nt, nh, ni, cfg.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())