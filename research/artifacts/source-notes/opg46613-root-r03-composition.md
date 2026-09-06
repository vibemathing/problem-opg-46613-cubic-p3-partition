# ROOT-R03 source comparison: composition is conditional

Verdict: `candidate_only`. Retrieved 2026-09-06.

Primary source: Alexander Kelmans, *Packing 3-vertex paths in cubic 3-connected
graphs*, arXiv:0910.2766v2 (25 July 2011),
https://arxiv.org/pdf/0910.2766v2 .

Theorem 3.1, printed pages 7-8, compares universally quantified assertions over
cubic 3-connected graphs. It does not permit upgrading the existence of one
factor in one smaller graph to every prescribed local deletion property there.
Observation 2.4, printed pages 6-7, classifies crossing paths at a vertex 3-sum.
Theorem 5.1, printed page 24, describes factor projection and products for graph
compositions under three explicit local deletion hypotheses. Its cap order is
two modulo six. ROOT-R03 instead assumes that the relevant bricks realize all
nine residue-allowed boundary words; its paired bricks have cap order zero
modulo six. Thus Theorem 5.1 is prior art for composition, not an automatic
verification of these hypotheses or of the root conjecture. PDF pages 7 and 24
were inspected as rendered pages in addition to parsed text.

Repository dependencies: ROOT-R01 boundary-theorem.md and proof-addendum.md at
base aadae0bf4828e112405f778a689389b33069a82e. They are proof candidates, not
admitted mathematical evidence. The replacement proof includes its own
connectivity argument and uses no uninspected BG theorem. The triangle control
only excludes boundary-preserving lifting of a specified factor; a different
factor is explicitly provided. There is no claim of a general failure of
triangle-based induction, no novelty claim, and no source-based root closure.
