#!/usr/bin/env python3
"""
Append a single Internal Okayness rating to _data/okayness/ratings.yml.

Usage:
  python3 scripts/rate-okayness.py <board-id> <score 0-7> [note...]

Example:
  python3 scripts/rate-okayness.py self-health 6 slept well, back feels good
  python3 scripts/rate-okayness.py social-sarah 7
  python3 scripts/rate-okayness.py world-ai 0  # numb
"""

import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TREE_FILE    = REPO / "_data" / "okayness" / "tree.yml"
RATINGS_FILE = REPO / "_data" / "okayness" / "ratings.yml"

VALID_SCORES = range(0, 8)


def load_valid_ids():
    """Walk the tree and return all leaf + parent ids so we can validate."""
    text = TREE_FILE.read_text()
    ids = set()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- id:"):
            ids.add(line.split("id:", 1)[1].strip())
        elif line.startswith("- {") and "id:" in line:
            after = line.split("id:", 1)[1]
            tok = after.split(",", 1)[0].split("}", 1)[0].strip()
            ids.add(tok)
    return ids


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)

    board = sys.argv[1]
    try:
        score = int(sys.argv[2])
    except ValueError:
        sys.exit(f"score must be an integer 0..7, got {sys.argv[2]!r}")
    if score not in VALID_SCORES:
        sys.exit(f"score must be 0..7, got {score}")

    note = " ".join(sys.argv[3:]).strip()

    valid_ids = load_valid_ids()
    if board not in valid_ids:
        sys.exit(f"unknown board id {board!r}. Known ids: {sorted(valid_ids)}")

    ts = datetime.now().astimezone().isoformat(timespec="seconds")

    entry_lines = [
        f"  - id: {board}",
        f"    at: {ts}",
        f"    score: {score}",
    ]
    if note:
        safe_note = note.replace('"', '\\"')
        entry_lines.append(f'    note: "{safe_note}"')

    text = RATINGS_FILE.read_text()
    if text.rstrip().endswith("ratings: []"):
        text = text.replace("ratings: []", "ratings:\n" + "\n".join(entry_lines))
    else:
        text = text.rstrip() + "\n" + "\n".join(entry_lines) + "\n"
    RATINGS_FILE.write_text(text)

    print(f"  ✓ logged {board} = {score}" + (f' "{note}"' if note else "") + f" at {ts}")


if __name__ == "__main__":
    main()
