# ROOT-R03: residue-preserving compression of adjacent full-signature bricks

Verdict: `candidate_only`. Primary owner: `math-proof`.
Problem: `problem:opg-46613-cubic-p3-partition`.
Target: `obligation:opg46613-root`.
This is a partial root-oriented proof candidate. It uses neither the false
universal divisible-two-factor assertion nor an unrecorded stronger induction
hypothesis. The protected legacy DAG is unchanged; its obsolete dependency
still needs trusted repair before any eventual root admission.

## 1. Definitions and dependencies

Use the exact incidence signatures of ROOT-R01 and the selected, not necessarily
induced, P3 convention. A three-port brick has three distinct terminal vertices
of internal degree two; all other vertices have internal degree three. Its cap
adds one vertex adjacent to the terminals. All caps considered below are finite,
simple, cubic, and 3-connected.

The port states are U (unused), A (an endpoint supplied by an outside center),
and B (a center supplied with an outside endpoint). Give them charges 0,1,2 in
F3 respectively. Joined incidences must have opposite charges. This is precisely
U-U, A-B, B-A, not an additional relaxation. For a fragment Z, every realizable
word satisfies sum of charges = |V(Z)| mod 3. The converse need not hold.

Call a three-port brick full if its actual signature set contains all nine
words satisfying this conservation equation. The word 'full' is a hypothesis
about witnessed P3 realizations, not about 2-factors, connectivity alone, or
arithmetic alone. ROOT-R01 supplies both the exact gluing theorem and the
signature-inclusion replacement lemma. Its addendum explicitly certifies that
the five-vertex prism-minus-vertex brick is full of residue two.

## 2. Composition lemma (claim root-r03-full-composition)

Take a connected finite network of full three-port bricks, and pair some ports
according to its internal edges. Assume the resulting graph is simple. Ports
not paired remain external. Write r_v for the order of brick v modulo three.
Then the composite fragment realizes exactly the external words whose total
charge equals sum_v r_v.

Proof. Necessity follows by adding the local conservation equations, because
the two charges on an internal edge cancel. For sufficiency, fix such an
external word and a spanning tree of the network. Give every non-tree internal
edge charge zero at both ends. Process a leaf of the remaining tree. All of its
incidences except the one toward its parent are assigned, so assign that last
charge to make its sum r_v, and assign the opposite charge at the parent.
Remove the leaf and repeat. At the last vertex the equation is satisfied by
the assumed total balance. This assigns one of the nine actual signatures at
every brick. Choose a witnessing realization for each and glue them by ROOT-R01.
The selected graph is a disjoint union of P3s, with exactly the prescribed
external signature. No claim about replacing arbitrary bricks by full ones is
used. For a one-brick network the statement is its defining hypothesis.

In particular, a closed connected network entirely made from full bricks has a
P3-factor exactly when its total order is divisible by three. This is only a
restricted class of root instances; ordinary vertices and triangles are not
full three-port bricks.

## 3. The four-port interface of a pair (root-r03-pair-interface)

Let X,Y be full residue-two bricks joined by exactly one port edge. Index their
remaining ports x1,x2,y1,y2. The union has order one modulo three and realizes
all 27 four-letter words of total charge one.

For an explicit compatibility rule put sx=q(x1)+q(x2), sy=q(y1)+q(y2). The
internal X charge is 2-sx and the internal Y charge is 2-sy. They are opposite
exactly when sx+sy=1. Thus no feasibility search over the internal edge remains:
its state is uniquely determined. The following table gives that unique state
on the X side, using ordered external pairs:

| External pair at X | Internal X state |
|---|---|
| UU, AB, BA | B |
| UA, AU, BB | A |
| UB, BU, AA | U |

The Y side obeys the same table. Exactly 27 external words survive the total
balance condition, and each is realized because both local bricks are full.
This is a complete four-port existence signature, not a claim of equal numbers
of realizations for different words.

## 4. A connectivity-preserving four-cycle replacement (root-r03-compress)

Let G be a finite simple cubic 3-connected graph in the root domain. Suppose
it contains disjoint induced vertex sets X,Y as above, their boundaries each
being three-edge cuts, and exactly one edge runs between X and Y. Suppose both
are full and their orders are two modulo three.

Contract X to u and Y to v, keeping their incident edges. The resulting frame
H is simple cubic and 3-connected. Indeed, a nontrivial three-edge cut of G is
a matching and its capped opposite side is simple cubic 3-connected, by
ROOT-R01. Contracting X produces precisely that capped opposite side. The
three Y attachments are still at distinct vertices: only one ends at the new
u, and its other two endpoints were distinct outside X union Y. Applying the
same capped-side argument to Y proves the assertion. In particular H has at
least four vertices.

Write N_H(u)={v,a,b} and N_H(v)={u,c,d}, with a!=b and c!=d; overlap between
{a,b} and {c,d} is allowed. Subdivide the distinct edges ua and vc by new
vertices p and q, and add pq. Keep uv, ub and vd. The four internal vertices
u,v,q,p now induce a C4, with external edges ub,vd,qc,pa. Let K be this graph.

