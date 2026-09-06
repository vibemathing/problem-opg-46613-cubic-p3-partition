# ROOT-R05 source and statement-faithfulness note

Verdict: `candidate_only`. Retrieved 2026-09-06. No novelty claim.

## Fixed-center characterization: exact known input

Prosenjit Bose, Anil Maheshwari, Bobby Miraftab, Yota Otachi,
*3-Packings in Triangulations: Algorithms, Bounds, and Complexity*,
arXiv:2606.29743v1, Section 2.1, Theorem 7 and its proof:
https://arxiv.org/html/2606.29743v1 .

The theorem is for arbitrary graphs of eligible order, despite the paper title.
It characterizes a possible center set via the endpoint-side doubled Hall
inequalities. The proof passes through a perfect matching on two copies of each
center. This is exact prior art for our finite center test, not an existence
result for an appropriate C in cubic graphs. No packing lower bound elsewhere
in the paper is promoted to a spanning statement. ROOT-R05's special initial
factor and its uniqueness follow directly from the displayed neighborhoods.

## Terminology for the special starting set

Mari Castle, Joe DeMaio, Keegan Gary, *Total Efficient Domination and Cayley
Graphs*, J. Combin. Math. Combin. Comput. 88 (2014), 147-159, publisher abstract:
https://combinatorialpress.com/jcmcc-articles/volume-088/total-efficient-domination-and-cayley-graphs/ .

The publisher defines efficient open domination by requiring every vertex to
have exactly one neighbor in the specified set. This is exactly our starting
private-endpoint condition, including the internal matching on centers. The
published Cayley-graph results are not used to supply our family or its
connectivity, and no general existence of such sets is inferred for the root.
This is a terminology/statement comparison, not a full-paper audit.

## Why matroid exchange is a separate premise

Taihei Oki and Tamas Schwarcz, *Generalizing the Multiple Exchange Property for
Matroid Bases*, arXiv:2511.16021v1, 20 November 2025, abstract:
https://arxiv.org/abs/2511.16021v1 .

The abstract describes exchange properties and local search for already given
matroid bases. We use only the explicitly stated ordinary basis-exchange axiom
as the definition being tested, not a theorem that P3-center sets form a matroid.
The record lists newer versions; no theorem from their unread full text is
imported. ROOT-R05 supplies explicit feasible C,C* and proves every single
exchange out of C infeasible, so it defeats the required axiom on V(G) itself.
It does not exclude every larger-ground-set or multi-center formulation.

## Difference from the repository's earlier barrier

ROOT-R04, `research/artifacts/candidates/opg46613-root-r04/hall-cores.md`, at
revision af5cba907a1c85dedd295402bd92407c7f5b6fb2, shows a one-exchange barrier
from a bad center set with a Hall-deficient support. ROOT-R05 instead starts
from a good set and has many other good sets. These are distinct assertions.
Neither is a root counterexample. Source hits, recurrence checks, and candidate
transport do not close the root or create an EvidenceLink.
