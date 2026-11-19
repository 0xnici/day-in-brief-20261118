#!/usr/bin/env python3
"""Entry program: "Sum up 18 November's world news in one image".

Visual edition. The front page — masthead, arrival illustration, lead
and six stories — is composed ahead of time by tools/compose18.py and
committed as entry.png. Grading runs offline, so this program's work is
delivery with proof: stream the page to /output/entry.png in chunks,
then compare a running SHA-256 of what landed against the source, so a
short or corrupted write fails instead of passing.
"""

import hashlib
import os
import sys

CHUNK = 64 * 1024
BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE, "entry.png")


def stream_copy(src_path, dst_path):
    """Copy in chunks; return (bytes, sha256 hex) of the source stream."""
    digest = hashlib.sha256()
    total = 0
    with open(src_path, "rb") as src, open(dst_path, "wb") as dst:
        while True:
            block = src.read(CHUNK)
            if not block:
                break
            digest.update(block)
            total += len(block)
            dst.write(block)
    return total, digest.hexdigest()


def file_digest(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def run() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    total, digest = stream_copy(SOURCE, target)
    if file_digest(target) != digest:
        print("error: delivered page fails its checksum", file=sys.stderr)
        return 1
    print(f"delivered {target}: {total} bytes, sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
