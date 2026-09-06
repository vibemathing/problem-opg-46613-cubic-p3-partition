# Exact contraction of unmarked regions and a finite nine-retained search space

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This is a proved reduction of the repair problem, not a claim that the remaining finite cases have been enumerated.

## 1. Quotient data

Let Q be a finite simple cubic graph, let U be its retained vertices, and let S=V(Q) minus U be the vertices replaced by Petersen nine-vertex bricks. Assume |U| is divisible by three. Contract each connected component of Q[S] to one unmarked hub, delete the resulting loops, and retain all edges incident with U. Call this multigraph K.

Parallel edges from a retained vertex to the same hub are kept as distinct incidences. There are no edges between distinct hubs. The retained induced graph Q[U] is unchanged and simple, and each retained vertex still has exactly three incident edge slots.

Give each oriented edge of K a value x_uv in the field F3, with x_vu=-x_uv. A feasible quotient assignment means:

- divergence is -1 at each retained vertex;
- at most two incident edge values are nonzero at each retained vertex;
- divergence is zero at every hub.

All degrees and supports count edge incidences, including parallel edges.

## 2. Exact equivalence, including the lifting argument

**Candidate contraction theorem.** The Petersen-expanded graph has a P3-factor if and only if K has a feasible quotient assignment.

A P3-factor gives a signed frame flow exactly as proved in `p3-interface.md`: edges are oriented from centers to endpoints; divergence is -1 and support degree at most two on U, and zero on S. Summing divergence over an S component cancels all its internal contributions. Contracting that component therefore gives the required zero divergence at its hub. This proves necessity.

For sufficiency, take a feasible quotient assignment and restore each component C of Q[S]. Its boundary values are prescribed. For s in C, let b_s be the sum of its prescribed outgoing boundary values and set d_s=-b_s. The hub equation says sum_(s in C) d_s=0.

Choose a spanning tree of C and root it. For the edge from a child w to its parent, assign the internal value

```
x_(w,parent) = sum_(s in subtree(w)) d_s in F3.
```

Use the negative value on the reversed orientation and zero on all other internal edges. Telescoping gives internal divergence d_s at every non-root vertex; the zero total gives the same equation at the root. Thus internal plus boundary divergence is zero at every vertex of C. This is an explicit finite construction, valid also for a component consisting of a single vertex.

After doing this for every component, the full frame Q carries a flow with exactly the conditions of the local Petersen-brick transfer proof. At each unmarked cubic vertex the zero-divergence pattern is UUU, UAB, AAA or BBB. At each retained vertex, divergence -1 and support degree at most two means one entering edge or two outgoing edges. The explicit local certificates therefore glue to a P3-factor.

In particular, the internal topology and size of an unmarked connected region affect neither feasibility nor the required boundary equation. Only its connectedness and the retained boundary incidences matter. This statement concerns P3-interface feasibility, not preservation of vertex connectivity under arbitrary quotient expansion.

## 3. Necessary restrictions inherited from a 3-edge-connected frame

Now assume Q has edge connectivity at least three and U is nonempty. Every unmarked component is a proper vertex subset, so its boundary has size at least three. Contracting connected vertex sets preserves the lower bound three on every nontrivial edge cut: a quotient cut lifts to a cut of Q. Hence K is connected and has edge connectivity at least three as a multigraph.

Write k=|U|, e=|E(Q[U])|, p for the number of hubs, and r for the number of retained-to-hub edge incidences. Cubicity gives

```
r = 3k-2e,
p <= floor(r/3),
|V(K)| = k+p,
|E(K)| = e+r = 3k-e.
```

These are necessary quotient restrictions. It is not asserted that every abstract quotient satisfying them has a 3-connected cubic lift. For proving a positive result, testing this larger necessary-condition class would be sufficient. For turning a bad quotient into an original-domain counterexample, a valid lift would still have to be constructed and checked separately.

## 4. The remaining nine-retained parameter

The candidates already prove all eligible cases with at most six retained vertices, every independent retained set, and every retained set with at most five internal edges. A remaining nine-retained case can therefore be restricted to e>=6.

Because a cubic frame has even order, a nine-retained frame has at least one unmarked vertex, hence p>=1. Thus r>=3, giving e<=12. Consequently every remaining quotient has

```
k=9,
6 <= e <= 12,
3 <= r=27-2e <= 15,
1 <= p <= floor(r/3) <= 5,
|V(K)| <= 14,
|E(K)| <= 21.
```

This is a finite reduction independent of how many unmarked frame vertices were originally present. Quotients for which the nine retained vertices themselves already have a P3-factor can be omitted: use that factor on U and UUU inside every brick.

## 5. A complete bounded flow search for each fixed quotient

For a fixed connected quotient, choose a spanning tree and orient every edge arbitrarily. Assign any of the three F3 values to each non-tree edge. The divergence equations uniquely determine all tree-edge values by the same subtree-sum argument. The compatibility condition is satisfied because the prescribed total divergence is -k=0 in F3.

Therefore enumerating the non-tree values enumerates every solution to the divergence equations exactly once. The number of free edge values is

```
|E(K)|-|V(K)|+1 = 2k-e-p+1.
```

In the nine-retained range this is 19-e-p<=12. Thus at most 3^12=531441 assignments need to be examined for each fixed quotient. Reject a solution precisely when some retained vertex has three nonzero incident edge values. A surviving solution is an exact certificate and can be lifted constructively by Section 2.

No assignment counts or successful quotient coverage are reported here as executed output. The per-quotient bound does not imply that enumerating all quotient types is cheap. A complete outer enumeration must separately generate the simple retained graph of maximum degree three and all partitions of its residual edge slots into hub blocks of size at least three, preserving multiplicities and covering all isomorphism types. Symmetry pruning requires its own completeness justification.

A negative search on one abstract quotient is not automatically a graph counterexample. It must first be checked against the cut constraints and, for original-domain use, an actual simple 3-connected cubic lift. A positive exhaustive search over the whole necessary-condition class would not have that lifting obstacle.

## 6. Next falsifiable objective

Produce and audit one canonical outer-quotient enumerator for k=9, e=6,...,12, p=1,...,floor((27-2e)/3), together with exact F3 certificates or a fully specified bad quotient. Preserve finite scope and independent replay requirements. The global root is not closed by the reduction or by the number 531441.

Dependencies are the explicit local interface proof, the independent-retained and sparse/six-retained candidates, and elementary finite graph incidence identities supplied above. No external theorem or runtime receipt is assumed by this reduction.
