#!/usr/bin/env python3
"""Validate the league's roster snapshot structure and ownership consistency.

This utility is intentionally validation-only for now. It does not rewrite the
append-only transaction ledger or derive files automatically. Initialization
and future update workflows can build on these checks.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXPECTED_TEAMS = [f"TEAM_{i:02d}" for i in range(1, 11)]
ROSTER_COLUMNS = ["Player ID", "Player Name", "Position", "NFL Team", "Status"]
SEPARATOR = re.compile(r"^\|\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?$")


def parse_roster(path: Path) -> tuple[str, list[str], list[str]]:
    """Return team id, player ids, and validation errors from one snapshot."""
    errors: list[str] = []
    match = re.search(r"^#\s+(TEAM_\d{2})(?:\s|$)", path.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        return path.stem, [], [f"{path}: missing '# TEAM_##' heading"]
    team_id = match.group(1)
    player_ids: list[str] = []
    in_table = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not in_table:
            if cells[: len(ROSTER_COLUMNS)] == ROSTER_COLUMNS:
                in_table = True
            continue
        if SEPARATOR.match(line):
            continue
        if len(cells) < len(ROSTER_COLUMNS):
            errors.append(f"{path}: malformed roster row: {line}")
            continue
        player_id = cells[0]
        if not player_id or player_id.upper() in {"PLAYER ID", "PENDING"}:
            continue
        player_ids.append(player_id)
    duplicates = sorted({pid for pid in player_ids if player_ids.count(pid) > 1})
    if duplicates:
        errors.append(f"{path}: duplicate player IDs: {', '.join(duplicates)}")
    return team_id, player_ids, errors


def validate_rosters(roster_dir: Path) -> int:
    errors: list[str] = []
    ownership: dict[str, str] = {}
    found: dict[str, Path] = {}
    for path in sorted(roster_dir.glob("TEAM_*.md")):
        team_id, player_ids, team_errors = parse_roster(path)
        errors.extend(team_errors)
        if team_id in found:
            errors.append(f"duplicate roster snapshot for {team_id}: {found[team_id]} and {path}")
        found[team_id] = path
        for player_id in player_ids:
            previous = ownership.get(player_id)
            if previous and previous != team_id:
                errors.append(f"duplicate ownership: {player_id} appears on {previous} and {team_id}")
            ownership[player_id] = team_id
    missing = sorted(set(EXPECTED_TEAMS) - set(found))
    unexpected = sorted(set(found) - set(EXPECTED_TEAMS))
    if missing:
        errors.append("missing roster snapshots: " + ", ".join(missing))
    if unexpected:
        errors.append("unexpected roster snapshots: " + ", ".join(unexpected))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: validated {len(found)} team roster snapshots; no duplicate ownership found.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    return validate_rosters(args.repo_root / "rosters")


if __name__ == "__main__":
    sys.exit(main())
