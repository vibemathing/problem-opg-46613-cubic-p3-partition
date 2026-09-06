# C03: unbounded cycle defects and positive triangle-expansion constructions

Status: `candidate_only`; primary owner: `math-proof`.
Candidate: `candidate:opg46613-c03-family-analysis`.
Target: `obligation:opg46613-divisible-two-factor`; root remains open.
Base: `3e449fd189511af83ed36bc5df9559f1a31afe90`.

## Scope and frozen inputs

Continue the consequence/repair analysis of the failed strengthening, not a renewed search for its universal proof. All graphs below are finite and simple; 3-connectivity is vertex connectivity. P3-factors are spanning subgraphs with noninduced three-vertex paths. The root asks for P3-factors, whereas the strengthening asks for a complementary 2-factor all of whose cycle lengths are multiples of three.

The Petersen presentation, its six perfect matchings, its vertex-deleted spanning 9-cycles, and the vertex 3-sum connectivity lemma are taken from the explicit arguments in `research/artifacts/candidates/opg46613-c01/proof.md`, SHA-256 `3f94eb0c0f06f3684e3fcae347358988d5613f475dc89c09e29138bc71ed9835`. Those are candidate dependencies, not admitted Evidence. The graph substitution operation is attributed there to Kelmans, arXiv:0910.2766v2, Section 2; neither the operation nor the following specializations are asserted to be new.

## C03.1: Petersen inflation of a bipartite frame

Let B be a simple cubic 3-connected bipartite graph with parts A and Z, each of size t. Equality of the sizes follows by counting the 3|A|=3|Z| cross incidences. For each a in A replace a by a separate copy of P-a0, attaching its three terminals a1,a4,b0 bijectively to the former neighbors of a. Leave every vertex of Z unchanged. Denote the resulting graph by T(B).

T(B) is simple, cubic, and has 9t+t=10t vertices. It is 3-connected by applying the C01 vertex 3-sum lemma at each replacement. Thus T(B) is in the root order domain precisely when 3 divides t.

For any spanning 2-factor F of T(B), let c_a count its selected edges leaving the brick for a. The cut has three edges and selected-degree counting makes c_a even, so c_a is 0 or 2. The t untouched Z-vertices each have selected degree two, and all their edges lead to bricks. Thus sum_a c_a=2t, forcing c_a=2 for every brick.

Restore a0 at each brick using the selected two terminal incidences. The result is a Petersen 2-factor. Consequently each brick contains one entire 5-cycle and a separate four-vertex path joining the two active terminals. Contract each such path to its original A-vertex and discard the internal 5-cycles. The remaining selected edges form a spanning 2-factor Q of B. A cycle of Q has length 2r, alternates between r A-vertices and r Z-vertices, and expands to length 4r+r=5r. Hence every spectrum has the exact form

    {5 repeated t times} union {5r_1,...,5r_s},
    where Q has cycle lengths 2r_1,...,2r_s and sum_j r_j=t.

Conversely every Q can be lifted this way. For the unique unused incidence at a, the Petersen graph has exactly two perfect matchings containing the corresponding edge at a0. Restrict either one inside the brick and use the unused boundary edge in the complementary matching. Choices at different bricks do not interfere. Thus each Q has exactly 2^t lifts and

    number of perfect matchings of T(B) = 2^t times that of B.

This count is nonvacuous. A cubic bipartite B has a perfect matching by a direct augmenting argument: if a maximum matching leaves an A-vertex uncovered, let X,Y be the A- and Z-vertices reachable from it by alternating paths. Every vertex of Y is matched (otherwise augment) and its matched A-partner is in X. Every neighbor of X belongs to Y. Thus |Y|<|X|, while counting the 3|X| incident edges into Y gives 3|X|<=3|Y|, a contradiction. Equal part sizes make the matching perfect.

## C03.2: quantitative obstruction to bounded-defect repairs

For a 2-factor F define b_c(F) to be its number of cycles whose lengths are not divisible by three, and b_v(F) to be the number of vertices on those cycles. Every factor of T(B) satisfies

    b_c(F) >= t = |V(T(B))|/10,
    b_v(F) >= 5t = |V(T(B))|/2,

because the t disjoint internal 5-cycles cannot be avoided.

If 3 divides t and B has a Hamiltonian cycle, lift that cycle as Q. Its one long lifted cycle has length 5t, divisible by three. The remaining t cycles all have length five. Both lower bounds are attained, so the minimum possible values are exactly t and 5t respectively.

