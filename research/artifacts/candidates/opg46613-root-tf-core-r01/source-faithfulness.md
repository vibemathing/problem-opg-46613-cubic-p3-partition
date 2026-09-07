# Source and statement boundary

Verdict: candidate_only. Base d1df88796cc753123f53796f8de5c9e89066e0cc.
Canonical contract: research-domain paths P3 are selected, not necessarily
induced. Triangle-freeness makes these induced, without changing the target.
All new universal fixed-M lemmas have a supplied perfect matching as a premise.
The universal existence of an admissible subset S is not proved or assumed.

Repository dependencies read this turn:
- root-r06/charged-flow.md: charge/support identity and the remaining minimum gap.
- c07/mixed-cell-forest.md: all-retained max-degree-two specialization.
- root-r07/triangle-free-root-reduction.md and root-equivalences.md: exact universal
  domain maps, not hypotheses asserting their universal endpoints.
- root-r07/cycle-local-minimum-family.md and neutral-defect-transitions.md:
  strict-cycle descent already fails; neutral transitions need a global bridge.
- triangle-simulator-audit-r01/admission-request.json: prior fixed-object audit
  does not have a trusted mathematical admission receipt.
All these prefixes extend research/artifacts/candidates/.

Primary literature checked: Alexander Kelmans, Packing 3-vertex Paths in Cubic
3-connected Graphs, arXiv:0910.2766v2 (25 July 2011),
https://arxiv.org/pdf/0910.2766 . Theorem 3.1 (printed pp.7-8) gives equivalent
universal claims: (z1) is the zero-mod-six factor statement, (z2) arbitrary
edge avoidance, and (f1) deletion of a specified vertex in the four-mod-six
domain. This is an equivalence theorem, not a proof that the claims hold;
Section 3.10 proves the relevant universal (z1)/(f1) connection. Neither a
pointwise factor nor a proper-subclass result licenses those universal claims.
The adjacent claw-free discussion does not apply to triangle-free cubic graphs,
whose three neighbors at every vertex form an induced claw. Text extraction
was available; the PDF screenshot request failed and no figure was used.
No novelty conclusion for the new gap criterion is asserted from this search.

New G36 is a positive root instance. Its 42-edge subgraph G0 is noncubic and
has no factor; that certificate cannot be attached to the root negation.
The second negative certificate adds a cost<=2 restriction on a supplied M;
its failure is not factor nonexistence. The two-way fixed-M theorem retains
internal matching chords and exact cyclic positions, unlike the discarded
loop-erasure shortcut. Caps of its three-edge cuts have orders 8/30 and 12/26;
none supplies two smaller zero-mod-six induction instances.

Four new implementations/replays are generator-side observations. The complete
negative DAG consumer and direct count polynomial do not import the other
programs' cores. The old R07 and simulator audits were read, not rerun as this
step's audit. Exploratory program observations are separately marked and not
mathematical dependencies. Historical absent raw outputs and uncompiled C08
Lean remain absent/pending. There is no Lean elaboration, axiom report, trusted
verifier fingerprint, EvidenceLink, Result or Solution in this package.
