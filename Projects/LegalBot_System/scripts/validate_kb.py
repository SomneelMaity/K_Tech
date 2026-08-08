"""
validate_kb.py — Validate all knowledge-base entries against the schema.

Usage:
    python scripts/validate_kb.py

Checks:
  - Required YAML front-matter fields are present
  - entry_id matches the filename
  - last_verified is not older than 6 months
  - source_url is present and non-empty
  - Content body is non-empty
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yaml  # pip install pyyaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

REQUIRED_FIELDS = ["entry_id", "segment", "title", "act", "section", "state",
                   "language", "last_verified", "source_url"]
KB_DIR = Path(__file__).parent.parent / "knowledge-base"
STALE_THRESHOLD = timedelta(days=185)  # ~6 months


def parse_entry(filepath: Path) -> tuple[dict, str]:
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    front = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return front, body


def validate_file(filepath: Path) -> list[str]:
    errors: list[str] = []
    front, body = parse_entry(filepath)

    for field in REQUIRED_FIELDS:
        if not front.get(field):
            errors.append(f"Missing field: {field}")

    expected_id = filepath.stem.split("-", 1)[0] + "-" + filepath.stem.split("-", 1)[1] if "-" in filepath.stem else filepath.stem
    # entry_id should match filename prefix (e.g. s5-001)
    entry_id = str(front.get("entry_id", ""))
    if entry_id and not filepath.stem.startswith(entry_id):
        errors.append(f"entry_id '{entry_id}' does not match filename '{filepath.stem}'")

    last_verified = str(front.get("last_verified", ""))
    if last_verified:
        try:
            lv_date = datetime.strptime(last_verified, "%Y-%m")
            if datetime.now() - lv_date > STALE_THRESHOLD:
                errors.append(f"Entry may be stale — last_verified: {last_verified}")
        except ValueError:
            errors.append(f"Invalid last_verified format (expected YYYY-MM): {last_verified}")

    if not body:
        errors.append("Empty content body")

    return errors


def main() -> None:
    all_errors: dict[str, list[str]] = {}

    for md_file in sorted(KB_DIR.rglob("*.md")):
        if md_file.name in ("SCHEMA.md", "README.md"):
            continue
        errors = validate_file(md_file)
        if errors:
            all_errors[str(md_file.relative_to(KB_DIR))] = errors

    if all_errors:
        print("❌ Validation FAILED\n")
        for path, errs in all_errors.items():
            print(f"  {path}")
            for e in errs:
                print(f"    - {e}")
        sys.exit(1)
    else:
        total = sum(1 for _ in KB_DIR.rglob("*.md")
                    if _.name not in ("SCHEMA.md", "README.md"))
        print(f"✅ All {total} KB entries valid.")


if __name__ == "__main__":
    main()
