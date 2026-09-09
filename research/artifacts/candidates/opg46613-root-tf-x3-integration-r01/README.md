# X3 one-exception integration candidate

Read report.md for the exact unrestricted-size statement and remaining gaps.
Run `python3 -I -S restore_archive.py`, then run `python3 -I -S run_bounded.py`
in the restored replay directory. Restored execution.json records an earlier
run; executing creates a new observation, not a trusted verifier receipt.
No old host census or protected record is part of the replay.
