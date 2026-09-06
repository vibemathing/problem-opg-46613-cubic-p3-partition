# Traceability through order sixteen and the dense nine-retained cases

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This is a finite structural proof, not an enumeration report. No novelty or registered verification claim is made.

## 1. Candidate traceability theorem

Every finite simple cubic graph of edge connectivity at least three and order at most sixteen has a Hamiltonian path.

The perfect-matching existence input is proved, including its matching criterion, in `lower-order-factor-cover.md`. The remainder of the proof is supplied below. The theorem concerns Hamiltonian paths, not Hamiltonian cycles; in particular it makes no Hamiltonicity assertion about the Petersen graph.

## 2. Remove triangles inductively

The order is even. At order four the graph is K4 and the claim is immediate. Proceed inductively in even order.

Suppose a triangle T occurs and the graph has more than four vertices. Its three edges leaving T have distinct outside endpoints. If an outside vertex x received two or more of them, the cut of T union {x} would have size at most

```
3+3-2*2=2.
```

This is a proper nonempty vertex set because the graph has more than four vertices, contradicting edge connectivity. Contract T to one vertex and remove its internal edges. The resulting graph is simple and cubic of order two less. Every cut in it lifts to a cut in the original graph, so its edge connectivity is still at least three.

By induction it has a Hamiltonian path. If the contracted vertex is internal on that path, replace it by the three-vertex path in T joining the two used ports through its third vertex. If it is an endpoint, replace it by a path through all three triangle vertices ending at the used port. Either operation lifts the Hamiltonian path. It remains to handle triangle-free graphs.

## 3. A local path fact for a cycle with one chord

Consider a cycle C with either no internal matching chord or one chord xy. Call the vertices not incident with the chord the external ports; with no chord every vertex is a port.

Form an auxiliary graph on the ports, joining two ports when the cycle together with the allowed chord has a spanning path with those two endpoints. This auxiliary graph is connected.

With no chord it contains the cycle adjacency graph, since deleting an edge of C gives a spanning path with its endpoints.

With one chord, write the two cycle arcs as

```
x,A_1,...,A_a,y       and       x,B_1,...,B_b,y,
```

where a,b>=1 because xy is not a cycle edge. Consecutive ports within each arc are adjacent in the auxiliary graph, again by deleting their cycle edge. The path

```
A_1,...,A_a,y,x,B_1,...,B_b
```

uses the chord yx and joins A_1 to B_b while spanning all vertices. The analogous path joins B_1 to A_a. Thus the two arc paths of the auxiliary graph are connected to each other.

Consequently, if the external ports are colored with two colors and both colors occur, some spanning path has endpoints of different colors. This is all that will be needed; Hamiltonian paths between every prescribed port pair are not asserted.

## 4. A triangle-free two-factor has at most four components

Take a perfect matching M, and let F be its complementary 2-factor. Because the graph is triangle-free, every F cycle has at least four vertices. At order at most sixteen, F has at most four cycles.

With one cycle, delete any edge to obtain a Hamiltonian path. With two cycles, connectedness supplies an M edge between them. Delete one cycle edge incident with its port in each cycle. The two resulting spanning paths join through that M edge to give a Hamiltonian path.

Suppose F has three cycles. Contract the cycles and keep their cross-matching edges, discarding internal matching chords. The connected underlying graph on the three cycle-nodes is either a triangle or a path.

If it is a triangle, at least one F cycle has length four or five; otherwise the total order would be at least eighteen. Use such a cycle as the middle cycle. It has no internal M chord, since any chord of a four- or five-cycle creates a triangle in the original graph. All its vertices are therefore external ports. Color these ports according to the other cycle they meet. Both colors occur, so adjacent differently colored ports occur on the cycle. Delete the edge between these two ports. Break each of the other two cycles at an edge incident with its chosen port, and join the three spanning paths by the two selected matching edges.

If the three cycle-nodes form a path, each leaf cycle has at least three matching edges to the middle cycle, by the edge-connectivity hypothesis applied to its vertex set. The middle cycle therefore has at least six external ports. Its length is at most sixteen minus four minus four, namely eight. It can consequently have at most one internal matching chord. Color its external ports according to the two leaf cycles. The local fact of Section 3 gives a spanning path of the middle cycle, allowing that chord, with endpoints of different colors. Break each leaf cycle at its chosen port and join the three paths. Again the result is a Hamiltonian path of the whole graph.

