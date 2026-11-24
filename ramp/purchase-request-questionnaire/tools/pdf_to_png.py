#!/usr/bin/env python3
"""Turn a full-page screenshot PDF (for example from GoFullPage) into one tall PNG.

  pdf_to_png.py in.pdf out.png

Extracts the embedded page images with pdfimages and stacks them top to bottom.
Crop the result with crop.py.
"""
import glob
import subprocess
import sys
import tempfile

from PIL import Image


def main(src, dst):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-j", "-png", src, f"{tmp}/p"], check=True)
        pages = [Image.open(f).convert("RGB") for f in sorted(glob.glob(f"{tmp}/p-*"))]
    if not pages:
        sys.exit(f"no images found in {src}")
    width = max(p.width for p in pages)
    out = Image.new("RGB", (width, sum(p.height for p in pages)), "white")
    y = 0
    for page in pages:
        out.paste(page, (0, y))
        y += page.height
    out.save(dst, optimize=True)
    print(f"{dst}: {out.width}x{out.height}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
