# X3 physical existence: terminal cofactors and a bounded-chord theorem

Status: NONTERMINAL_CHECKPOINT. Verdict: candidate_only.
Primary owner: math-proof. All computation is in the generation trust domain.
Repository: vibemathing/problem-opg-46613-cubic-p3-partition.
Base: f800cab61f4047fba97a0e336c8feb282ec6662f (after completing PR29).
No root closure, trusted attestation, Lean elaboration or axiom report is claimed.

## 1. Scope and first gap

G is finite, simple, triangle-free, cubic and 3-vertex-connected. A supplied
perfect matching M has complementary cycles C0,C1,C2, all of order 2 modulo3.
Hence |G| is a positive multiple of6. P3 means two selected edges on three
distinct vertices, not a requirement that the ambient path be induced.
Internal matching chords are never erased from a host or local cofactor test.

PR28's physical role/gap iff and PR29's kappa=t+b+3u are reused. Under the
hypothetical GLOBAL minimum kappa*=3, a two-cross-edge quotient-tree state can
be chosen with two owners, a loop at each and three parallel demand units.
The target is an actual simultaneous exchange giving kappa<3. A positive local
value3 in a graph already having a factor is not evidence for kappa*=3.

The new theorem below excludes X3 (indeed gives a full factor) whenever a
mixed-target complementary circle has at most THREE internal M chords. Circle
length is unbounded. Its proof combines an exhaustive finite certificate with
an explicit three-subdivision lifting argument, not finite-order extrapolation.
The existence step for arbitrary internal chord count remains OPEN. No general
three-circle or root conclusion is asserted.

Document-local DAG, not newly admitted obligation IDs:
finite terminal certificates + subdivision lifting -> bounded-chord terminal
connectivity -> different-target cofactor gluing -> P3-factor for this subclass.
OPEN: force such a cofactor, or a different strict exchange, in the remaining
hypothetical X3 hosts. Existing X2, root and trusted-closure gaps remain open.

## 2. Terminal relation and exact physical gluing

For a circle C, let B contain C and ALL M edges with both ends on C. Let P be
its vertices incident with M edges leaving C (the ports). Define Gamma(B) on P
by pq in E(Gamma) iff B-{p,q} has a P3-factor. It is a relation of explicit
spanning partitions, not just endpoint distance or a scalar congruence.

If p,q have M partners in DIFFERENT other complementary circles, a cofactor
of B-{p,q} gives a factor of the whole host. Keep the local cofactor. At the
partner w of p, choose either F-neighbor z, and take (p,w,z), centered at w.
Deleting the consecutive pair w,z from that outside circle leaves a path of
order L-2 divisible by3; tile it consecutively. Do the same for q on the third
circle. These vertex sets are disjoint, and every vertex is covered once.
All used edges belong to the unchanged G. Unused internal/external M edges are
still host edges; they simply are not selected by the factor. There is no need
for a matching edge directly between the two outside circles.

Restriction is exact for this gluing family: a factor with these two cross
P3s and no other selected edge between C and the outside leaves precisely a
P3-factor of B-{p,q}. This is not a claim that every possible host factor has
this restricted shape. The unrestricted fixed-M iff is still the earlier one.

Color each port of a circle by which of the other two circles contains its M
partner. If both colors occur and Gamma(B) is connected, a path between the
colors has a differently colored edge. The previous construction applies.
Thus a connected terminal relation on ANY mixed-target circle suffices.
Every connected three-vertex quotient has a mixed-target vertex: all vertices
in a triangle quotient, or the middle vertex in a path quotient. Parallel
cross edges and internal quotient loops cause no change to this observation.

## 3. Three-subdivision cofactor lifting

Replace a graph edge uv by u-a-b-c-v, with three new vertices. Fix two OLD
vertices as deleted holes and take any P3-factor after their deletion.

If uv is unused (including an edge incident with a deleted endpoint), retain
every old P3 and add (a,b,c). If uv is selected and its old component is
(w,u,v), replace it by (w,u,a) and (b,c,v). If its old component is (u,v,w),
replace it by (u,a,b) and (c,v,w). These are all possibilities: a selected edge
lies in exactly one P3 and either endpoint is its center. All new selected
edges exist and the replacements cover exactly the old component plus a,b,c.
This is an explicit one-way lift for fixed old holes, sufficient below.
No converse for arbitrary subdivisions or arbitrary local interfaces is used.

Now take a port run between consecutive internal-chord endpoints on C. If it
has r>0 vertices, retain r' in {1,2,3} with r'=r modulo3; if r=0 retain zero.
The removed vertices are restored in groups of three by edge subdivision.
Chord endpoints, their matching, and all cyclic orders are retained. A chord
cannot become a circle edge: that would require two consecutive endpoints and
a zero run, already a duplicate edge in the original B. The compressed B' is
simple, but it may contain a triangle. This is permitted in the FINITE LOCAL
certificate domain. B' is not asserted cubic or 3-connected and is never used
as an inductive root instance. G itself is not contracted or changed.

