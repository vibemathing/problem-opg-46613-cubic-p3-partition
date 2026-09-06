# C04: complete lower-order replay and the order-18 route obstruction

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
Root: `obligation:opg46613-root`, still open in repository truth.

## Frozen claim and scope

Candidate conclusion: eighteen is the least possible order of a finite simple
3-connected cubic graph with no perfect matching whose complementary cycles all
have lengths divisible by three, when the graph order is divisible by three.
This is NOT a minimum counterexample claim for the original P3-factor problem.
The displayed eighteen-vertex graph has a P3-factor.

This conclusion combines the self-contained finite-combinatorial cover proof in
`lower-order-factor-cover.md` with the exact finite certificates below. Neither
candidate-side replay nor transport checks constitute a mathematical EvidenceLink.

## Complete lower-order argument

The handshake identity forces an eligible cubic order to be a positive multiple
of six. Below eighteen the only possible orders are six and twelve.
The companion proof supplies the perfect-matching criterion via edge saturation,
then its application using odd-component cut counts in a 3-edge-connected cubic
graph. It also supplies the implication from 3-vertex to 3-edge connectivity.
Thus a complementary 2-factor exists. At order six its only length partitions
are (6) and (3,3), so it is automatically divisible.

At order twelve the only bad length partitions are (4,8), (5,7), (3,4,5), and
(4,4,4). Fix each cycle union on consecutive vertex labels. Every putative
obstruction can be relabeled as one of these unions plus a disjoint perfect
matching. The least-unmatched-vertex recursion enumerates each such matching
exactly once. Connectivity is checked after every deletion of zero, one, or two
vertices. No isomorphism pruning or unproved graph-catalog coverage is used.

The local run of the already frozen `factor_cover12.cpp` produced the following
complete counts. These count specified cycle/matching unions, not isomorphism
classes.

| Fixed bad factor | Disjoint matchings | 3-connected unions with a good witness |
|---|---:|---:|
| (4,8) | 3327 | 2448 |
| (5,7) | 3325 | 2940 |
| (3,4,5) | 3330 | 2520 |
| (4,4,4) | 3329 | 1728 |
| Total | 13311 | 9636 |

Every retained union has a supplied perfect matching with divisible complement.
The sibling Python checker checked the witnesses by component traversal and
regenerated the entire input cover. The selected good spectra were (12):8068,
(3,3,6):34, (3,9):754, and (6,6):780. These are selected witnesses, not the full
matching spectrum of each union.

## Exact certificate transport

The full TSV has 269886 bytes and SHA-256
`57e0f9d1365ad6a053c9c35b3cc1c005470f4c469d2f8882dcb89c5773403960`.
It is represented losslessly by `cover12-ranks.json` and
`expand_factor_cover12.py`. For each retained union in the deterministic input
order, a byte selects a zero-based rank among its perfect matchings. There are
9636 bytes, with ranks 0 through 5. The compressed data is a finite certificate,
not executable text. Expansion regenerated the TSV byte-for-byte and checked its
length and digest. Expansion alone is not a positive-witness check; the separate
checker must still be run.

Commands, relative to this candidate directory, with fresh output filenames:

```sh
g++ -std=c++17 -O2 -Wall -Wextra -pedantic factor_cover12.cpp -o factor_cover12
./factor_cover12 > generated.tsv
python3 -S expand_factor_cover12.py cover12-ranks.json expanded.tsv --seconds 15
python3 -S check_factor_cover12.py expanded.tsv --seconds 30
python3 -S audit_controls.py expanded.tsv
```

Use one process/thread and external wall, CPU, memory and output limits from
`execution-observation.json`. Exact compiler/interpreter versions and observed
exit statuses are recorded there. No package installation is needed. The final
expansion used a clean environment and disabled site imports; two earlier
inherited-environment attempts were resource-terminated and are recorded as
failures, not mathematical negatives. No full Harness command was run locally.

## Negative and adversarial controls

`audit_controls.py` contains the frozen C02 graph's explicit 27-edge list and six
P3 paths. It checks all 172 deletion sets, enumerates all 26 perfect matchings,
and obtains (5,13) sixteen times, (4,5,9) six times, and (5,6,7) four times.
Each complement contains a five-cycle. The six explicit P3 paths cover all
vertices exactly once and use actual graph edges. Hence the same graph separates
the stronger route from the original question.

The checker rejects five explicit certificate mutations: missing DONE marker,
omitted first case, duplicate first case, the bad original matching substituted
as a supposed positive witness, and an incorrect footer. These attacks test
specific failure modes; they are not a proof that the programs have no bugs.
The programs and finite-cover proof remain available for another trust domain to
replay, formalize and review for statement faithfulness.

## Audit boundary and continuation

Only the finite cover, its supplied witnesses, and the explicit eighteen-vertex
control are newly reported as executed here. Earlier C04 drafts, including BG
construction coverage and the marked-forest/quotient deductions, are preserved
as candidate derivations; their presence does not turn them into replayed facts.
The BG program was not needed for this replay.

The C01 failed-route proposal remains the existing proposal; no canonical
failure ledger is edited. Both admitted obligations remain open. The next
substantive repair step is to combine the exact P9 interface with the published
nine-point cyclability theorem, rather than enumerate nine-retained quotients
whose positive answer follows from that source. No unchanged attempt to prove
the obstructed divisible-cycle assertion is being resumed.
