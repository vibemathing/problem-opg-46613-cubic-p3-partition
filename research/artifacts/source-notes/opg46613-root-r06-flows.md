# ROOT-R06 statement comparisons

Verdict: `candidate_only`. Retrieved 2026-09-06. No novelty claim.

## Root and the connectivity hypothesis

Alexander Kelmans, *Packing 3-vertex Paths In Cubic 3-connected Graphs*,
arXiv:0910.2766v2, revised 25 July 2011:
https://arxiv.org/abs/0910.2766v2 .
The primary abstract discusses the universal cubic 3-connected packing claim
and related stronger-looking formulations. On orders divisible by three,
a packing leaving at most two vertices must be spanning. The present use is
only statement alignment. No theorem about prescribed edges or deleted paths
is assumed for an individual graph from the abstract's compressed wording.
The full 29-page proof has not been re-audited in this cycle.

Kelmans, *Packing 3-Vertex Paths in 2-Connected Graphs*, arXiv:0712.4151v1,
26 December 2007: https://arxiv.org/abs/0712.4151v1 .
Its primary abstract reports an infinite construction of 2-connected cubic
bipartite planar graphs of eligible order without spanning P3-packings. This is
a warning against dropping 3-connectivity. ROOT-R06's affine space is nonempty
for every connected eligible graph, so affine solvability alone cannot be used
as the spanning conclusion. We have read the abstract, not replayed those
particular graph constructions, and do not claim a new negative witness here.

## Fixed centers versus free charged optimization

Prosenjit Bose, Anil Maheshwari, Bobby Miraftab and Yota Otachi,
*3-Packings in Triangulations: Algorithms, Bounds, and Complexity*,
arXiv:2606.29743v1, Section 2.1, Theorem 7 and proof:
https://arxiv.org/html/2606.29743v1 .
The exact fixed-center Hall characterization applies to arbitrary eligible
connected graphs and uses two copies of each proposed center in a bipartite
matching. It does not select the center set in a cubic 3-connected graph.
ROOT-R05 used that characterization to cross-check finite center-set counts.
ROOT-R06 independently describes all constant-charge edge assignments and
proves that their weight-2n/3 layer is bijective with the actual P3-factors.
Neither source supplies the missing universal optimum bound.

## Relation to earlier repository candidates

At main 8aae1789e48f7ec5cf5a6a11272dbc214e182769, C04's p3-interface.md and C07's
mixed-cell proofs already use F3 divergence, subtree reconstruction and cycle
cancellation for replacement cells. These mechanisms are reused, not claimed
new. The additional content is the all-vertex charge problem, the identity
w=2n/3+b for every assignment, the exact minimum-factor bijection, and metric
restrictions from signed cycle-update costs. ROOT-R05 supplies G_m, the finite
positive controls. The old divisible-two-factor obstruction is not used as
an existence premise or as a counterexample to the root.

The charged equations are not the zero-boundary equations for ordinary flows,
and edge values are allowed to be zero. No nowhere-zero-flow or group-connectivity
theorem is imported. All combinatorial implications are proved in the candidate.
The search did not establish priority for this reformulation; no originality
or complete literature coverage is asserted. Source retrieval and matching
statements do not produce mathematical EvidenceLinks.
