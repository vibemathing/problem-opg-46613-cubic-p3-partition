# A route obstruction at every admissible order at least eighteen

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This is a parametric extension of C02, not a claim against the original P3-factor statement. No executable output, novelty claim, EvidenceLink or Result is asserted.

## 1. A general Petersen/bipartite three-edge sum

Let P be the Petersen graph and choose a vertex p. Let B be any finite simple bipartite 3-connected cubic graph, and choose v in V(B). Delete p and v, then join their three respective neighbors by any bijection. Denote the resulting graph by G(P,p;B,v).

The vertex 3-sum deletion lemma of C01 shows that G is simple, cubic and 3-connected. Its order is |V(B)|+8. The Petersen brick has nine vertices; the other brick has |V(B)|-1 vertices, an odd number because every cubic graph has even order.

Let F be any 2-factor of G. The number of F-edges crossing the joining three-edge cut is even: sum the degree two over one side of the cut. Thus it is zero or two. It cannot be zero, because the B-minus-v brick is bipartite of odd order, and an internal 2-factor would partition that odd number of vertices into even cycles.

The crossing number is therefore two. Restore p and v and their two F-edges in the completed pieces. This yields a 2-factor of P and a 2-factor of B. Every 2-factor of P consists of two five-cycles, as explicitly classified in C01 and in the companion analytic matching certificate. The P-cycle avoiding p remains a five-cycle entirely within G. Consequently no 2-factor of G has every cycle length divisible by three.

This proof holds for every choice of the boundary bijection. It does not depend on enumerating perfect matchings or on Hamiltonicity of B.

## 2. Exact correspondence of perfect matchings and cycle spectra

Every perfect matching of G uses exactly one joining edge, by the preceding complementary-factor argument. Restoring the deleted vertices produces compatible perfect matchings of P and B. For a fixed matching of B, the edge matched at v fixes the port. Exactly two Petersen matchings use the corresponding edge at p; for p=a_0 these two choices per port are listed in the analytic certificate, and the two-subset representation transports the statement to any p.

Thus there is a two-to-one map from perfect matchings of G to perfect matchings of B, and

```
number_of_perfect_matchings(G) = 2 * number_of_perfect_matchings(B).
```

Let the B-complementary cycle through v have length ell, and let its other cycle lengths be ell_1,...,ell_r. Removing v and p and joining the two resulting paths gives a cycle of length (ell-1)+(5-1)=ell+3. The complete complementary cycle multiset in G is exactly

```
{5, ell+3, ell_1,...,ell_r}.
```

Because B is bipartite, ell and all ell_i are even. Hence every 2-factor of G has exactly two odd components, one of which is a five-cycle. This is an exact transformation of the complete cycle spectrum, not just a lower bound on the number of bad cycles.

## 3. Hamiltonian bipartite cubic graphs of every needed order

Fix k>=3 and put m=3k-4. Then m>=5. We construct a Hamiltonian bipartite simple 3-connected cubic graph B on 2m vertices.

### Odd m

Use the Mobius ladder with vertex set Z/(2m)Z, cycle edges i--(i+1), and diameters i--(i+m) for i=0,...,m-1. Since m is odd, every edge joins opposite parities. The outer cycle is Hamiltonian. The graph is simple and cubic for m>=3.

For 3-connectivity, deleting one vertex leaves the remaining outer cycle as a spanning path. For two deleted vertices, rotations and reflection reduce to deleted vertices 0,d with 1<=d<=m. If d=1, the remaining cycle vertices form a path. If d>=2, the surviving diameter 1--(m+1) joins the two nonempty remaining cycle paths. Therefore deletion of at most two vertices always leaves a connected graph.

### Even m

Use the prism C_m Cartesian-product K_2. Label its vertices (i,j), where i is modulo m and j is 0 or 1. Edges are (i,j)--(i+1,j) and (i,0)--(i,1). Since m is even, the coloring i+j modulo 2 is bipartite. The graph is simple and cubic, and a Hamiltonian cycle is

```
(0,0),(1,0),...,(m-1,0),(m-1,1),(m-2,1),...,(0,1),(0,0).
```

For 3-connectivity, if the two deleted vertices lie in one rail, the other rail remains a connected cycle and every surviving vertex in the damaged rail has a surviving vertical edge to it. If one vertex is deleted from each rail, each rail becomes a connected path and at least m-2>=2 vertical edges survive between the paths. The cases of zero or one deletion are contained in the same argument. Thus this graph is 3-connected as well.

## 4. The full-order obstruction family and an explicit P3 construction

Apply the construction of Section 1 to the graph B just defined. Its order is

```
|V(G)| = 2m+8 = 6k.
```

It is simple, cubic and 3-connected, and every 2-factor contains a five-cycle. Hence it is a counterexample candidate to the divisible-cycle strengthening at every admissible order 6k with k>=3.

Nevertheless G has a P3-factor. Delete v from the displayed Hamiltonian cycle of B to obtain a spanning path on

```
2m-1 = 6k-9 = 3(2k-3)
```

vertices. Partition this path into consecutive triples and retain the two path edges of each triple. In the Petersen brick use the three paths from C01, in its numeric labeling:

```
(0,1,2), (4,7,5), (3,8,6).
```

The two brick tilings are vertex-disjoint and together cover all of G. None of the three joining edges is used. The total number of P3 components is (2k-3)+3=2k=|V(G)|/3. This explicitly verifies why these graphs are not counterexamples to the original ProblemContract.

For odd k, m is odd and this recovers the order-18+12q Mobius-ladder family in C02. For even k, the prism construction supplies the previously missing orders 24+12q. Together they cover every positive multiple of six from eighteen onward. The handshaking identity forces every graph in the original cubic domain to have even order, so its order being divisible by three means exactly that its order is a multiple of six.

## 5. Lower-order scope and next verification

Within this particular Petersen/bipartite-sum construction, eighteen is the smallest admissible order. A simple cubic bipartite B has at least six vertices. The congruence |V(B)|+8=0 modulo 3, together with even |V(B)|, requires |V(B)|=4 modulo 6; the smallest such value at least six is ten, giving eighteen vertices in G.

This construction-specific lower bound is not by itself a global minimum-order theorem. Excluding all other possible six- and twelve-vertex graphs still needs the separate BG construction coverage and exact finite replay candidate. The present all-orders existence result and its P3-factor witnesses are purely constructive and do not depend on that replay.

Repository dependencies: C01 `proof.md` supplies the 3-sum connectivity lemma and Petersen matching classification; both are also expanded in the companion analytic certificate as needed. C02 is prior candidate work on the eighteen-vertex instance and the odd-k family. The open root and admitted target remain unchanged in repository truth.
