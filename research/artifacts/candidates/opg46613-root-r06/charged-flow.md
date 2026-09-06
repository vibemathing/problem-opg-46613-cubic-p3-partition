# ROOT-R06: constant-charge ternary flows and exact P3 defect

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root` under the existing admitted Attempt/Route/Graph.
This supplies an exact reformulation and local restrictions. It does not prove
that its global optimum always attains the required value in the root domain.

## 1. Frozen optimization problem

Let G be a finite connected simple graph of maximum degree at most three and
order n divisible by three. Fix an arbitrary reference direction for every edge.
For each edge uv assign x_uv in F3, with x_vu=-x_uv. Require at every vertex u

    sum over neighbors v of x_uv = -1 in F3.                    (1)

Let A(G) be the finite set of such assignments. Its weight w(x) is the number
of edges with nonzero value. A value +1 is read as an arc in that direction;
-1 means the reverse arc; zero means an unselected edge. These are prescribed
nonzero vertex charges, NOT the zero-boundary equations for an ordinary flow.
Zeros on edges are allowed. No nowhere-zero-flow theorem is being imported.

The root asks about simple 3-connected cubic graphs, a subclass of the domain
above. P3 means a selected two-edge path on three distinct vertices, not induced.

## 2. The affine space always exists and has an exact finite parametrization

Choose a rooted spanning tree T. Assign values arbitrarily to edges outside T.
Start with demand -1 at each vertex and subtract the divergence supplied by
these chord values. Process nonroot vertices from leaves toward the root. At
vertex v set its remaining edge value toward its parent equal to its current
demand, then add that value to the parent's demand. This makes equation (1)
hold at v. The remaining root equation holds because total demand was -n=0
and every edge contribution cancels between its endpoints.

The choices on chords determine the tree values uniquely: at each processed
vertex only the parent edge is undetermined. Conversely every solution follows
this procedure for its own chord values. Therefore

    |A(G)| = 3^(|E(G)|-|V(G)|+1).                              (2)

For cubic G the exponent is n/2+1. Equation (2) is an enumeration count, not a
claim of polynomial-time minimization. Existence of a charged assignment is
strictly different from existence of a P3-factor.

## 3. An exact identity for every assignment

At a vertex of support degree at most three, equation (1) permits precisely:

| Type | Selected directions | Integer divergence |
|---|---|---:|
| L | one incoming | -1 |
| C | two outgoing | 2 |
| B | two incoming and one outgoing | -1 |

Support degree zero is excluded by (1). To check exhaustiveness, write incoming
incidences as -1 and outgoing incidences as +1. Among one, two or three such
values, the sums congruent to -1 modulo three are respectively -1, 2 and -1.
Thus there are no other local cases.

Write l,c,b for the numbers of these types. Summing integer divergences over
all vertices cancels all arcs, giving 2c-l-b=0. Together with n=c+l+b this gives
c=n/3. Counting all outgoing arcs gives the stronger identity

    w(x) = 2n/3 + b(x).                                       (3)

This holds without assuming that the support is acyclic or that G is cubic.
In particular every assignment has weight at least 2n/3.

Equality holds precisely when b=0. In that case each selected arc goes from
a type C vertex to a type L vertex: C has no incoming arc, and L has no outgoing
arc. Every C has two distinct L neighbors and each L has one selected neighbor.
Hence every component is exactly a P3. Conversely orienting a P3-factor from
its centers to endpoints gives a unique assignment satisfying (1), with b=0.
Thus there is a bijection

    P3-factors of G <-> assignments in A(G) of weight 2n/3.    (4)

Define beta(G)=min_x b(x). The root is exactly the assertion beta(G)=0 on its
frozen domain. This is not the stronger divisible-complementary-factor claim.
The minimum is attained because A(G) is nonempty and finite.

## 4. Every minimum has forest support

Suppose a simple cycle lies entirely in the nonzero support of x. Orient this
cycle and add a nonzero scalar multiple of its unit circulation, choosing the
scalar to cancel one edge. Divergences do not change. Every cycle edge was
already nonzero, so no formerly zero edge becomes nonzero. At least one edge
disappears, decreasing weight. Therefore a minimum cannot contain such a cycle.

More generally this applies to every assignment with no weight-decreasing
single-cycle update. After adding isolated graph vertices the support would be
a spanning forest, but there are in fact no isolated vertices by (1). Summing
charges over a component shows that each tree has order divisible by three.
For an edge directed from a subtree W toward the rest of its tree, summing (1)
over W gives its value -|W|. Every support edge is nonzero, so no tree edge can
split off a number of vertices divisible by three.

A forest with q components has w=n-q. Combining this with (3) yields

    b = n/3-q.                                               (5)

On one tree of order 3r the type counts are c=r, b=r-1 and l=r+1: use (3) and
w=3r-1 within that tree. Thus beta measures exactly the loss of tree components
from the desired n/3 components. Equation (5) does not imply that every tree
can be split into P3s.

If b=1 for such a forest, precisely one component has order six and all others
are P3s. The six-vertex tree has one degree-three vertex, two degree-two vertices
and three leaves. It is a subdivided three-arm star, with arm lengths either
(1,1,3) or (1,2,2). An arm of length three would give a tree edge splitting off
three vertices, which is impossible for nonzero support. Therefore its shape
is exactly (1,2,2). Label it with edges aa',ab,bc,cc',bd. Its forced directions
are a toward a' and b, c toward c' and b, and b toward d. This is the first
possible positive-defect component, not a proof that it can always be repaired.

## 5. Exact cost of a single simple-cycle update

For an oriented simple cycle K, count k zero-valued edges, p nonzero values
aligned with its unit circulation, and q nonzero values opposed to it. Adding
that circulation changes weight by k-q; subtracting it changes weight by k-p.
Indeed every zero becomes nonzero, every opposing value cancels in the first
update, every aligned value stays nonzero with its sign reversed, and the roles
are reversed in the second update. Therefore absence of a strictly improving
single-cycle update is equivalent to

    p <= k and q <= k for every oriented simple cycle K.      (6)

In particular p+q<=2k. Conversely the latter inequality alone is insufficient,
since the signs still matter. Here 'single-cycle' means a genuine simple cycle;
a traversal of an edge and its reverse is not an allowed cycle update.

A global minimum satisfies (6). The converse, that every assignment satisfying
(6) is globally minimum, is NOT proved or assumed. Nor is it assumed that every
cycle-local minimum in a root graph has b=0. The finite tests below cannot close
this additional descent obligation.

## 6. Metric restrictions on a cycle-local minimum

Let F be the forest support of an assignment satisfying (6). Suppose an unused
edge joins two vertices of the same F tree at distance d. This edge and their
unique tree path form a simple cycle with k=1 and p+q=d. Thus d<=2. Simplicity
excludes d=1 because the tree edge is already present, so d=2 and the edge closes
a triangle. Its two tree incidences must have opposite signs when read along
the cycle, since p,q<=1. In particular, when G is triangle-free every F tree
is an induced tree of G.

Now consider two distinct unused edges joining the same two different F trees,
with ends a,a' in the first and b,b' in the second. The two edges and the unique
paths between a,a' and b,b' form a simple cycle. One path may have length zero
when the corresponding ends coincide. Both cannot have length zero, as G is
simple and the two edges are distinct. Here k=2, so

    dist_F(a,a') + dist_F(b,b') <= 4.                        (7)

The sharper signed bounds are still p,q<=2. In a triangle-free cubic graph,
an induced tree component on t vertices has exactly 3t-2(t-1)=t+2 boundary edges.
Together these facts sharply restrict how a six-vertex defect tree or a larger
defect tree can attach to its neighboring P3 components. They are necessary
conditions, not an exclusion of every possible attachment pattern.

## 7. Exact finite enumeration on two positive controls

The controls are G_2 and G_3 from ROOT-R05. In general G_m has z_0,...,z_(4m-1)
on a cycle, c_i adjacent to z_i,z_(i+2m) for 0<=i<2m, and c_i adjacent to c_(i+m)
for 0<=i<m. Label z_i by i and c_i by 4m+i. The preceding candidate supplies
complete simplicity, cubicity, three-connectivity and positive-factor proofs.

For G_2 and G_3 the complete affine enumerations have respectively 2187 and
59049 solutions, from (2). The observed minimum weights are 8 and 12, attained
65 and 297 times. Every solution's divergence, local type and identity (3) were
checked. Every minimum was decoded into actual disjoint P3 components; their
counts agree with the earlier direct centered-exact-cover counts on these same
graphs. Both signs of every simple-cycle update were checked against the cost
formula on the first sixteen lexicographic flows: 3488 and 25056 updates.

There are 109 and 783 simple cycles in these two labeled graphs. Among every
nonoptimal forest-supported assignment, at least one of the tested simple-cycle
updates decreases weight. This is an exhaustive statement about these two fixed
affine spaces, not about all graphs of orders twelve and eighteen.

A further deterministic descent test used 200 starts for each ordered pair of
T,D,J,R cells with identity port gluing (16 graphs), and 200 starts on the
30-vertex three-Petersen-cell/three-hub graph. All 3400 descents reached weight
2n/3. These are samples of starts, not complete affine enumerations. They do
not justify replacing global minimization by greedy cycle descent in general.

## 8. Reproduction and execution boundary

Use sorted undirected edges with reference direction from lower to higher label.
Build a breadth-first spanning tree from vertex zero, scanning neighbors in
increasing order. List chords in edge order and enumerate their value tuples
lexicographically in {0,1,2}. Extend them using Section 2. The flow-stream hashes
in the companion JSON are SHA-256 of the concatenation of the edge-value bytes,
with no separators, in this exact enumeration order.

To enumerate cycles, choose their least vertex s, extend a simple path using
only vertices greater than s, and close it back to s. Retain the orientation
whose second vertex is less than its last vertex. This lists each simple cycle
once. For each nonoptimal forest, compare both updates on every such cycle.
A disjoint-set component test detects a support cycle without assuming any P3
conclusion. At weight 2n/3, explicitly check component sizes and degrees (1,1,2).

For the descent samples the cells and their ordered ports are exactly those in
C07's audit note. Offset the right cell labels by the order of the left cell and
join corresponding ports. In ordered cell order T,D,J,R, seed Python's Random
with 70200+i for ordered pair number i starting at zero. Choose 200 chord tuples
with randrange(3). After each step rescan cycles in the fixed enumeration order,
take the first strictly decreasing update, preferring addition over subtraction
when both improve, and stop only when none does. Every step decreases an integer
weight, so at most |E(G)| steps occur. The 30-vertex input uses three copies of R
on labels 0..8,9..17,18..26, with respective ports attached to hubs 27,28,29; its
seed is 4661330. It has 18273 enumerated simple cycles in the recorded run.

All reported runs were actual local generator-side Python 3.13.5 calculations,
one process per bounded run, CPU limit 35 seconds, outer wall 40 seconds, memory
512 MiB and output 2048 KiB. Internal deadlines were 30 seconds for the full
probe/replay and 28 seconds for descent. Each reported run exited zero. The
companion JSON freezes code/dependency/output hashes, finite counts and exact
scope. The executable sources remain local-only; no previously blocked upload
is repackaged, and no remote execution or registered verifier receipt is claimed.
The complete algorithm is specified above for permitted reproduction.

## 9. Precise remaining root obligation

For every simple 3-connected cubic G of eligible order, prove beta(G)=0, or
produce an original-domain graph and complete certificate with beta(G)>0.
The current candidates establish the exact translation, not this conclusion.
The next bounded question is whether a positive-defect cycle-local forest can
satisfy the root's connectivity constraints, especially with its unique (1,2,2)
six-vertex component when b=1. Zero-cost sequences and simultaneous multicycle
updates must be distinguished from strictly improving single-cycle moves.

All statements here are candidate proofs or explicitly bounded observations.
The obsolete divisible-two-factor DAG dependency remains unchanged and is not
used as a premise. No new canonical record, EvidenceLink, Result or root closure
is generated by this artifact.
