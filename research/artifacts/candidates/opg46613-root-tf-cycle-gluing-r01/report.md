# Triangle-free root: cycle gluing, an order-18 theorem, and a sharp fixed-matching boundary

Status: NONTERMINAL_CHECKPOINT. Verdict: candidate_only.
Primary owner: math-proof. Trust domain: web-candidate-generation.
Repository: vibemathing/problem-opg-46613-cubic-p3-partition.
Source/base: 0f009927bfffa44335148cb65ae93596288b50c4.
Target: obligation:opg46613-root under the existing Attempt/Route/Graph.
The legacy divisible-two-factor route ID is a transport binding, not a premise.
No previous 18-vertex object or 45-vertex simulator audit is repeated here.

## 1. Frozen statement, minimal counterexample and dependencies

R_tf: every finite simple triangle-free 3-vertex-connected cubic graph G with
|V(G)|=3k, k>0, has a spanning P3-factor. P3 is a selected path on three distinct
vertices, not required induced by the ProblemContract. Triangle-freeness makes
such paths induced automatically. Cubicity implies even order, so the eligible
orders are precisely positive multiples of six.

If R_tf has a counterexample, let N be its least order. This minimum exists
by well-ordering; no minimum for a different class is substituted. The candidate
proof below shows N>=24. It does not establish existence of a counterexample,
and does not give this bound for the smallest unrestricted root counterexample
via the expansive triangle simulator.

Document-local proof DAG (not new admitted registry IDs):
P: a root-domain host is bridgeless and hence has a perfect matching M (the
classical Petersen theorem, retained as a named external theorem dependency).
L: exact cycle-piece gluing for a supplied M, with explicit two-port formulas.
C: exact criterion for at most two selected M edges when F=G-M has three cycles.
B18: for orders 6,12,18 every possible cycle-length partition satisfies a
constructive case of L/C; thus a P3-factor using at most two M edges exists.
X: universal selection of a feasible subset S of M in arbitrary order remains
OPEN. P + X + the previously recorded exact gap-forest bridge would prove R_tf.
The existing triangle simulator then gives the candidate equivalence to R.
B18 and the new finite checks do not close X or R_tf.

Petersen's theorem is not replaced by a new axiom or a claim of a local Lean
replay. The exact theorem statement is confirmed by the primary research
source recorded in source-note.md. The new constructive theorem is conditional
on any supplied M and does not require computing M by the test generator.

A simple cubic 3-vertex-connected graph has no edge cut of size at most two:
a side of size one has boundary three, and a side of size two has boundary at
least four. Otherwise deleting the at most two cut endpoints in one side
leaves nonempty vertices on both sides disconnected, violating vertex
connectivity. In particular all the nontrivial cycle-union cuts used below
have boundary at least three, and the graph is bridgeless.

## 2. Exact gluing on the unchanged host

Fix a perfect matching M and complementary 2-factor F. Every P3 uses at most
one M edge. A P3 using a selected e in M is an A singleton at one end of e
joined to a consecutive B pair on an F cycle centered at the other end. A P3
not using M is a consecutive triple on an F cycle. All selected M edges have
one A end and one B end, including an internal M chord when it is selected.

Conversely, partition every F cycle into such singleton/pair/triple pieces,
and glue each A to the B pair across its selected M edge. Distinct matching
ends and disjoint local pieces make all resulting triples vertex-disjoint;
every host vertex occurs once. The two selected edges of every glued triple
meet at its B center. This is an exact bidirectional normal form for a fixed
selected subset S, not a one-way graph contraction.

The original G is never altered. Simplicity, cubicity, triangle-freeness,
3-connectivity and order therefore remain unchanged. No auxiliary noncubic
subgraph is promoted to the root domain and no modulus-changing cap induction
is used. This specializes the earlier gap-forest criterion, rather than
assuming that a feasible S always exists.

Let a cycle have length L>=4. With no active vertex it can be tiled iff L=0
mod3. One active A is feasible iff L=1 mod3; delete its singleton and split
the remaining path into triples. One active B is feasible iff L=2 mod3;
choose one of its two cycle neighbors as its internal leaf and tile the
remaining path. These statements also give complete local certificates.

For two distinct active vertices u,v, let d be the number of edges from u to
v in one fixed cyclic direction, 1<=d<L. Each intervening inactive path must
lose an endpoint vertex for each B extending into that gap. A gap of d edges
has d-1 inactive vertices, so it demands (d-1) mod3 extensions. This demand is
0,1 or2. Adjacent active vertices demand zero; a one-vertex gap demands one,
so no vertex is used twice. A demand-two gap has at least two vertices.

