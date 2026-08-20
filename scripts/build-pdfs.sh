#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PDF_DIR="$ROOT/docs/pdf"
CSS="$ROOT/docs/pdf.css"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found — install it (e.g. 'brew install pandoc') and re-run." >&2
  exit 1
fi
if [ ! -x "$CHROME" ]; then
  echo "Chrome not found at: $CHROME" >&2
  echo "Set CHROME=/path/to/chrome and re-run, or install Google Chrome." >&2
  exit 1
fi

mkdir -p "$PDF_DIR"

# source_md : resource_dir (for resolving relative image paths) : output_name
DOCS=(
  "docs/00_DocCenter.md:docs:00_DocCenter"
  "README.md:.:01_README"
  "docs/UseCases.md:docs:02_UseCases"
  "docs/Dictionary.md:docs:03_Dictionary"
  "docs/GeneralKnowledge.md:docs:04_GeneralKnowledge"
  "docs/TrackingCoordinates.md:docs:05_TrackingCoordinates"
)

for entry in "${DOCS[@]}"; do
  IFS=":" read -r src resdir name <<< "$entry"
  echo "-> docs/pdf/$name.pdf"
  tmp_html="$(mktemp /tmp/doc_XXXXXX).html"
  pandoc "$ROOT/$src" \
    -o "$tmp_html" \
    --standalone --embed-resources \
    --resource-path="$ROOT/$resdir" \
    --css="$CSS" \
    --metadata title="$name"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$PDF_DIR/$name.pdf" "file://$tmp_html" 2>/dev/null
  rm -f "$tmp_html"
done

echo ""
echo "Done — $(ls "$PDF_DIR"/*.pdf | wc -l | tr -d ' ') PDFs in $PDF_DIR/"
