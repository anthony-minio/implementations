#!/usr/bin/env python3
"""Place cropped screenshots side by side, top-aligned, on white.

  combine.py out.png left.png right.png [more.png ...] [--gap 40]
"""
import argparse

from PIL import Image


def main():
    p = argparse.ArgumentParser()
    p.add_argument("dst")
    p.add_argument("srcs", nargs="+")
    p.add_argument("--gap", type=int, default=40)
    args = p.parse_args()

    ims = [Image.open(s).convert("RGB") for s in args.srcs]
    width = sum(i.width for i in ims) + args.gap * (len(ims) - 1)
    out = Image.new("RGB", (width, max(i.height for i in ims)), "white")
    x = 0
    for im in ims:
        out.paste(im, (x, 0))
        x += im.width + args.gap
    out.save(args.dst, optimize=True)
    print(f"{args.dst}: {out.width}x{out.height}")


if __name__ == "__main__":
    main()
