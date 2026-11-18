#!/usr/bin/env python3
"""Entry program for make.fun's "Sum up 18 November's world news in one image".

The image — a one-page newspaper front page for Wednesday 18 November 2026 —
was composed ahead of time by tools/render.py from that day's wire reporting
(its CONTENT table lists the stories and figures used: the Qeshm Island
missile-site strike and Iran's drone answer, the second Kerch Bridge hit,
the Xi–Putin meeting in Shenzhen, Peltola's Alaska win taking Democrats to
56 Senate seats, the doubling Ebola outbreak in DR Congo, and Nvidia's
record revenue).

Rendering at run time is not an option under the rules: the runner is
offline and standard-library only, and a legible front page needs a real
typesetting pass over the day's reporting, not a runtime guess. So this
program does the one thing the runner asks, exactly and deterministically:
it writes the committed page, byte for byte, to /output/entry.png (or to
$MAKEFUN_OUTPUT_DIR/entry.png when that variable is set). The source file
never changes, so two runs produce identical bytes.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(SOURCE, "rb") as f:
        page = f.read()
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as f:
        f.write(page)
    # Read the file back and prove the bytes on disk are the committed page:
    # the entry is only valid if the output is that page, unchanged.
    with open(target, "rb") as f:
        written = f.read()
    if written != page:
        print(f"error: {target} does not match the committed page", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(page)} bytes, sha256 {hashlib.sha256(page).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
