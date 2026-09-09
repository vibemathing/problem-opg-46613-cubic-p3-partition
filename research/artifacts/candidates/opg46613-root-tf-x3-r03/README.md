# Replay X3-R03

All mathematics is candidate_only. Read report.md before using the finite data.
Run `python3 -I -S restore_archive.py` to restore fixed source/data into `replay/`.
Then, in an isolated copy of `replay/`, run `python3 -I -S run_bounded.py`.
The new execution.json produced there is a new observation, not the historical
execution.json in this outer directory. The consumer performs no cofactor
search and imports no producer. Full cofactor blocks are reconstructed from
special P3s plus the canonical remaining circle paths.

No old host census, historical transport, Lean elaboration or trusted closure
is part of this replay. Actual receipt fields are posted to Issue #3 after PR.