The complete two-port formulas are:

| roles | necessary length residue | further condition | number of local covers |
|---|---|---|---|
| AA | L=2 mod3 | d=1 mod3 | 1 |
| AB or BA | L=0 mod3 | d!=0 mod3 | 1 |
| BB | L=1 mod3 | none | 2 if d=2 mod3, otherwise 1 |

For AA both demands must be zero, giving the first row. For AB/BA there is
one extension: d=0 makes both demands two, while d=1 or2 gives demands 0,1
or1,0 and the B extends into the unique demanding gap. For BB the demands sum
two and are (0,2),(1,1),or(2,0). The first and last force both B ends into one
gap; the middle allows either bijection of B ends to gaps. All remaining paths
are tiled consecutively. This proves existence, exclusion and counts for
arbitrary L, not merely for the tested range 4..60.

## 3. Exact three-cycle criterion at matching cost at most two

Suppose F has exactly three cycles and total order is divisible by three.
Contract each F cycle only as a notation for the multigraph of crossing M
edges. Internal M chords are retained in G; they are loops in this notation.
Connectedness of G gives a connected crossing quotient.

The residue multisets are exactly 000,111,222,012.

000: tile every cycle internally, using no M edge.

111: choose two crossing M edges whose quotient is a tree spanning the three
cycles. Use A on the two end cycles and BB on the middle cycle. Section 2
works for every distinct pair of middle endpoints. This gives a factor with
exactly two M edges, independent of all cycle lengths and attachment phases.

012: denote the cycles C0,C1,C2 by residues. If any M edge joins C1 and C2,
use A on C1 and B on C2 and tile C0 internally. Otherwise the quotient is the
path C1-C0-C2. Choose one edge on each link. On C0 their roles must be B toward
C1 and A toward C2. Section 2 works iff their positions on C0 differ modulo
three. Thus a factor of cost <=2 exists iff there is a direct C1-C2 edge, or
there is such a differently phased pair of C0 attachment positions.

222: choose two crossing edges spanning the three cycles. The end-cycle
roles must be B and the middle roles AA. This works iff the middle endpoints
have directed cyclic distance 1 mod3. Since the middle length is 2 mod3,
reversing direction preserves this condition. Existence of such a pair is
necessary and sufficient for a factor with at most two M edges.

For necessity in the last two cases, any group of F cycles disconnected from
the rest by the selected crossing edges has its vertices covered internally
by whole P3s and hence has total order 0 mod3. In particular a single nonzero
cycle cannot be isolated, even if an internal matching chord is selected.
In 111/222, two edges must therefore be crossing edges spanning all three
cycles; in 012 with no direct C1-C2 link they must use the stated two links.
The local role counts then force exactly the states listed. This argument
does not erase internal chords as a general proof method.

## 4. Cut capacity makes the 012 phase obstruction start at order 36

Assume G is in the triangle-free root domain, F has residue multiset 012,
and no factor uses at most two M edges. There is no C1-C2 M edge. Every
attachment of C0 to C1 and every attachment to C2 must have the same residue
position on C0, by Section 3. Both sets are nonempty. Consequently all these
positions lie in one of the three phase classes.

Write Li=|Ci| and di=|delta(V(Ci))| for i=1,2. These cuts consist of matching
edges, have di>=3, and their endpoints on C0 are all distinct. Thus

    L0 >= 3(d1+d2),       n >= (L1+3d1)+(L2+3d2).

A 4-cycle or 5-cycle in a triangle-free cubic graph has no internal M chord:
every chord would create a triangle. If L1=4, d1=4, so L1+3d1=16; if L1>=7,
d1>=3 gives the same lower bound. For C2: L2=5 gives d2=5 and sum20; L2=8
has even d2 (3L2=2|E(C2)|+d2), hence d2>=4 and sum20; L2>=11 gives sum>=20.
Therefore

    n >= 36.

In particular, a three-cycle 012 factor in a root-domain graph of order below
36 always yields a P3-factor by the explicit one-/two-edge gluing. The prior
ROOT-TF-CORE-R01 graph with cycle lengths 7,18,11 and three attachments on each
link attains equality and has minimum matching cost three. That archived
candidate is referenced, not re-audited or submitted again. This threshold
concerns a restricted matching cost and residue pattern, not root nonexistence.

## 5. Complete constructive coverage through order 18

THEOREM (candidate proof). If G is finite simple triangle-free 3-connected
cubic of order 6,12 or18, then for every supplied perfect matching M, G has a
P3-factor using at most two edges of M.

