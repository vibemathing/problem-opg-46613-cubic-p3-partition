# ROOT-R07: a complete twelve-pattern interface for strict one-defect cycle descent

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root` in the existing admitted Attempt/Route/Graph.
This completes the cycle-repair interface left deliberately restricted in `source-aware-transits.md`. It is an exact theorem about strict single-cycle updates, not an assertion that such an update exists in every host. The companion infinite family shows that existence can fail even in the root domain.

## 1. Charged forest and conventions

Let G be finite, simple and cubic, and let x be a spanning F3 flow of divergence 2 whose selected support is a forest with one defect. Sources S have two outgoing selected edges; leaves L have one incoming selected edge. The unique defect b has two incoming selected edges and one outgoing selected edge. Its component T has arcs

    a->a', a->b, c->c', c->b, b->d.

All other components are ordinary P3s (l,x,r), directed from x toward l and r. A cycle update means adding a unit circulation around an oriented simple ambient cycle. The opposite nonzero update is obtained by reversing the cycle orientation. The cost is the number of previously unselected cycle edges minus the number of selected cycle edges traversed backwards.

Throughout, a route external to T may have an empty interior: a single unselected edge between two core ports is allowed. Otherwise all its internal vertices lie outside T. This also specifies the r=0 convention for the companion single-pass construction.

## 2. Exact incidence identity for every simple cycle

Fix an oriented simple cycle C, with no restriction on how it meets the forest components. Define:

- s: number of source vertices of C;
- r: number of traversed unselected edges arriving at a source;
- z: number of leaves of C whose two incident cycle edges are both unselected;
- h: number of cycle edges between b and sources;
- j: number of cycle edges between b and leaves;
- epsilon: 1 if C traverses d->b, and 0 otherwise.

If b is absent, h=j=epsilon=0. If b is present, (h,j) is (2,0) or (1,1).

Let K count the unselected cycle edges and Q the selected cycle edges traversed backwards. Then

    Q=s-r+epsilon,
    K=s+z+(j-h)/2,
    Delta weight = r+z+(j-h)/2-epsilon.

Proof of the first identity: a backwards selected edge ending at a source is exactly a selected arrival at that source. There are s arrivals in all and r of them use unselected edges. The only backwards selected edge not ending at a source is d->b.

For the second identity, let t be the number of unselected cycle-edge incidences at sources. There are 2s-t selected incidences at sources. Removing the h incidences ending at b and adding the j incidences supplied by b shows that 2s-t-h+j leaves use their selected edge. Each such leaf has one unselected cycle incidence, while the z other cycle leaves have two. The total number of unselected incidences at all vertices is therefore

    t+(2s-t-h+j)+2z = 2s-h+j+2z.

Vertex b has no unselected incident edge. Divide by two to obtain K. Subtracting the first identity proves the cost formula.

Consequently a strictly decreasing cycle must contain b and satisfy r=z=0. If its two b-edges both lead to sources, these conditions suffice for cost -1. If one b-edge leads to d, it must additionally traverse d->b. There is no strict decrease larger than one.

This identity does not assume that unselected edges have particular endpoint types, nor that an ordinary component is visited only once.

## 3. Why ordinary components cannot be revisited in an improving cycle

For a decreasing cycle r=z=0. Every visited leaf must use its unique selected incident edge. Its selected neighbor is therefore also visited. A visited ordinary source cannot receive the traversal through an unselected edge, because r=0. Thus the cycle enters that source from a selected leaf and exits either through its unselected third edge or through its other selected edge to the other leaf.

It follows that the intersection with each ordinary P3 is exactly one of

    l->x, l->x->r, r->x, r->x->l.

It is connected and consists of selected edges. A second disjoint visit to that same ordinary component would require a leaf whose selected source-edge is missing, contradicting z=0, or would repeat its source, contradicting simplicity of C. Therefore every ordinary component is used at most once.

This necessary fact upgrades the component-distinctness condition of the companion search from an imposed restriction to a consequence for all strict repairs. The exceptional tree T can still be visited twice; that is the only additional possibility.

## 4. The eight one-piece core patterns

If C meets T in a single selected path, that path must contain two reversed edges. Its ordered endpoints are exactly

    (a',c), (a',c'), (c',a), (c',a'),
    (d,a), (d,a'), (d,c), (d,c').

These are the eight entries equal to two in the companion port table. Close the specified directed core path by an external route from its exit back to its entry. Every ordinary component on that route must have one of the four directed shapes in Section 3. Components cannot repeat. These conditions are both necessary and sufficient: with t ordinary components, there are t+1 unselected edges and t+2 reversed selected edges.

An external route may be one direct unselected edge between core ports. Such a cycle is included, not lost by requiring a nonempty external interior.

## 5. Exactly four two-piece core patterns

If C uses a-b and b-c, both sources a,c are already on the selected core path. Any unvisited core leaf cannot occur separately, since z=0. Thus this case has only one core piece.

Suppose instead C uses b-d and b-sigma, where {sigma,tau}={a,c}. Its direction at b must be d->b->sigma. The main selected core piece is either

    P = d->b->sigma,

or

    P = d->b->sigma->sigma'.

The other source tau either does not occur, giving Section 4, or occurs with its leaf in the separate directed selected piece

    Q = tau'->tau.

There is no further core vertex that can occur separately: its unique selected edge would be missing. Thus the two choices of sigma and the two choices of the main endpoint give exactly four two-piece patterns.

Let v be the endpoint of P, so v is sigma or sigma'. To form a single oriented cycle from these two pieces, the external routes must connect

    v -> tau'  and  tau -> d.

The two routes have disjoint interiors, avoid T internally, and use distinct ordinary components globally. Each ordinary traversal has a shape from Section 3. These conditions are sufficient: if the routes together use t ordinary components, there are t+2 unselected edges, while P and Q supply three reversed edges and the ordinary pieces supply t more. The cost is -1.

They are also necessary. The cyclic order after the end of P must next reach the beginning of Q and then return from the end of Q to the beginning of P. Connecting each piece back to itself would yield two cycles, not the simple cycle under consideration. The incidence identity and Section 3 force all remaining route conditions.

## 6. Complete finite criterion

A one-defect charged spanning forest admits a strictly decreasing simple-cycle update if and only if at least one of the following has a certificate:

- one of the eight one-route conditions in Section 4;
- one of the four disjoint-two-route conditions in Section 5.

The certificate names the core pattern, actual unselected route edges, and the ordered component transits. A checker checks distinct vertices and components, reconstructs the single simple cycle, and checks its divergence-preserving update and cost -1. The resulting weight is 2n/3 and therefore the result is a P3-factor.

All possible certificates can be searched finitely because every ordinary component is visited at most once. For the two-route cases, the visited-component set must be shared between the two searches. Ordinary directed reachability without this condition, or two individually successful paths that intersect, is not a sufficient certificate. No polynomial-time bound is asserted.

A complete failure of these twelve tests is an exact certificate of absence of a strictly improving simple cycle for this specified charged forest. It is not a no-P3-factor certificate. The graphs G_q in the companion `cycle-local-minimum-family.md` fail all twelve tests initially yet have an explicit neutral-six-cycle then decreasing-seven-cycle repair and explicit P3-factors.

## 7. Dependencies and open question

The proof uses only the local divergence classification, the one-defect forest shape, and incidence counting. Its output is a complete local/route interface rather than a global existence theorem. It adds the two-piece cases that the earlier single-pass file did not claim to cover, while proving that repeated ordinary-component visits cannot be part of a strict repair.

The next unresolved issue is how neutral updates change these twelve tests, and whether a larger invariant can control neutral plateaux for arbitrary positive-defect forests. The homogeneous-layer secondary-potential lemma is one verified-in-prose candidate case, not a proof of global termination at zero defect. No mathematical verifier receipt or admission is asserted, and both canonical obligations remain open.
