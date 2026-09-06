# An explicit source-polarity cell and the full mixed forest criterion

Verdict: `candidate_only`. Primary owner: `math-proof`.
Problem: `problem:opg-46613-cubic-p3-partition`.
Attempt: `attempt:web-20260906-opg46613-a01`.
Target: `obligation:opg46613-divisible-two-factor`.
This is a finite interface candidate continuing the route-repair analysis. Neither the root nor a verifier obligation is declared closed.

## 1. A nine-vertex cell with a different exact interface

Let J have vertices p0,p1,p2,w,x,y,z,r,s, with terminals p0,p1,p2. Its internal edges are

```
wp0 wp1 wp2 p0x p1y p2z xy xr ys zr zs rs
```

The terminals have degree two and every other vertex has degree three. Attach exactly one external edge to each terminal.

Use the companion candidate's boundary states: 0 means an unused external edge, A is a singleton terminal receiving an edge from an outside P3 center, and B is an internal pair centered at the terminal and completed by an outside endpoint. Internal P3s, A singletons and B pairs must partition the cell vertices.

The exact signature set of J is

```
000, BBB, and all six ordered permutations of 0AB.
```

In particular AAA is absent. This is the sign-reversed zero-divergence interface of a triangle, not the interface of the Petersen cell.

## 2. Complete finite certificates

For 000 use the three P3s

```
(p0,w,p1), (p2,z,r), (x,y,s).
```

For BBB use pairs (p0,w), (p1,y), (p2,z), each centered at its terminal, and the P3 (x,r,s).

For A at pi, B at pj and 0 at pk, where i,j,k are all distinct, use the singleton pi and the B pair (pj,w). The six remaining vertices are pk together with x,y,z,r,s. Tile them according to k:

```
k=0: (p0,x,y), (z,r,s)
k=1: (p1,y,x), (z,r,s)
k=2: (p2,z,r), (x,y,s).
```

This gives a certificate for every ordered 0AB placement without assuming that J has all terminal-permuting automorphisms. Each listed consecutive pair is one of the displayed edges, and each certificate covers every cell vertex exactly once.

For AAA, all three terminals must be isolated in the internal restriction. The vertex w would then have no available neighbor, since its entire neighborhood is {p0,p1,p2}. It cannot belong to any remaining internal P3. Thus AAA is impossible.

If a,b count A,B, the vertex count gives a+2b=0 modulo three and a+b<=3. The only possibilities are (0,0),(1,1),(3,0),(0,3). Therefore no unlisted signature is possible, and the preceding argument proves the exact classification.

## 3. The cell has an original-domain three-connected completion

Add a vertex v adjacent to p0,p1,p2. The resulting ten-vertex graph H is a vertex three-sum of K3,3 and the triangular prism: remove one vertex from one part of K3,3, leaving the other two vertices v,w adjacent to p0,p1,p2; remove a triangle vertex from the prism, leaving the five-vertex graph on x,y,z,r,s with terminals x,y,z and edges xy,xr,ys,zr,zs,rs. Join the corresponding terminal triples.

Here is the required connectivity argument for a vertex three-sum of simple three-connected cubic graphs. Deleting at most one vertex in each of the two sides leaves each side connected, because in each original graph at most two vertices have been deleted including the removed sum vertex. At least one of the three joining edges survives. If both deleted vertices lie on one side, the other side is connected; every component on the affected side has a surviving terminal, because otherwise those same two deletions would disconnect that original graph from its removed sum vertex. All affected components are therefore joined through the unaffected side. This proves three-vertex-connectivity. The matching between distinct terminals preserves simplicity and cubicity.

Consequently H is a simple three-connected cubic graph. Its order ten is not eligible for the root and is used only as a completion of the cell. Substitution of J into a cubic frame is a vertex three-sum with H and preserves the same connectivity properties. An expanded graph with retained vertices U and order divisible by three is in the root domain whenever its frame is a simple three-connected cubic graph. No ten-vertex root instance is being asserted.

## 4. Exact mixed forest theorem with both polarities

