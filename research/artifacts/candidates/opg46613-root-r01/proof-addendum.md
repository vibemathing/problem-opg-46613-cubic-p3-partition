# ROOT-R01 addendum: hand-checkable residue-two brick and transport scope

Verdict: `candidate_only`. Target: `obligation:opg46613-root`.

## A. Explicit five-vertex replacement signature

Use vertices 0,1,2,3,4, edges 01,04,12,23,24,34, and ports in order (0,1,3).
The capped graph adds vertex 5 joined to 0,1,3. It is the triangular prism:
triangles (0,1,5) and (2,3,4), matching 04,12,53. It is simple cubic and
3-connected: deleting two vertices on one triangle leaves its surviving vertex
attached to the intact opposite triangle; deleting one on each triangle leaves
two connected edges with at least one matching edge surviving. Cases of fewer
deletions follow immediately.

In the table, a B pair is written (center,internal endpoint); P3 triples have the
center in the middle. U ports impose no role restriction on their vertices.

| State | A singletons | B pairs | Internal P3 |
|---|---|---|---|
| AAU | 0,1 | none | (3,2,4) |
| AUA | 0,3 | none | (1,2,4) |
| UAA | 1,3 | none | (0,4,2) |
| ABB | 0 | (1,2),(3,4) | none |
| BAB | 1 | (0,4),(3,2) | none |
| BBA | 3 | (0,4),(1,2) | none |
| BUU | none | (0,1) | (3,2,4) |
| UBU | none | (1,2) | (0,4,3) |
| UUB | none | (3,2) | (1,0,4) |

Each row uses every vertex once and only displayed edges. These are all nine
residue-two words. The converse follows from the conservation equation, so this
is a complete signature proof requiring no program. Consequently the residue-two
replacement in the main proof has an explicit small witness rather than depending
on the local census. No claim about arbitrary large bricks having all nine states
is made.

## B. Exact scope of the current GitHub candidate

The mathematical proof and this table are the submitted proof candidate. The
872-fragment / 72-gluing figures in the main draft are generator-side observations;
the executable audit material remains local and is not submitted or promoted.
The attempted upload of `p3_boundary.py` was blocked by a platform safety check;
there was no commit or HTTP result for it. The code is not resubmitted through
another endpoint, encoding or filename. The Issue checkpoint records that block.

References in section 7 of `boundary-theorem.md` describe prepared local replay
files, NOT files presently available in this branch. The current PR must not
claim a replay-ready code package. The boundary theorem, residue proof, triangle
and singleton controls, capping/gluing argument and conditional substitution
lemma are mathematical derivations and do not depend on those observed runs.
The exact Petersen-brick signature remains the explicit prior C04 candidate
cited in the main proof. Trusted verification, code-transport resumption and
canonical dependency repair remain open.

This addendum narrows transport claims; it does not alter any frozen ProblemContract,
record, source theorem, candidate computation result, or root status.
