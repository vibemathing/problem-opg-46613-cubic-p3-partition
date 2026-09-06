# ROOT-R01: exact P3 cut interfaces and valid minimal-counterexample substitutions

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root`; existing graph/attempt identifiers are retained.
This is a partial root-oriented proof candidate, not a proof of the root statement.
The legacy graph still lists the divisible-two-factor dependency. This candidate
neither uses its false universal assertion nor changes the protected graph.
Any eventual admission must also resolve that obsolete dependency explicitly.

## 1. Frozen scope and difference from C04

Graphs are finite and simple. Cubic means degree three; connectivity is vertex
connectivity. P3 is a selected two-edge path on three distinct vertices, not an
induced-subgraph requirement. A factor covers every vertex exactly once.
The root domain has order divisible by six, since the sum of cubic degrees is even.

C04 `p3-interface.md` gives the nine states of the specific Petersen-minus-vertex
brick and a special marked-forest criterion. The present theorem handles arbitrary
subcubic fragments, repeated boundary incidences, every port count, exact counting,
and replacement in a hypothetical smallest root counterexample. It does not assume
that every residue-allowed state is feasible. Kelmans 0910.2766v2, Lemma 2.4,
already classifies crossing paths of a cubic vertex 3-sum; our three-port table is
an explicit coordinate version of that prior structure. No novelty is asserted.

## 2. General incidence states (claim root-r01-interface)

A fragment B consists of an internal simple graph and an indexed list of ports.
Each port is attached to a vertex; multiple ports may share a vertex. The sum of
internal degree and incident ports is at most three. A local realization selects
orients internal edges, labels each vertex center or endpoint, and assigns each
port one of U, A, B:

| Port state | Meaning from this fragment's side |
|---|---|
| U | The cut edge is not selected. |
| A | The vertex is an endpoint receiving its unique selected edge from outside. |
| B | The vertex is a center sending a selected edge to an outside endpoint. |

Every selected internal edge goes from a center to an endpoint. Including selected
ports, a center has indegree zero and outdegree two; an endpoint has indegree one
and outdegree zero. This defines the feasible signature set Sigma(B), and the
integer multiplicity w_B(s) counts local realizations of signature s.

For ports at distinct vertices, every realization partitions the fragment into
internal P3s, A singletons and B two-vertex segments (port vertex first, the center).
With repeated ports one must also allow a center singleton using TWO B ports.
Discarding this last tile would incorrectly exclude a P3 whose center is alone
on one side of a cut. A component with an outside center and two inside endpoints
contributes two separate A singletons. U restricts its edge, not its vertex's role.

**Exact gluing theorem.** Join all ports of fragments X and Y in a prescribed
bijection pi, obtaining a simple graph G. Write d(U)=U, d(A)=B, d(B)=A. Then

    G has a P3-factor iff some s in Sigma(X), t in Sigma(Y)
    satisfy t[pi(i)] = d(s[i]) for every i.

More precisely,

    number of P3-factors(G)
      = sum over compatible (s,t) of w_X(s) * w_Y(t).

Proof. A factor has a unique orientation from each center to its two endpoints.
Restriction gives the local roles and dual port states. Conversely choose two
compatible realizations and join the selected ports. Every selected edge joins a
center and an endpoint; every center has degree two, every endpoint degree one.
A connected component cannot contain two centers: any path between them would
have to pass through an endpoint with degree at least two. Consequently every
component is exactly one center and two distinct endpoints, a P3. The roles cover
all vertices. Restriction and gluing are mutually inverse, proving the count as
well as existence. This proof also works for multi-fragment networks by imposing
the same constraint on each paired incidence. Unpaired ports remain the external
signature; this gives an exact finite-state composition rule.

Degrees {1,2} alone are NOT an adequate replacement for the center/endpoint edge
constraint: longer paths and cycles can otherwise occur.

## 3. Residue conservation and complete compatibility tables (root-r01-residue)

Let n=|B|, c its number of centers, e its selected internal edges, a its A ports
and b its B ports. Counting outgoing and incoming selected incidences gives

    2c = e+b,  n-c = e+a,  hence n = 3c+a-b.

Thus a+2b = n modulo 3. This is a necessary condition, not a sufficient one.
The entire alphabet per edge has compatibility matrix

| X \\ Y | U | A | B |
|---|---:|---:|---:|
| U | 1 | 0 | 0 |
| A | 0 | 0 | 1 |
| B | 0 | 1 | 0 |

The r-edge matrix is the tensor product of these matrices, restricted to the
actual realizable signatures and the specified port permutation.

For two ports the residue tables are:

| n mod 3 | Possible signatures |
|---|---|
| 0 | UU, AB, BA |
| 1 | AU, UA, BB |
| 2 | BU, UB, AA |

For three ports they are:

| n mod 3 | Possible signatures (all distinct permutations indicated) |
|---|---|
| 0 | UUU; six permutations of UAB; AAA; BBB |
| 1 | three permutations of AUU; three of BBU; three of AAB |
| 2 | three permutations of BUU; three of AAU; three of ABB |

Each row contains nine words. The alphabet duality maps residue r to -r.
An arbitrary three-port fragment therefore has at most nine states, and at most
2^9 different feasible subsets for a fixed residue before quotienting port labels.
This finite bound does not prove that any specified subset is realizable or that
all fragments with the same residue are interchangeable.

## 4. Exact missing-state controls (root-r01-missing)

The triangle with one port at each vertex has all residue-zero states EXCEPT BBB.
UUU has three realizations (three choices of center); every ordered UAB word has
one realization; AAA has one. BBB would need three disjoint internal pairs and
there are only three vertices. This explicitly falsifies the auxiliary assertion
that every arithmetic-allowed state is feasible in every capped cubic brick.
It is not a counterexample to the root.

A singleton with three ports at that vertex has exactly six words: permutations
of AUU and BBU. All three permutations of AAB are infeasible because the same
vertex cannot simultaneously be an endpoint and a center. This also tests the
repeated-port case; treating ports as distinct vertices would give a wrong answer.

The supplied finite input collection gives 872 rooted vertex-deleted fragments
from capped graphs of orders 4,6,8,10,12. They have eight distinct ordered signature
sets. 72 pair/permutation tests between their signature representatives compare
complete global P3-factor counts against the product formula, with exact agreement
and counts between 15 and 364. Four invalid-certificate/compatibility controls
are rejected; a separate two-port C6 test also agrees. These are local generator
calculations, not registered verifier receipts. ROOT-R01 claims only this supplied
finite collection; the separate census candidate will audit its outer coverage.

## 5. Three-cuts in the root domain (root-r01-caps)

A 3-connected cubic graph has no one- or two-edge cut: for a cut of size at most
two with a side having vertices beyond its at most two endpoints, deleting those
endpoints disconnects the graph; a side of size one or two in a simple cubic graph
has boundary at least three or four, respectively. This exhausts the exceptions.

Let delta(S) be a nontrivial three-edge cut, with both sides having more than one
vertex. Both sides are connected, because every component has boundary at least
three. The identity 3|S|=2|E(S)|+3 makes each side odd and thus at least three.
No two cut edges share an endpoint u on a side. If they did and the third has
endpoint v different from u, deleting u and v disconnects the nonempty rest of
that side from the other side. If all three meet u, connectedness of the side
forces it to be the singleton u. Both cases contradict the hypotheses. Thus the
cut is a matching, so the simpler singleton/pair/internal-P3 tile description is
exact for every nontrivial three-cut in this root domain.

Capping either side by one new vertex joined to its three distinct ports gives a
simple cubic 3-connected graph. To see this, deleting at most two old vertices
leaves the cap connected by contracting the other side in the connected original
graph. Deleting the cap vertex and one old vertex x leaves the side minus x
connected: otherwise each of its components must have at least two edges into
the other side in G-x (which is 2-connected and hence bridgeless), requiring at
least four cut edges, whereas at most three exist. Deleting only the cap is the
already established connected-side case.

Conversely, the vertex 3-sum of two simple cubic 3-connected graphs is again
simple cubic 3-connected. If two deleted vertices lie one on each side, each
punctured side is connected and at least one of the three matching cut edges
survives. If both deletions lie on one side, every remaining component of that
side meets a surviving port, since the capped side minus the two vertices is
connected. The untouched opposite side connects these components. The cases
of zero or one deletion follow by the same argument.

## 6. A sound reduction invariant (root-r01-substitution)

Suppose G is a smallest-order root counterexample and has a matching three-cut
with fragment B on one side. Suppose a smaller replacement Q has the same
indexed boundary, |Q|=|B| modulo 3, and Sigma(Q) is a subset of Sigma(B) under the
specified port correspondence. Require also that replacing B by Q gives a simple
3-connected cubic graph H. Then such B cannot occur in G: H has smaller order
still divisible by three, so minimality gives H a P3-factor. Its Q signature is
realized by B, and the gluing theorem lifts that factor to G, a contradiction.
This uses an inclusion of actual signatures, not just equal residues.

Two useful instances follow.

1. A brick of order greater than three congruent to zero modulo three which
realizes all eight triangle states is replaceable by a triangle. The capping
argument ensures the required connectivity. In particular, a smallest root
counterexample cannot contain the Petersen-minus-vertex nine-vertex brick with
its natural three ports: C04 supplies all nine states, hence the eight triangle
states. Replacement lowers the order by six. This is a local structural exclusion,
not an assumption that G has any divisible-cycle 2-factor.
2. A brick of order greater than one congruent to one modulo three which realizes
all six singleton states is replaceable by one vertex. The resulting graph is
precisely the capped opposite side, whose connectivity was proved above.

For residue two, a five-vertex fragment obtained from either cubic graph of
order six supplies all nine words; any larger residue-two brick with all nine
is replaceable by that fragment. An eight-state brick need not contain this
signature, so this reduction must NOT be applied solely from its order.

Neither these exclusions nor minimum order alone currently imply cyclic
4-connectivity or triangle-freeness. Contracting a triangle reduces order by two
and leaves the root's residue class; it is not a valid one-step root induction.
Kelmans Theorem 3.1 gives universal equivalences, but its proofs may enlarge a
witness graph, so it does not automatically supply stronger deletion assertions
below a hypothetical minimal counterexample's order.

## 7. Replay and remaining obligations

`p3_boundary.py` is the exact tile/cover implementation. `audit_boundary.py`
uses the frozen finite inputs; `unpack_data.py` restores byte-bound copies from
`boundary-data.json` without changing existing different files. Run the unpacker,
then the auditor in this candidate directory, with one CPU thread. The audit
sets 38-second wall, 35-second CPU and 768-MiB address-space limits. Observed
Python version is 3.13.5. No remote command execution or trusted verification
is asserted. Returned counts refer to selected edge paths, so a triangle has
three internal P3 choices rather than zero or one.

Next: complete the outer cubic census directly with P3 exact covers; audit
signature-inclusion minimal replacements, and isolate the remaining smallest
missing-state bricks. Both canonical obligations remain open. The absence of a
root counterexample in finite inputs and these separator lemmas do not close root.
