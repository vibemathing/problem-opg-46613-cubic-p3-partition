# Statement and implementation faithfulness

Verdict: candidate_only. This note is a generator-side audit, not a semantic
verifier receipt. Source revision: db657865c432d10c6f57b6355f0ab17c42f57a09.

The audited source is research/artifacts/candidates/opg46613-root-r07/triangle-free-root-reduction.md,
blob 28fbdcd073b1216a1263d9a8ad5a7c6eedc5b6c4. Its companion
root-equivalences.md, blob 4b8197a3b1c1d2c3e318e7a28cfa370e2db01712, supplies
context for the identical three-sum operation; its universal deletion and edge
avoidance statements are not assumed true. The prior R07 object audit was read
through its current Issue #3 checkpoint and was not re-executed or treated as a
certificate for the different H used here. No external literature theorem or
novelty claim is imported by this bounded audit.

input.json transcribes the full H edge table and three Hamilton cycles. J's w
reuses label 0 only AFTER deleting H's vertex 0. T uses disjoint label blocks
0..20 and 21..41, outer ports 42,43,44 and cap 45. Thus 18,21,22,45,46 refer to
different fixed graphs, and capped J girth four is not confused with internal
J girth six. The original source labels map explicitly to the frozen numbers.

Every local certificate is a partition into A singletons, B pairs with the
port FIRST as center, and P3 triples with the center in the MIDDLE. State 0
means an unused external edge, not an uncovered port. No test requires absence
of a chord inside a selected P3. All 27 ordered states are examined without
assuming a symmetry of H, J or T. Positive solver outputs are fully checked
for roles, host edges, disjointness and coverage. Negative outputs use exhaustive
B-neighbor choices and complete internal exact cover, separately cross-checked
by residue/isolation certificates. Resource errors are not UNSAT results.

The T BBB proof respects direction: an outer B center needs one INTERNAL leaf,
so its chosen J port is A. It cannot use both J neighbors in addition to its
external edge. The 8 side choices exhaust all internal choices. A 0/A-only J
signature has 0 or 3 A-ports by vertex count, not because of a matching analogy.
The 3 case fails at w. This excludes precisely BBB, not an arbitrary stronger
interface rule.

The general theorem preserves each selected cut edge and its endpoint roles.
It allows an outside center to meet two A-ports. Every resulting selected edge
joins a degree-two center and degree-one leaf; this supplies the P3 component
bridge. The contraction proof requires order n>=6 and contracts ONE triangle
at a time; it does not assume simultaneous contraction is simple. The finite
prism control includes the smallest eligible n=6 case. The transformation
increases order by 42 each time. It proves counterexample transport and global
R iff R_tf, not that a smallest counterexample has no triangle, not a girth-six
reduction, and not a proof of R itself.

Core checker provenance: written in this turn, using fresh exact-cover row
search and integer frontier expansion; it imports only Python standard-library
modules. Neither the old C08 code nor the closed R07 checker is imported or
copied. This implementation separation DOES NOT create a separate trust domain.
Historical missing originals and C08's uncompiled Lean remain pending.
