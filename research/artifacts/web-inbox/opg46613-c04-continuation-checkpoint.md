# C04 continuation checkpoint

Verdict: `candidate_only`. Research state: `nonterminal`.
This is a checkpoint, not a WEB_ATTEMPT_PACKET, verifier receipt or admission record.

## Frozen binding

- Problem: `problem:opg-46613-cubic-p3-partition`
- ProblemContract SHA-256: `f22ec1937d8b771614cb85435b6d4e0712afb9a3939780e04b74e4649617c26a`
- Harness 1.1.2 SHA-256: `9ff6002285f1cc3ee7bec0a201a09d048dc0fa95a3156120d20aeb9b4177858a`
- Attempt: `attempt:web-20260906-opg46613-a01`
- Route: `route:two-factor-divisible-cycles-v1`
- Graph: `graph:opg46613-initial-v1`
- Target: `obligation:opg46613-divisible-two-factor`
- Root: `obligation:opg46613-root`
- Research Issue: #3
- C04 branch requested: `web/attempt-opg46613-a01-c04`
- C04 starting base: `4ea85f7f958211eed8ba3cdca91532e2d5e68618`

## Best preserved candidate

`best_verified_result=none`; `best_verified_candidate=none` under the admitted-verifier meaning.
Best previously preserved obstruction candidate: `candidate:opg46613-c02-small-obstruction`.
Its proof locator is `research/artifacts/candidates/opg46613-c02/proof.md`, SHA-256 `adefecbcb53362b57c9dc5326e4284a64c61db5b9e27046bc5f9b9af8a091275`.

The eighteen-vertex Petersen/Mobius sum has an explicit P3-factor, while every complementary 2-factor has a five-cycle. This is negative knowledge about the stronger route only. C01's failed-route proposal and the immutable C01-C03 packets must be retained; do not repeat the unchanged strengthening or reopen the obsolete pre-admission diagnosis.

## New C04 proof material

File-create actions have been requested for these candidate paths. Read back their actual contents and hashes before treating the transport as reconciled:

1. `research/artifacts/candidates/opg46613-c04/bg12.cpp`: no-isomorphism-pruning BG(c) construction trace search through order twelve, complete matching witness search and the eighteen-vertex negative control.
2. `research/artifacts/candidates/opg46613-c04/p3-interface.md`: exact nine-state Petersen-brick interface; two-way equivalence with a spanning forest whose components contain a multiple of three retained vertices and whose retained vertices have degree at most two; explicit three-retained-vertex and path-contained positive cases.
3. `research/artifacts/candidates/opg46613-c04/matching-spectrum-analytic.md`: a hand classification of thirteen Mobius-ladder matchings and six Petersen matchings, giving the exact twenty-six-matchings spectrum (5,13) x16, (4,5,9) x6, (5,6,7) x4 without relying on executable output.
4. `research/artifacts/candidates/opg46613-c04/all-admissible-orders.md`: for every k>=3, a simple 3-connected cubic graph on 6k vertices with a P3-factor but no divisible-cycle 2-factor. Use m=3k-4 and choose the bipartite Hamiltonian base as the 2m-vertex Mobius ladder for odd m or the prism C_m x K_2 for even m. The exact spectrum transform is {5,ell+3,ell_1,...,ell_r}, with two matching lifts per base matching.
5. `research/artifacts/candidates/opg46613-c04/port-minimality-and-cycle-loss.md`: nine is the minimum order of a universal cubic three-port brick; deleting the three Petersen-brick chords leaves a nine-cycle with ports at positions 0,3,6 and destroys every non-UUU boundary signature.

No SHA-256 for these newly requested remote writes is asserted in this checkpoint. These fields are pending exact-byte read-back and computation, not placeholders to be filled by guessing.

## Lower-order certificate scope

The degree-monotonicity reduction of a basic BG construction to operation (c) gives trace counts 2,72,4752,498960 at orders 6,8,10,12 after retaining the two K4 edge-pair orbits. These are construction-trace counts, not isomorphism-class counts.

The source bridge is Schmidt, *Construction Sequences and Certifying 3-Connectivity*, Section 2.2 and Theorem 2.5. The publisher locator must be reconciled to DOI 10.4230/LIPIcs.STACS.2010.2491, not the earlier draft locator ending 2490. The operation list is a section, not a Definition 2.2.

The lower-order proof, bounded execution metadata and output were prepared separately. Before publication, compare every compiler-version literal and histogram entry to the exact execution/output files; do not reuse a stale draft table. A global minimum-order eighteen conclusion depends on this source-faithfulness and exact replay. The all-orders existence construction above does not depend on that finite replay.

## Transport observability and recovery

In this continuation, later tool responses did not supply readable receipts in the working context. No HTTP status, permission change, new CI success or C04 merge is inferred from that absence. File-create and Issue-comment requests may have taken effect; absence of a readable response is not evidence that they failed. Therefore no blind duplicate branch creation, overwrite, packet hash or merge claim is justified.

No C04 packet/PR/check/merge success receipt is asserted here. This checkpoint also does not claim platform-forced quota termination or mathematical closure.

## Exact next actions

Fresh-read main, Issue #3 comments, the C04 branch and the candidate paths above. Reconcile the current head, all files, existing packets and any PR before new writes. Compute SHA-256 from the exact candidate bytes and preserve the actual output/metadata without promoting generator screening into Evidence. Complete exactly one schema-valid C04 WEB_ATTEMPT_PACKET with globally unique candidate IDs, the actual cycle base, and the Issue #3 binding. If a PR already exists, reuse it; otherwise create one, then backfill the real number and URL in the packet. Read the three required checks and merge only after all pass on the final head and the diff remains candidate-only.

The next mathematical attack is the global existence of the marked forest, starting with six retained vertices; it is not automatically implied by its three-retained-vertex case. When all frame vertices are retained the forest criterion includes the original problem, so the criterion alone cannot close the root.

Open obligations remain `obligation:opg46613-divisible-two-factor` and `obligation:opg46613-root`. All later checkpoints belong to the same Issue #3. No background execution is represented by this checkpoint.