Let a finite simple cubic frame Q have vertex partition U,T,Jset,P. Retain U as single vertices; replace T by triangles, Jset by copies of the displayed cell J, and P by Petersen-minus-vertex cells. Port bijections are arbitrary. The resulting graph has order

```
|U| + 3|T| + 9|Jset| + 9|P|.
```

It has a P3-factor exactly when Q has a spanning forest F satisfying:

1. Each tree contains a number of vertices of U divisible by three.
2. Every vertex in U has F-degree at most two.
3. At each degree-three vertex of T, the three branches of its tree do not all contain 1 modulo 3 vertices of U.
4. At each degree-three vertex of Jset, the three branches of its tree do not all contain 2 modulo 3 vertices of U.

Isolated unretained vertices are allowed. These are branch counts in the complete forest, not constraints on the immediate neighboring vertices. Petersen cells impose neither of the last two restrictions.

To prove necessity, orient selected P3 edges from center to endpoint and use values 0,+1,-1 on frame edges over F3. The divergence is -1 on U and zero on all cells. At a triangle the forbidden pattern is three outgoing edges; at J it is three incoming edges. Support degree is at most two at retained vertices.

As in the companion forest proof, cancel a nonzero support cycle with a scalar multiple of its unit circulation. No new support edge is introduced and at least one edge disappears. The extra restrictions are preserved: a degree-three restricted cell necessarily has all three incidence values equal, either all +1 or all -1. The circulation changes its two cycle incidences by opposite nonzero increments. One becomes zero and the other changes sign, so its support degree falls to two. A vertex already of support degree at most two cannot gain a third edge. After finitely many cancellations the support is a forest. Component divergence sums give condition 1. For a branch W adjacent to a cell t the incidence directed from t into W has value |U intersect W| modulo three. The two forbidden all-equal branch-residue patterns are exactly conditions 3 and 4.

Conversely root each tree and assign child-to-parent value minus the number of retained vertices in the child's subtree, modulo three. The root equation follows from condition 1. These values give the required divergences and support-degree bound on U. Conditions 3 and 4 exclude precisely the two forbidden local signatures. The remaining local signatures are realized by the explicit certificates here and in the companion proof. Gluing their selected external edges gives degree-two centers, degree-one endpoints, and no selected center-to-center edge. Every component is exactly P3 and all vertices are covered. This proves both directions.

Zero-valued forest edges cause no difficulty: they are removed before interpreting a local signature. If a cell has three nonzero incidences, their zero sum forces their outward values to be all +1 or all -1. Thus the branch-residue restrictions omit no other degree-three case.

## 5. What this rules out and what it does not

The triangle and J interfaces are incomparable: the triangle realizes AAA but not BBB, whereas J realizes BBB but not AAA. Both are contained in the Petersen cell interface. A claim that every nine-vertex three-port cell can be replaced by a triangle while preserving the same outside P3-factor is therefore false: choose the BBB certificate of J, which a triangle cannot realize. Conversely the AAA triangle certificate cannot be realized in J.

These statements concern exact local signatures and preservation of a specified outside factor. They do not assert that some eligible three-connected cubic graph has no P3-factor, or that changing a cell necessarily changes graph-level existence. Another global factor might exist even when a particular boundary certificate fails.

Replacing either a triangle or J by a Petersen cell preserves existence of P3-factors by local signature inclusion. Replacing J by a triangle is not justified by that argument. The earlier Petersen-to-triangle minimal-counterexample compression remains valid in its stated direction; the present example prevents its silent extension to all cells of the same order.

For any fixed retained set whose vertices lie on one path of Q, that path with all other vertices isolated is a qualifying forest whenever |U| is divisible by three. Its cell degrees are at most two, so neither polarity restriction is activated. This gives a positive construction independent of the number of cells of either polarity. No general path-existence or forest-existence theorem is asserted here.

## 6. Verification and provenance

The proofs use the displayed cell and explicit decompositions, finite congruence arithmetic, the supplied vertex three-sum connectivity argument, and the companion C07 mixed-cell forest proof. C04 supplies the fixed Petersen interface. No novelty claim, executable run, verifier receipt or admission is asserted. Next checks should replay every local certificate, audit the absent AAA argument and preserve both polarity constraints during cycle cancellation and gluing.
