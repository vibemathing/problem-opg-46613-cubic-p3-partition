# Minimal universal three-port brick and a cycle-only gluing obstruction

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This is an audit of the weaker P3 interface developed in `p3-interface.md`. It is not a global minimum-order claim about the original graph problem.

## 1. The class and its exact minimum order

A simple cubic three-port brick means a finite simple graph R with three distinct specified terminals of internal degree two and all other vertices of internal degree three. Each terminal is to receive one external edge. Use the states U, A, B defined in the companion interface candidate: unused port, singleton endpoint, or internal edge segment centered at the terminal. A brick is universal here precisely when it realizes UUU, every permutation of UAB, AAA, and BBB by disjoint local pieces covering all its vertices.

**Candidate minimum-order proposition.** Every universal brick in this class has at least nine vertices, and the Petersen graph with one vertex removed attains nine. The lower bound holds even without connectedness or a condition on its cubic completion.

Let n=|V(R)|. Summing internal degrees gives

```
2|E(R)| = 3(n-3)+2*3 = 3n-3.
```

Consequently n is odd. The UUU realization partitions all n vertices into P3 paths, so n is divisible by three. The BBB realization contains three pairwise disjoint internal edge segments, and hence uses at least six vertices. The smallest odd multiple of three at least six is nine.

For attainment, the fixed nine-vertex brick has terminals 0,3,4 and internal edges

```
01 05 12 16 23 27 38 46 47 57 58 68.
```

The complete nine-state certificates and explicit terminal automorphisms are in `p3-interface.md`. The graph is connected; for example,

```
(0,1,2,3,8,6,4,7,5,0)
```

is a Hamiltonian cycle. Adding one new vertex adjacent to the three terminals recovers the Petersen graph, whose 3-connectivity is checked in C01. Thus the same nine-vertex example also attains the lower bound when connectedness and a 3-connected cubic completion are required.

## 2. A Hamiltonian cycle does not preserve the full interface

Consider only a nine-cycle with its three ports at cyclic positions 0,3,6. Local paths and pairs are now required to use cycle edges only. This graph realizes UUU, but none of the other eight allowed signatures.

UUU is obtained from consecutive triples. Necessity of the nine-state list still follows from the vertex-count congruence a+2b=0 modulo three.

For AAA, deleting the three singleton port vertices leaves three disjoint two-vertex paths. None can be covered by internal P3 paths, so AAA is impossible.

For BBB, the three disjoint internal edge segments consume all three port vertices and three further vertices. The remaining three vertices would have to form an internal P3. Every P3 in a nine-cycle consists of three cyclically consecutive vertices, and every such triple contains a port because the ports are exactly the positions divisible by three. All ports have already been consumed by the B segments. Hence BBB is impossible.

For UAB, orient the cycle and place the A singleton at position 0. The B terminal lies at distance d=3 or 6. If its internal partner is its successor, removing the singleton and the B pair leaves path components of lengths d-1 and 9-d-2, congruent to 2 and 1 modulo three. If its partner is its predecessor, the component lengths are d-2 and 9-d-1, congruent to 1 and 2 modulo three. The lengths are positive in both cases. Neither pair of components can be covered by P3 paths. This covers both B-edge choices and every ordering of the two selected ports.

Therefore the nine-cycle alone has exactly the signature UUU.

## 3. The exact missing edges in the Petersen brick

In the Hamiltonian cycle displayed in Section 1, the terminals 0,3,4 occur at positions 0,3,6. The full twelve-edge Petersen brick differs from this cycle by exactly three chords:

```
(1,6), (2,7), (5,8).
```

The cycle-only obstruction from Section 2 therefore applies to this very Hamiltonian cycle. The full brick nevertheless realizes every allowed signature. For instance, the UAB certificate with A at 0 and B at 3 uses the pair (3,8) and paths (1,6,4),(2,7,5); the two chords (1,6) and (2,7) restore the missing boundary behavior. The AAA certificate uses paths (1,2,7),(5,8,6), and the BBB certificate uses internal pairs (0,5),(3,8),(4,7) and path (2,1,6).

Thus replacing the full brick by one spanning divisible cycle loses essential P3 gluing states. The exact failure is at the local interface, not at the existence of an internal UUU P3-factor. An argument that retains only cycle lengths and silently assumes arbitrary UAB boundary routing would fail on this explicit nine-cycle.

## 4. Scope and next obligation

The minimum nine here concerns universal cubic three-port bricks as explicitly defined; it does not prove that eighteen is the smallest counterexample to the divisible-2-factor assertion. The latter requires the separate lower-order candidate.

The cycle-only example invalidates an auxiliary interface simplification. It is not a cubic graph and is not offered as a counterexample to the ProblemContract. The full Petersen brick, its local certificates, and the marked-forest transfer theorem remain the proposed weaker replacement for the failed divisible-cycle route. No canonical failure record or mathematical admission is created by this artifact.
