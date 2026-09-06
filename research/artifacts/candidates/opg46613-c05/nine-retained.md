# C05: a common-cycle construction and nine retained vertices

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor` (repair analysis).
The original `obligation:opg46613-root` remains open.

## 1. Exact claim and source dependency

Let Q be a finite simple cubic graph, U a subset of its vertices, and X the graph
obtained by retaining U as single vertices and replacing every vertex outside U
by the nine-vertex Petersen-minus-vertex brick R. Each of the three incident frame
edges is attached bijectively to its brick's three terminals; the bijections may
be chosen separately at every brick. The order of X is |U|+9|V(Q) minus U|.

**Common-cycle lemma.** If 3 divides |U| and a simple cycle of Q contains all of U,
then X has a P3-factor. This includes any number of retained vertices and does
not require Q to be 3-connected. The cycle need not be Hamiltonian or induced.

**Nine-retained corollary.** If Q is 3-connected and |U|=9, then X has a P3-factor.
The additional input is the Holton--McKay--Plummer--Thomassen theorem: any nine
specified vertices of a 3-connected cubic graph belong to a common cycle.
The publisher's precise abstract and bibliographic identity were checked; its
full proof has not been audited here. See the accompanying source note. The
common-cycle lemma is proved in full below, rather than importing an unstated
P3 conclusion from that source.

This improves the preceding repair search: the nine-retained quotient cases do
not require brute-force enumeration to obtain a positive candidate conclusion.
Together with C04's zero-, three- and six-retained constructions, an obstruction
within this family and in the divisible-order domain must retain at least twelve
vertices. That restriction does not concern arbitrary cubic graphs outside the
specified replacement description, and does not assert a common cycle for twelve
retained vertices.

## 2. The only local brick certificates needed

Use vertices 0,...,8, terminals 0,3,4 and edges

```
01 05 12 16 23 27 38 46 47 57 58 68
```

An unused boundary is denoted U. A terminal in state A is a singleton needing
one incoming selected boundary edge from an outside center. A terminal in state
B is the center of an internal pair needing one outgoing boundary edge to an
outside endpoint. We need only these realizations:

- UUU: internal P3 paths (0,1,2), (4,7,5), (3,8,6).
- A at 0, B at 3, U at 4: singleton 0, internal pair (3,8) centered at 3,
  and internal P3 paths (1,6,4), (2,7,5).

Each row covers all nine distinct vertices. Every stated path or pair uses only
listed edges. The second row transports to all six ordered choices of A and B.
For an explicit justification, identify vertices 0,...,8 with the two-subsets
34,15,24,35,45,25,23,13,14, respectively, and the deleted Petersen vertex with 12.
Adjacency is disjointness. Permuting 3,4,5 while fixing 1,2 preserves adjacency
and realizes every permutation of the three terminal subsets 34,35,45. Thus all
six UAB signatures are available. No claim about the completeness of the full
P3 interface is needed for this sufficient construction.

## 3. Assign a flow along the supplied cycle

Write the cycle in cyclic order v_0,...,v_(l-1), with reference edge e_i directed
from v_i to v_(i+1), indices modulo l. Put m_i=1 for v_i in U and m_i=0 otherwise.
Over the field F3 assign

```
x_i = -sum_(j=0)^i m_j,       x_(l-1)=0.
```

The second equality is consistent with the first because sum m_j=|U| is divisible
by three. In particular x_i-x_(i-1)=-m_i, using x_(-1)=x_(l-1)=0. Edges outside
the cycle receive value zero. Value 1 selects a reference-direction arc, value 2
selects its reverse, and value 0 leaves the edge unused.

At a brick vertex on the cycle, consecutive values agree. They are either both
zero, giving no selected boundary, or both nonzero, giving exactly one incoming
boundary A and one outgoing boundary B. Its third boundary is unused. A brick
outside the cycle has no selected boundary at all. Fill each brick using the
appropriate certificate from Section 2, allowing its actual terminal attachment
bijection.

At a retained vertex the possible ordered pairs (x_(i-1),x_i) are exactly

```
(0,2), (1,0), (2,1).
```

The first two yield one incoming selected edge and no outgoing edge, so the
retained vertex is an endpoint. The third yields two outgoing selected edges
and no incoming edge, so it is a center. Since all retained vertices lie on the
cycle, no retained vertex is left unaccounted for.

## 4. Check that gluing gives P3, not just the right degrees

Orient each internal P3 from its center toward its endpoints. Orient the internal
B pair from its terminal center to its internal endpoint. Every selected boundary
arc runs from a center side to an endpoint side by the definitions of A and B
and the retained-vertex cases above.

After gluing, each center has exactly two selected outgoing edges and each
endpoint has exactly one selected incoming edge. Every selected edge joins a
center and an endpoint. Thus an endpoint cannot connect two centers, and a
selected component consists of one center and its two distinct endpoints. Every
component is exactly P3. The local certificates cover all vertices of all bricks,
and every retained vertex has its prescribed role, so the selected subgraph is
spanning. Extra edges in X are simply unselected; no induced-path assumption is
used. This proves the common-cycle lemma for every supplied cycle and every
independent choice of port bijections.

Applying the published nine-point theorem to Q and the nine distinct vertices
of U now gives the nine-retained corollary. Its hypotheses are exactly simplicity,
cubicity and 3-vertex-connectivity of the frame. The theorem is not being applied
to the expanded graph, nor to a multigraph quotient.

## 5. Relation to the frozen question

The P3 implication from a divisible 2-factor is a different sufficient argument:
on every cycle of length 3r select consecutive triples (v_(3j),v_(3j+1),v_(3j+2))
and their two cycle edges for j=0,...,r-1. These triples partition each cycle;
the cycles partition all vertices. Extra closing edges, including the third
edge of a triangle, are not selected. The matching itself contributes no selected
edge. This construction needs no connectivity or cubicity once the stated
2-factor is supplied.

C01--C04 already give explicit obstructions to the universal availability of
that 2-factor. The present common-cycle construction works on the smaller frame
and tiles the replacement bricks without requiring a divisible complementary
2-factor of X. It is therefore a repair, not a repetition of the obstructed
strengthening. The original P3-factor claim has not been contradicted.

For a 3-connected cubic frame, the standard vertex 3-sum with the Petersen graph
preserves the simple cubic 3-connected domain, as checked by the explicit
vertex-deletion argument in C01. Our P3 construction does not depend on that
preservation lemma; it is relevant only when placing the resulting family in
the original domain. No root or new canonical record is admitted here.

## 6. Falsification attempts and reproducibility

`cycle_glue.py` constructs the actual expanded graph and selected edges, then
checks that every selected component has three vertices and degree sequence
(1,1,2). It also checks that every selected edge belongs to the expanded graph
and that the latter is cubic. Its six explicit terminal automorphisms are checked
against the full brick edge set.

The bounded local run tested 10890 cases: all eligible retained subsets on the
specified Hamiltonian cubic frames of orders 6,8,10,12, each with six deterministic
heterogeneous port assignments, and six assignments for the explicit nine-cycle
of the Petersen frame. All seven local signatures occurred. Invalid retained
counts, retained vertices off the supplied cycle, repeated cycle vertices and a
cycle containing a nonedge were rejected. Exact counts, a sample factor, stream
digest and Python version are in `cycle-glue-output.json`; limits and observed
exit status are in `execution-observation.json`.

Reproduce from this candidate directory with `python3 -S cycle_glue.py`, one
process, CPU limit 35 seconds, wall limit 40 seconds, memory 256 MiB, and output
file limit 1 MiB. The script has its own 30-second audit deadline. These tests do
not certify universal cyclability, all global port assignments, or all cubic
frames. Arbitrary port assignments are covered by the local proof, not by an
exhaustive claim about the tests. The source theorem and semantic linkage still
require the target's prescribed verification. Both admitted obligations stay open.
