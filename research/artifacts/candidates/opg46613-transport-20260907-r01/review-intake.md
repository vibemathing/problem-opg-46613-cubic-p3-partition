# PR18 review intake and recovery scope

Verdict: `candidate_only`. Recorded 2026-09-07. This is a transport/review note, not a verifier receipt.

## Fresh repository facts

PR18 is merged, not open. Its retained final head is `0874d7bac254bd2fe98d3acf7be29f76763ff8f6`; its merge is `14b8dc64ac2d89c98cf3a2bbb2fcba76ced0df6a`. PR19 subsequently archived ROOT-R07 at current base `8eed5b0552ed3f257917d3a161ca5d6d9b358bed`. Machine PR state takes precedence over stale prose in PR bodies.

The PR18 transport COMMENT review 5127226533 already notes that `outputs/all_26_matchings.json` and `outputs/fragment_states.json` were absent. A fresh directory read confirms only `audit.json` existed at this base. The present recovery adds the two detail files from a new run of the exact submitted script. It does not fabricate their old bytes or overwrite the original summary. JSON whitespace is compacted without changing any field, order or value; raw and delivered hashes are separate in execution-records.json.

## User-supplied isolated review, not replayed by this agent

The user reports Lean 4.33.0 and Mathlib revision prefix `db584cd6`. The full Mathlib commit, edited draft bytes and raw logs were not provided. MathlibTargets.lean lines 76-83 fail because the symmetry/irreflexivity fields require Std.Symm/Std.Irrefl; the user's isolated SimpleGraph.fromRel replacement reportedly compiled. Local.lean sets maxHeartbeats to zero. The reported 12 GiB run failed; a 24 GiB run passed in about 411 seconds with peak RSS about 12.4 GiB. Arithmetic.lean passed. The user also reports agreement of two Python enumeration methods, make check-full with eight tests, the PR diff gate, and an escape-token audit. These observations retain their user-reported provenance; they are not new machine receipts.

The review directory is not present in the current execution environment. No user host path is retained here. No Lean executable is available here. A versioned follow-up may replace the H constructor with fromRel and remove the unbounded heartbeat setting, but such source must remain pending compilation and semantic comparison unless actually compiled in the pinned environment. Do not overwrite C08's immutable sources or its packet hashes.

## Recovery boundary

C06 and C08 Python replays were actually executed from byte-identical archived sources in this turn; their new execution observations are in execution-records.json. No Lean, SMT, global-family proof or root proof was executed. Prior local-only programs and historical originals remain listed in missing-originals.json. Their absence is not hidden by a new proof or by a passing transport check.
