#!/usr/bin/env python3
"""news-image-20261125: copy the entry image to /output/entry.png.

The entry is a pre-rendered newspaper front page summing up
Wednesday 25 November 2026 in a single image (entry.png, bundled
in this repository). Running this script only copies those exact
bytes, so repeated runs always produce identical output. It uses
only the Python standard library and never touches the network.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
TARGET = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def check_png(data):
    """Fail unless data is a PNG within the bounty's size limits."""
    if len(data) > MAX_BYTES:
        print("error: entry.png is %d bytes, over the 1 MiB cap" % len(data),
              file=sys.stderr)
        sys.exit(1)
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        sys.exit(1)
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        print("error: entry.png is %dx%d, over the 1024x1024 cap"
              % (width, height), file=sys.stderr)
        sys.exit(1)


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    data = SOURCE.read_bytes()
    check_png(data)
    TARGET.write_bytes(data)
    if digest(SOURCE) != digest(TARGET):
        print("error: copied bytes differ from entry.png", file=sys.stderr)
        sys.exit(1)
    print("wrote %s (%d bytes, sha256 %s)" % (TARGET, len(data), digest(TARGET)))


if __name__ == "__main__":
    main()
