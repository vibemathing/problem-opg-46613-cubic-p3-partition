# ROOT-R07: neutral defect transport and the structure of a repair difference

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root` under the existing admitted Attempt/Route/Graph.
This is a further finite proof candidate. It does not assert that neutral descent always reaches a P3-factor, and it does not report an executed search or a verifier receipt.

## 1. Local roles and a useful simplification

In a cubic graph, a nonzero edge value in F3 represents a selected direction. Divergence 2 permits exactly these roles: a source has two outgoing selected edges, a leaf has one incoming selected edge, and a defect has two incoming and one outgoing selected edge.

A flow with exactly one defect automatically has the six-vertex exceptional tree used in the companion files; no separate forest hypothesis is needed. Indeed the two selected edges entering the defect b come from two distinct sources a,c. They cannot come from leaves, and there is no other defect. The outgoing edge of b ends at a leaf d. The second outgoing edge of each of a,c ends at another leaf a',c'. The five nondefect vertices are distinct because sources have no incoming selected edge and leaves have exactly one. All remaining sources have two distinct leaf neighbors and form ordinary P3 components. Thus the complete support is a forest consisting of that tree and P3s.

For any connected selected component with s sources, l leaves and h defects, integer degree counting gives l=2s-h, so it has 3s vertices and 2s+h selected edges. Its cycle rank is h-s+1. The preceding direct role argument excludes the formally conceivable cyclic alternatives when h=1.

## 2. Complete local transition table

Fix an orientation of a simple cycle and add its unit circulation. At a cycle vertex, call its first incidence the arriving cycle edge and its second the departing cycle edge. A forward selected edge is traversed in its selected direction; a reverse selected edge is traversed against it; a zero edge was unselected.

The following table follows by adding 1 to the reference-direction edge value. Every possible local case is included.

| Old role | Arriving and departing cycle incidences | New role |
|---|---|---|
| source | reverse selected, forward selected | leaf |
| source | reverse selected, zero | source |
| source | zero, forward selected | defect |
| leaf | forward selected, zero | source |
| leaf | zero, reverse selected | leaf |
| leaf | zero, zero | defect |
| defect | the two incoming selected edges | source |
| defect | incoming then outgoing, both forward | defect |
| defect | outgoing then incoming, both reverse | leaf |

For example, a source entered through a zero edge receives a new incoming edge; its forward selected exit reverses and becomes a second incoming edge; its other old outgoing edge remains. It has become a defect. A leaf using two zero cycle edges keeps its old incoming selected edge and acquires one incoming and one outgoing edge, again becoming a defect.

The old defect using its two incoming edges has one of them reversed and the other canceled. Its old outgoing edge remains, leaving two outgoing edges. In the two-reverse case both used edges cancel and its third incoming edge remains. In the two-forward case its outgoing neighbor and one incoming neighbor exchange their roles; the vertex remains a defect.

## 3. Exact description of neutral one-defect moves

Let r count old sources entered through a zero edge and z count old leaves using two zero cycle edges. Let eta be 1 when the old defect becomes a source or a leaf under the table, and 0 otherwise. The exact defect change is

    b_new-b_old = r+z-eta.

This also equals the weight change, by w=2n/3+b. For an initially one-defect flow, a neutral update is consequently one of just two types:

- eta=0 and r=z=0: the defect remains at its old vertex; it is either off the cycle or in the two-forward local case;
- eta=1 and r+z=1: the old defect disappears and exactly one new defect is created, at the unique exceptional source or leaf specified by the table.

A strictly decreasing update has eta=1 and r=z=0 and removes the defect altogether. Any update producing two or more new exceptional source/leaf incidences cannot be neutral when there was only one old defect.

After a neutral update the support is again automatically a six-vertex exceptional tree plus ordinary P3s, by Section 1. One need not perform an additional support-cycle cancellation before applying the twelve-pattern strict-repair interface again. This does not mean that the same six vertices form the exceptional component: neutral moves can move the defect and change its neighboring sources and leaves.

## 4. The exact change of the source-edge secondary potential

Let C be the old source set, let R be the old sources that cease to be sources, and let A be the vertices newly becoming sources. These sets are disjoint and the new source set is (C minus R) union A. The source count is n/3 for every charged flow, so |A|=|R|.

Writing e(X,Y) for edges with one endpoint in each of two disjoint sets, the exact identity is

    e(C_new)-e(C) = e(A,C minus R)+e(A)-e(R,C minus R)-e(R).

Equivalently,

    e(C_new)-e(C) = e(A,C minus R)+e(A)+e(R)-sum_(v in R) deg_C(v).

Both are direct partitions of the changed induced edges. A source has two selected edges to non-sources, so every induced source graph has maximum degree at most one. This bounds its induced edge count but does not give a universal sign for the displayed change.

In the homogeneous-layer situation of the companion family, the old source graph is a perfect matching and the new sources of the relevant alternating leaf-block cycle have no adjacency to unchanged sources. The identity then reduces to

    e(C_new)-e(C) = -|R|+e(R)+e(A) <= 0,

with strict inequality if an old source in R has its matching partner outside R. Outside that stated situation the term e(A,C minus R) must be retained. Omitting it would be an unjustified extension of the secondary-potential lemma.

## 5. What the difference between a charged flow and a factor looks like

Suppose x is a one-defect charged flow and y is a P3-factor flow, using the same orientation convention. Put z=y-x in F3. Its divergence is zero. At every vertex of its nonzero support, either exactly two edges are nonzero, one directed in and one out, or all three are nonzero, directed all in or all out. A support vertex cannot have degree one.

A connected support component containing no degree-three vertex is a directed simple cycle. If it has degree-three vertices, suppress every maximal path whose internal vertices have degree two. The resulting core is a connected loopless cubic bipartite multigraph: its two parts are the all-out and all-in branch vertices. Every suppressed directed path runs from an all-out vertex to an all-in vertex. It cannot be a loop. The two parts have equal size by counting the three incidences at each branch vertex. Parallel paths are allowed and must not be discarded.

This statement concerns the support of this exact difference, not an assumed decomposition into edge-disjoint simple-cycle updates. The smallest branch-containing core consists of two vertices joined by three parallel paths, a theta. Larger connected cubic bipartite cores are possible in the structural classification. No constant bound on their size is asserted.

At an ordinary old source, a degree-three difference occurs precisely when it becomes a leaf using its previously unselected third edge; the difference is all-in. At an ordinary old leaf, it occurs precisely when it becomes a source using its two previously unselected edges; the difference is all-out. Source-to-source and leaf-to-leaf role changes have difference degree zero or two.

At the old defect there are two degree-three possibilities: becoming a source along its two old incoming edges gives an all-in difference, while becoming a leaf receiving along its old outgoing edge gives an all-out difference. Its other factor-compatible changes have difference degree two. These assertions follow by subtracting the old outward incidence values from the new ones; for example (1,1,0) changing to (0,0,-1) gives (-1,-1,-1).

## 6. A necessary condition for repairing a strict-cycle minimum

Assume x admits no strictly decreasing simple-cycle update, but some P3-factor y exists. Decompose the support of y-x into connected components. Updates on different support components affect disjoint vertices and edges. A component not containing the old defect cannot remove it; such an update cannot have negative defect count and hence cannot have negative weight change. Since the total change is -1, the component containing the old defect has change -1 and every other component has change zero. Applying only that one component to x already gives a P3-factor.

That improving connected component cannot be a directed simple cycle, by the assumed cycle-local minimum. It therefore has a branch-containing cubic bipartite core from Section 5, with at least one all-in and one all-out branch vertex. If the old defect has difference degree two, at least one ordinary old source must become a leaf through its unused third edge and at least one ordinary old leaf must become a source using both of its old zero edges. A search that preserves these incidences can miss every repair of such a state.

If the old defect is itself a branch vertex, at least one branch of the opposite polarity is still required. This is a necessary repair-support condition, not an existence theorem for a theta update or for a bounded number of branch vertices.

## 7. The companion family has a concrete theta repair

For the twenty-four-vertex base flow in `cycle-local-minimum-family.md`, the difference between the initial flow and the factor obtained after the two displayed updates is the sum of the circulations on

    N=(4,8,6,7,9,5),
    D=(3,0,1,2,8,6,7).

They share the path 8-6-7 in the same direction. In F3 its coefficient becomes 2, so its direction reverses. The union is a theta with branch vertices 7 and 8 and path lengths two, four and five. All three difference paths are directed from 7 to 8:

    7->6->8,
    7->9->5->4->8,
    7->3->0->1->2->8.

Vertex 7 was a leaf and becomes a source using its old zero edges; vertex 8 was a source and becomes a leaf through its old zero edge. The old defect 1 lies internally on the third path and has difference degree two. The entire theta update has weight change -1, although no initial simple-cycle update has negative cost. The decomposition into a neutral six-cycle followed by a decreasing seven-cycle is the already supplied exact realization.

The same theta survives every six-vertex extension in the companion family. Thus its two branch vertices, eleven support edges and two-step update remain fixed even as the host order grows. This fact does not assert that every strict-cycle local minimum has a theta repair.

## 8. Next obligation

Neutral one-defect transitions can now be checked by the local table, the exact source-edge identity and the twelve strict-repair patterns. The remaining question is global: whether every nonfactor one-defect neutral component reaches a state with one of those strict patterns, or whether larger exchange cores and temporary increases are necessary. The homogeneous family does not decide that question. No root closure, numerical census, verifier receipt or admission is asserted here.
