# Independent retained vertices: a constructive positive class

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This advances the marked-forest repair criterion. The root remains open in repository truth. No novelty, verifier receipt or admission is asserted. Every combinatorial lemma used below is proved here.

## 1. Main candidate statement

Let Q be a finite simple cubic graph with edge connectivity at least three. Let U be an independent set of vertices, with |U| divisible by three, and replace every vertex of S=V(Q) minus U by a Petersen graph with one vertex removed, attaching its three terminals to the incident frame edges by any bijection. Then the expanded graph has a P3-factor.

The proof constructs a spanning tree T of Q with degree at most two at every vertex of U. The marked-forest transfer theorem in `p3-interface.md` then applies to the single component T. The case U empty is immediate from the local UUU tiling; assume U is nonempty below. Since Q is cubic and U is independent, S is nonempty and every neighbor of U lies in S.

In fact, for any specified u_0 in U the spanning tree can be chosen with u_0 a leaf. No assertion is made that the same spanning-tree conclusion holds for arbitrary non-independent U.

## 2. Pair-selection lemma

Consider a finite indexed family E of subsets of a finite set W. Different indices may have the same subset. Suppose that for every nonempty subfamily A,

```
|union(A)| >= |A|+1.
```

Then one can choose, from each indexed subset e, a pair of distinct elements of e so that the resulting indexed pairs form a forest on W. Parallel selected pairs would form a two-edge cycle and are therefore excluded by the conclusion.

### Proof by induction on |E|

The empty family is immediate. Each nonempty indexed subset has at least two elements by the hypothesis for a singleton subfamily.

First suppose there is a proper nonempty tight subfamily A, meaning |union(A)|=|A|+1. Induction gives a forest representing A on W_A=union(A); it has |W_A|-1 edges and is therefore a tree spanning W_A. Contract W_A to one new element and consider the remaining indexed subsets, with this contraction applied to their elements.

The contracted remaining family still satisfies the hypothesis. For a subfamily B that meets W_A, the original inequality for A union B gives

```
|union(B) outside W_A| >= |B|,
```

and contraction supplies one further element representing W_A. For B disjoint from W_A, its union is unchanged and the original inequality applies directly. Thus induction represents the contracted remaining family by a forest. Lift each occurrence of the contracted element to an original element belonging to the relevant indexed subset and W_A, and expand that element to the already chosen tree on W_A. Expanding a vertex of a forest into a tree preserves acyclicity. This produces the desired representation of E.

Now suppose no proper nonempty tight subfamily exists. Choose an indexed subset e and two distinct elements x,y in e. Remove e and contract x,y to one element. For every nonempty subfamily B of the remaining family, B was proper in E, so its original union has at least |B|+2 elements. Contraction reduces this count by at most one. Induction therefore applies. Expanding the contracted element to the chosen edge xy preserves the forest property. This completes the induction.

The argument uses indexed subfamilies throughout, so repeated hyperedge subsets are handled without identifying their indices.

## 3. A partition criterion for a spanning pair-tree

Let H be a finite indexed family of nonempty subsets of a finite set W, with p=|W|. Suppose that for every partition of W into r>=2 nonempty parts, at least r-1 indexed subsets meet two or more parts. Then some p-1 indexed subsets admit pair choices forming a spanning tree on W. Subsets of size one can be ignored when choosing pairs.

Choose a subfamily F of maximum size satisfying the inequality in Section 2 for every nonempty subfamily. Its pair representation is a forest, so |F|<=p-1. Suppose |F|<p-1.

Call A contained in F tight when it is nonempty and |union(A)|=|A|+1. If the vertex unions of two tight subfamilies A,B intersect, their union is tight. To check this, the inequality for A union B gives

```
|union(A) intersect union(B)| <= |A intersect B|+1.
```

If A intersect B is nonempty, its own inequality gives the reverse bound; if it is empty, the assumed nonempty vertex intersection supplies the reverse bound 1. Equality follows in either case, and hence A union B is tight.

It follows that the maximal vertex unions of tight subfamilies are pairwise disjoint. Use these unions as partition parts and add singleton parts for all remaining vertices. Let the resulting partition have r parts. Within a tight part W_i, exactly |W_i|-1 indexed subsets of F are contained entirely in that part. Indeed its defining tight subfamily has that size, and an additional F subset contained there would violate the defining inequality. A singleton part contains no subset of F. Hence the number of F subsets internal to parts is p-r, and the number crossing parts is |F|-(p-r).

Every unused subset e of H is internal to one part. This is immediate when e has size one. Otherwise maximality of F means adding e violates the inequality on some subfamily A union {e}. A cannot be empty because |e|>=2. The inequality for A itself forces |union(A)|=|A|+1 and e contained in union(A); thus e lies in a tight part. Therefore all crossing subsets of H are already in F, and their number is

```
|F|-(p-r) < r-1.
```

This contradicts the partition hypothesis. Consequently |F|=p-1, and the forest representation from Section 2 is a spanning tree on W.

For p=1 the empty pair-tree gives the conclusion directly.

