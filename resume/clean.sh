#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Build & clean the resume.

# Usage:
#   ./clean.sh            # compile both versions, then delete temp files
#   ./clean.sh --clean    # only delete temp files (no compilation)
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

# Temporary extensions produced by (Xe)LaTeX / hyperref / latexmk.
TEMP_EXT=(aux log out toc lof lot fls fdb_latexmk synctex.gz xdv \
          bbl blg nav snm vrb idx ilg ind)

remove_temp() {
  for base in main_cn main_en; do
    for ext in "${TEMP_EXT[@]}"; do
      rm -f -- "$base.$ext"
    done
  done
}

if [[ "${1:-}" == "--clean" ]]; then
  remove_temp
  echo "Temporary files removed."
  exit 0
fi

for base in main_cn main_en; do
  echo "==> Compiling $base.tex"
  # Two passes: the page border and photo use TikZ remember-picture/overlay,
  # which (with hyperref) need a second run to settle positions and page count.
  xelatex -interaction=nonstopmode -halt-on-error "$base.tex" >/dev/null
  xelatex -interaction=nonstopmode -halt-on-error "$base.tex" >/dev/null
done

remove_temp
echo "Done -> main_cn.pdf, main_en.pdf"
