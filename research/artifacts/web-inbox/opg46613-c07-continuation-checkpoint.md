# C07 continuation checkpoint

Verdict: `candidate_only`. Research state: nonterminal.
Problem: `problem:opg-46613-cubic-p3-partition`.
Attempt: `attempt:web-20260906-opg46613-a01`.
Route: `route:two-factor-divisible-cycles-v1`.
Graph: `graph:opg46613-initial-v1`.
Admitted target: `obligation:opg46613-divisible-two-factor`.
Root: `obligation:opg46613-root`.
Coordination Issue: #3. Do not create a duplicate research Issue.

## Mathematical content of this continuation

The following three proof artifacts were submitted to the file-create action on `web/attempt-opg46613-a01-c07-mixed-cells`:

1. `research/artifacts/candidates/opg46613-c07/mixed-cell-forest.md`: exact P3 forest criterion for retained vertices, triangles and Petersen nine-vertex cells. A degree-three triangle cell forbids the case in which each incident forest branch contains 1 modulo 3 retained vertices. The proof explicitly preserves this restriction during cycle cancellation. The K4/star example invalidates omission of the restriction while the expanded triangular prism still has an explicit P3-factor. Signature inclusion gives the conditional root lemma that a smallest-order counterexample cannot contain the designated induced Petersen nine-vertex cell: replacement by a triangle reduces order by six and preserves the root domain and the lifting of every smaller-graph P3-factor.

2. `research/artifacts/candidates/opg46613-c07/triangle-nine-equivalence.md`: a nine-vertex cell consisting of three triangles joined cyclically has exactly the triangle's eight P3 signatures. Its replacement map is two-to-one on perfect matchings; a complementary cycle of length L passing through the old triangle lifts to (L+3,3) or (L+6), while an isolated triangle lifts to (3,3,3) or (9). Thus both P3-factor existence and divisible-cycle 2-factor existence are preserved in both directions. Minimum-order counterexamples to either specified assertion cannot contain this induced nine-vertex cell. No confluence of repeated compressions is asserted.

3. `research/artifacts/candidates/opg46613-c07/source-polarity-cell.md`: the explicit nine-vertex cell with edges wp0,wp1,wp2,p0x,p1y,p2z,xy,xr,ys,zr,zs,rs has exactly 000, BBB and all six 0AB signatures; AAA is impossible because w would be isolated. Its completion is the vertex three-sum of K3,3 and the triangular prism. The mixed forest criterion extends by forbidding three branch counts all equal to 2 modulo 3 at these source-polarity cells. This prevents an unsupported extension of Petersen-to-triangle compression to arbitrary nine-vertex cells.

All three artifacts contain explicit local certificates, finite proofs and scope qualifications. They are not new attempts to prove the unchanged divisible-two-factor universal assertion. The prior eighteen-vertex obstruction and the already preserved positive P3 witnesses remain relevant negative knowledge; the root remains open.

## Transport reconciliation required

The last main revision confirmed in the available continuation context before C07 was `20f9a423a1185172eb41d06c39e2a0ce7b197fb5`. C07 branch creation was requested from that revision. Subsequent reads and writes did not consistently expose usable receipts in this continuation context. Do not infer a current main SHA, successful file read-back, exact byte digest, completed packet, PR number, passing checks or merge from an operation request. An unsuccessful read using a mistyped commit identifier does not establish that a file or repository is missing.

The three proof-file writes and this checkpoint write are requested transport operations. Reconcile their actual remote effects before retrying or replacing anything. Do not duplicate candidate paths or branch names blindly. An earlier code-bearing action awaiting platform approval elsewhere is not bypassed by these distinct prose-only candidates.

This Markdown file is a continuation note, not a schema-valid WEB_ATTEMPT_PACKET. No C07 attempt packet or PR is asserted by this note. Exact artifact SHA-256 values must be computed from successfully read-back bytes rather than guessed.

## Resume state

- `best_verified_result`: none.
- `best_verified_candidate`: none under the admitted-verifier meaning.
- Generator-audited content: the three finite proof candidates listed above.
- Open obligations: `obligation:opg46613-divisible-two-factor`, `obligation:opg46613-root`.
- Canonical failed-routes ledger: not edited by this continuation.
- Route state: obstruction consequences and weaker P3-interface analysis; unchanged universal strengthening not retried.
- Current transport limitation: receipt/read-back reconciliation and packet hashes pending in the available context; not a reported mathematical counterexample or an invented HTTP failure.
- C07 PR/check/merge status: unconfirmed; do not claim completion.

## Exact next action

Fresh-read main, Issue #3, the C07 branch and all open PRs. Read back the three candidate files and this checkpoint, compute their actual SHA-256 values, and audit the complete branch diff. Where the base has advanced, follow the protected baseline-sync policy without force-push or modifying protected files. Build one unique candidate-only C07 packet using the admitted identifiers and the actual base. Reuse an existing C07 PR if one exists; otherwise create one only after the packet is valid. Backfill its real number/URL, verify all three required checks on the final head, and merge only when they genuinely pass and the diff remains within the candidate allowlist.

Append the resulting checkpoint to Issue #3; preserve C01-C06 and their existing identities. No root Result, verifier identity, hidden reasoning, secret or full chat is stored here.