## 5. Four four-cycles

If F has four cycles, all four have length four and the graph has sixteen vertices. No matching chord lies inside a four-cycle because the graph is triangle-free. Contract the four cycles. The quotient is a loopless 4-regular multigraph on four vertices, and every cut still has size at least three.

Label its vertices A,B,C,D. Equal degrees imply that opposite edge multiplicities are equal. Writing

```
x = m(AB) = m(CD),
y = m(AC) = m(BD),
z = m(AD) = m(BC),
```

we have x+y+z=4. For any pair of quotient vertices, its cut has size 8-2m, so m<=2. The only possible triples, up to permutation, are (2,2,0) and (2,1,1).

For (2,2,0), the underlying quotient is a four-cycle with every edge doubled. Choose a three-edge spanning path in that cycle and fix one matching edge for its middle connection. At each of the two middle F cycles there are two possible ports for its outer connection. A fixed port of a four-cycle has only one other vertex that is not adjacent to it. At least one of the two candidate outer ports is therefore adjacent to the fixed middle port. Choose it.

For (2,1,1), take the doubled pairs to be AB and CD, and use the quotient path A-B-C-D. Fix its unique BC connection. At B choose one of the two AB ports adjacent to its BC port; at C choose one of the two CD ports adjacent to its BC port. Such choices exist for the same four-cycle reason.

In both cases, each middle cycle has two chosen adjacent ports, so deleting the edge between them gives its spanning path. Break the two end cycles at their chosen ports. Joining these four paths along the selected three matching edges gives a Hamiltonian path of the original graph.

Sections 2-5 exhaust the induction and prove the candidate traceability theorem.

## 6. Consequence for the original small P3 orders

At orders six and twelve, the Hamiltonian path partitions into consecutive triples, each with its two path edges. Thus this proof also gives P3-factors for the original-domain graphs at both eligible orders below eighteen.

This consequence must not be confused with the stronger divisible-2-factor claim. A Hamiltonian path is not a spanning cycle, and the present proof does not remove the separate twelve-vertex two-factor coverage obligation. The four-bad-factor enumeration remains one route to that stronger lower-order certificate.

## 7. Eliminate the dense nine-retained quotients

Now consider a Petersen-replacement instance with nine retained frame vertices U. Let e be the number of internal retained edges. The preceding reductions leave 6<=e<=12. Its exact quotient has r=27-2e retained-to-hub incidences.

Use `cubic-quotient-normalization.md` to expand every hub into a suitably ordered cycle. The resulting frame is finite, simple, cubic and 3-connected, has the same quotient interface, and has exactly

```
9+r = 36-2e
```

vertices. If e is ten, eleven or twelve, this order is sixteen, fourteen or twelve, respectively. The traceability theorem supplies a Hamiltonian path in this normalized frame.

View that path as a spanning tree. It contains exactly nine retained vertices and has degree at most two at every retained vertex. It therefore satisfies the exact marked-forest criterion of `p3-interface.md`, regardless of the total path order. This gives a P3-factor after the unmarked cycle vertices are replaced by Petersen bricks. Exact preservation of quotient feasibility transfers the conclusion back to the initial, possibly much larger, unmarked frame regions.

Thus all nine-retained instances with e>=10 are positive at candidate level. The earlier sparse theorem covers e<=5. The only remaining nine-retained internal-edge counts are

```
e = 6,7,8,9.
```

Their normalized cubic frames have orders twenty-four, twenty-two, twenty and eighteen. If an actual bad quotient is found among them, the cycle-normalization and Petersen replacement give an original-domain witness of order 144,126,108 or 90, respectively. No such negative quotient is reported by this artifact.

## 8. What is still open

The finite quotient cover for e=6,...,9 has not been exhausted here. The endpoint-allocation shortcut and exact spanning-tree-coordinate F3 test remain available. Neither this parameter restriction nor a Hamiltonian-path proof through order sixteen supplies a general solution of the root obligation.

Both admitted obligations remain open in repository truth. Natural-language proofs, their self-audit and any future candidate CI must retain their actual evidence scope.