There are arbitrarily large frames meeting these hypotheses. Take the prism with two disjoint (6q)-cycles and corresponding rungs, q>=1, and bipartition by parity of cycle index plus rail index. Each part has size t=6q. The prism is cubic and simple. If at most two deleted vertices lie on one rail, the other rail cycle is intact and each remaining segment on the damaged rail attaches to it by surviving rungs. If one vertex is deleted on each rail, both rails are paths and at least one rung survives. This proves 3-connectivity. Traversing one rail, crossing a rung, and traversing the other rail in reverse gives a Hamiltonian cycle.

Therefore the order-60q graphs T(B) have minimum bad-cycle count 6q and minimum bad-vertex count 30q. No repair of the route that allows only a fixed number of exceptional cycles can hold for the entire root domain. Likewise no universal bound strictly below half the vertices on exceptional cycles can hold. This is a limitation of two-factor-based repairs, not a negative conclusion about P3-factors. We do not assert a P3-factor for every possible T(B) merely from this spectral calculation.

## C03.3: a positive triangle-expansion lemma

Let G be simple cubic, S a nonempty set of its vertices, and v in S such that G-v has a Hamiltonian cycle C. Replace each u in S by a triangle with one vertex (port) for each of the three incident edges of u; connect ports according to the original edges. Let G_S be the resulting graph, of order N=|V(G)|+2|S|.

Choose the triangle replacing v as a cycle component. Lift C through all other vertices: at an unexpanded vertex retain its two C-edges; at an expanded u, connect the port for its predecessor on C to the unused third port and then to the successor port. These are two edges of a triangle. The lifted C is a single cycle using every vertex outside the v-triangle, of length N-3. The two cycles are disjoint and spanning. Thus if 3 divides N, they give a 2-factor with spectrum (3,N-3), and its complement is a perfect matching satisfying the stronger condition. Consecutive triples then give a P3-factor by C01.

If G is 3-connected, so is G_S: expanding one vertex is a vertex 3-sum with K4, hence the C01 connectivity lemma applies successively. The third port is included in each lifted passage; omitting it would fail the spanning requirement. Edges to the v-triangle are not selected, so the triangle really is a separate component.

Triangle expansion also preserves the existence of a Hamiltonian cycle in both directions. A Hamiltonian cycle in G_S must cross each expanded triangle's boundary in two edges, since the outside is nonempty, the boundary has size three, and the cycle is connected and spanning. Its two internal triangle edges form a spanning path through the three ports. Contracting every such path gives a Hamiltonian cycle in G. Conversely a Hamiltonian cycle of G lifts through every triangle by the same three-port passage. This proves the equivalence, including expansions at adjacent vertices.

## C03.4: all eligible Petersen triangle expansions are positive

In the Petersen graph every vertex-deleted graph has a spanning 9-cycle by C01. For |S| equal to 1,4,7,10 the expanded order 10+2|S| is respectively 12,18,24,30, and C03.3 constructs the spectra (3,9), (3,15), (3,21), (3,27).

This covers all 10+210+120+1=341 labeled choices of S. The count is of labeled subsets, not pairwise nonisomorphic graphs. The Petersen graph is non-Hamiltonian because all its 2-factors are (5,5); the preceding equivalence makes every one of these expansions non-Hamiltonian as well. Thus non-Hamiltonicity alone does not produce a stronger-route obstruction. In particular all these natural expanded-Petersen cases are eliminated from that search without needing a matching search on each expanded graph.

## Finite checks and limitations

`families.py` is a bounded standard-library reproduction script. It enumerates both base and inflated perfect matchings within the generator process for K3,3, the cube prism, and the hexagonal prism, comparing the spectra to C03.1. It also checks connectivity after every vertex-deletion set of size at most two on those three inflated graphs, and explicitly checks the constructed factor for all 341 labeled Petersen expansions.

The observed base/inflated matching counts are 6/48, 9/144, and 20/1280 for inflated orders 30,40,60. The corresponding deletion-set counts are 466,821,1831. Order 40 is deliberately outside the root order condition; it tests the general spectral formula, not a root instance. The actual output is `families-output.json`.

Reproduce with `python3 research/artifacts/candidates/opg46613-c03/families.py`. The saved run used CPython 3.13.5, one process/thread, a 20-second wall deadline and CPU limit, 256 MiB address space, and 32 KiB output. It is a generator-side exact check, not a verifier receipt. It does not enumerate all cubic graphs of orders 18,24,30,40,60. The proofs of the family statements are the arguments above, not extrapolations from these examples. No formal replay, mathematical EvidenceLink, or Result admission is claimed.

Next bounded obligations: a source-faithful exhaustive generator for the order-12 domain, then exact P3 boundary-transfer states for the Petersen brick. The unchanged divisible-cycle strengthening is not being retried; root closure still needs a different sufficient mechanism.
