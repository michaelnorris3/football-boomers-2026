# League State

## Purpose

This repository is the durable source of truth for the 2026 fantasy-football league. League state is maintained as a combination of:

1. The append-only transaction ledger in `league/TRANSACTION_LOG.md`.
2. Authoritative roster snapshots in `rosters/`.
3. Derived indexes and current-state documents in `league/`.

## Source-of-truth rules

- Transactions are append-only. Historical rows must never be edited, deleted, or rewritten.
- A new correction is recorded as a new transaction that references the prior record; it does not replace the prior record.
- Roster snapshots are authoritative only when explicitly identified as authoritative and dated in their file.
- Current ownership is derived from the transaction ledger and reconciled against the latest authoritative roster snapshots.
- If a ledger-derived result and an authoritative snapshot disagree, preserve both, flag the disagreement, and resolve it with a later dated authoritative input or correction transaction.
- No player, team, score, rule, or transaction may be inferred without authoritative initialization or update data.

## League mechanics

League-specific mechanics are intentionally pending authoritative initialization data. See `league/LEAGUE_RULES.md`.

## Synchronization

- Latest synchronization date: **PENDING INITIALIZATION DATA**
- Latest authoritative source: **PENDING INITIALIZATION DATA**
- Initialization status: **NOT INITIALIZED**
- Validation command: `python scripts/update_league_state.py`

## Directory map

- `league/TRANSACTION_LOG.md`: append-only chronological transaction ledger.
- `league/MASTER_ROSTER_INDEX.md`: current ownership index for the 10 teams.
- `league/WAIVER_ORDER.md`: current rolling waiver priority.
- `league/league_schedule.csv`: weekly matchups and final scores.
- `league/LEAGUE_RULES.md`: league format and transaction/lock rules.
- `rosters/`: one dated snapshot file per team.
- `scripts/update_league_state.py`: consistency and duplicate-ownership validator.