All F cycles have length at least four. The full unordered length partitions
are listed below; no graph-order enumeration is used to claim completeness.

6: (6).
12: (4,4,4), (4,8), (5,7), (6,6), (12).
18: (4,4,4,6), (4,4,5,5), (4,4,10), (4,5,9), (4,6,8),
    (4,7,7), (4,14), (5,5,8), (5,6,7), (5,13), (6,6,6),
    (6,12), (7,11), (8,10), (9,9), (18).

One cycle is tiled internally. With two cycles, either both residues are zero
or they are 1 and2; connectedness supplies an M link in the latter case and
A/B gluing applies. This elementary subcase already appeared in PR26.
Three-cycle 000 and111 use Section 3; 012 uses Section 4. At order18 the only
remaining 222 lengths are (5,5,8).

For (5,5,8), all five vertices of each 5-cycle are crossing M endpoints.
If either 5-cycle has neighbors in both other cycles, the cyclic sequence of
its two destination labels has adjacent unequal entries. Their matching
edges give a spanning quotient tree with middle distance one, so Section 3
repairs. Otherwise each 5-cycle sends all five edges to just one other cycle.
It cannot send all five to the other 5-cycle: that saturates both cycles and
disconnects the 8-cycle. Thus both send all five to the 8-cycle, requiring ten
distinct endpoints on eight vertices, a contradiction.

For (4,4,4,6), each 4-cycle has four crossing M edges. The crossing quotient
induced on the three 4-cycles is connected. If it had three components, twelve
edges would have to enter the 6-cycle. If it had two components, one is a
single 4-cycle needing four incident edges, and the other is the union of two
4-cycles needing at least three by the edge-cut lower bound. Seven distinct
endpoints on the 6-cycle are impossible. Choose two crossing edges forming a
tree on the three 4-cycles, apply 111 gluing and tile the 6-cycle internally.
The use of a cut of a UNION of cycles, not just individual cycle cuts, matters.

For (4,4,5,5), all matching edges join different F cycles. Let A,B be the
4-cycles and C,D the 5-cycles. Consider the bipartite adjacency of crossing
edges between {A,B} and {C,D}. It is nonempty, otherwise G is disconnected.
If it has no matching of size two, all its edges share one vertex: any two
must meet, and a bipartite graph with this property is a star. If its center
is A, B must send all four of its edges to A, exhausting A's degree and
contradicting a cross-group edge. If its center is C, D sends all five to C,
with the same contradiction. Renaming covers the other choices. Thus two
disjoint 4-/5-cycle pairs exist; choose an M edge for each pair and glue A/B
pieces independently. This covers all four cycles using two M edges.

There cannot be five cycles at order18. The partition list exhausts the cases,
so the theorem follows. Petersen supplies M for the root-domain corollary.
It follows conditionally that a minimum triangle-free root counterexample has
N>=24. This is a proof by finite LENGTH classification, not an extrapolation
from 85 sampled HOST graphs or an assertion about all larger orders.

## 6. Order24 is a sharp boundary for the two-M-edge method, not for root

The next spectrum (8,8,8) has a concrete obstruction to cost at most two.
Take three consecutive cycles on 0..7,8..15,16..23. In each offset a=0,8,16,
add the two internal matching edges (a+2,a+5),(a+4,a+7). Join its vertices
(a,a+1) to (b+3,b+6) respectively, where b is the next offset cyclically.
This fixes a perfect matching and the complete 24-vertex graph with edges:

```
0-1 0-7 0-11 1-2 1-14 2-3 2-5 3-4 3-16
4-5 4-7 5-6 6-7 6-17 8-9 8-15 8-19 9-10
9-22 10-11 10-13 11-12 12-13 12-15 13-14 14-15
16-17 16-23 17-18 18-19 18-21 19-20 20-21 20-23
21-22 22-23
```

All edges are distinct, each degree is three, no triangle occurs, and all301
vertex deletion sets of size at most two pass the new separate consumer.
Each cycle has crossing ports {0,1} toward one neighbor cycle and {3,6}
toward the other, in its offset labels. Their four forward distances are
3,6,2,5, none congruent to1. Every spanning two-edge quotient tree therefore
fails the AA middle condition. Section 3 excludes cost<=2 rigorously.

The actual graph has this P3-factor (middle entry is center):

```
(1,0,7) (2,3,4) (5,6,17) (9,8,19)
(10,11,12) (13,14,15) (16,23,22) (18,21,20).
```

It uses precisely M edges 6-17,8-19,18-21. Hence its minimum matching cost is
three. It is a POSITIVE root instance. The combined order18 theorem and this
example give the smallest eligible order for failure of the uniform cost<=2
method. They do not give the smallest root counterexample or a root UNSAT.

