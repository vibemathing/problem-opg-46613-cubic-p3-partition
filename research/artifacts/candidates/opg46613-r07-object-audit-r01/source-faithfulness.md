# Source and faithfulness note: R07 fixed-object audit

Verdict: `candidate_only`. Retrieved 2026-09-07.

Authoritative finite input: sections 2--4 of
`research/artifacts/candidates/opg46613-root-r07/one-defect-repair.md` at revision
`0fb44ea490bb350f232c348ce3cc9d4072bc792f`, blob
`b655125f01f3d0fe75f3c538e6fc25599ac023d1`.
Relation: exact transcription of its finite objects; a new finite audit and
an expanded audit of its general sufficient-lemma proof. No novelty claim.
The checker does not execute or trust numeric assertions extracted from prose.
All host, forest, auxiliary, cycle and factor data are recomputed.

C08 source inspected for method separation:
`research/artifacts/candidates/opg46613-c08-independent-verifier/verify.py`,
blob `f9b929884a5342d598f840c4b8dcc7ea1f1b49d4` at the same revision.
It concerns C02, not this R07 graph. No code from it is imported or copied.
Its original branding does not supply another verifier trust domain.

Current pending formalization read:
`research/artifacts/candidates/opg46613-c08-review-repair-r01/repair-status.json`,
blob `55221dac7d5b7533b7955ee3855a230a778fcc19` at the same revision.
The recorded Lean 4.33.0 / Mathlib db584cd6d46c92f209a44c0f1c829460d327499d
plan does not constitute an elaboration receipt. No Lean source or old output
is changed, replayed or promoted by this audit.

Issue #3 checkpoint 5564129961 records missing historical original programs,
outputs and review logs. Their loss remains open and does not block this new
fixed-object package. In particular, no historical 136/972-case repair test,
135-row chord certificate or old elapsed time is reproduced here.

The target excluded premise is precisely: for every one-defect forest in a
root-domain graph, a maximum restricted auxiliary matching certifies that no
simple-cycle repair exists. R07 supplies a counterexample to this premise,
not to the frozen root or its separate two-factor strengthening. The general
nonmaximum-matching implication is proved in report.md by symmetric difference
and typed path lifting; it is not inferred from the example (where its premise
is false). Cut cases and non-induced P3 semantics are explicitly audited there.

An attempted external lookup for matching provenance returned a service error.
No external paper was retrieved or used as a proof dependency. The finite
symmetric-difference argument is supplied in full. Search availability, CI,
source hashes and PR status do not establish mathematical admission.
