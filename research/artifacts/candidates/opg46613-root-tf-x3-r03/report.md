# X3-R03: physical ear elimination and the four-chord crossing cores

Status: NONTERMINAL_CHECKPOINT. Verdict: candidate_only.
Primary owner: math-proof. Trust domain: web-candidate-generation.
Repository: vibemathing/problem-opg-46613-cubic-p3-partition.
Frozen source/base: 091dafa259e69e789338870ce36e9375f002c271.
No general X3/X2/root closure or trusted mathematical attestation is asserted.

## 1. Frozen objective and dependency boundary

The host G is finite, simple, triangle-free, cubic and 3-vertex-connected.
A supplied perfect matching M has complement C0,C1,C2, all with order 2 modulo
3. The total order is therefore a positive multiple of six. P3 means a selected
two-edge path on three distinct vertices, not an induced-path restriction.

For B=C plus ALL its internal M chords, let P be its genuine external-matching
ports. Define Gamma(B) on P by pq in Gamma iff B-{p,q} has a spanning P3-factor.
The required crossing edge is an edge of THIS COFACTOR RELATION between the two
outside-target color classes. It is not a host M edge between external ports:
a genuine port's M partner is, by definition, outside B.

The prior exact gap system and kappa=t+b+3u are reused from PR28/29. The terminal
cofactor gluing and the simple-local at-most-three-chord theorem are reused
from PR30, report SHA-256
161b844d7f79a2d97c317639073db9dd600e1ddd72dff8c8ad704feb7c59a398.
Their old finite censuses and G24/G42/G60/H42 are NOT rerun.

New dependency chain, local labels only (not new admitted record IDs):
E: constructive physical ear lifting;
N: noncrossing matching chords -> connected Gamma by induction on chord count;
K4: complete finite certificates for seven irreducible four-chord diagrams;
T4: prior three-chord result + E + K4 -> triangle-free four-chord theorem;
R: repeated E -> an unresolved X3 circle has an irreducible core of at least
five chords, or an open alternative exchange must be used.
General existence on those cores remains OPEN. No root-domain induction is
performed on a compressed local block.

## 2. Three exact terminal-connectivity operations

Throughout, C is a simple cycle of order 2 modulo 3, H is a matching of chords
not duplicating cycle edges, B=C+H, and P consists of vertices not incident with
H. Assume P is nonempty; a singleton relation is connected by convention.

### 2.1 Three consecutive ports

Deleting two cycle vertices at circular distance 1 modulo 3 leaves two paths
whose orders are both divisible by three. Tile each consecutively. If three
ports are consecutive, their adjacent pairs connect them, and every other
port has distance 1 modulo 3 to one of these three in their cyclic order.
Hence Gamma is connected using the cycle alone. Extra H edges remain in B;
they are unused, not removed from the host.

### 2.2 A triangular port ear

Suppose u,p,v are consecutive on C, p is a port, and uv is a chord. B-p contains
the Hamilton cycle obtained by bypassing p along uv. For EVERY other port q,
deleting q from that cycle leaves a Hamilton path of order |C|-2, divisible by
three. Its consecutive triples certify pq in Gamma. Thus p is the center of a
terminal-relation star. This operation is used in LOCAL intermediate blocks;
it is not a claim that the original triangle-free host contains a triangle.

### 2.3 A quadrilateral port ear: the central lifting lemma

Suppose the cyclic order contains a,u,p,q,v,b, the only H edge incident with
these four ear vertices is uv, and p,q are ports. The outside vertices a,b are
distinct. Replace u,p,q,v by a single new port z between a,b, remove the one
chord uv, and keep every other chord and vertex. The new local block B' has
order |B|-3, one fewer chord and port set (P-{p,q}) union {z}. The implementation
uses the old label u for z but keeps the four original physical vertices in
its lifting record.

Every cofactor with two OLD outside holes lifts. Only the triple containing z
changes. These are all possible roles, since z has only neighbors a,b:

| old triple | replacement triples in B |
| --- | --- |
| (a,z,b), center z | (a,u,p), (q,v,b) |
| (c,a,z), center a | (c,a,u), (p,q,v) |
| (c,b,z), center b | (c,b,v), (u,p,q) |

Endpoint order reversal gives the same selected paths. Every new edge is a
cycle edge, and the replacements cover exactly the old triple plus three new
vertices. All other triples and both old holes are unchanged. If an attachment
is itself a hole, only the rows compatible with the actual old cofactor can
occur; no missing attachment is silently used.

