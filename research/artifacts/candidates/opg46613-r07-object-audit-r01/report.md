# R07 fixed-object audit: maximum restricted matching is not a repair obstruction

Status: `RESULT_CANDIDATE_READY`. Verdict: `candidate_only`.
Primary owner: `math-proof`. Generator trust domain: `web-candidate-generation`.
This status applies only to this finite route-exclusion candidate. It is not
Result admission, a kernel receipt, or closure of either canonical obligation.

## 1. Frozen scope and source mapping

The sole object is the 18-vertex labeled graph and charged forest in sections
2--4 of `research/artifacts/candidates/opg46613-root-r07/one-defect-repair.md`,
read at main `0fb44ea490bb350f232c348ce3cc9d4072bc792f`, Git blob
`b655125f01f3d0fe75f3c538e6fc25599ac023d1`. `witness.json` transcribes every
host edge, selected arc, Hamilton vertex order, named chord position, claimed
interlacement-tree edge, auxiliary typed matching edge, update vertex order
and output P3. These are input assertions, not silently trusted certificates.

This graph is NOT C02's different labeled 18-vertex two-factor obstruction.
The C08 verifier's 26-perfect-matching statistics are not reused for it.
P3 means a selected two-edge path on three distinct vertices, not an induced
path. Reference edges have increasing labels. Edge value 1 means that direction,
2 its reverse and 0 unused; charge is outward divergence 2 modulo 3.

Candidate claims:
- R07-A: the supplied graph is simple cubic, triangle-free and 3-vertex-connected.
- R07-B: the supplied 13 arcs form a charged forest with exactly one defect.
- R07-C: the exact restricted auxiliary matching is maximum, of cardinality 4.
- R07-D: the supplied nine-cycle nevertheless decreases weight by one and gives
  exactly the supplied six P3s.
- R07-E: for the general one-defect setting, a nonmaximum restricted matching
  is a sufficient repair condition. Its converse is not asserted.
Dependencies: A--D are checked directly below and by the new code; E follows
from the explicit symmetric-difference/lifting argument in section 6. C and D
exclude only the inference 'restricted matching maximum implies irreparable'.
There is no dependency from this exclusion to root closure.

## 2. Host and full cut-case audit

All 27 unordered edges are distinct, have two different labels in 0..17, and
all 18 degrees equal 3. Every one of the 816 vertex triples is inspected for a
triangle; none is present. The Hamilton order is

    0,10,9,1,6,8,5,13,11,7,16,14,12,4,15,17,3,2.

It covers all vertices, and all 18 cycle edges, including 2--0, belong to the
host. Its complementary nine chords are a perfect matching. At Hamilton
positions their names are

    A=0,3  B=1,5  C=2,8  D=4,9  E=6,17
    F=7,12 G=10,14 I=11,15 J=13,16.

The edges AB, AC, BD, CE, CF, FG, FI, GJ are eight valid interlacements and
connect all nine chords. All 36 chord pairs are tested; 14 interlace. Every
listed chord has cyclic distance at least 3, so none could complete a triangle
with two consecutive Hamilton edges. A triangle cannot contain two matching
chords. This also gives a structural triangle-free check.

Here is the complete implication from this certificate to edge connectivity.
For every nonempty proper vertex set S, the Hamilton cycle crosses delta(S) a
positive even number of times, at least twice. Thus a cut of size at most two
would have exactly two Hamilton edges and no crossing chord. Each side would
be one cyclic interval. Every vertex has a chord partner on its own side, so
each interval contains at least one chord. Chords in opposite intervals cannot
interlace. This partitions the interlacement graph into two nonempty components,
contradicting its displayed spanning tree. All cuts therefore have size at
least three. A singleton has boundary three, so edge connectivity is exactly 3.

For a simple cubic graph of order at least four with every nontrivial edge cut
of size at least three, all vertex-cut cases are as follows.
- Empty deletion: the cut bound entails connectivity.
- One deleted vertex u: every component of G-u needs at least three incident
  boundary edges. Two components would require at least six of u's three edges.
- Two adjacent deleted vertices u,v: at most 3+3-2=4 edges leave the pair, less
  than the six required if two components remain.
