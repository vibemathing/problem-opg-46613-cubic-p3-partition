# ROOT-R04 source and statement comparison

Verdict: `candidate_only`. Retrieved 2026-09-06. No novelty or root closure claim.

## Exact fixed-center characterization

Prosenjit Bose, Anil Maheshwari, Bobby Miraftab, Yota Otachi,
*3-Packings in Triangulations: Algorithms, Bounds, and Complexity*,
arXiv:2606.29743v1, 29 June 2026, Section 2.1, Theorem 7:
https://arxiv.org/html/2606.29743v1 .
Although the paper studies triangulations, this theorem is stated for arbitrary
graphs. Its doubled-center Hall condition is expressed for X subset D:
2|N_C(X)|>=|X|. ROOT-R02 uses the equivalent center-side condition
|N_D(S)|>=2|S|. With |D|=2|C|, a failed center-side S gives the failed endpoint
set D-N_D(S), and a failed endpoint-side X gives the failed center set
C-N_C(X). Thus the characterization has exact prior art; it does not assert
that every cubic 3-connected graph has a suitable center set. The packing
bounds elsewhere in the paper must not be read as spanning factors.

## Incidence-core topology, not a center-set exchange theorem

Matt DeVos, Daryl Funk, Luis Goddyn, Gordon Royle,
*There are only a finite number of excluded minors for the class of bicircular
matroids*, arXiv:2102.02929v4, 20 October 2023, Introduction and Section 3.1:
https://arxiv.org/html/2102.02929v4 .
The paper describes bicycles, including theta and handcuff topology, as
bicircular circuit subgraphs. This is prior art for the terminology and shapes.
Our degree/cycle-rank proof derives their appearance in this specific Hall
incidence graph without importing a matroid representation theorem. A fixed
incidence graph does not remain fixed when C changes. No basis-exchange axiom
for feasible center sets is inferred from the topological resemblance.

## Recent edge-decomposition source has different output

Jicheng Ma, *Matching complements in subcubic graphs and a proof of the
3-Decomposition Conjecture*, arXiv:2608.25385v2, Theorem 1.3 and Section 5:
https://arxiv.org/html/2608.25385v2 .
The preprint states a matching-complement theorem for bridgeless degree-two/
three graphs with at least two degree-two terminals, and uses it for an EDGE
partition into a spanning tree, a 2-regular subgraph, and a matching. This is not
a vertex partition into P3s. It is not used as a premise of ROOT-R04 and has
not been independently certified here. Any future use would need a separate
statement bridge and proof audit, not a title-based root update.

All three source items were read directly; no article body is mirrored. The
ROOT-R04 minimal-core and exchange proofs are given in full in the candidate.
The 18-vertex control is a positive root instance with a bad specified center
set, not a counterexample to the ProblemContract.
