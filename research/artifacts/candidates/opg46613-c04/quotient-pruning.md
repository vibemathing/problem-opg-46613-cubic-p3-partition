# Quotient filters and endpoint-allocation certificates

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This refines `quotient-reduction.md`. The conclusions are mathematical reductions and sufficient conditions, not reports of a completed outer enumeration.

## 1. Retained-vertex deletion constraints

Use the quotient K formed by contracting each connected component of the unmarked induced subgraph Q[S] to a hub, retaining the marked vertices U and every incident edge slot. Suppose Q is 3-vertex-connected and U has nine vertices.

For every D contained in U with |D|<=2, the multigraph K-D is connected. Indeed Q-D is connected, and none of the deleted vertices lies in S. Its S components are therefore the same connected sets used in the quotient. Contracting them cannot disconnect Q-D.

In particular every hub has at least three distinct neighbors in U, not merely three incident edge slots. A hub with at most two distinct retained neighbors would be isolated after deleting them, while at least seven retained vertices survive elsewhere. Parallel incidences are still permitted when the hub has at least three distinct retained neighbors.

These filters are strictly stated as necessary conditions for quotients of the original 3-connected frames. Arbitrary vertex connectivity of K is not asserted: deleting a hub corresponds to removing an entire unmarked region, which need not be a small vertex deletion in Q. A quotient that fails a retained-vertex deletion test cannot be a lift of the required kind, even if it passes every small edge-cut test.

## 2. Endpoint allocation: a sufficient condition

Let K be any quotient of the stated Petersen-replacement construction, and assume |U| is divisible by three. Suppose each retained vertex u can be assigned to a hub adjacent to u, so that the number assigned to every hub is divisible by three.

Orient one selected edge from the assigned hub to each retained vertex and give it value 1 in the direction of that orientation. Give every other quotient edge value zero. Each retained vertex then has divergence -1 and support degree one. Every hub has divergence equal to its assigned count, hence zero in F3. The exact lifting theorem in `quotient-reduction.md` produces a P3-factor of the expanded graph.

This is a sufficient condition, not a necessary characterization of all P3-factors. It uses no selected edges inside Q[U], and makes every retained vertex an endpoint. General feasible flows may use retained centers and internal retained edges instead.

A useful immediate case is that every retained vertex has a neighbor in one common unmarked connected region. Assign all of U to that hub. This positive class does not require a path or cycle passing through all retained vertices.

Multiple edges from u to its assigned hub cause no ambiguity: select any one of the corresponding original boundary incidences. No selected edge is used twice.

## 3. A complete finite test for this sufficient condition

Let k=|U|=3s and let there be p hubs. Choose nonnegative integers c_1,...,c_p with sum c_i=s. The desired load of hub i is 3c_i. Replace hub i, for this auxiliary test only, by 3c_i distinct slots, each adjacent to the retained vertices neighboring that hub.

A perfect matching between U and these k slots exists precisely when

```
|A| <= sum_(i in N_K(A)) 3c_i
```

for every A contained in U. Here N_K(A) is the set of hubs adjacent to at least one vertex of A; parallel edges do not create extra slots. Such a perfect matching assigns exactly 3c_i vertices to each hub. Conversely any desired endpoint assignment gives this slot matching.

For completeness, the finite matching condition can be proved directly. Necessity counts the distinct partners available to a subset. For sufficiency, induct on the number of left-side vertices. If there is a nonempty proper subset A with exactly |A| neighbors, first match A to those neighbors inductively. Remove both sets. For a subset B of the remaining left side, the condition for A union B leaves at least |B| neighbors outside N(A), so induction matches the rest. If there is no proper nonempty equality subset, choose any left vertex and one of its neighbors and match them. Every remaining nonempty left subset previously had at least one spare neighbor, so deleting that one right vertex preserves the condition. Induction finishes. A single left vertex and the empty instance are immediate. This proves both directions without a black-box matching algorithm.

There are exactly binomial(p+s-1,s) possible nonnegative load vectors, by the elementary stars-and-bars encoding of s identical units and p-1 separators. For nine retained vertices, s=3 and the quotient bound gives p<=5, so at most binomial(7,3)=35 vectors need be considered. Each vector has at most 2^9=512 retained subsets to test. Thus this endpoint-only sufficient condition can be decided with at most 17920 such subset inequalities per quotient. This is a proved operation-count bound, not a run result.

Reject a vector immediately when 3c_i exceeds the number of distinct retained neighbors of hub i. A retained vertex with no hub neighbor also makes the endpoint-only condition impossible, but does not rule out a general P3-factor.

## 4. Add an internal retained P3 packing

A stronger sufficient certificate consists of a vertex-disjoint P3 packing using only retained vertices and an endpoint allocation for the retained vertices not covered by that packing. The number of uncovered retained vertices is still divisible by three.

Use the chosen internal P3 paths on their vertices. On the remaining retained vertices use the quotient flow of Section 2. No edge between the two vertex sets is selected. At each internally covered retained vertex the orientation from its path center to its endpoints gives divergence -1 and support degree at most two. The internally covered triples make zero total contribution to hub equations because none of their boundary edges is selected. The uncovered retained vertices satisfy the same equations through the endpoint allocation. The exact quotient lifting proof therefore gives a P3-factor of the full expanded graph.

For nine retained vertices, the internal packing may have zero, one, two or three paths. Three paths already cover U completely. Two paths leave three vertices, for which a common neighboring hub suffices. One path leaves six vertices, whose endpoint loads are either six at one hub or three at each of two hubs. These are optional sufficient certificates; failure to find one must fall back to the complete F3 feasibility test rather than be labeled a graph obstruction.

A crude deterministic upper bound on internal packing enumeration is also small enough to be explicit. A nine-vertex graph of maximum degree three has at most sum_u binomial(deg(u),2)<=27 centered P3 paths, counting a triangle with each possible center separately. Enumerating all subsets of at most three such path objects gives at most

```
1 + 27 + binomial(27,2) + binomial(27,3) = 3304
```

candidates, before rejecting intersecting vertex sets. This is a safe coverage bound, not a claim of optimal enumeration or a measured count. For each surviving packing apply the slot test to its uncovered retained vertices.

## 5. Order of a sound nine-retained search

A candidate outer enumeration may now use these stages:

1. Generate the simple retained graph and the residual slot partition into hubs, without unproved symmetry omissions.
2. Reject disconnected quotients, edge cuts of size below three, hubs with fewer than three distinct retained neighbors, and disconnection after any deletion of at most two retained vertices.
3. Try a directly checkable internal-packing/endpoint-allocation certificate.
4. For every remaining quotient, enumerate all F3 divergence solutions by its spanning-tree coordinates and check retained support degrees.

The first two stages are necessary-condition filters; the third is only a sufficient-condition shortcut; the fourth is the exact quotient test. This distinction must be preserved in output records. In particular a failed shortcut is not a negative answer, and a bad abstract quotient still needs a valid original-domain lift before it can be used against the original graph assertion.

Both admitted obligations remain open in repository truth. The new filters and local certificates do not supply a completed finite enumeration, verifier receipt or Result.