- Two nonadjacent deleted vertices u,v: there are six leaving edges, so if the
  deletion disconnects, exactly two components have boundary three each. Each
  component meets both u and v, since otherwise one of them would be a cut
  vertex. A component C has two edges to one vertex, say u, and one to v.
  Then delta(C union {u}) has size 3+3-2*2=2. This set is nonempty and proper
  because v and the other component survive, contradicting the cut bound.
This proves the vertex-connectivity implication without importing a library.

The checker also recomputes all 131071 unordered nontrivial bipartitions;
the minimum boundary is 3. There are 19 cuts of size 3, not just the 18 singleton
cuts. No stronger cyclic-connectivity assertion is made. A separate disjoint-set
calculation checks all 172 vertex deletions: 1 empty, 18 singletons, 27 adjacent
pairs and 126 nonadjacent pairs. Every remaining graph is connected.

## 3. Charged forest and exact auxiliary matching number

The initial sources are {0,3,6,9,12,15}. Each has two outgoing and no incoming
selected edges, hence integer divergence 2. The leaves are

    L={1,4,5,7,8,10,11,13,14,16,17}.

Each has one incoming edge and divergence -1. Vertex 2 has two incoming edges
0->2, 3->2 and one outgoing edge 2->5, so it is the sole defect and also has
integer divergence -1. Every modular divergence is therefore 2. The exact
components are {0,1,2,3,4,5}, {6,7,8}, {9,10,11}, {12,13,14}, {15,16,17}.
Their 13 edges equal 18-5, so the support is a forest; its exceptional tree has
arm lengths (1,2,2).

The four virtual edges, each retaining its source label, are

    7--8 [source 6], 10--11 [9], 13--14 [12], 16--17 [15].

The host-induced leaf edges are exactly

    5--8,5--13,7--11,7--16,8--10,11--13,14--16,14--17.

Real and virtual edge types are kept distinct. In this particular auxiliary
multigraph no real/virtual pair has coincident endpoints. Its exposed vertices
are {1,4,5}; vertices 1 and 4 are isolated. Hence every matching uses at most
floor((11-2)/2)=4 edges, while the displayed virtual matching uses four.
Thus its matching number is exactly 4. A fresh bottom-up dynamic program over
all 2048 vertex masks gives the same maximum. Parallel multiplicity would not
change maximum cardinality, but edge types remain necessary for path lifting.

## 4. Nine-cycle update and the actual factor

The cycle is (0,1,6,7,16,15,17,3,2). All nine vertices are distinct and its
closing edge 2--0 exists. Along this orientation the original values are

    1,0,1,0,2,1,0,1,2.

Therefore p=4, q=2, k=3. Subtraction of the unit circulation changes these
values to 0,2,0,2,1,0,2,0,1. It cancels four selected edges, introduces three,
and reverses the other two; the weight change is k-p=-1. At every cycle vertex
one incoming and one outgoing incidence are modified equally, so every
modular divergence is preserved. The support after subtraction is exactly

    2->0,2->5,3->4,3->17,6->1,6->8,
    9->10,9->11,12->13,12->14,16->7,16->15.

This is precisely the factor

    (0,2,5), (4,3,17), (1,6,8),
    (10,9,11), (13,12,14), (7,16,15).

Every consecutive edge is in the host; the eighteen vertex occurrences are
pairwise distinct and cover 0..17; the centered arc set equals the
computed updated arc set exactly. The updated types have six sources,
twelve leaves and no defects. The omitted source incidences 1--6 and 3--17
are real host edges used by this update but absent from the leaf-only auxiliary
graph. This identifies the lost information in the restricted test.

## 5. Fresh implementation and mutation pressure

`checker.py` is a new 244-line standard-library implementation. It imports no
old candidate code, C08 verifier, graph library, SAT solver or Lean module.
The unavailable R07 historical implementation is not reconstructed or claimed
recovered. C08 uses Boolean transitive closure and enumeration of edge subsets
for its matching calculation. This checker uses disjoint-set contraction,
cut-mask counting and bottom-up vertex-mask matching dynamic programming.
Elementary notions such as incidence and modular arithmetic are shared
mathematics, not an imported verification core. The trust domain is still the
same generator domain; this is not a separately staffed verification.

