# Extension to eighteen vertices

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This extends the finite structural proof in `small-traceability-and-dense-nine.md`. It does not assert an enumeration, external verification or general root closure.

## 1. Candidate theorem and inherited reductions

Every finite simple cubic graph with edge connectivity at least three and order at most eighteen has a Hamiltonian path.

Orders through sixteen were handled in the preceding candidate. At order eighteen, a triangle can be contracted exactly as in that proof; the smaller graph is simple, cubic and 3-edge-connected, and its Hamiltonian path lifts through the triangle. It remains to handle a triangle-free eighteen-vertex graph.

Take a perfect matching and its complementary 2-factor F. Every F cycle has length at least four. One or two cycles are joined as previously proved. There are at most four cycles. The local fact that a cycle with at most one internal matching chord has a connected graph of feasible spanning-path endpoint pairs will be used below; its explicit proof is in the preceding candidate.

## 2. Three factor cycles

Contract the three cycles and discard internal matching chords. If the underlying quotient is a triangle, at least one cycle has length at most six. A four- or five-cycle has no internal matching chord in a triangle-free graph. A six-cycle has at most one: two would leave a cut of size two, contrary to edge connectivity. Thus the selected middle cycle has the connected endpoint-pair property. Its external ports meet both other cycles. Some feasible endpoint pair meets different cycles, and the three local spanning paths join to a Hamiltonian path.

If the underlying quotient is a path, write l_1,l_2 for the leaf-cycle lengths and b_1,b_2 for their boundary sizes. Each leaf satisfies l_i+b_i>=8. For length four all four matching edges are external; for length at least five the boundary is at least three. If the middle cycle has h internal matching chords, degree counting gives

```
2h = 18 - (l_1+b_1) - (l_2+b_2) <= 2.
```

Hence h<=1, and the same connected endpoint-pair lemma permits a spanning middle path between the two leaf types. The leaf paths join to it as before.

## 3. Four factor cycles of lengths four, four, four, six

The three four-cycles have all their matching edges external. The six-cycle D has either no internal chord, giving six external ports, or one internal chord, giving four external ports.

With one chord, triangle-freeness forces it to join opposite vertices of the six-cycle. Label its cycle 0,1,2,3,4,5,0 and its chord 0--3. The external ports are 1,2,4,5. Their feasible spanning-path pairs include the four-cycle

```
1--2--5--4--1.
```

The pairs 1--2 and 5--4 come from deleting their cycle edge. The other two are witnessed by

```
(2,1,0,3,4,5) and (1,2,3,0,5,4).
```

Thus this component can be treated as a four-port cycle for the previous four-cycle quotient argument. The quotient is 4-regular on four vertices, with opposite multiplicity triples (2,2,0) or (2,1,1), and that argument applies unchanged to the feasible port-pair cycle.

Now suppose D has no internal chord. Let A,B,C be the four-cycles. Put x=m(AB), y=m(AC), z=m(BC). Their degrees and the degree six of D give

```
x+y+z=3,
m(AD)=1+z, m(BD)=1+y, m(CD)=1+x.
```

A cut on two four-cycle nodes implies x,y,z<=2. Up to permutation the possibilities are (1,1,1) and (2,1,0).

For (2,1,0), take x=2,y=1,z=0. At D the port groups toward A,B,C have sizes one,two,three. There must be adjacent ports toward B and C: one port of the third color cannot separate two nonempty color groups around both directions of a cycle. Choose such a pair. At B there are two ports toward A, so at least one is adjacent to its now fixed port toward D. The quotient path A-B-D-C therefore lifts to a Hamiltonian path.

For (1,1,1), each of A,B,C has one port to each of the other two and two ports to D. If one of these four-cycles has its two single ports adjacent, use that cycle between the other two, and put D at one end of the quotient path. At the other middle four-cycle, two candidate D ports guarantee adjacency to its fixed single port.

