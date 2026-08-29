# AGENTS.md — Resume Template Maintenance Guide

Rules for any human or AI assistant editing this résumé. Follow them exactly so
the template stays clean, consistent, and **one page per language**.

## 1. Files & build
| File | Role |
|------|------|
| `resume.sty` | Design system: all layout/typography parameters live here. |
| `main_cn.tex` / `main_en.tex` | Content only (Chinese / English). Identical structure. |
| `photo.jpg` | ID photo (portrait ratio). |
| `clean.sh` | Compile both + delete temp files. |
| `readme.md`, `AGENTS.md` | Docs. |

Build with **`./clean.sh`** (runs XeLaTeX twice — required by the TikZ
`remember picture` border/photo — then removes all aux files). Never commit
`*.aux/*.log/*.out/*.synctex.gz` etc.

## 2. Hard constraints (do not violate)
1. **One page each.** After editing, verify `pdfinfo main_xx.pdf | grep Pages`
   returns `1` for **both** files. Recompile twice before trusting the count
   (it can oscillate when content sits exactly on the boundary).
2. **Identical layout parameters** for CN and EN. All shared sizing/spacing/
   color is defined **once** in `resume.sty`. Never tune layout in only one
   `.tex`. If only one language overflows, **shorten that language's text** —
   do not change a layout parameter for just one version.
3. **Edit layout only in `resume.sty`; edit wording only in the `.tex` files.**
   Do not hard-code `\vspace`, colors, or rules inside the `.tex` files.

## 3. Design tokens (change here, globally)
Defined at the top of `resume.sty`:
- Colors — **exactly two**: `themeblue` (titles/icons/border/links) and
  `bodyblack` (text); `ruleblue` is only the lighter divider tint. Do **not**
  introduce new colors.
- Vertical rhythm: `\SecBeforeSkip`, `\SecAfterSkip`, `\TitleRuleGap`,
  `\BlockSkip`; list spacing via `\setlist` (`itemsep`/`topsep`). Keep the
  rhythm uniform — same value for every peer element.
- Sizes: `\RuleWeight`, `\BorderWeight`, `\BorderInset`, `\DateColW`,
  `\PhotoHeight`, `\PhotoColW`, `\IconColW`, `\InfoArrayStretch`, `\NameGap`.

## 4. Layout rules
- **Border**: single thin line, `\BorderInset` equal on all four sides. No
  double lines, no side/bottom bars.
- **Top block**: no banner, no “Personal Info / 个人信息” heading. Name (`\zihao{3}`,
  themeblue) then the aligned info grid; photo is a top-right overlay
  (`\headerphoto`) whose bottom sits ~2 mm above the Education rule. Don't turn
  the photo back into an in-flow column.
- **Alignment**: labels use fixed-width boxes (`\cnlabel` / `\enlabel`) so all
  colons and values line up. Single-line rows use `\entry{date}{body}{right}`.
- **Indentation hierarchy**: section → `\project{…}` bullet (level 1) →
  `enumerate` numbers (level 2, one indent deeper). Don't nest further.
- **Bottom margin**: the last section must not touch the border — keep a safe
  gap comparable to the top.

## 5. Links & icons (keep it to two colors, minimal noise)
- Links are themeblue, **no underline**.
- A repository link **is** its GitHub icon: `\ghlink{url}` → `\faGithub`.
- Use a **text** link (`\tlink{url}{text}`) only when there is no icon
  (e.g. Homepage, Google Scholar, a project page).
- Don't scatter decorative icons in body text. Section icons only via
  `\cvsection{\faIcon}{Title}`; keep them uniform in size/weight.

## 6. Keeping it one page (when you add content)
Prefer, in order: (a) tighten wording / shorten an over-long line that wraps;
(b) drop low-value detail (verbose fund/partner names) from titles so each title
is one line; (c) only as a last resort, adjust a spacing token in `resume.sty`
— and re-check **both** languages afterward. English wraps more than Chinese,
so simplify English first and keep it accurate.
