# ROOT-R01 statement-difference note

Verdict: `candidate_only`. Retrieved 2026-09-06. Only bounded statement facts
and locators are retained, not paper text.

## Kelmans

Alexander Kelmans, *Packing 3-vertex Paths In Cubic 3-connected Graphs*,
arXiv:0910.2766v2 (25 July 2011), https://arxiv.org/pdf/0910.2766v2.

Lemma 2.4, printed pp. 6-7: crossing-path cases for a vertex 3-sum, with order
residues explicit. Relation: prior art for our three-port table, not an existence
theorem for every state. Theorem 3.1, pp. 7-8: equivalences between universally
quantified claims on cubic 3-connected graphs, including factors, prescribed-path
deletions, and residue-dependent deletions. Relation: equivalent global targets,
NOT a license to apply all deletion properties to an individual graph merely
because it has one factor. The proof of (z1)=>(f1), Theorem 3.10, pp. 11-12,
uses three copies of a putative bad rooted graph; this exposes the size increase
that a minimal-order induction must account for. Theorem 5.1, pp. 24-25, is a
composition theorem with hypotheses (h1)-(h3) on the bricks. Those hypotheses
cannot be dropped. Parsed theorem/proof text was read. An arXiv screenshot
request failed; no successful image inspection is claimed.

## Earlier repository candidate

`research/artifacts/candidates/opg46613-c04/p3-interface.md` at commit
`fe3c4aa3161dfc103f366a0df271e37bbbbce731`: all nine feasible states of Petersen
minus a vertex; marked-forest transfer for the corresponding special expansion.
Relation: prior candidate dependency for the explicit Petersen substitution.
ROOT-R01 extends to arbitrary fragments and repeated incidences, supplies exact counts
and a signature-inclusion replacement theorem. It does not repeat the false
universal divisible-two-factor assertion.

## Finite input generation, kept separate from ROOT-R01 interface proof

J. M. Schmidt, *Construction Sequences and Certifying 3-Connectedness*, STACS 2010,
Theorem 2.5, p. 636; BG operations on p. 635, Figure 1.
https://doi.org/10.4230/LIPIcs.STACS.2010.2491
https://drops.dagstuhl.de/storage/00lipics/lipics-vol005-stacs2010/LIPIcs.STACS.2010.2491/LIPIcs.STACS.2010.2491.pdf

The paper guarantees basic BG construction from K4 for every simple 3-connected
graph. For a cubic final graph, degrees of existing vertices never decrease,
so operations (a),(b), which increase an old degree, cannot occur. Only (c),
subdivision of two distinct edges and joining the new vertices, remains. This is
the outer-coverage bridge to be audited in ROOT-R02; ROOT-R01's universal interface theorem
does not depend on that enumeration. Figure 1 was actually inspected by screenshot.

RDKit official API: https://www.rdkit.org/docs/source/rdkit.Chem.rdmolfiles.html,
MolToSmiles and its canonical flag. Actual local version 2025.09.4, distinct from
the current documentation version. It was used only to propose full graph
serializations/isomorphism maps for the supplied inputs. Every deduplication
checked the complete adjacency under the returned permutation, so correctness
does not rest on an unverified claim of graph-key uniqueness.