If the cofactor holes in B' are z and x, keep its whole partition and instead
use holes p,x in B, adding (u,v,q), centered at v. Alternatively use holes q,x
and add (p,u,v), centered at u. These triples use the REAL chord uv. Finally
pq itself is an edge of Gamma(B), since p,q are adjacent on C.

Therefore connected Gamma(B') implies connected Gamma(B). More explicitly,
map every relation edge z-x to p-x, lift every other relation edge as above,
and append pq. A spanning tree on the smaller terminal set becomes a spanning
tree on the old terminal set. This also covers a singleton smaller port set.
The proof preserves actual partitions and does not assume any converse of
this local simplification.

The exceptional cycle order five needs no illegal two-cycle contraction:
an ear u,p,q,v then leaves a single outside port a=b, and u,a,v is a triangular
port ear, already covered by 2.2. All genuine contractions thus have |C|>=8
and leave a simple cycle of order at least five.

## 3. Unbounded noncrossing theorem and termination

Two matching chords cross when their four endpoints alternate around C.
A nonempty noncrossing chord diagram has two matched consecutive endpoints
in the cyclic ENDPOINT word: take an innermost paired arc; all endpoints in
its interior must be paired within that interior, so an interior pair would
contradict innermost choice. The physical arc between this consecutive pair
therefore consists entirely of ports.

Let r be the number of those ports. r=0 would duplicate a cycle edge and is
excluded by simplicity. For r=1 use 2.2. For r>=3 use 2.1. For r=2 apply 2.3.
Deleting that pair of endpoints keeps all other endpoints in the same cyclic
order, so noncrossing is preserved. The chord count strictly decreases.

Induct on the NONNEGATIVE INTEGER number of chords. The zero-chord base has all
vertices as ports, and adjacent-pair cofactors connect them around C. The
previous paragraph either proves terminal connectivity directly or invokes
the induction hypothesis at one fewer chord and lifts it by 2.3. This is a
finite terminating construction, valid for arbitrary chord count and cycle
length. Local triangles are allowed in this theorem; every such ear is handled
by its actual spanning path construction, not a triangle-free hypothesis.

Consequently, ANY mixed-target complementary circle with a noncrossing internal
matching yields a full host P3-factor by the prior cofactor gluing. This is an
unbounded structural subclass, not extrapolation from the samples below.
The sampled noncrossing blocks are only implementation pressure tests.

## 4. Four arbitrary chords: complete crossing-core certificate

Now assume the original local B is triangle-free and has exactly FOUR chords.
If a run of ports has length at least three, use 2.1. Otherwise every endpoint
run has length 0,1 or 2. If two matched endpoints are consecutive in the endpoint
word, their run cannot be zero (duplicate edge) or one (triangle), so it is two.
Operation 2.3 leaves three chords. The existing PR30 theorem applies to that
simple local block EVEN IF the operation creates a triangle, and the cofactor
partitions lift. That prior three-chord result is explicitly a dependency.

The only remaining diagrams have no consecutive matched endpoint pair. There
are 31 labeled pairings on eight ordered endpoints, in seven dihedral orbits.
Canonical representatives, with endpoints 0,...,7 in circular order, are:

A: 02,13,46,57
B: 02,14,36,57
C: 02,15,36,47
D: 02,15,37,46
E: 03,15,26,47
F: 03,16,25,47
G: 04,15,26,37

Every rotation or reflection permutes the eight run entries, so enumerating
ALL run words in {0,1,2}^8 for each representative covers each physical pairing
and every port placement. Keep a nonzero run sum divisible by three and reject
triangles by the full adjacency matrix. No connectivity hypothesis is imposed
on these finite local blocks. Their orders are 11,14,17,20 or23.

| core | valid triangle-free cases | exception cases | extra cofactors |
| --- | ---: | ---: | ---: |
| A | 1452 | 524 | 692 |
| B | 1728 | 611 | 797 |
| C | 1944 | 703 | 908 |
| D | 1728 | 614 | 800 |
| E | 2186 | 804 | 1028 |
| F | 2186 | 804 | 1028 |
| G | 2186 | 804 | 1028 |
| total | 13410 | 4864 | 6281 |

All 13410 relation graphs are connected. A generator searches only for additional
cofactors needed beyond the circle-only relation. Each of 6281 extra certificates
stores the holes and every P3 using a non-circle chord. The other vertices are
uniquely completed by consecutive triples on the remaining physical C paths.
check.py rebuilds those ENTIRE partitions and checks graph edges, centers,
distinctness, both holes, disjointness and spanning coverage. It imports no
producer and performs no cofactor search. It separately enumerates involutions,
dihedral representatives and all run words, verifies the domain counts, checks
every extra cofactor, and rejects missing/out-of-domain/duplicate certificates.
The format is a lossless description of full positive partitions, not an
unverified truth table or a solver assertion.

These cases, 2.1, 2.3 and the explicit old three-chord dependency prove the NEW
candidate theorem: every triangle-free local circle with at most four internal
matching chords has connected terminal relation, at arbitrary original length.
The finite-to-general bridge uses the proved long-run case and the complete
endpoint-order split; it does not claim that finite order checks prove an
unbounded chord-count assertion.

## 5. Why the triangle-free qualifier cannot be silently removed

The broader four-chord LOCAL claim allowing triangles is false. On the cycle
0,...,10,0 take chords 02,13,57,68. Ports are 4,9,10. The relation has only edge
9-10, with cofactor (0,1,2),(3,4,5),(6,7,8).

Deleting 4,9 leaves components {0,1,2,3,10} and {5,6,7,8}, of orders five and
four. Deleting 4,10 leaves {0,1,2,3} and {5,6,7,8,9}, of orders four and five.
Neither deletion has a P3-factor. These are complete component-order negative
certificates, not an incomplete exact-cover run. The consumer checks every
listed component boundary and the positive cofactor.

This is the minimum possible local order with four matching chords, at least
one port, and order2 modulo3: eight chord endpoints require a positive port
count divisible by three. It is NOT a minimum eligible host counterexample.
It has triangles and the port-free vertex set {0,1,2,3} has edge boundary two.
It cannot be a local block of a 3-connected cubic host with exactly those ports.
The initial broad-core test found this object; the corrected final theorem
retains triangle-freeness. No claim under the hypothetical kappa*=3 assumption
is withdrawn or contradicted by this ineligible local object.

## 6. Real cut constraint and the remaining irreducible X3 core

In a cubic simple 3-vertex-connected host every proper edge cut has size at
least three. For a direct proof, a one-vertex side has boundary three and a
two-vertex side has boundary at least four. If both sides have at least three
vertices, a cut of size at most two has at most two endpoint vertices on either
side; deleting those endpoints on one side leaves nonempty sets on both sides
disconnected, contrary to 3-vertex-connectivity.

A nonempty consecutive interval of a complementary circle with no external
port therefore has an internal M chord leaving it: otherwise its two boundary
circle edges form a forbidden two-edge cut. This is the concrete cut consequence
used here; no Menger path is presumed to have a prescribed residue.

Repeated quadrilateral-ear elimination preserves this necessary interval
condition. A port-free interval in the smaller circle avoids its new port z,
so it consists only of unchanged old vertices and maps to the same physical
interval, with the same cut size in the original host. All remaining internal
M chords are retained; the removed ear chord has both ends outside that interval.

If a quadrilateral contraction from a triangle-free block creates a triangle,
it contains the NEW port z and its two attachments, joined by an old chord.
Operation2.2 immediately proves terminal connectivity, and the proof lifts
back. Thus along any still-unresolved elimination sequence the local block
remains triangle-free. The number of chords strictly falls at each step.

It follows that an unresolved mixed-target X3 circle can be reduced only to a
core with at least FIVE chords, no paired consecutive endpoints, no run of
three ports, and the port-free-interval escape condition above. Otherwise the
four-chord or noncrossing argument supplies the factor. This statement does
NOT promote the simplified local core to a cubic/3-connected root instance.

There is also a color interpretation: adjacent ear ports p,q must have the
same outside-target color in a hypothetical X3 host, since their adjacent-pair
cofactor already gives a full factor if their colors differ. Contract them to
one port of that color. Both original nonempty colors remain present. Relation
edges and cofactors produced in the smaller block then lift to real ports of
the same target colors in the original host before any global gluing occurs.

In the triangle quotient, every circle is mixed and therefore has at least five
internal matching chords. Together with at least three cross edges, its order
is at least14 (the next possible order2 modulo3 above13). Hence a hypothetical
X3 triangle-quotient host has order at least42. This is an X3/spectrum222 bound,
not a general root bound. The prior path-quotient lower bound30 is not improved.

OPEN: prove a cross-color cofactor or another strict exchange for the remaining
five-or-more-chord cores with their physical cut constraints. Neither the cut
condition nor the seven four-chord cases supply that implication. General X3,
X2, and root remain open; no arbitrary-number-of-cycles promotion is made.

## 7. Two NEW physical 48-vertex exchanges, including five selected M edges

physical-certificates.json freezes every edge, matching edge, circle order,
local cofactor, whole factor, gap, owner and augmentation. Both hosts have
complementary cycles0..13,14..30,31..47; they are not any prior G24/G42/G60/H42.

Q48-noncrossing has local chords 03,4-12,5-10,6-9. A quadrilateral ear0,1,2,3
reduces it to a three-chord local block, and its lifted cofactor with holes1,13
is (4,5,6),(7,8,9),(10,11,12),(0,3,2). Its pure-circle relation isolates port13,
so the displayed bridge genuinely uses the chorded ear lifting.

R48-interlaced-core4 uses diagramA with runs(0,1,0,0,0,1,2,2). Its local chords
are03,14,58,6-11 and its cofactor with holes2,7 is
(5,8,9),(6,11,10),(1,4,3),(12,13,0).
This certificate uses three internal matching chords. After the two outside
cross P3s are added, the displayed full factor uses FIVE matching edges.
No minimum matching-cost claim about this positive host is made.

The complete sorted matchings and sixteen-path partitions are in the JSON.
For both, each outside partner is a B center joined to its C successor, and the
remaining fifteen outside vertices are tiled in consecutive triples. The host
is unchanged throughout. The checker verifies all72 edges, perfect matching,
complement, simplicity, cubicity, triangle-freeness, and ALL1177 deletion sets
of at most two vertices for each host. Both are positive root instances.

| host | old selected indices | new selected indices | Delta s | Delta D | loss ell | augment a | kappa |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Q48 | 1,9 | 0,1,9 | 1 | -2 | 2 | 3 | 3->0 |
| R48 | 2,5 | 1,2,3,4,5 | 3 | 0 | 2 | 5 | 3->0 |

Delta u is zero. For Q48,2(a-ell)=2>-1=Delta s+Delta D. For R48,6>3.
The strict margin is three in both cases. No intermediate toggle monotonicity
is assumed. EVERY changed activity order and gap is rebuilt, and a retained
old match requires the same full circle path, unit label, owners and surviving
matched owner. The two losses are checked, not guessed from selected-edge count.
The consumer recomputes rank by owner-mask DP and separately verifies t,b,u.
At the new endpoint all components are unicyclic and u=0. A/B roles are read
from the whole actual factor and checked against every exact gap equation.

## 8. Actual bounded execution, limitations and requests

Three FINAL stages (core4.py,produce.py,check.py) ran with Python3.13.5. Each
exited0 with empty stderr. Effective limits: CPU25 seconds, wall35 seconds,
address-space512 MiB, each output file2 MiB, one worker/thread. Their observed
wall times were1.370984,0.216179,7.091941 seconds. execution.json records exact
source/interpreter/input-output identities, UTC starts, caps and exits.

Thirty additional fixed noncrossing blocks with4,5,6,8,12 chords check the
constructed terminal spanning trees and contraction records. The general
noncrossing theorem is proved by the explicit induction, not those samples.
Nineteen semantic mutations reject: deleted host chord, changed center/vertex,
repeated factor component, circle order, fake M edge, gap demand/path/owner,
ignored loss, fake retained pair, truncated augmentation, incorrect A/B role,
independently added insertion cost, wrong selected set, missing cofactor bridge,
cofactor using a hole, false noncrossing label, and incomplete negative components.
Reversing P3 ENDPOINT order alone is legal and is not treated as a mutation.

The generator's initial overly broad four-chord local statement was rejected
by the explicit eleven-vertex object in Section5. It was not a root theorem
failure or an excuse to erase the host-domain constraints. The final finite
domain is triangle-free; the proof explicitly audits that distinction.

All executions remain in the SAME generation trust domain. A different checker
implementation is not a trusted verifier. No Lean elaboration, axiom audit,
statement-faithfulness attestation, EvidenceLink, Result, Solution or root closure
has been produced. The registered capability owners are named only in a pending
verifier/formalization request. Transport CI checks only candidate structure.

Historical X3-r01 and orphan exchange-r02 transport is untouched, as requested.
This new namespace has one packet. The next atomic task is the irreducible
five-or-more-chord, mixed-color cofactor/strict-exchange implication, retaining
all internal chords and exact simultaneous gap accounting.