For k internal chords there are 2k endpoint gaps, each with at most3 retained
ports, so |B'|<=8k. Its order is still2 modulo3 and it retains at least one port
whenever B had one. Every Gamma(B') edge lifts through the explicit subdivision
construction with the same two old holes.

Each restored port run attaches its NEW ports to a retained port by consecutive
port pairs. Any adjacent pair on a circle of order2 modulo3 is deletable using
the rest of the circle alone. Hence Gamma(B) contains a path along each such
run. Consequently connected Gamma(B') implies connected Gamma(B), including
all new ports, regardless of how their outside-target colors are distributed.
This completes the unbounded-run induction: each step restores exactly three
vertices and there are finitely many such steps. For k=0, Gamma contains the
whole circle on its ports and is connected directly.

## 4. Finite base certificates: k<=3, every pairing and every run word

For each k=1,2,3 enumerate all perfect pairings of the 2k ordered chord
endpoints and all run words in {0,1,2,3}^{2k}. Build the labeled circle in that
cyclic order. Keep exactly cases of order at least3 and 2 modulo3, with at least
one port, and with no chord duplicating a circle edge. Do NOT filter out
triangles: the compression proof needs those bases too.

The complete domain has:

|Internal chords|Valid compressed cases|
|---|---:|
|1|3|
|2|181|
|3|15060|
|Total|15244|

The generator performs direct P3 exact cover only when needed to connect the
terminal relation. Circle-only pair edges have distance1 modulo3; both arcs
then have internal order divisible by3 and an explicit consecutive partition.
They need no stored search proof. The certificate lists1693 additional pair
cofactors in1373 exceptional cases. Each entry contains the entire P3 partition
of B'-{p,q}, including centers. exceptions.b85 is a bounded lossless encoding:
encoded14323 bytes, decoded93637 bytes;
encoded SHA256 1d0f44d20ca4df0c9b5ff0eb373d294160a2947934e273e10beb152192b259a5;
decoded SHA256 4b2c63241909046582e266cd7b388819755a5cada8a22b92c3fa9cf1ad5abd76.

case_check.py imports no producer and performs no cofactor search. It separately
enumerates symmetric partner arrays and all run words, rebuilds a Boolean
adjacency matrix, validates every circle-only cofactor and every stored extra
cofactor, and merges the terminal components. A missing exception must still
pass connectivity; duplicate/out-of-domain entries fail. It checks every
ordered pair of selected path edges, deleted holes, disjointness and full
coverage. All15244 cases pass; 12 semantic mutations reject. The finite
certificate plus Section3 proves the candidate bounded-CHORD theorem for ALL
circle lengths. It does not certify k=4 or any larger chord count.

## 5. Consequences for hypothetical X3 hosts

Combining Sections2-4 gives the candidate theorem:
If any mixed-target circle has at most3 internal matching chords, the original
three-222 host has a P3-factor. This conclusion imposes no cost-three limit:
the middle cofactor may use all its internal chords, in addition to two cross
matching edges. G42's previously known cost-four requirement is not contradicted.
No old G24/G42 subset census has been run here.

Thus every mixed-target circle in a hypothetical kappa*=3 host has k>=4.
There is also a direct unbounded-chord condition: three consecutive ports make
the circle-only terminal relation connected. Their adjacent pairs connect them,
and any other port has circle-distance1 modulo3 to one of these three. Hence
no mixed-target circle of a hypothetical X3 host has three consecutive ports.
For k>0 its port count therefore satisfies p<=4k, by counting at most2 ports
in each of the 2k endpoint gaps. This is a necessary restriction, not sufficient
for infeasibility.

A useful size consequence concerns X3 ONLY. If the quotient is a triangle, all
three circles are mixed and have k>=4. Each also has at least3 cross edges by
3-connectivity, so its length is at least11. The total is an even multiple of3,
and therefore at least36.

If the quotient is a path, let L be its middle circle length. Its two leaf
circles have at least3 incident cross edges each; hence its port count is at
least6. With k>=4, L cannot be5,8 or11. If L=14, its port count is at most6;
both leaf cuts must equal3. A triangle-free five-circle has no internal chord
and cut5. An eight-circle has even cut, thus cut at least4. So both leaves have
length at least11, giving total at least36. If L=17, its port count is at most9;
two five-circle leaves would need10 ports, so at least one leaf has length at
least8, giving total at least30. If L>=20, the two leaves have total length at
least10, again giving total at least30. Thus hypothetical X3 hosts have order
at least30 (at least36 in the triangle-quotient case). This does NOT give a lower bound30 for a general root counterexample whose
chosen complement need not have spectrum222, and does NOT prove the root
through order24. No general X2 existence assertion follows.

## 6. Small exact failure of the INTERNAL-pair family, not of X3

A new positive18-vertex control has circles0..4,5..9,10..17 and matching

(0,5),(1,6),(2,11),(3,14),(4,16),(7,12),(8,15),(9,17),(10,13).

Its complete27-edge table is in physical-certificates.json. The only internal
matching chord anywhere is(10,13). Deleting its endpoints from its LOCAL block
leaves components{11,12} and{14,15,16,17}, neither divisible by3. Thus all choices
in the narrow removable-internal-pair family fail: there is only this one pair.
This is a complete component-order nonexistence certificate, not a heuristic
failure to find a partition. The outside target graph is a triangle, so absence
of the opposite cross edge is not the reason for failure.

The whole graph has factor
(0,1,2),(3,4,16),(5,6,7),(8,9,17),(10,11,12),(13,14,15),
with middle entries centers. Its global minimum is zero. The object only
excludes domain-assumptions-alone => removable internal pair; it CANNOT
contradict that implication with the additional hypothetical kappa*=3 premise.
It is minimum order for this restricted-family failure among eligible three-222
hosts: every triangle-free residue2 circle has at least5 vertices, the total is
at least15, and an eligible even multiple of3 is consequently at least18.
No minimality claim about X3 or root counterexamples is made.

The new24-vertex physical gluing control has middle circle0..10, outside
circles11..15 and16..23, and matching
(0,3),(1,11),(2,12),(4,16),(5,8),(6,17),(7,18),(9,19),
(10,13),(14,21),(15,22),(20,23).
The local cofactor after deleting ports1,4 is
(0,3,2),(8,9,10),(5,6,7).
It uses internal chord(0,3), whereas the circle-only deletion at distance3
fails. Section2 gives the full factor recorded in the certificate.
These new G18/H24 are not the old R07 object or G24 control.

## 7. Exact simultaneous exchange checks and actual execution

The physical generator and consumer use separate cores. The consumer imports
no producer or old verifier. It regenerates each gap by successor walking,
computes exact slot-owner rank by owner-mask DP, checks center/leaf roles from
the full factor, and replays each retained match and alternating path. No
assumption is made that intermediate one-edge steps decrease the potential.

|New host|Selected indices, sorted matching|kappa|Delta s|Delta D|lost l|augment a|
|---|---|---|---:|---:|---:|---:|
|G18|{2,7}->{4,7}|3->0|0|-3|1|1|
|H24|{1,3}->{0,1,3}|3->0|1|-2|2|3|

Both have Delta u=0 and strict margin3 in
2(a-l) > Delta s+Delta D+3Delta u.
Complete cyclic paths, r demands, maximum slot matches and augmentation walks
are stored. The old matches are retained ONLY by whole physical-gap identity;
several changed endpoints are never treated as independent old-gap splits.
The consumer checks simplicity, cubicity, triangle-freeness, supplied M and
three-222 complement, all172/301 vertex-deletion sets, both spanning factors,
the unique internal-pair failure, six subdivision cases, and15 additional
physical mutations. These are27 semantic mutations together with Section4,
not fingerprint-only rejection tests.

Four FINAL bounded stages actually exited0 with empty stderr. execution.json
records actual Python3.13.5 identity, interpreter/source/input/output digests,
UTC start times and observed wall times. CPU limits are28,28,20,25 seconds;
wall limit35 seconds per stage; address-space caps512,512,256,512 MiB; each
output file cap2 MiB; one worker/thread. run_bounded.py replays only this new
package. Resource errors are errors, never negative mathematical certificates.
A provisional physical summary variable-shadowing error was corrected before
the final replay and is explicitly recorded in development-note.json. It was
not a theorem failure or a trusted receipt. No performance or source hashes
from an unperformed execution are substituted.

## 8. Open physical obligation and verification ceiling

The first open step is to exclude hypothetical X3 hosts in which EVERY
mixed-target circle has at least4 internal chords and lacks the easy terminal
configurations. Either prove the full terminal relation is connected in the
appropriate physical cut structure, force a removable internal pair with its
opposite cross edge, or construct another simultaneous exchange with
u'=0,D'=s',t'=b'<=1. Menger connectivity alone has not been proved to control
the required cofactor or residues, and is not cited as if it did.

No graph with min_S kappa>0 was found here. The negative certificate in Section6
is local and explicitly coexists with a full positive factor. Neither a general
X3 failure certificate nor a proof of kappa*=0 for all three-circle hosts is
present. Accordingly no arbitrary-number-of-cycles promotion is attempted.
Trusted replay, statement-faithfulness, axiom audit and obligation-closure gates
remain unexecuted. A request is provided, not a self-signed EvidenceLink.

PR29 completed the prior global-min transport; its original bytes were not
reuploaded. The previous local X3-r01 archive and the orphan exchange-r02 remain
separately identified in the checkpoint, not silently marked merged. This new
R02 candidate has its own single packet and immutable namespace.
