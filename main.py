#!/usr/bin/env python3
"""Copy the entry line to the grader output path.

Reads entry.txt sitting next to this script and writes its exact bytes
to $MAKEFUN_OUTPUT_DIR/entry.txt (falling back to /output/entry.txt).
Stdlib only.
"""

import os
import sys
from pathlib import Path

ENTRY_NAME = "entry.txt"
MAX_BYTES = 4096


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / ENTRY_NAME
    raw = source.read_bytes()

    if not raw:
        print("entry.txt is empty", file=sys.stderr)
        return 1
    if len(raw) > MAX_BYTES:
        print(f"entry.txt too large: {len(raw)} bytes", file=sys.stderr)
        return 1
    if not raw.strip():
        print("entry.txt contains only whitespace", file=sys.stderr)
        return 1
    if raw.count(b"\n") != 1 or not raw.endswith(b"\n"):
        print("entry.txt must be exactly one line plus a trailing newline",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_path = Path(out_dir) / ENTRY_NAME
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)

    check = out_path.read_bytes()
    if check != raw:
        print("output does not match entry.txt", file=sys.stderr)
        return 1
    print(f"wrote {len(raw)} bytes to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
