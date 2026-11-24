#!/usr/bin/env python3
"""Crop, redact and resize a screenshot for the document.

Examples:
  # crop to a box (left, top, right, bottom in source pixels)
  crop.py raw/in.png cropped/out.png --box 120 80 1400 900

  # crop, then black out two regions (coordinates are in the source image)
  crop.py raw/in.png cropped/out.png --box 0 60 1600 1000 \
      --redact 300 200 520 230 --redact 300 260 520 290

  # trim uniform borders automatically, no box
  crop.py raw/in.png cropped/out.png --trim
"""
import argparse

from PIL import Image, ImageChops, ImageDraw

# 6.5in of usable page width at 2x density keeps text sharp in Google Docs.
DEFAULT_MAX_WIDTH = 1600


def trim(img, tolerance=12):
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg).convert("L").point(lambda p: 255 if p > tolerance else 0)
    bbox = diff.getbbox()
    return img.crop(bbox) if bbox else img


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--box", nargs=4, type=int, metavar=("L", "T", "R", "B"))
    p.add_argument("--redact", nargs=4, type=int, action="append", default=[], metavar=("L", "T", "R", "B"))
    p.add_argument("--trim", action="store_true")
    p.add_argument("--pad", type=int, default=0, help="white padding added after cropping")
    p.add_argument("--max-width", type=int, default=DEFAULT_MAX_WIDTH)
    args = p.parse_args()

    img = Image.open(args.src).convert("RGB")

    # Redact on the source image so coordinates stay in one frame of reference.
    draw = ImageDraw.Draw(img)
    for box in args.redact:
        draw.rectangle(box, fill=(40, 40, 40))

    if args.box:
        img = img.crop(tuple(args.box))
    if args.trim:
        img = trim(img)
    if args.pad:
        padded = Image.new("RGB", (img.width + 2 * args.pad, img.height + 2 * args.pad), "white")
        padded.paste(img, (args.pad, args.pad))
        img = padded
    if img.width > args.max_width:
        img = img.resize((args.max_width, round(img.height * args.max_width / img.width)), Image.LANCZOS)

    img.save(args.dst, optimize=True)
    print(f"{args.dst}: {img.width}x{img.height}")


if __name__ == "__main__":
    main()
