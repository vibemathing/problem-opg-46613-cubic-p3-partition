# Exact P3 boundary states and a marked-forest transfer criterion

Verdict: `candidate_only`. Primary owner: `math-proof`.
Admitted target: `obligation:opg46613-divisible-two-factor`.
The root `obligation:opg46613-root` remains open in repository truth.
This is a repair/consequence analysis, not another attempt to prove the unchanged divisible-cycle strengthening. No novelty claim or verifier receipt is asserted.

## 1. The fixed nine-vertex brick

Let R be the Petersen graph with vertex a0 removed. Label the remaining vertices a1,a2,a3,a4,b0,b1,b2,b3,b4 by 0,1,2,3,4,5,6,7,8, respectively. Its internal edge set is

```
01 05 12 16 23 27 38 46 47 57 58 68
```

Its three terminals are 0,3,4; each has exactly one external edge when used as a replacement brick. The other six vertices have no external edges. These definitions agree with C01's brick labeling.

A local boundary signature uses one of three states at each terminal:

- U: the boundary edge is unused.
- A: the terminal is an isolated vertex of the restriction of a global P3-factor to the brick. It must be attached along its boundary edge to a center outside the brick.
- B: the terminal is the center of an internal two-vertex edge segment. Its one boundary edge attaches an outside endpoint to complete that P3.

U means that the boundary edge is unused, not an additional requirement on the component containing that terminal. Local realizations must be vertex-disjoint and cover every brick vertex by internal P3 paths, A singletons, and B edge segments.

Every restriction of a global P3-factor has this form. A vertex with a used boundary edge is a terminal. Such a terminal has only one boundary edge, so it cannot be a center with two outside neighbors. A crossing path therefore leaves either an A singleton or a B internal edge segment. Paths with two separated terminals inside the brick and a center outside contribute two A singletons. Entirely internal paths contribute three vertices. These possibilities exhaust paths of length two.

## 2. Exact signature classification

If a and b count A and B states, respectively, disjoint vertex counting gives a+2b congruent to 0 modulo 3, with a+b at most 3. The only possibilities are

```
(a,b) = (0,0), (1,1), (3,0), (0,3).
```

Thus the only possible signatures are UUU, the six permutations of UAB, AAA, and BBB. All nine possibilities are realized:

| Signature | A singletons | B pairs, terminal first | Internal P3 paths |
|---|---|---|---|
| UUU | none | none | (0,1,2), (4,7,5), (3,8,6) |
| AAA | 0,3,4 | none | (1,2,7), (5,8,6) |
| BBB | none | (0,5), (3,8), (4,7) | (2,1,6) |
| A at 0, B at 3, U at 4 | 0 | (3,8) | (1,6,4), (2,7,5) |

Every listed pair or consecutive pair in a triple is an edge in the displayed edge set. Each row partitions the nine vertices. The six ordered UAB choices follow from explicit automorphisms, not an unsupported appeal to symmetry.

Identify the ten Petersen vertices

```
a0 a1 a2 a3 a4 b0 b1 b2 b3 b4
12 34 15 24 35 45 25 23 13 14
```

with the ten two-element subsets of {1,2,3,4,5}. Adjacency in the displayed Petersen graph is exactly disjointness: its listed edges satisfy disjointness, and each two-subset has exactly three disjoint two-subsets, accounting for every edge. Permuting 3,4,5 while fixing 1,2 preserves disjointness, fixes a0, and induces all permutations of the terminal subsets 34,35,45. Applying these six permutations to the fourth row gives every UAB placement. This proves sufficiency as well as necessity of the nine-state classification.

## 3. Frame replacement and the exact criterion

Let Q be a finite simple cubic graph. Choose S contained in V(Q), and put U=V(Q) minus S. Replace each vertex in S by a disjoint copy of R, attaching its three incident frame edges bijectively to the three terminals. Retain vertices in U as single vertices. Call the resulting graph X(Q,S).

The order is 9|S|+|U|. Therefore divisibility of the expanded order by three is exactly divisibility of |U| by three. If Q is 3-connected, successive vertex 3-sums with Petersen graphs preserve simplicity, cubicity and 3-connectivity, by the deletion argument already supplied in C01. The criterion below itself does not require 3-connectivity.

**Candidate transfer theorem.** X(Q,S) has a P3-factor if and only if Q has a spanning forest F satisfying both:

1. Each component T of F has |U intersect V(T)| divisible by three.
2. Every vertex u in U has degree at most two in F.

A spanning forest here contains every frame vertex; isolated vertices of S are permitted. An isolated vertex of U is excluded by condition 1. There is no requirement that each component have exactly three retained vertices.

### 3.1 From a P3-factor to a signed frame flow

Orient every selected edge of a P3-factor from its center to its endpoint. For each frame edge uv set x_uv to 1 if its expanded edge is selected in the direction u to v, to -1 if selected in the opposite direction, and to 0 if unselected; arithmetic is in F3, and x_vu=-x_uv.

