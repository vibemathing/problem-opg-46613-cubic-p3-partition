# C02: an 18-vertex obstruction and an infinite family with P3-factors

Status: `candidate_only`; primary owner: `math-proof`.
Candidate: `candidate:opg46613-c02-small-obstruction`.
Target: `obligation:opg46613-divisible-two-factor`; root retained open: `obligation:opg46613-root`.
Base: `c9ba094ce8240cf3b02c02cab67ca7265275c232`.

## Scope and dependencies

The domain is finite simple 3-connected cubic graphs of order divisible by three. The root conclusion is a vertex partition into noninduced P3 subgraphs. The stronger assertion S requires a perfect matching with every complementary cycle length divisible by three. C01 already supplies the constructive implication S(G) => P3-factor and an obstruction of order 30. C02 reduces the witness order to 18 and gives infinitely many graphs satisfying the root conclusion but not S. No minimum-order or novelty claim is made.

Use P with vertices a_i,b_i (indices modulo 5) and edges a_i a_(i+1), a_i b_i, b_i b_(i+2). C01 gives elementary proofs that P is 3-connected, P-a0 has a spanning 9-cycle, every P 2-factor is two 5-cycles, and each edge incident to a0 belongs to exactly two perfect matchings. It also proves that the cubic vertex 3-sum preserves 3-connectivity. The dependencies are frozen in `research/artifacts/candidates/opg46613-c01/proof.md`, SHA-256 `3f94eb0c0f06f3684e3fcae347358988d5613f475dc89c09e29138bc71ed9835`. They remain candidate lemmas, not admitted Evidence.

The vertex 3-sum operation is prior art: A. Kelmans, *Packing 3-vertex Paths In Cubic 3-connected Graphs*, arXiv:0910.2766v2, Section 2, observation 2.1. https://arxiv.org/abs/0910.2766v2 . The comparison with the root statement is in the C01 source note. The arguments below use the explicit definitions, rather than a claim of a new operation or a source theorem solving the root.

## C02.1: a three-edge-cut obstruction

Let B be any finite simple 3-connected bipartite cubic graph, let x be a vertex of B, and join the three neighbors of a0 in P-a0 bijectively to the three neighbors of x in B-x. Call the resulting graph J(B,x). It is simple and cubic, and the C01 vertex-sum lemma makes it 3-connected. Its order is |V(B)|+8.

Every spanning 2-factor F of J(B,x) uses an even number of edges of the three-edge cut between its two bricks: sum the selected degrees in either brick. Hence it uses zero or two cut edges. Zero is impossible because B-x is bipartite of odd order (B is cubic and has even order), whereas a disjoint union of cycles in a bipartite graph has even order. Therefore exactly two cut edges are selected.

On the Petersen side restore a0 and the two corresponding incident edges. This gives a spanning 2-factor of P, hence two 5-cycles. One of these cycles avoids a0 and remains an entire 5-cycle of F inside P-a0. Thus every 2-factor of J(B,x) contains a 5-cycle, and no perfect matching satisfies S. This exhausts all F without extrapolating from a finite matching search. J(B,x) lies in the root order domain when |V(B)| is congruent to 4 modulo 6.

## C02.2: explicit order 18+12q family and a P3-factor

For an integer q >= 0 set t=6q+5. Define B_q on c_0,...,c_(2t-1) with cycle edges c_i c_(i+1) (indices modulo 2t) and the t opposite chords c_i c_(i+t), 0 <= i < t. This is a simple cubic graph. Since t is odd, parity of the index gives a bipartition.

Here is a direct connectivity proof. Deleting zero or one vertex leaves the Hamiltonian cycle or a spanning path. For two deleted vertices, rotation and reflection normalize them to c_0,c_d with 1 <= d <= t. For d=1 the remaining cycle edges are a spanning path. For d>=2 they give two paths on indices 1,...,d-1 and d+1,...,2t-1. The surviving opposite chord c_1 c_(t+1) joins these paths. Thus deleting at most two vertices preserves connectivity, so B_q is 3-connected.

Set H_q=J(B_q,c_0), joining a1 to c1, a4 to c_(2t-1), and b0 to c_t. By C02.1 it is simple, cubic, 3-connected, has 2t+8=18+12q vertices, and every 2-factor contains a 5-cycle. Nevertheless H_q has a P3-factor with no cut edge selected: use consecutive triples of the spanning 9-cycle in P-a0 and consecutive triples of the path c1,...,c_(2t-1) in B_q-c0. Both vertex counts, 9 and 12q+9, are divisible by three. The two collections are vertex-disjoint and cover all vertices. This establishes the claimed strict separation throughout the family at candidate level.

