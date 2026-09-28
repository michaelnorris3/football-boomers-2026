#!/usr/bin/env python3
"""Validate current league snapshots against the append-only transaction ledger."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

TEAM_FILES = {
    "TEAM_01": ("The Team Who Would Be Champs", "The_Team_Who_Would_Be_Champs.md"),
    "TEAM_02": ("Cat Scratch Fever", "Cat_Scratch_Fever.md"),
    "TEAM_03": ("Lamar can't hurt me", "Lamar_cant_hurt_me.md"),
    "TEAM_04": ("Kars4Gibbs", "Kars4Gibbs.md"),
    "TEAM_05": ("Long Live the King", "Long_Live_the_King.md"),
    "TEAM_06": ("boomers.", "boomers.md"),
    "TEAM_07": ("The Branch Covidians", "The_Branch_Covidians.md"),
    "TEAM_08": ("Cazzata Malanga", "Cazzata_Malanga.md"),
    "TEAM_09": ("Barcelona Pickpockets", "Barcelona_Pickpockets.md"),
    "TEAM_10": ("Champs?AllSigns Point 2 YES!!", "Champs_AllSigns_Point_2_YES.md"),
}
PLAYER_LINE = re.compile(r"^-\s+(QB|RB|WR|TE|D/ST|K|IR)\s+(.+),\s+([A-Z]{2,3})\s*$")


def parse_rosters(root: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    errors: list[str] = []
    ownership: dict[str, dict[str, str]] = {}
    seen_files: set[str] = set()
    for team_id, (team_name, filename) in TEAM_FILES.items():
        path = root / "rosters" / filename
        if not path.exists():
            errors.append(f"missing roster snapshot: {path}")
            continue
        seen_files.add(filename)
        text = path.read_text(encoding="utf-8")
        if f"# {team_name}" not in text:
            errors.append(f"{path}: team heading does not match expected name")
        players: dict[str, str] = {}
        for line in text.splitlines():
            match = PLAYER_LINE.match(line)
            if not match:
                continue
            position, player, nfl_team = match.groups()
            key = player.casefold()
            if key in players:
                errors.append(f"{path}: duplicate player on one roster: {player}")
            players[key] = team_id
            if key in ownership and ownership[key]["team_id"] != team_id:
                errors.append(
                    f"duplicate ownership: {player} appears on "
                    f"{ownership[key]['team_name']} and {team_name}"
                )
            ownership[key] = {"team_id": team_id, "team_name": team_name, "position": position}
        if not players:
            errors.append(f"{path}: no rostered players found")
    return ownership, errors


def parse_transaction_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.startswith("|") or raw.startswith("|---") or "Transaction ID" in raw:
            continue
        cells = [cell.strip() for cell in raw.strip("|").split("|")]
        if len(cells) != 15:
            continue
        rows.append(dict(zip(
            ["id", "date", "time", "week", "type", "team", "player_id",
             "player", "from_team", "to_team", "bid", "waiver_before",
             "waiver_after", "source", "notes"],
            cells,
        )))
    return rows


def check_drops_against_rosters(root: Path, ownership: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    latest_action: dict[tuple[str, str], str] = {}
    for row in parse_transaction_rows(root / "league" / "TRANSACTION_LOG.md"):
        player = row["player"].casefold()
        if not player or row["type"] not in {"Drop", "Add"}:
            continue
        latest_action[(row["team"], player)] = row["type"]
    for player, record in ownership.items():
        if latest_action.get((record["team_name"], player)) == "Drop":
            errors.append(
                f"dropped-but-still-rostered: {player} remains on {record['team_name']}"
            )
    return errors


def check_waiver_order(root: Path) -> list[str]:
    path = root / "league" / "WAIVER_ORDER.md"
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.startswith("|") or raw.startswith("|---") or "Priority" in raw:
            continue
        cells = [cell.strip() for cell in raw.strip("|").split("|")]
        if len(cells) >= 3:
            rows.append((cells[0], cells[1]))
    errors = []
    priorities = [int(priority) for priority, _ in rows if priority.isdigit()]
    if priorities != list(range(1, 11)):
        errors.append(f"waiver priority must contain 1-10 exactly; found {priorities}")
    team_ids = [team_id for _, team_id in rows]
    if len(team_ids) != len(set(team_ids)):
        errors.append("waiver order contains duplicate teams")
    if set(team_ids) != set(TEAM_FILES):
        errors.append("waiver order does not contain exactly the 10 known teams")
    return errors


def check_schedule(root: Path) -> list[str]:
    errors = []
    with (root / "league" / "league_schedule.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        if row["status"] == "final" and (not row["team_1_score"] or not row["team_2_score"]):
            errors.append(f"final matchup missing score: {row['matchup_id']}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--max-active-slots", type=int)
    parser.add_argument("--max-total-slots", type=int)
    args = parser.parse_args()
    ownership, errors = parse_rosters(args.repo_root)
    if args.max_active_slots or args.max_total_slots:
        # Slot limits are optional because the initialization data did not specify them.
        for team_id, (team_name, filename) in TEAM_FILES.items():
            lines = (args.repo_root / "rosters" / filename).read_text(encoding="utf-8").splitlines()
            rostered = [line for line in lines if PLAYER_LINE.match(line)]
            active = [line for line in rostered if not line.startswith("- IR ")]
            if args.max_active_slots and len(active) > args.max_active_slots:
                errors.append(f"{team_name}: active roster exceeds configured limit")
            if args.max_total_slots and len(rostered) > args.max_total_slots:
                errors.append(f"{team_name}: total roster exceeds configured limit")
    errors.extend(check_drops_against_rosters(args.repo_root, ownership))
    errors.extend(check_waiver_order(args.repo_root))
    errors.extend(check_schedule(args.repo_root))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: roster ownership, drop history, waiver order, and known schedule validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