All eight bijections of the three paired cross links were screened as fixed
labeled controls. Each passes 3-connectivity and has minimum matching cost three. The canonical
000 wiring has complete factor polynomial by M-edge cost

    0,0,0,24,108,102,141,174,36.

Its total is585, and it has24 minimum-cost factors. Some other wirings have
coefficient168 instead of174 at cost seven, with total579. All eight have24
minimum-cost factors; the full per-wiring polynomials are preserved. No claim is made that
these eight labeled graphs are pairwise nonisomorphic. The canonical wiring
also has a complete79-subset certificate (all S of size0,1,2): each row gives
an isolated nondivisible cycle or an incompatible middle gap. The consumer
checks coverage and recomputes the entire factor polynomial without importing
the producer. Certificate truncation and a false gap are rejected. These are
restricted-cost negative certificates, not certificates of no P3-factor.

## 7. Actual bounded checks, scope, and implementation review

Six final bounded stages really ran with exit0 and empty stderr:
- generate.py: seed466132709 produces85 fixed labeled root-domain hosts across
  all22 length partitions at orders6,12,18. Label duplicates are rejected; no
  isomorphism reduction or complete graph-order census is claimed.
- constructor.py: chooses at most two crossing M edges by the proved cases,
  creates local pairs and residual paths, and emits every full P3-factor.
- verify.py: generates P3 rows from unordered triples, computes an exact
  minimum-cost cover by a residual-vertex recurrence, and checks every local
  and global certificate. All85 minima agree, with cost histogram25/36/24
  at costs0/1/2. All12,610 host deletion cases pass;15 semantic mutations fail.
- local_check.py: an exact-cover row search separate from residual path tiling
  checks7,239 specified states on cycle lengths4..60;1,672 are feasible. The
  complete deterministic test-stream hash and negative/positive controls are
  saved. General formulas are proved in Section2, not inferred from this range.
- explore24.py: centered-neighbor/frozenset optimization over eight wirings.
- verify24.py: unordered-triple/bitmask factor-polynomial recurrence, separate
  graph checks and the complete79-row restriction certificate.

CPU caps for the first four stages are30 seconds, walls40 seconds, address
space512MiB, each output2MiB, one worker/thread. The extension stages use20/30
second CPU/wall caps,512MiB,2MiB output and one worker. Budget exhaustion raises
an error, not UNSAT. Interpreter versions, actual dates/times, exact commands,
exit codes and hashes are retained in the lossless replay-data.json archive.
Run decode_data.py to recover exact input/output/observation bytes in this
candidate directory before running the checks; existing mismatching files are
never overwritten. The archive is data persistence, not a verification badge.

Review correction: the first verify24 draft used tuple-valued subset indices
in its internal certificate but list-valued indices after JSON mutation. This
could make a mutation reject for representation rather than the changed gap.
The final code makes indices lists uniformly and adds an acceptance control
for the intact certificate. Its fresh final run passes both controlled
mutations. Initial code and observation are retained under exploratory/ in
the archive; they are not the final mutation-assurance source. Mathematical
inputs, factor polynomial and serialized certificate did not change.

Both consumers were newly written and import neither their producer nor any
old verifier. They remain in the SAME generation trust domain. No independent
trust identity, Lean elaboration, axiom audit, attestation or EvidenceLink is
claimed. Historical missing raw outputs and C08 Lean status remain unresolved.

## 8. First open lemma and continuation

The first open mathematical lemma remains X: for every triangle-free root
host with a supplied M, some S satisfies the exact gap-forest allocation
criterion. The cost<=2 shortcut is now exhaustively classified for three
cycles, proved sufficient through order18, and sharply blocked at order24.
A proof for arbitrary order must allow additional selected M edges, including
internal chords and genuine allocation constraints; neither quotient residue
alone nor scalar mass zero suffices as an admission argument.

Next atomic action: in the (8,8,8) and larger 222 phase-blocked setting, retain
all internal matching chords and characterize a three-edge S by the gap-forest
criterion. Seek a universal repair under explicit cut hypotheses, or a fully
specified positive-host obstruction to that restricted repair. Do not label
its failure root nonexistence. Treat the arbitrary-many-cycle selection lemma
as open, and do not recycle the failed divisible-cycle strengthening.

The existing triangle-free reduction and the new core lemma have separate
frozen verification requests. The web principal cannot issue trusted receipts;
registered execution, statement-faithfulness and any real closure gate remain
open. Even verification of all claims in this report would not close the root.
