# C06 source comparison for few-claw-center candidates

Verdict: `candidate_only`. Retrieved 2026-09-06. Owner: `math-proof`.

## Nine marked vertices

Holton, McKay, Plummer and Thomassen, Combinatorica 2 (1982), 53--62,
DOI 10.1007/BF02579281, publisher and author metadata as frozen in
`research/artifacts/source-notes/opg46613-c05-cyclability.md` at commit
`20f9a423a1185172eb41d06c39e2a0ce7b197fb5`.
https://link.springer.com/article/10.1007/BF02579281

The source supplies a cycle through nine specified vertices of a 3-connected
cubic graph. It is an exact reuse for that cycle subclaim, not the root or the
triangle contraction/gluing conclusions. C06 explicitly handles quotients with
fewer than nine vertices instead of assuming the source's quantifier settles
them. Its full proof is not audited here.

## At most twenty-three marked vertices, with planarity

R. E. L. Aldred, S. Bau, D. A. Holton and B. D. McKay,
*Cycles Through 23 Vertices in 3-Connected Cubic Planar Graphs*,
Graphs and Combinatorics 15 (1999), 373--376.
DOI 10.1007/s003730050046.
https://link.springer.com/article/10.1007/s003730050046
Author bibliography: https://users.cecs.anu.edu.au/~bdm/publications

The publisher's abstract says every set of at most twenty-three vertices in a
3-connected cubic planar graph lies on a common cycle, and states sharpness for
that cycle result. Metadata and the abstract were directly read; full subscription
content was not retrieved. The author bibliography corroborates attribution.

Relation to the planar marked-cycle subclaim is exact after the cell-contraction
hypotheses have been proved. The retained cardinality is divisible by three,
so the resulting upper bound is twenty-one. Source sharpness for common cycles
does not imply a sharp bound for P3-factors. Planarity belongs to the frame; only
the all-triangle specialization is used to deduce an intrinsic planar-G statement.
A Petersen-minus-vertex brick contains a subdivision of K3,3: suppress its three
terminals to obtain parts {1,7,8} and {2,5,6}. Thus including such a brick does not
preserve planarity, and no planar conclusion is based on that replacement.

## Existing claw-free work and scope difference

A. Kelmans, *Packing 3-vertex paths in claw-free graphs and related topics*,
arXiv:0910.4681, submitted 24 October 2009;
Discrete Applied Mathematics 159 (2011), 112--127,
DOI 10.1016/j.dam.2010.05.001.
https://arxiv.org/abs/0910.4681
https://www.sciencedirect.com/science/article/pii/S0166218X10001605

The author's abstract includes P3-factor existence with stronger prescribed-edge
properties for 3-connected claw-free graphs of divisible order. This is relevant
prior art for the zero-claw-center case. It does not by itself cover graphs with
positive claw-center count. The older arXiv:0711.3871 abstract omits the word
"induced" in its claw-free definition; the 2009 abstract and journal preview
include it, consistent with the definition used here. No theorem with the wrong
subgraph convention is imported, and none of the source's stronger edge/deletion
properties is asserted for C06's larger graph class.

## Admission boundary

The intrinsic triangle/cubic-connectivity argument and local flow proof are
candidate derivations. The cited cycle theorems are external proof dependencies,
not newly admitted axioms. These source comparisons do not prove novelty or
close a mathematical obligation. A complete primary-source proof audit and the
prescribed statement-faithfulness and proof checks remain necessary.
