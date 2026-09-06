# C07 finite audit and transport reconciliation

Verdict: `candidate_only`. Primary owner: `math-proof`.
The three original C07 proof texts are preserved byte-for-byte. Their conclusions are local interface, gluing and conditional minimal-counterexample lemmas, not a proof of the root.

## Exact byte identities

At C07 head a3fae30d194d6a759fe6bbd14fd779348f4b086b the files were read and their UTF-8 bytes reconstructed locally. Both byte counts and Git blob hashes match the actual GitHub metadata. SHA-256 values were then computed from those same bytes:

| File | Bytes | Git blob | SHA-256 |
|---|---:|---|---|
| mixed-cell-forest.md | 12628 | 49e86424e0fb125a0bf2a5a61dafd0cd676cf39f | 7e11d9fdc6ea9e6c07dc69af5f8126d93c4ac1b7c3baf158bbba36020299cdf6 |
| source-polarity-cell.md | 9355 | 62e0e56d16f3ce7919c5adc6390d96addd5aed8c | 34d7d922e6b2c01997a038c0cb99b6742fc059484c81dc4c22ffca380cee9ba5 |
| triangle-nine-equivalence.md | 7923 | 2b7936565c577c14d0a4f3d08ae0017d4941742a | ed940982322b6b2707658fc565473fa1f684deaaa0569905db91b8ab6ee2fc70 |

## Finite test with an exact reproduction specification

Name the triangle T, the cyclic three-triangle cell D, the source-polarity cell J, and the Petersen-minus-vertex cell R. Use precisely their displayed edge lists and ordered ports. For D label a_i,b_i,c_i as 3i,3i+1,3i+2. For J use p0,p1,p2,w,x,y,z,r,s as 0,...,8. For R use its original 0,...,8 labels. The respective ordered port tuples are (0,1,2), (0,3,6), (0,1,2), (0,3,4).

A complete local enumeration scans every internal-edge subset, at most 2^12 per cell. Its connected components must have one of these forms: a singleton at a terminal, giving A; a single edge with a terminal chosen as its center, giving B there and unused state at any other terminal in the pair; or a three-vertex two-edge path, giving unused states at its terminals. Reject every other component. A two-terminal pair has two different center choices. Multiply the choices across components and count each resulting ordered signature. This procedure is exhaustive because the restriction of every factor has exactly those components. It counts selected edge sets together with the required boundary-center designation, not merely unordered vertex triples.

The resulting count vectors, in order 000,0AB,0BA,A0B,AAA,AB0,B0A,BA0,BBB, are:

- T: (3,1,1,1,1,1,1,1,0).
- D: (29,4,4,4,3,4,4,4,0).
- J: (13,5,7,5,0,3,7,3,5).
- R: (11,4,4,4,3,4,4,4,6).

All other ordered words have count zero. These finite counts support the exact signature sets. They also show that J's existence-level symmetry does not imply equality of ordered realization counts.

For each ordered pair of the four cells and each of the six permutations pi of the ports, add three disjoint joining edges. The gluing prediction is the sum over words s of N_left(s) N_right(t), where t_(pi(i)) is obtained from s_i by swapping A and B and leaving 0 unchanged. No path can use two joining edges, since the joining edges are a matching. Therefore the restrictions and their compatible union give a bijection, proving this counting formula.

As a different finite calculation, list every centered P3 (a,c,b), with a<b in the neighborhood of c. Recursively take the least uncovered vertex and branch over each centered P3 containing it and otherwise contained in the uncovered set. Sum the counts on the remaining vertices; the empty set has count one. Keep different centers even when their vertex sets agree in a triangle. Memoizing by the uncovered set changes runtime, not the recurrence or its exhaustive meaning.

All 96 gluing counts from this recurrence agreed with the signature formula. They range from 15 to 937. Each capped cell and each glued graph was checked to be simple cubic and connected after deleting every vertex set of size at most two. This concerns four explicit cells and their specified pairwise gluings, not all cubic graphs at any order. The raw graphs have orders six, twelve or eighteen; none is a root counterexample.

## Execution boundary

This was actual local generator-side work under Python 3.13.5, one process, CPU 35 seconds, wall 40 seconds, memory 256 MiB, and output cap 2048 KiB. The process exited zero. The algorithm has an additional 30-second internal deadline. The compact finite-audit.json preserves the counts, input labeling convention, local code hash and full-output hash. The local audit program is not represented as committed to GitHub, and no blocked executable upload was retried through another endpoint. The explicit algorithm above supplies a language-neutral reproduction specification. None of these tests is a registered verifier receipt or a full proof of the forest theorem.

## Reconciliation

Current base for this transaction is 4ce5d36f97de2e9e339401ca919006073e95bc93. The old C07 branch contained the three real proofs and two real Markdown checkpoints but no packet or PR. The mistaken duplicate Issue #10 was read and closed as duplicate, preserving Issue #3. The prior checkpoint statements about unavailable read-back are historical and are superseded by this note. A normal non-force baseline synchronization preserves both main and C07 ancestry; the net candidate diff must be checked before merge. No protected ledger, schema, Harness, workflow or Result is edited.

Next substantive task remains direct root research. In particular, ROOT-R04's feasible-center exchange continuation is separate from these cell theorems. A universal divisible-two-factor assertion is not assumed, and the obsolete root dependency in the protected DAG must eventually be reconciled by the trusted coordinator rather than silently used as a proof premise.
