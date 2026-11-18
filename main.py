#!/usr/bin/env python3
"""Entry program: "Sum up 18 November's world news in one image".

The entry is a newspaper front page for Wednesday 18 November 2026,
typeset ahead of time by tools/render.py from that day's wire reporting.
Its six panels carry the US strike on an Iranian missile site on Qeshm
Island and Iran's drone answer, the Kerch Bridge hit for a second
straight day, Xi and Putin meeting in Shenzhen, Mary Peltola's Alaska
win taking the Democrats to 56 Senate seats, Ebola cases more than
doubling in DR Congo, and Nvidia's record revenue.

The runner is offline and standard-library only, so the page cannot be
typeset at run time — a legible front page needs the real typesetting
pass, not a runtime guess. What the runner asks for is one file, written
exactly: this program copies the committed page to /output/entry.png
(or to $MAKEFUN_OUTPUT_DIR/entry.png when that is set), reads the copy
back, and fails unless the bytes on disk are the committed page, byte
for byte. The source never changes, so every run writes identical bytes.
"""

import hashlib
import os
import sys

PAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def deliver_page() -> int:
    with open(PAGE_FILE, "rb") as handle:
        page = handle.read()

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(page)

    # Read the copy back before reporting success: the entry counts only
    # if the file on disk is the committed page, unchanged, so a short
    # write or a swapped source must fail here rather than pass silently.
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != page:
        print(f"error: {target} does not match the committed page", file=sys.stderr)
        return 1

    digest = hashlib.sha256(page).hexdigest()
    print(f"wrote {target} ({len(page)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(deliver_page())