Otherwise, at each of A,B,C the two single ports are opposite. Every D port there is then adjacent to both single ports. Around D, choose adjacent ports of different colors, say X and Y, among A,B,C. Such a pair exists because all three colors occur. Let Z be the remaining four-cycle. The quotient path X-D-Y-Z lifts: the chosen ports work at D, and at Y its incoming D port is adjacent to its single port toward Z.

## 4. Four factor cycles of lengths four, four, five, five

Label the four-cycles A,B and the five-cycles C,D. There are no internal matching chords. The quotient degrees are four,four,five,five. Its edge multiplicities have the form

```
m(AB)=x,       m(CD)=x+1,
m(AC)=m(BD)=y, m(AD)=m(BC)=z,
x+y+z=4.
```

Pair-cut bounds give x<=2 and y,z<=3. Interchanging C,D permits y>=z. All possibilities and a usable quotient path are listed below.

| x | y | z | Quotient path |
|---:|---:|---:|---|
| 0 | 3 | 1 | A-C-D-B |
| 0 | 2 | 2 | C-A-D-B |
| 1 | 3 | 0 | A-C-D-B |
| 1 | 2 | 1 | C-A-B-D |
| 2 | 2 | 0 | C-A-B-D |
| 2 | 1 | 1 | B-A-C-D |

Here is the complete port justification, so the table does not hide a compatibility search. A fixed port of a four-cycle is adjacent to at least one of any two candidate other ports. A fixed port of a five-cycle is adjacent to at least one of any three candidate other ports. Except in the second row, fix any available edge for the middle connection of the listed path. At each middle cycle the outer connection has at least the requisite two or three candidate ports, so the two local choices work independently.

In the second row, D has two ports toward A, two toward B and one toward C. Some A port and B port are adjacent: deleting the single C port leaves a path containing both other colors and hence a color transition. Choose that A-D and D-B pair. At A, at least one of its two ports toward C is adjacent to the fixed port toward D. This realizes C-A-D-B as well.

The six rows exhaust the integer solutions under the stated bounds. At the end cycles, break an edge incident with the selected port. At each middle cycle, break the edge between its two selected adjacent ports. Joining the resulting spanning paths completes the Hamiltonian path in every case.

## 5. Exhaustion and consequences

The two four-cycle length partitions above are the only partitions of eighteen into four parts at least four. Along with Sections 1-2 and the lower-order induction, they exhaust the candidate traceability theorem.

The original P3-factor assertion is therefore covered by these natural-language candidates at each eligible order six, twelve and eighteen: partition the Hamiltonian path into consecutive triples. This is a finite scope statement and not an assertion about every cubic order.

For the nine-retained quotient reduction, e=9 internal retained edges normalize to a simple 3-connected cubic frame on 36-2e=18 vertices. The Hamiltonian path contains all nine retained vertices and has retained degree at most two. The exact marked-forest and quotient-lifting proofs therefore give a P3-factor in the associated Petersen-expanded graph. This eliminates e=9, in addition to e>=10 and e<=5 already covered.

Only the internal retained-edge counts

```
e=6,7,8
```

remain in that nine-retained reduction. Their normalized cubic frames have orders twenty-four,twenty-two,twenty, and the corresponding normalized Petersen-expanded witnesses, if a negative quotient is actually found, would have orders 144,126,108. The outer quotient enumeration is still not reported as executed.

## 6. Boundary of the present path-lifting argument

At order twenty, a three-cycle factor can have two four-cycle leaves and a twelve-cycle middle with two internal matching chords. The one-chord connected-endpoint lemma no longer applies. In fact the companion `single-pass-twenty-obstruction.md` gives an explicit 3-connected cubic example where this particular factor cannot be joined by three single spanning cycle-pieces, although the graph has an explicit Hamiltonian cycle.

That example blocks a silent extension of the current local argument; it is not a nontraceable graph or a counterexample to the ProblemContract. New crossing patterns or a complete quotient search are needed for the remaining parameter range. Both admitted obligations remain open in repository truth.
