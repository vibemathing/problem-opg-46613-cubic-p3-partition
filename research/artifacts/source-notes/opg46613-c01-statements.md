# C01 source and statement-difference note

Status: `candidate_only`; target `obligation:opg46613-divisible-two-factor`.
Retrieved 2026-09-06. Only bounded bibliographic facts and paraphrases are retained. No paper text or figures are mirrored. No assertion of research novelty or current global problem status is made.

## Frozen comparison

The contract concerns finite simple 3-vertex-connected cubic graphs and a vertex partition into noninduced P3 subgraphs. Handshake counting makes its order-divisible-by-3 condition equivalent to order-divisible-by-6 in this domain. The proposed all-cycle-lengths-divisible-by-3 condition is an explicitly stronger assertion, not a restatement.

## S1: perfect matching existence is weaker

Wuyang Sun, *Covering a cubic graph by 5 perfect matchings*, arXiv:1601.03248v2, 29 February 2016, Introduction, paragraph containing Petersen's theorem. https://arxiv.org/html/1601.03248v2 (CC BY 4.0; attribution retained).

The paper recalls that every bridgeless cubic graph has a perfect matching. Our 3-connected simple graphs are bridgeless and so meet that premise. Its conclusion ensures some complementary 2-factor but imposes no congruence on individual cycle lengths. A cover by several perfect matchings is also a different object from one matching with a restricted complement. Relation to the route: weaker. No matching-cover theorem is used to close the target.

## S2: exact P3 statement and construction attribution

Alexander Kelmans, *Packing 3-vertex Paths In Cubic 3-connected Graphs*, arXiv:0910.2766v2, 25 July 2011, Section 2, Figure 2, observations 2.1-2.3, and Theorem 3.1(z1). https://arxiv.org/pdf/0910.2766v2

The Lambda-factor definition matches a noninduced P3-factor. Theorem 3.1 compares universally quantified claims on cubic 3-connected graphs; it does not prove the universal conjecture, and must not be read as a pointwise implication from one graph's factor to all of its edge-deletion variants. Claim (z1) has the same root domain after handshake normalization. The graph used in C01 is the specialization Y(P,a0) of the paper's three-copy construction. Connectivity preservation is also stated there; C01 supplies a self-contained deletion proof. Relations: exact root statement; prior-art construction; no asserted equivalence with the divisible 2-factor route. PDF pages 6-7 and the construction diagram were inspected.

## S3: cycle spectra versus perfect matching index

J.-L. Fouquet and J.-M. Vanherpe, *On the perfect matching index of bridgeless cubic graphs*, arXiv:0904.1296v1, 8 April 2009, Section 3.2 and Figures 1-2; Section 6 on Petersen matchings. https://arxiv.org/abs/0904.1296v1 ; https://arxiv.org/pdf/0904.1296

The paper discusses both Blanusa snarks with a two-cycle factor of lengths 9 and 9. These are positive instances of the route, not a universal spectrum restriction. Its perfect matching index measures edge coverage by a family of matchings, not divisibility of the complementary cycles of a single matching. The Petersen matching facts used for our brick are reproved by the six-case classification in C01 rather than assumed from a covering theorem. Relation: prior art and special-family positive examples. The two figures were inspected as PDF images. The versioned PDF endpoint returned a transient error; the unversioned PDF identified itself as v1 and was readable.

## S4: mixed path factors are not P3-factors

Heping Zhang and Shan Zhou, *A note on path factors in claw-free graphs*, Ars Combinatoria 97 (2010), 87-95, p.88, Theorems 2 and 5 and Conjecture 3. https://combinatorialpress.com/article/ars/Volume%20097/volume-97-paper-9.pdf

The introduction distinguishes the cubic 3-connected P3 conjecture from a cited {P3,P4}-factor theorem for 2-connected cubic graphs. The authors' claw-free result allows P4 components and has additional hypotheses. Those conclusions do not supply a P3-factor on the contract's entire domain. Relation: weaker conclusion or restricted domain, not exact reuse. Page 88 was inspected as an image because text extraction returned no lines. Historical attribution is reported there as Akiyama and Kano, whereas Kelmans supplies a separate attribution; priority is not adjudicated here.

## Consequence for the candidate

Only standard graph definitions and the attributed graph construction are reused. The cycle-indexing implication, explicit Petersen classification, three-cut counting argument, and supplied P3 witness are written out in the companion proof. The resulting obstruction is to the stronger route only. No source hit, diagram, or generator-side check is treated as mathematical admission.