## C02.3: full labeling and P3 witness for q=0

Label Petersen a_i=i, b_i=i+5 before deleting 0; remaining label j maps to j-1, giving 0,...,8. On B_0 delete c0 and map c_j to j+8, giving 9,...,17. Join (0,9),(3,17),(4,13). The complete edge list is in `witness.json`; it has 18 vertices and 27 edges.

A P3-factor, with the middle entry the center of each path, is

    (0,1,2), (4,7,5), (3,8,6),
    (9,10,11), (12,13,14), (15,16,17).

The labels occur once each and every consecutive pair is an edge. The three joining edges are unused. Hence H_0 is not a counterexample to the root conclusion.

## C02.4: all 26 perfect matchings and their spectra

For any perfect matching of H_0, its complementary factor uses two cut edges by C02.1, so the matching uses exactly one. Restore a0 and c0 on both sides with that chosen edge. This gives a perfect matching of B_0 and a Petersen matching containing the prescribed incident edge. Conversely every such pair reconstructs a unique H_0 matching. There are exactly two Petersen choices for each B_0 matching. Thus the count is twice the number of B_0 perfect matchings.

Classify B_0 matchings by the chosen opposite-chord index set D subset {0,1,2,3,4}. If D is empty, the 10-cycle has its two alternating perfect matchings. If D is nonempty, the remaining cycle edges form paths; all their vertex counts must be even. Equivalently the cyclic gaps between successive elements of D on the five-index circle must all be odd. The possibilities are: a singleton (five choices), three consecutive indices (five choices, gaps 1,1,3), or all five indices (one choice). Each nonempty choice leaves a unique matching of the remaining paths. This proves that B_0 has 2+5+5+1=13 matchings and H_0 has 26.

For completeness, the complementary spectra follow from these same cases. Indices in the following displayed cycles are c-indices modulo 10, not the final H_0 labels.

- No opposite chord chosen: for the matching (01,23,45,67,89), the complementary 10-cycle is (0,9,4,3,8,7,2,1,6,5); rotation gives the other case.
- Three chosen opposite chords: normalize D={0,1,2}; the complementary 10-cycle is (0,1,2,3,8,7,6,5,4,9). Rotation gives the five cases.
- All five chords chosen: the complement is the defining 10-cycle.
- One chosen chord: normalize D={0}; the complement has cycles (0,1,6,5,4,9) and (2,3,8,7). The five rotations give five (4,6) factors. The distinguished c0 lies in the 4-cycle for exactly two rotations and in the 6-cycle for three.

Thus B_0 has eight Hamiltonian complements and five (4,6) complements. Replacing c0 by the four-vertex Petersen path increases the cycle through c0 by three vertices and adds the internal Petersen 5-cycle. The two Petersen matching choices give exactly:

    spectrum (5,13):   2*8 = 16 matchings;
    spectrum (4,5,9):  2*3 =  6 matchings;
    spectrum (5,6,7):  2*2 =  4 matchings.

In particular every possibility contains a length not divisible by three.

## Reproduction, attacks, and limits

`screen18.py` constructs exactly this one labeled graph, checks simplicity/cubicity, checks connectivity after all 172 vertex-deletion sets of sizes at most two, enumerates all perfect matchings, and finds a P3-factor by exact-cover recursion. The saved generator-side run in `witness.json` used CPython 3.13.5, one process/thread, 20-second CPU and wall limits, 256 MiB address space, and 16 KiB output. Run from the repository root with `python3 research/artifacts/candidates/opg46613-c02/screen18.py`. This finite check agrees with all counts above; it is not a verifier receipt or a proof-assistant replay.

The essential assumption in C02.1 is the bipartite odd-order brick. Dropping bipartiteness may allow zero selected boundary edges and invalidate that step. The construction has a cyclic three-edge cut; it says nothing about the strengthening restricted to cyclically 4-edge-connected graphs. The infinite-family order and internal P3 partitions are explicit, not inferred from q=0. No claim that 18 is the smallest possible obstruction is made; orders below 18 have not yet been exhaustively audited here.

C01's failed-route proposal already records the unchanged universal strengthening. C02 improves the obstruction and extends its scope, so it does not add a duplicate failure record. The original root remains open. Next bounded tasks: audit the order-12 search space, generalize the brick cut count over bipartite frames, and derive weaker P3 boundary-transfer conditions that do not require divisible cycles.
