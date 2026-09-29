# League State

## Purpose and source of truth

This repository is the persistent source of truth for the 2026 10-team PPR fantasy-football league.

- `league/TRANSACTION_LOG.md` is an append-only chronological ledger. Historical rows are never deleted or rewritten.
- `rosters/` contains the latest confirmed authoritative roster snapshot for each team.
- `league/MASTER_ROSTER_INDEX.md` is the current ownership index derived from the latest confirmed state and reconciled against roster snapshots.
- `league/WAIVER_ORDER.md` is the current rolling waiver priority.
- `league/league_schedule.csv` contains only supplied results and known schedule entries.
- Missing data remains blank or marked pending; it is never inferred.

When historical data conflicts with a later confirmed transaction, the later transaction supersedes the earlier state while both records remain in the ledger. The confirmed rename `Kars4Kids -> Kars4Gibbs` preserves the same manager/franchise.

## Latest synchronization

- Latest synchronization date: **2026-09-29**
- Latest authoritative roster snapshot: **2026-09-27**
- Latest confirmed transaction date: **2026-09-27**
- Current record: after applying all confirmed transactions supplied through Sunday 2026-09-27 and final Week 3 scoreboard results supplied 2026-09-29
- Waiver order effective: **2026-09-25**
- Initialization status: **INITIALIZED**

## League mechanics

See `league/LEAGUE_RULES.md` for the authoritative mechanics supplied for this initialization.

## Validation

Run:

```bash
python scripts/update_league_state.py
```

Optional roster-size checks can be supplied once the league's exact slot limits are authoritative:

```bash
python scripts/update_league_state.py --max-active-slots N --max-total-slots N
```

## Verification — 2026-09-28

Repository reconciliation completed against the latest authoritative league materials available in the Football boomers 2026 project and confirmed screenshots through 2026-09-27. The following were verified as already reflected in the canonical files: Kars4Kids -> Kars4Gibbs rename; Sean Vitale's Jameis Winston and Cameron Dicker adds with Dominic Zvada dropped; Barcelona Pickpockets' Khalil Shakir add with Justin Herbert dropped; boomers.' Eddy Pineiro add with Dontayvion Wicks dropped; and Chris Gibson's Daniel Carlson add with Emanuel Wilson dropped to waivers. No roster-state correction was required by this verification.

## Week 3 results — confirmed 2026-09-29

Final scoreboard results were added from user-provided league screenshots:

- boomers. 139.88 def Champs?AllSigns Point 2 YES!! 84.64
- Barcelona Pickpockets 126.80 def Cat Scratch Fever 111.16
- Kars4Gibbs 162.58 def The Team Who Would Be Champs 160.28
- Cazzata Malanga 151.92 def Long Live the King 144.14
- Lamar can't hurt me 137.02 def The Branch Covidians 134.44
