# Résumé (中文 / English)

Single-page, two-language résumé built with **XeLaTeX**.

apt install texlive-xetex \
                 texlive-lang-chinese \
                 texlive-fonts-recommended \
                 texlive-latex-extra texlive-fonts-extra

## Build

```bash
./clean.sh          # compile main_cn.tex + main_en.tex, then remove temp files
./clean.sh --clean  # only remove temp files
```

Or compile one version manually (run twice — the TikZ border/photo overlay
needs a second pass):

```bash
xelatex main_cn.tex && xelatex main_cn.tex
```

Outputs: `main_cn.pdf`, `main_en.pdf`.

## Files

- `main_cn.tex`, `main_en.tex` — content (identical structure).
- `resume.sty` — the design system: all layout, spacing and color tokens.
- `photo.jpg` — ID photo.
- `AGENTS.md` — rules for editing the template (read before changing layout).

Requires the `fandol` CJK font and the `fontawesome5` package (both ship with a
full TeX Live).
