# ROOT-R02 source and statement-difference note

Verdict: `candidate_only`. Retrieved 2026-09-06.

P. Hall, On Representatives of Subsets, Journal of the London Mathematical
Society s1-10 (1935), 26-30. DOI: 10.1112/jlms/s1-10.37.26.
Publisher metadata: https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/jlms/s1-10.37.26
Relation: prior art for distinct representatives / bipartite matching. Publisher
metadata was read; full original text was not claimed inspected. ROOT-R02 gives
a complete finite alternating-path proof of the exact matching consequence it
uses. Cloning a center twice and subtracting external-port demands are explicit
specializations, not new universal existence theorems for cubic graphs.

Alexander Kelmans, Packing 3-vertex Paths In Cubic 3-connected Graphs,
arXiv:0910.2766v2 (25 July 2011), https://arxiv.org/pdf/0910.2766v2.
Theorem 3.1, printed pp. 7-8, is about equivalences of universal assertions.
In particular the full P3-factor assertion must not be inferred from a bound
on the domination number or from a factor for one individual graph. Lemma 2.4,
pp. 6-7, treats three-cut crossing configurations. Theorem 5.1, pp. 24-25,
requires explicit brick hypotheses (h1)-(h3); it does not make arbitrary
signature sets feasible. Parsed theorem text was read. The web screenshot
service returned Internal Error on pages 7 and 8; no image inspection is claimed.

B. Y. Stodolsky, On Domination in 2-Connected Cubic Graphs, Electronic Journal
of Combinatorics 15 (2008), N38. DOI: 10.37236/913.
https://www.combinatorics.org/ojs/index.php/eljc/article/view/v15i1n38
Relation: assumption mismatch, not a root counterexample. Its abstract constructs
2-connected cubic domination counterexamples. The frozen root requires
3-vertex-connectivity; this cannot be silently weakened to two.

B. Brešar, T. Dravec and M. A. Henning, A proof of the 3/8-conjecture
for independent domination in cubic graphs, arXiv:2510.14762,
https://arxiv.org/abs/2510.14762 (submitted 16 October 2025).
Relation: weaker numerical bound.
The abstract's bound is i(G)<=3n/8 with stated exceptions, not a size-n/3 center
selection satisfying all capacity Hall inequalities. It does not close root.
Only the abstract was used; no detailed proof or current revision audit claimed.

Existing repository dependencies at 130057cd97ee53d31d6a0898267bda05b9329e1e:
- research/artifacts/candidates/opg46613-root-r01/boundary-theorem.md:
  exact U/A/B gluing and residue semantics; prior candidate, not admitted evidence.
- research/artifacts/candidates/opg46613-root-r01/proof-addendum.md:
  explicit five-vertex replacement and code-transport limitations.

The new mathematical content is the explicit capacity/permanent realization
criterion, Hall-defect constraints, and a hand-checkable specified-center failure
on M12. No source is attributed a universal positive result beyond its statement.
