# League Rules

## Format

- Teams: 10
- Scoring: PPR
- Matchups: Weekly head-to-head
- Schedule, results, standings, and current player ownership are maintained in their respective authoritative files. Do not infer their current state from this rules document.
- Use the latest confirmed ESPN screenshots and reconciled GitHub records for time-sensitive league information.

## Starting lineup requirements

- QB: 1
- RB: 2
- WR: 3 (three mandatory WR starters, not two)
- TE: 1
- FLEX: 1 (RB, WR, or TE eligible)
- D/ST: 1
- K: 1
- Total weekly starters: 10
- Bench: 5 active reserve slots; separate IR slot: 1.
- When evaluating lineups, roster needs, waiver claims, trades, and bye-week coverage, always account for all three required WR starters and the additional FLEX.

## Transaction and lock rules

- Rolling waiver priority: a successful waiver claim moves that team to the bottom.
- Players lock at the start of their individual NFL game whether rostered, benched, or unrostered.
- After weekly games finish, available players go to waivers.
- After waivers clear, unclaimed players become free agents until their individual kickoff.
- Some players dropped within the league's 24-hour pregame threshold remain waiver-locked rather than becoming immediate free agents.
- An eligible player placed into an empty IR slot creates an active-roster opening without requiring a drop.
- Ownership-sensitive recommendations must use the current authoritative roster state.
- Never recommend a waiver/free-agent add without verifying the player is currently unrostered.
- Historical transactions are append-only. Later confirmed transactions supersede earlier state without rewriting history.

## Analysis guidance

- This document contains stable league rules, not current standings, rosters, injuries, or matchup status.
- For rostered players and ownership, consult `league/MASTER_ROSTER_INDEX.md` and the individual team files under `rosters/`, applying any newer confirmed transactions.
- For waiver order, consult `league/WAIVER_ORDER.md`; do not infer priority from league standings.
- For historical transactions, consult `league/TRANSACTION_LOG.md` and confirmed screenshots. Do not invent missing transactions.
- For weekly matchups and results, consult the latest confirmed schedule/results files and screenshots.
- For weekly analysis, prioritize the upcoming head-to-head matchup, injury and bye-week coverage, and the user's expected starting lineup over speculative long-term bench value.
- For news reports, focus on injuries, practice status, workload/depth-chart changes, opponent implications, waiver opportunities, and start/sit impact.
