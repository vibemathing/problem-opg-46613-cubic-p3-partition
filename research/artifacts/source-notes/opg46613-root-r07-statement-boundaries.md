# ROOT-R07: statement boundaries and pending source comparison

Verdict: `candidate_only`. Primary owner: `math-proof`.
This note records exact logical relationships. It does not assert a newly retrieved publication, a novelty result, an executed test, or a mathematical admission.

## Frozen root

For every positive integer k, every finite simple 3-vertex-connected cubic graph on 3k vertices has a spanning subgraph whose components are k selected copies of P3. The selected copies need not be induced. Cubicity makes the admissible orders multiples of six.

Canonical source: `problem-library/records/canonical-problems.jsonl`.
ProblemContract SHA-256: `f22ec1937d8b771614cb85435b6d4e0712afb9a3939780e04b74e4649617c26a`.
The declared digest is not a claim of a new full Harness execution.

## Relationships of the current proof candidates

1. **Strict cycle descent: stronger auxiliary assertion, not an equivalent.** A one-defect charged flow has divergence 2 over F3 and weight 2n/3+1. The proposed assertion that it always has a strictly decreasing simple-cycle update is invalidated by the explicit families in `cycle-local-minimum-family.md`, `girth-five-cycle-minima.md` and `cyclic-five-cycle-minima.md`. The strongest family lies in the root domain with girth six and cyclic edge connectivity five. Every host has an explicit P3-factor. These examples therefore do not negate the root.

2. **Twelve-pattern repair interface: exact for a specified flow and specified update class.** `complete-one-defect-cycle-interface.md` characterizes all strictly improving simple-cycle updates of a one-defect flow. It does not characterize all possible ways of changing a factor candidate. Neutral updates, temporary increases and larger circulation supports are not excluded by failure of its tests.

3. **Neutral transition table: exact local description, not a global termination theorem.** `neutral-defect-transitions.md` gives the exact defect change r+z-eta and source-edge potential change. It does not prove that every one-defect neutral component reaches a strict repair. A connected repair difference can have a cubic bipartite branch core; a theta is exhibited in one family but is not asserted universal.

4. **Specified vertex deletion and specified edge avoidance: genuine global equivalents.** `root-equivalences.md` proves R=>D4=>E=>R by explicit three-port constructions. D4 quantifies over every vertex of every order-4-modulo-6 host. E quantifies over every edge of every order-0-modulo-6 host. These are equivalences of universal statements, not consequences of knowing that a particular graph has some factor. The reductions increase orders, and the finite-range translations are explicitly recorded.

5. **Triangle-free restriction: genuine global equivalent with an expansive witness reduction.** `triangle-free-root-reduction.md` constructs a girth-six 45-vertex cell with exactly the triangle's eight ordered P3 signatures. Replacing all triangles preserves factor existence and produces a triangle-free root-domain graph of order at most 15n. This does not prove that a smallest counterexample is triangle-free, does not eliminate all pre-existing squares and pentagons, and does not preserve high cyclic edge connectivity. The cell's internal girth is not a universal girth-six reduction.

The older divisible-two-factor strengthening remains a separate, already obstructed sufficient route. None of the current proofs invokes that universal strengthening as a premise.

## Provenance and attribution limits

The local F3 role and weight conventions continue the repository's ROOT-R06 `charged-flow.md` work. The three-port convention and the distinction between selected and induced P3s continue the earlier boundary-interface candidates. Current files provide their own finite constructions, tables and proof steps where used.

Publication searches for the precise Kelmans Lambda-factor equivalences and related packing statements were requested during this continuation, but no readable search result or full source statement was available in the working tool responses. Accordingly this note assigns no theorem number, DOI, publication date, quotation, current literature status or novelty claim. Exact source comparison remains pending and must be based on an actually read primary source, not on the filename or a remembered result.

A future comparison must distinguish spanning factors from near-perfect packings; every specified vertex from existence of some removable vertex; every specified edge from existence of some removable edge; and global equivalence from a pointwise or finite-order implication. In particular, none of the present single-edge statements authorizes avoidance of an arbitrary four-edge matching.

## Verification boundary

All R07 arguments are natural-language proof candidates. Their remote byte identities and packet bindings require actual read-back before any SHA-256 or transport success is asserted. No source search, self-review, Issue, PR, check or merge substitutes for the prescribed mathematical verification and statement-faithfulness review. Both canonical obligations remain open.
