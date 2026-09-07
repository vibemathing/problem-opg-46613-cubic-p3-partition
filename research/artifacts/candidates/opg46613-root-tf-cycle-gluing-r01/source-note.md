# Source scope and statement differences

Verdict: candidate_only. Base: 0f009927bfffa44335148cb65ae93596288b50c4.

1. Frozen ProblemContract: problem-library/records/canonical-problems.jsonl,
   digest f22ec1937d8b771614cb85435b6d4e0712afb9a3939780e04b74e4649617c26a.
   Noninduced P3, simple finite cubic 3-vertex-connected, positive order0mod6.
2. ROOT-TF-CORE-R01/report.md: exact supplied-M normal form and fixed-S
   gap-forest criterion; arbitrary feasible-S existence stays open. Its
   36-vertex positive host already blocks the general two-M-edge shortcut.
   New work supplies a three-cycle exact classification, a length-classification
   theorem through order18, a sharp36 lower bound for the012 phase pattern,
   and a different24-vertex positive host at matching cost three.
3. root-r07/triangle-free-root-reduction.md and the merged simulator audit:
   R iff R_tf only. No expansive replacement is used to shrink a smallest
   counterexample or to inherit a bounded-order result for arbitrary G.
4. root-r07/root-equivalences.md: global R/D4/E equivalences, not pointwise
   edge avoidance or a modulus-preserving cap induction. They are not assumed
   true as universal statements in the present proof.
5. Primary theorem statement checked on 2026-09-07:
   Pawel Gawrychowski and Mateusz Wasylkiewicz, Finding perfect matchings in
   bridgeless cubic multigraphs without dynamic (2-)connectivity,
   arXiv:2405.03856v1, submitted2024-05-06.
   https://arxiv.org/abs/2405.03856v1
   The abstract states the bridgeless-cubic perfect-matching theorem of
   Petersen. Our host is simple cubic and bridgeless, so its hypotheses apply.
   We use this named standard dependency, not the paper's running-time result.
   Full proof/algorithm and a formal-library declaration were not replayed.

No novelty, priority, or improvement over an external exhaustive graph census
is claimed. The new order18 argument is a constructive proof for every length
case, not a statement that a sampled list contains every graph. The24-vertex
restricted obstruction has a displayed P3-factor and cannot falsify the root.