At a replacement brick, outgoing edges correspond to B states and entering edges to A states. The exact local classification gives divergence sum_v x_uv = b-a = 0 in F3. At a retained vertex there is either one entering edge, with divergence -1, or two outgoing edges, with divergence 2=-1. Its support degree is at most two.

Thus the frame flow has divergence 0 on S and -1 on U, and support degree at most two on U.

### 3.2 Removing support cycles

If the nonzero support contains a cycle, orient that cycle arbitrarily and let c be its unit circulation. Choose a nonzero scalar lambda in F3 that cancels one selected edge value, and replace x by x+lambda*c. Divergences do not change. Every edge of this cycle was already nonzero, so no formerly absent support edge is introduced. At least one edge disappears. In particular, support degrees at retained vertices cannot increase.

Repeat at most |E(Q)| times. The resulting nonzero support is a forest. Add isolated frame vertices to make it spanning. Summing divergence over one component cancels its internal edge contributions, giving -|U intersect V(T)|=0 in F3. The two required forest conditions follow. This cancellation is a finite algebraic construction, not a claim about a program having run.

### 3.3 Constructing a flow from a forest

Conversely, root each tree T in a forest satisfying conditions 1 and 2. For an edge from a child w to its parent, let W be the subtree rooted at w and assign

```
x_(w,parent) = -|U intersect W| in F3,
x_(parent,w) = -x_(w,parent).
```

Set values on edges outside F to zero. Telescoping subtree counts gives divergence -1 at retained vertices and 0 at replacement vertices. The root equation follows from condition 1. Some tree-edge values may be zero; discard them from the support.

At a retained vertex, nonzero divergence prevents support degree zero. Degree at most two and divergence -1 allow exactly one entering edge or two outgoing edges. At a replacement vertex, degree at most three and divergence zero allow exactly no nonzero edges, one entering plus one outgoing edge, three entering edges, or three outgoing edges. These are precisely UUU, UAB, AAA, BBB.

Choose the corresponding local brick realization from Section 2, transporting the UAB witness by the explicit terminal permutation as necessary. Retained vertices use the prescribed incident edges. Each selected frame edge now joins a center-side to an endpoint-side. Each B pair is completed by its outside endpoint, each A singleton is attached to its outside center, and internal P3 paths are retained. Vertices are disjoint because the local realizations partition every brick and each retained vertex has its prescribed role.

In the resulting selected subgraph every center has degree two, every endpoint has degree one, and every selected edge joins a center to an endpoint. A component cannot contain two centers, because an endpoint has degree one. Every component is therefore exactly a P3. This completes both implications of the candidate theorem.

## 4. Positive subclasses obtained without a divisible 2-factor

**Exactly three retained vertices.** If Q is connected and |U|=3, take a minimal tree joining those three vertices and prune all unmarked leaves. Every leaf of the resulting tree belongs to U. A vertex of U cannot have tree-degree at least three: deleting it would expose at least three branches, each requiring another terminal leaf, but only two other terminals exist. Hence each retained vertex has degree at most two. This tree and the remaining isolated vertices of S form the forest required by the theorem. The construction works for any terminal attachment bijections.

**All retained vertices lie on a path.** If |U| is divisible by three and one path of Q contains all of U, that path together with the remaining isolated vertices of S is a qualifying forest. A cycle containing all retained vertices also suffices, after deleting one cycle edge.

**No retained vertices.** Use the edgeless spanning forest and the UUU realization in every brick.

These are positive P3-factor constructions. They do not assert the existence of a 2-factor with divisible cycle lengths. In particular, the three-hub C01 graph lies within the first subclass while its complementary 2-factors have the obstructing spectrum already recorded there.

## 5. A precise failed strengthening of the repair criterion

The forest condition cannot be silently strengthened by splitting every valid support tree into vertex-disjoint three-terminal Steiner trees. Consider the tree consisting of an unmarked central vertex, three unmarked neighbors, and two marked leaves adjacent to each of those neighbors. It contains six marked vertices, all of degree one. It satisfies the stated marked-count and degree conditions. A nonzero flow is obtained by orienting each branch vertex toward the central vertex and toward its two marked leaves.

Every connected subtree containing three marked leaves must meet at least two branches and hence contain the central vertex. Two disjoint three-terminal Steiner trees cannot both do this. Thus the proposed splitting rule fails on this exact ten-vertex support tree. This tree is not cubic; its role is solely to invalidate the auxiliary forest-decomposition assertion, not to give a counterexample to the ProblemContract.

## 6. Verification scope and next question

The nine local certificates, their automorphisms, cycle cancellation, subtree flow and gluing argument are finite, explicit proof material. They still require the target's external checks and statement-faithfulness review. No root closure, canonical failed-route record, or Result is created by this artifact.

The global forest-existence problem for arbitrary marked subsets of 3-connected cubic frames remains unresolved in this candidate. When S is empty it includes the original P3-factor problem, so the transfer theorem must not be presented as a solution of that problem. Its useful content is the exact behavior of the replacement gadget, the weaker gluing condition, and the unconditional positive subclasses above.