Here is a direct proof that this operation preserves 3-connectivity. Let e=ua
and f=vc, and delete a set W of at most two vertices from K.

* If neither p nor q is deleted, H minus the deleted old vertices is connected.
  Its surviving edges are merely subdivided. A subdivision vertex with at least
  one surviving endpoint attaches to this connected part. If both endpoints of
  one subdivided edge were deleted, the other subdivision vertex still has a
  surviving endpoint (two distinct simple edges cannot both have precisely the
  same two endpoints), and pq attaches the exceptional vertex as well.
* If p is deleted and at most one old vertex w is deleted, the surviving old
  vertices are connected in H-w-e. The graph H-w is 2-connected, hence deleting
  one of its edges cannot disconnect it. An edge already incident to w needs
  no further deletion. The remaining q has a surviving endpoint of f. The case
  with q deleted is symmetric; with no old deletion use H-e connected.
* If both p and q are deleted, the remaining graph is H-{e,f}, which is
  connected because a cubic 3-connected simple graph has no edge cut of size
  at most two, as proved in ROOT-R01.

Thus K-W is connected. The construction is simple and cubic because e and f
are distinct, p,q are new, and pq did not exist. This proves the required
connectivity without assuming an unverified program run or an external
construction theorem.

The four-cycle fragment has order four, so each of its actual signatures has
charge one. Section 3 shows that every such signature can be realized by
X union Y, with the indicated correspondence of its four ports. Consequently

    if K has a P3-factor, then G has a P3-factor.

The rest of the chosen K factor is unchanged; replace just its C4 realization
by a compatible realization of X union Y. Roles at outside vertices agree,
even when some of a,b,c,d coincide.

Both |X| and |Y| are odd: 3|X|=2|E(X)|+3, and similarly for Y. Thus each is
five modulo six and at least five. It follows that

    |V(K)| = |V(G)| - |X| - |Y| + 4 < |V(G)|,
    |V(K)| = |V(G)| mod 6.

A smallest-order root counterexample therefore cannot contain this configuration.
For two five-vertex bricks the reduction is exactly six vertices. This excludes
a concrete family of pairs of three-cuts, not all nontrivial three-cuts and not
all triangles or squares.

## 5. Explicit control: three triangle contractions do not preserve a chosen factor

It is tempting to contract three triangles at once because this reduces the
order by six. That arithmetic does not supply a boundary-preserving lifting
lemma for a chosen factor of the smaller graph.

Let H=K3,3 with parts {a,b,c} and {x,y,z}. A specified factor is

    (x,a,y), (b,z,c),

with the center in the middle of each triple. Expand a,b,c to disjoint triangles
(a_x,a_y,a_z), (b_x,b_y,b_z), (c_x,c_y,c_z), attaching u_t to t for
u in {a,b,c}, t in {x,y,z}. Call the resulting twelve-vertex graph G_T.
Each expansion is a vertex 3-sum with K4, so G_T is simple cubic 3-connected
by ROOT-R01. Both H and G_T lie in the root's order class.

Define boundary-preserving lift to mean that the selected/unselected status
and center/endpoint role at each unexpanded vertex are retained, under the
natural correspondence of external edges. In the displayed factor, the word
at a is BBU (ports x,y,z); the words at b and c are UUA. These are also the
words forced at the respective expanded triangles by outside compatibility.
Each has charge one, whereas every triangle word has charge zero. Hence this
specified factor has no boundary-preserving lift through the three expansions.

This is NOT a root counterexample or a proof that triangle contractions cannot
be used with more global changes. G_T has the explicit factor

    (a_x,x,b_x), (y,a_y,a_z), (z,b_z,b_y), (c_x,c_y,c_z).

All twelve vertices occur once. The four paths use only triangle edges or the
listed external edges. The last selected path is allowed even though its two
endpoints are adjacent in the ambient triangle. The successful factor changes
the roles and selected incidence pattern at the unexpanded vertices.

## 6. Sources, scope, and verification requests

The companion source note distinguishes this conditional compression from
Kelmans' universal equivalences and graph-composition theorems. The new proofs
are the finite F3 leaf elimination, explicit C4 replacement, and explicit
boundary-preserving-lift control. No novelty is asserted.

Requested review: check every local signature dependency against ROOT-R01,
check repeated outside endpoints in Section 4, verify the two-deletion argument,
and verify both explicit factors in Section 5. The companion JSON contains
all edges and selected triples of that control. No cubic census is claimed in
this packet. Earlier partial order-18 data is not silently completed or reused.
The previously blocked executable upload is not retried or repackaged.

Next: classify minimal Hall-defective supports of a proposed center set, seek
valid center exchanges, and obtain further signature inclusions for fragments
not covered by this full-signature hypothesis. Root remains open.
