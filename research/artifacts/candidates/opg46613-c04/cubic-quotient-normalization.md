# Cubic normalization of quotient data

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This removes the previously open lifting qualification in the finite quotient reduction. It also identifies a redundant filter in the preceding pruning proposal. No finite enumeration or verifier receipt is asserted.

## 1. Quotient hypotheses

Let K be a finite loopless multigraph. Its vertices are partitioned into retained vertices U and unmarked hubs. Assume:

- every retained vertex has degree three, counting parallel incidences;
- the graph induced by U is simple;
- there are no hub-to-hub edges;
- every hub has degree at least three;
- every nonempty proper vertex set has at least three incident cut edges.

The quotient of any original 3-connected cubic frame satisfies these conditions. Conversely, the construction below gives a simple 3-connected cubic frame with exactly this quotient. Feasibility of the F3 interface is unchanged by the construction.

The case with no hubs is included when the graph has at least four vertices. The nine-retained case necessarily has a hub, since a cubic graph has even order.

## 2. A cycle expansion preserving edge connectivity

Consider a vertex v of degree d>=3 in a loopless 3-edge-connected multigraph L. Its incident edges have distinct slots even when some have the same other endpoint. Replace v by a cycle of length d and attach one old incident edge to each cycle vertex. A suitable cyclic order of the slots makes the expanded graph 3-edge-connected.

Here is an explicit order and proof. Let C_1,...,C_c be the components of L-v. All edges leaving C_i go to v, and each such boundary has size d_i>=3. Color the corresponding slots by i.

If c=1, use any cyclic order. If c>=2, first arrange three slots of every color in the cyclic word

```
1,2,...,c, 1,2,...,c, 1,2,...,c.
```

Insert every additional slot next to a slot of the same color. For any nonempty proper union of colors, there are at least six transitions between that union and its complement around the resulting cycle. Indeed one full cyclic round has at least two transitions, the three rounds multiply this by three, and adjacent repetitions of one color do not change the transition count.

Suppose a nonempty proper cut in the expanded graph has size at most two. If it does not split the new cycle, it contracts to a cut of L of size at most two, which is impossible. If it splits the cycle, the cycle alone contributes at least two cut edges. Thus exactly two cycle edges cross, no other edge crosses, and the cycle vertices on one side form one cyclic interval.

Because no edge outside the cycle crosses, every component C_i is wholly on one side of the cut. Because no attachment edge crosses, the cycle slots on that side are exactly the slots of a union of those components. This is a proper nonempty union of colors. With c=1 it is impossible; with c>=2 it has at least six cycle transitions by construction, not two. The assumed cut cannot exist.

This proof treats every parallel edge as a separate slot and therefore does not assume that L is simple.

## 3. Normalize every hub

Apply Section 2 successively to all hubs of K. The retained vertices keep degree three. Every new cycle vertex has its two cycle edges and one attachment edge, so it also has degree three. Edge connectivity at least three is preserved at every step.

The resulting graph Q is simple. The old retained induced graph is simple. A hub had no loops or hub-to-hub edges, and its incident slots are attached to distinct new cycle vertices. Even parallel retained-to-hub edges now have different cycle endpoints. Every inserted cycle has length at least three. Thus no loop or parallel edge remains.

Each inserted hub cycle is a connected component of Q[V(Q) minus U], because there are no edges between different hub cycles. Contracting these components returns exactly K, including its incidence multiplicities. This gives an explicit cubic lift, not just a degree-sequence realization.

## 4. Why the cubic lift is 3-vertex-connected

A simple cubic graph with at least four vertices and edge connectivity at least three is 3-vertex-connected. The proof is short enough to include.

It has no cut vertex: after deleting one vertex, two or more components would each have at least three boundary edges in the original graph, but their boundaries together use only the three edges incident with that vertex.

Suppose deleting two vertices u,v disconnects it. If u and v are adjacent, only four edges leave {u,v}, fewer than the six required by two component boundaries. If they are not adjacent, there are exactly six such edges. There must be exactly two remaining components, each with a boundary of size three.

Each of these components has a neighbor at both u and v, since neither u nor v is a cut vertex. One component C therefore has two edges to one of them, say u, and one to v. The cut of C union {u} then has size

```
|delta(C)| + deg(u) - 2|E(C,{u})| = 3+3-4 = 2,
```

a contradiction. This proves the assertion and hence 3-vertex-connectivity of the lift Q.

The same counting argument works for deletion of two degree-three retained vertices in K, even though hubs can have higher degree. Consequently the retained-deletion condition proposed in `quotient-pruning.md` already follows from the exact three-edge-cut condition and retained degree three. It is a useful implementation consistency test, but not an additional mathematical filter. Likewise a hub with fewer than three distinct retained neighbors is incompatible with these conditions in the nine-retained setting. The proposed search should not claim extra coverage reduction from these redundant tests.

## 5. Exact preservation of P3-interface feasibility

The full quotient theorem in `quotient-reduction.md` applies to both the original frame and the normalized frame Q. In each case it characterizes the P3-factor of the Petersen-expanded graph by precisely the same quotient equations: divergence -1 and support degree at most two on U, and divergence zero on hubs.

Thus the two expanded graphs have P3-factors simultaneously. The internal flow on any connected hub region is reconstructed by the explicit subtree-sum formula already given there. No assumption about a Hamiltonian cycle inside the old unmarked region is needed.

A quotient failing the exact F3 feasibility test now has an explicit original-domain lift: construct Q as above and replace each of its unmarked cycle vertices by the Petersen nine-vertex brick. The vertex three-sum argument of C01 preserves simplicity, cubicity and 3-connectivity. Such a finite negative quotient, if actually found and its test verified, would therefore supply a finite graph witness in the original domain. This is a conditional construction, not a report that a negative quotient has been found.

## 6. Size bounds

Write k=|U|, e=|E(K[U])| and r=3k-2e for the number of retained-to-hub incidences. The normalized frame has exactly

```
|V(Q)| = k+r = 4k-2e
```

vertices, since a hub of degree d is replaced by d cycle vertices. Its Petersen-expanded graph has exactly

```
k+9r = 28k-18e
```

vertices.

For nine retained vertices in the previously isolated range 6<=e<=12, these formulas become 36-2e and 252-18e, respectively. Therefore a bad quotient in this finite range would have a normalized original-domain witness of at most 144 vertices, regardless of how large an initial unmarked frame region was. These are constructive size bounds, not executed searches or a claim that any bad quotient exists.

The exact quotient problem is now a finite equivalent reduction for each fixed retained parameter, not merely a necessary-condition superset with an unresolved cubic-lift condition. The outer enumeration, its certificates and their verification remain to be supplied.
