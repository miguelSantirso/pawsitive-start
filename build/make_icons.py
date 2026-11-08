#!/usr/bin/env python3
"""Generate Pawsitive Start's app icons without any third-party libraries.

Run directly:  python3 build/make_icons.py
Or let build.py call ensure() when an icon is missing.

The mark is a warm clay tile with a paper-coloured paw. PNGs are rendered at
4x and downsampled for clean edges. Everything is deterministic.
"""
import os
import struct
import zlib

CLAY = (163, 74, 38)     # #a34a26
PAPER = (247, 242, 233)  # #f7f2e9

# Paw geometry in a 100 x 100 coordinate space.
PAD = (50.0, 66.0, 21.0, 17.0)  # cx, cy, rx, ry
TOES = [
    (28.0, 43.0, 9.0),
    (42.0, 34.0, 9.5),
    (58.0, 34.0, 9.5),
    (72.0, 43.0, 9.0),
]


def _in_ellipse(x, y, cx, cy, rx, ry):
    dx = (x - cx) / rx
    dy = (y - cy) / ry
    return dx * dx + dy * dy <= 1.0


def paw(x, y, scale=1.0):
    """True when point (x, y) is inside the paw, scaled about the centre."""
    x = 50.0 + (x - 50.0) / scale
    y = 50.0 + (y - 50.0) / scale
    if _in_ellipse(x, y, *PAD):
        return True
    for cx, cy, r in TOES:
        if _in_ellipse(x, y, cx, cy, r, r):
            return True
    return False


def _chunk(kind, data):
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def _png(size, scale):
    ss = 4
    rows = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            hits = 0
            for sy in range(ss):
                for sx in range(ss):
                    x = (px * ss + sx + 0.5) / (size * ss) * 100.0
                    y = (py * ss + sy + 0.5) / (size * ss) * 100.0
                    if paw(x, y, scale):
                        hits += 1
            a = hits / float(ss * ss)
            row += bytes(
                int(round(CLAY[i] * (1.0 - a) + PAPER[i] * a)) for i in range(3)
            )
        rows.append(bytes(row))
    raw = b"".join(b"\x00" + r for r in rows)
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", zlib.compress(raw, 9))
        + _chunk(b"IEND", b"")
    )


def _svg():
    toes = "".join(
        '<circle cx="%g" cy="%g" r="%g"/>' % (cx, cy, r) for cx, cy, r in TOES
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<rect width="100" height="100" rx="22" fill="#a34a26"/>'
        '<g fill="#f7f2e9">'
        '<ellipse cx="50" cy="66" rx="21" ry="17"/>'
        + toes
        + "</g></svg>\n"
    )


FILES = [
    ("icon-180.png", 180, 1.0),
    ("icon-192.png", 192, 1.0),
    ("icon-512.png", 512, 1.0),
    ("icon-maskable-512.png", 512, 0.76),
]


def write_all(assets_dir):
    os.makedirs(assets_dir, exist_ok=True)
    with open(os.path.join(assets_dir, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(_svg())
    for name, size, scale in FILES:
        with open(os.path.join(assets_dir, name), "wb") as f:
            f.write(_png(size, scale))
    return [name for name, _s, _c in FILES] + ["favicon.svg"]


def ensure(assets_dir):
    names = [name for name, _s, _c in FILES] + ["favicon.svg"]
    if all(os.path.exists(os.path.join(assets_dir, n)) for n in names):
        return False
    write_all(assets_dir)
    return True


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, "site", "assets")
    made = write_all(out)
    print("Wrote icons to", out)
    for name in made:
        print("  ", name)
