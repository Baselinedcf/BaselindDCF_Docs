#!/usr/bin/env python3
"""Extract embedded JSON payloads from a Baseline .xlsx export.

Usage::

    python tools/extract-polyglot-json.py report.xlsx                 # print all parts
    python tools/extract-polyglot-json.py report.xlsx --part inputs   # print just inputs
    python tools/extract-polyglot-json.py report.xlsx --verify        # verify integrity

The script reads /customXml/ parts from the OOXML zip and prints the
embedded JSON to stdout.  Standalone — requires only the Python
standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

_NS = "urn:baseline:audit"


def extract_parts(xlsx_path: str) -> dict[str, str]:
    """Read /customXml/itemN.xml and return {type: raw_json}."""
    parts: dict[str, str] = {}
    with ZipFile(xlsx_path, "r") as zf:
        for name in zf.namelist():
            if name.startswith("customXml/item") and name.endswith(".xml") \
               and "Props" not in name:
                raw = zf.read(name).decode("utf-8")
                try:
                    root = ET.fromstring(raw)
                    ns = {"ff": _NS}
                    ptype_el = root.find("ff:type", ns)
                    json_el = root.find("ff:json", ns)
                    if ptype_el is not None and json_el is not None:
                        raw_json = (json_el.text or "").strip()
                        parts[ptype_el.text or ""] = raw_json
                except ET.ParseError:
                    continue
    return parts


def verify_integrity(parts: dict[str, str]) -> bool:
    """Verify SHA-256 hashes from audit_manifest."""
    if "audit_manifest" not in parts:
        print("ERROR: No audit_manifest found.", file=sys.stderr)
        return False

    manifest = json.loads(parts["audit_manifest"])
    ok = True
    for part_name in ("inputs", "outputs"):
        expected = manifest.get("parts", {}).get(part_name, {}).get("sha256")
        if not expected:
            continue
        if part_name not in parts:
            print(f"ERROR: {part_name} missing from xlsx.", file=sys.stderr)
            ok = False
            continue
        actual = hashlib.sha256(parts[part_name].encode("utf-8")).hexdigest()
        if actual != expected:
            print(
                f"FAIL: {part_name} hash mismatch\n"
                f"  expected: {expected}\n"
                f"  actual:   {actual}",
                file=sys.stderr,
            )
            ok = False
        else:
            print(f"OK: {part_name} hash verified ({actual[:16]}…)")
    return ok


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract JSON from a Baseline polyglot .xlsx"
    )
    parser.add_argument("xlsx", help="Path to the .xlsx file")
    parser.add_argument(
        "--part", choices=["inputs", "outputs", "audit_manifest"],
        help="Print only this part (default: all)",
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Verify integrity hashes and exit",
    )
    args = parser.parse_args()

    if not Path(args.xlsx).exists():
        print(f"File not found: {args.xlsx}", file=sys.stderr)
        sys.exit(1)

    parts = extract_parts(args.xlsx)
    if not parts:
        print("No embedded JSON found in this file.", file=sys.stderr)
        sys.exit(1)

    if args.verify:
        ok = verify_integrity(parts)
        sys.exit(0 if ok else 1)

    if args.part:
        if args.part not in parts:
            print(f"Part '{args.part}' not found. Available: {list(parts.keys())}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(json.loads(parts[args.part]), indent=2))
    else:
        for ptype, raw_json in parts.items():
            print(f"\n{'=' * 60}")
            print(f"  {ptype}")
            print(f"{'=' * 60}")
            parsed = json.loads(raw_json)
            # Truncate large payloads for display
            text = json.dumps(parsed, indent=2)
            if len(text) > 5000:
                print(text[:5000])
                print(f"\n  ... ({len(text):,} chars total, truncated)")
            else:
                print(text)


if __name__ == "__main__":
    main()
