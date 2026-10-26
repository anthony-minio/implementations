#!/usr/bin/env bash
# Build paste-ready outputs from sections/*.md. Settings come from doc.env.
#   output/<SLUG>.html  review page with copy-to-Google-Docs buttons (publish as an Artifact)
#   output/<SLUG>.docx  styled Word file; upload to Drive and open with Google Docs
#   output/<SLUG>-preview.pdf  PDF of the Word file, if LibreOffice is installed
set -euo pipefail
cd "$(dirname "$0")/.."

TITLE="Untitled document"; SUBTITLE=""; SLUG="document"
[ -f doc.env ] && source doc.env
mkdir -p output
python3 tools/csv_to_section.py MINIO_-_Noninventory_for_Sale.csv sections/02-LOAD-FILE.md
sections=(sections/*.md)

pandoc "${sections[@]}" \
  --from markdown \
  --resource-path . \
  --metadata title="$TITLE" \
  --metadata subtitle="$SUBTITLE" \
  -o "output/$SLUG.docx"
python3 tools/style_docx.py "output/$SLUG.docx"

# The review page embeds JPEG copies of the screenshots so it stays under the
# 16 MB Artifact limit. The Word file keeps the full-quality PNGs.
webdir=$(mktemp -d)
python3 - "$webdir" <<'PY'
import glob, os, re, sys
from PIL import Image
web = sys.argv[1]
os.makedirs(f"{web}/screenshots/cropped")
os.makedirs(f"{web}/sections")
for src in glob.glob("screenshots/cropped/*.png"):
    Image.open(src).convert("RGB").save(f"{web}/{src[:-4]}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
for src in sorted(glob.glob("sections/*.md")):
    text = open(src).read()
    text = re.sub(r"(\(screenshots/cropped/[^)]+)\.png\)", r"\1.jpg)", text)
    open(f"{web}/{src}", "w").write(text)
PY

pandoc "$webdir"/sections/*.md \
  --from markdown \
  --standalone --embed-resources --section-divs \
  --template tools/page-template.html \
  --resource-path "$webdir" \
  --metadata title="$TITLE" \
  --metadata subtitle="$SUBTITLE" \
  --metadata date="$(date +%Y-%m-%d)" \
  -o "output/$SLUG.html"
# Added after pandoc so --embed-resources doesn't try to inline the font service.
python3 - "output/$SLUG.html" <<'PY'
import sys
p = sys.argv[1]
fonts = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400'
    '&family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:opsz,wght@8..60,600&display=swap">'
)
s = open(p).read()
open(p, "w").write(s.replace("<!--FONTS-->", fonts, 1))
PY
rm -rf "$webdir"
echo "built: output/$SLUG.html output/$SLUG.docx"

if command -v soffice >/dev/null; then
  preview_dir=$(mktemp -d)
  HOME="$preview_dir" soffice --headless --convert-to pdf --outdir "$preview_dir" "output/$SLUG.docx" >/dev/null 2>&1 || true
  if [ -f "$preview_dir/$SLUG.pdf" ]; then
    mv "$preview_dir/$SLUG.pdf" "output/$SLUG-preview.pdf"
    echo "built: output/$SLUG-preview.pdf"
  fi
  rm -rf "$preview_dir"
fi
