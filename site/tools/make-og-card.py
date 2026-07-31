#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph / Twitter share card.

Link previews are the only thing most people ever see of a personal site — a
shared URL without a card is a bare blue line with a near-zero click rate.
This renders one deterministic PNG from the same brand palette as the site, so
the card can be regenerated whenever the headline changes.

Usage:  python3 tools/make-og-card.py
Output: assets/img/chaokang_jiang/og-card.png
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/chaokang_jiang/og-card.png"
AVATAR = ROOT / "assets/img/chaokang_jiang/avatar.png"
FONTS = Path("/usr/share/fonts/truetype/noto")
HAN = ROOT / "tools/blog_video_maker/fonts/SourceHanSansSC-Regular.otf"

W, H = 1200, 630
INK = (255, 255, 255)
MUTED = (154, 166, 189)
CYAN = (56, 225, 239)
PURPLE = (176, 155, 255)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def radial(size, center, radius, colour, strength):
    """A soft colour bloom, matching the site's hero gradients."""
    w, h = size
    layer = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(layer)
    d.ellipse(
        [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
        fill=int(255 * strength),
    )
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.55))
    tint = Image.new("RGB", (w, h), colour)
    return tint, layer


def main() -> None:
    card = Image.new("RGB", (W, H), (8, 10, 18))

    for center, radius, colour, strength in (
        ((150, -40), 520, (56, 130, 255), 0.42),
        ((1180, 90), 520, (150, 110, 255), 0.36),
        ((980, 700), 460, (56, 225, 239), 0.20),
    ):
        tint, mask = radial((W, H), center, radius, colour, strength)
        card.paste(tint, (0, 0), mask)

    draw = ImageDraw.Draw(card)

    # Portrait, circular, on the right.
    avatar = Image.open(AVATAR).convert("RGB")
    side = min(avatar.size)
    avatar = avatar.crop(
        (
            (avatar.width - side) // 2,
            (avatar.height - side) // 2,
            (avatar.width + side) // 2,
            (avatar.height + side) // 2,
        )
    ).resize((272, 272), Image.LANCZOS)
    mask = Image.new("L", (272, 272), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 271, 271], fill=255)
    card.paste(avatar, (862, 179), mask)
    draw.ellipse([860, 177, 1135, 452], outline=(255, 255, 255), width=2)

    x = 76
    draw.text((x, 92), "CHAOKANG JIANG", font=font("NotoSans-Bold.ttf", 26), fill=CYAN)
    draw.text(
        (x + int(draw.textlength("CHAOKANG JIANG", font=font("NotoSans-Bold.ttf", 26))) + 18, 89),
        "蒋超康",
        font=ImageFont.truetype(str(HAN), 27),
        fill=CYAN,
    )

    headline = font("NotoSans-Bold.ttf", 56)
    draw.text((x, 150), "Generative world models", font=headline, fill=INK)
    draw.text((x, 218), "for driving simulation", font=headline, fill=PURPLE)

    body = font("NotoSans-Regular.ttf", 26)
    for i, line in enumerate(
        [
            "7-camera surround world model, 35 denoising steps to 4.",
            "Closed-loop simulation, end-to-end driving, 3D/4D perception.",
        ]
    ):
        draw.text((x, 316 + i * 40), line, font=body, fill=MUTED)

    chip_font = font("NotoSans-SemiBold.ttf", 21)
    cx = x
    for label in ("ICML 2026 Spotlight", "T-PAMI", "CVPR", "Bosch (XC-CN)"):
        tw = draw.textlength(label, font=chip_font)
        draw.rounded_rectangle([cx, 444, cx + tw + 32, 490], radius=23, outline=(150, 165, 195), width=2)
        draw.text((cx + 16, 455), label, font=chip_font, fill=(224, 232, 245))
        cx += tw + 32 + 13

    draw.text((x, 548), "jiangchaokang.github.io", font=font("NotoSans-Medium.ttf", 24), fill=(130, 143, 168))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    card.save(OUT, optimize=True)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