## 4. Apply the criterion to a cubic frame

Let W_1,...,W_p be the vertex sets of the connected components of Q[S]. For each u in U, make an indexed subset e_u of {1,...,p}, consisting of the components containing its neighbors. Some e_u may have size one or two when several neighbors lie in the same component. Their indices remain distinct even when two subsets coincide.

Take any partition of {1,...,p} into r>=2 parts. For each part, take its S vertices and also every vertex of U whose entire neighborhood lies in those S vertices. Call these r vertex sets A_1,...,A_r. Let X be the remaining vertices of U; equivalently, X indexes exactly the subsets e_u crossing the partition.

Each A_i is a nonempty proper vertex set of Q. There are no edges between different S components, and U is independent. Therefore every edge leaving A_i goes to X, and every vertex of X contributes exactly three edges to the sum of all these boundaries. Edge connectivity at least three yields

```
3r <= sum_i |delta_Q(A_i)| = 3|X|.
```

Thus at least r indexed subsets cross the partition. In particular, even after deleting the single indexed subset e_(u_0), at least r-1 crossing subsets remain. Section 3 supplies a spanning pair-tree on the p S components using some vertices of U other than u_0 as its distinct edge indices.

Choose an arbitrary spanning tree inside each component Q[W_i]. For each selected index u whose chosen pair is {i,j}, retain one original edge from u to W_i and one from u to W_j. This replaces the corresponding pair-tree edge by a path through u. For every unselected vertex of U, retain one arbitrary edge to an S neighbor and attach that vertex as a leaf.

The resulting graph spans Q. It is connected and acyclic: the component trees expand the vertices of a tree, the selected U vertices subdivide its edges, and the remaining U vertices are added as leaves. Every selected U vertex has degree two; every unselected U vertex has degree one. In particular u_0 is a leaf.

Since |U| is divisible by three, this spanning tree satisfies the one-component case of the exact marked-forest criterion. The local Petersen-brick certificates and the subtree-flow construction from `p3-interface.md` give a P3-factor of the expanded graph, for every port attachment bijection.

## 5. Bipartite frames admit a simpler proof and need only connectedness

Suppose Q is a connected cubic bipartite graph with bipartition U,S. Both parts have the same size t, by counting incident edges. Fix u_0 in U. For every nonempty A contained in U minus {u_0}, cubic regularity gives |N(A)|>=|A|. Equality would use all three edges of every vertex of N(A) on vertices of A; then A union N(A) would be a connected-component union separated from the rest of Q. This contradicts connectedness, since u_0 lies outside it. Thus

```
|N(A)| >= |A|+1.
```

The t-1 indexed triples N(u), for u in U minus {u_0}, satisfy Section 2. Their selected pairs form a forest with t-1 edges on the t vertices of S, hence a spanning tree. Subdivide each selected edge by its corresponding u, and attach u_0 by any incident edge. This is a spanning tree of Q with every U vertex of degree at most two.

Consequently, whenever t is divisible by three, replacing all vertices of one side of any connected cubic bipartite frame by Petersen bricks gives a graph with a P3-factor. No Hamiltonian cycle of the frame is assumed. For the original 3-connected domain, choose frames that also are 3-connected; the P3 construction itself does not need that extra hypothesis.

This directly complements C03's divisible-cycle obstruction for bipartite frames: the forced internal five-cycles do not prevent P3 tilings, even when no Hamiltonian frame witness is available.

## 6. A shorter witness for the C01 thirty-vertex graph

Use the C01 labeling with brick offsets 0,9,18 and hub vertices 27,28,29. Apply BBB in the first brick, complete its three pairs with the three hubs, and use UUU in the other two bricks. The ten paths are

```
(5,0,27), (8,3,28), (7,4,29), (2,1,6),
(9,10,11), (13,16,14), (12,17,15),
(18,19,20), (22,25,23), (21,26,24).
```

The triples are disjoint and exhaust vertices 0,...,29. Every consecutive pair is a C01 internal edge or one of its joining edges. This is a more modular P3 witness for the existing graph, not a new graph or a new obstruction count.

## 7. Scope, sources and next attack

The auxiliary pair-selection and partition criteria are proved in full rather than assumed from a library. A bounded source search for hypergraphic-matroid shrinking and constrained spanning trees was requested, but no readable source receipt was available in this continuation; no priority or attribution conclusion is drawn from that search. The external-theorem dependency of this particular proof is therefore empty. Its graph and local-certificate dependencies are the already specified C01 brick and the companion exact interface candidate.

The independent-set assumption is essential to the boundary-counting construction used here: it makes every edge at a crossing retained vertex go to an S region and eliminates edges between retained vertices. The proof has not shown that the conclusion fails without that assumption; it has only identified where this argument stops.

The next open repair case is a retained set of six vertices with adjacencies. Do not promote the present positive subclass into the general marked-forest assertion. When no vertices are replaced, the latter includes the original P3-factor question. Both admitted obligations remain open in repository truth, pending the required verification and any coordinator action.