All nine corruptions run the same audit, with no digest rejection shortcut:
missing host edge; duplicate host edge; reversed 0->1; cycle vertex 6 replaced
by 8; first P3 center replaced by 1; invented auxiliary edge 1--4; omitted
interlacement-tree edge; claimed matching number 5; repeated cycle vertex.
Each must fail at its designated assertion. In particular the invented edge
is rejected because it is not an actual leaf-induced host edge, rather than
accepted as an augmenting edge. Full first-failure codes are in `stdout.json`.

## 6. General sufficient lemma, with all lifting cases

Let a finite simple cubic graph of order n=3k have a charged forest with one
defect. Write its exceptional arcs as a->a', a->b, c->c', c->b, b->d.
All other components are ordinary P3s. Build the typed auxiliary graph exactly
as in section 3. Its virtual matching M leaves just a',c',d exposed.

If a matching N is larger than M, the typed symmetric difference of M and N
has maximum degree two and decomposes into alternating paths and cycles.
Cycles contribute equally many edges from each matching. A path component
must have one extra N edge because |N|>|M|. It is a simple augmenting path;
both its endpoints are exposed by M and no internal vertex is exposed. This
argument also permits a real and virtual edge with the same endpoints: such
a parallel pair is an alternating two-cycle, never the required augmenting
path, and causes no identification of vertices on that path.

Lift each virtual edge l--r to the selected path l--x--r through its remembered
ordinary source. Path leaves are distinct; its virtual edges use distinct
sources; no such source belongs to the exceptional tree. Each real edge was
unselected since two leaves cannot support a selected arc. Consequently the
lift is a simple host path internally disjoint from the exceptional tree.
Join it to the unique exceptional-tree path between its two endpoints. The
union is a simple host cycle, including when there are zero virtual edges.

For t virtual edges, the lifted path has t selected incidences in each
orientation and t+1 unselected edges. The exceptional path a'--c' contributes
(2,2) selected orientation counts. Either path d--a' or d--c' contributes (2,1)
up to reversal. Thus the complete cycle has counts (t+2,t+2,t+1) or
(t+2,t+1,t+1), up to exchanging the first two. One circulation sign cancels
one more edge than it introduces, decreasing weight by exactly one.

To justify the final bridge, charge 2 and maximum degree three allow only
(out,in)=(2,0),(0,1),(1,2). Let their counts be c,l,b. Summing integer divergences
gives 2c-l-b=0; with c+l+b=n this yields c=n/3. Counting outgoing selected arcs
gives w=2n/3+b. The initial b=1 and a unit weight decrease therefore force b=0.
Every selected edge then joins a source with exactly two endpoints, so the
result is a spanning P3-factor. This proves sufficiency for all stated inputs,
not by extrapolating the single finite example. The maximum-matching case of
sections 3--4 excludes the converse 'maximum implies no repair'.

## 7. Execution, termination and remaining status

Run `python3 run_bounded.py` in this directory. It invokes
`python3 -I -S checker.py`, one worker, with CPU 25 seconds, wall 35 seconds,
address space 256 MiB, per-output-file limit 1 MiB and no core dumps. The actual
Python 3.13.5 execution exited 0; stderr was empty. Exact timestamps, elapsed
time, CPU usage, observed Linux peak RSS and all source/output hashes are in
`execution.json`. No Lean execution, elaboration or axiom report was produced.
The current runtime probe found no lean/lake/elan executable; that does not
change the separately recorded historical user review or pending Lean status.

Every cut loop is bounded by 2^17-1, every vertex-deletion loop by 172, the
matching DP by 2^11 states, the mutation list by nine. Union/find parent steps
terminate in finite equivalence classes. No unbounded search or background job
is needed. A single circulation preserves charges and decreases integer weight
by one; this is not a proof that every other charged forest has a decreasing
move. No induction, probability, asymptotic extrapolation, symmetry quotient,
minimum-order obstruction or graph-order census is asserted. The only symmetry
reduction in cut enumeration pairs complementary masks, exactly once via bit 0.

The primary source has a nine-cycle; earlier checkpoint references to a
seven-cycle are not the input for this audit. Historical source/raw-output
losses remain explicitly unresolved; this package supplies newly frozen data
and newly executed code, not those originals. Both
`obligation:opg46613-root` and `obligation:opg46613-divisible-two-factor` stay
open. No truth ledger, EvidenceLink, verifier registry or Result is modified.
