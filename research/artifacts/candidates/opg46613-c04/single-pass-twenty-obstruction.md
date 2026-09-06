# A twenty-vertex obstruction to a particular path-gluing rule

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This is an exact failure of an auxiliary construction rule. The displayed graph is Hamiltonian, and its order is not divisible by three. It is not a counterexample to either traceability or the original ProblemContract.

## 1. Exact graph

Use vertices 0,...,19. Take three disjoint cycles:

```
C: (0,1,2,3,4,5,6,7,8,9,10,11,0),
A: (12,13,14,15,12),
B: (16,17,18,19,16).
```

Add the perfect matching consisting of

```
(0,6), (3,9),
(1,12), (2,13), (7,14), (8,15),
(4,16), (5,17), (10,18), (11,19).
```

This is a finite simple cubic graph. It is triangle-free: the two internal C chords have distance six along C, the other two factor cycles have length four, and matching edges between distinct cycles cannot form a triangle.

The given factor has cycle lengths (12,4,4), with no matching edge between A and B. Its quotient on factor cycles is therefore the path A-C-B, with four edges on each side.

## 2. Edge and vertex connectivity

Suppose a nonempty proper vertex cut has at most two edges. Each split factor cycle contributes at least two cycle edges. If no factor cycle is split, the cut is a cut of the quotient A-C-B and has at least four edges.

Thus exactly one factor cycle must split, with exactly two cycle edges crossing and no matching edge crossing. A split four-cycle is impossible: all its matching partners lie in C, and C lies wholly on one side, forcing all four vertices of that leaf cycle to the same side.

Only C could split. Its vertices on one side would form one cyclic interval. If A and B lie on opposite sides, the C ports at 1,2,7,8 must lie on the A side and those at 4,5,10,11 on the B side. These fixed port groups alternate four times around C, forcing at least four cycle edges across the cut.

If A and B lie on the same side, all eight C ports lie on that side. The other side of C can contain only vertices 0,3,6,9. They are pairwise nonadjacent along C, so a nonempty cyclic interval of them contains just one vertex. But its matching mate, along chord 0--6 or 3--9, would also have to lie on that side because no matching edge crosses. This is impossible.

Every cut therefore has size at least three. By the finite cubic connectivity lemma in `cubic-quotient-normalization.md`, the graph is also 3-vertex-connected.

## 3. Precisely stated rule being tested

The single-pass rule would choose a spanning path inside each of A, B and the induced subgraph on C, and join those three paths with one matching edge between A and C and one between C and B. Internal C paths may use either or both of its internal matching chords; the rule is not restricted to cycle edges there.

Such a rule would need a spanning path of C plus its two chords with one endpoint in

```
P_A = {1,2,7,8}
```

and the other in

```
P_B = {4,5,10,11}.
```

No such path exists. The following classification exhausts the possible number of used C chords.

## 4. Complete endpoint obstruction

With zero chords, a spanning path of the twelve-cycle is obtained by deleting one cycle edge. The adjacent pairs that consist of external ports are exactly

```
(1,2), (4,5), (7,8), (10,11).
```

Each pair is contained in P_A or in P_B.

With exactly one chord, both chord endpoints are internal vertices of the proposed path, since its endpoints are external ports. One cycle edge incident with each chord endpoint must therefore be removed. The two removals on the same cycle arc would leave a separate cycle and path, rather than one spanning path. The other two choices are the only connected choices.

For chord 0--6 their endpoint pairs are (1,7) and (11,5). For chord 3--9 they are (4,10) and (2,8). Again every pair lies within one port group.

With both chords, a spanning path has eleven edges and so would retain nine of the twelve cycle edges: exactly three cycle edges would be removed. All four chord endpoints 0,3,6,9 would be internal path vertices, and each would need at least one of its cycle edges removed. No cycle edge joins two chord endpoints. Three removed cycle edges cannot supply these four required incidences. Thus this case is impossible.

This proves the exact failure of the single-pass rule for this specified factor, even when both internal chords are permitted.

## 5. Explicit Hamiltonian cycle of the full graph

The failure is purely a restriction of the construction method. The whole graph has the Hamiltonian cycle

```
(0,1,12,15,14,13,2,3,4,16,19,18,17,5,6,7,8,9,10,11,0).
```

Every consecutive pair is an edge displayed in Section 1, and the twenty vertices occur exactly once before returning to zero.

Equivalently, splice the A path 12-15-14-13 into the C edge 1--2, and splice the B path 16-19-18-17 into the C edge 4--5. This uses two joining edges at each leaf factor cycle, rather than the one-edge-per-leaf rule. The central factor cycle is correspondingly split into more than one piece.

## 6. Research consequence and scope

The one-chord endpoint argument in the eighteen-vertex proof cannot simply be repeated when the middle component has two chords. Its first relevant triangle-free three-cycle pattern at order twenty already admits the precise obstruction above. A continuation should allow two-edge splices or other multiple-crossing patterns, or use the exact quotient flow search.

This is not a negative result for Hamiltonian paths at order twenty; the explicit Hamiltonian cycle proves the opposite for this very graph. It is not a graph in the original order-divisible-by-three domain. It only invalidates the stated auxiliary rule for a fixed factor. No new route identifier, canonical failure ledger entry, EvidenceLink or Result is created here.
