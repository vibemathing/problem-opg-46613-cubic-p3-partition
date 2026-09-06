# ROOT-R07: the exact source-aware single-pass criterion

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root`, under the existing admitted Attempt/Route/Graph.
Dependency: ROOT-R06 charged-flow identities and the companion `one-defect-repair.md` for the notation of the exceptional six-vertex tree. No global descent or root closure is claimed.

## 1. The cycle class being characterized

Let a charged spanning forest have exactly one defect, with exceptional tree T and selected arcs

    a->a', a->b, c->c', c->b, b->d.

Every other component is an ordinary P3, directed from its source x to its leaves l,r. A single-pass cycle means a simple ambient cycle obtained by using one selected path in T, one selected path in each of some distinct ordinary components, and unselected edges between consecutive components. All components visited are distinct; in particular an ordinary component cannot be used twice. The cycle may use an ordinary source's third, unselected incident edge.

This definition is deliberate. The theorem below does not characterize all simple ambient cycles and does not turn unrestricted reachability walks into simple cycles.

For a traversal of a selected path, call an edge reversed if it is traversed against its selected direction. With a fixed cycle orientation, adding its unit F3 circulation changes the weight by

    number of unselected edges - number of reversed selected edges.

This follows edge by edge: an unselected edge becomes selected, a reversed selected edge vanishes, and a forward selected edge only changes direction.

## 2. Complete core-port table

The vertices of T that can meet an unselected external edge are a,a',c,c',d. Vertex b has all three incident edges selected. Let q(u,v) be the number of reversed selected edges on the unique T path from u to v. Rows and columns in the table are ordered a,a',c,c',d:

| q(u,v) | a | a' | c | c' | d |
|---|---:|---:|---:|---:|---:|
| a  | 0 | 0 | 1 | 1 | 0 |
| a' | 1 | 0 | 2 | 2 | 1 |
| c  | 1 | 1 | 0 | 0 | 0 |
| c' | 2 | 2 | 1 | 0 | 1 |
| d  | 2 | 2 | 2 | 2 | 0 |

The diagonal is recorded only for convenience: a simple cycle entering T once has distinct entry and exit vertices. The table is obtained directly from the five displayed arcs. Its maximum is two.

Exactly eight ordered pairs attain that maximum:

    (a',c), (a',c'), (c',a), (c',a'),
    (d,a), (d,a'), (d,c), (d,c').

For example, a'->a->b->c reverses a->a' and c->b, while traversing a->b forward. Thus it contributes two reversed edges. Omitting the source ports a,c would discard four of the eight ordered possibilities.

## 3. Necessary and sufficient condition within the single-pass class

**Transit theorem.** Orient a single-pass cycle so that its selected T path runs from u to v. Adding its unit circulation strictly decreases the weight if and only if both of the following hold:

1. (u,v) is one of the eight ordered pairs in Section 2.
2. In every visited ordinary component, the selected path starts at one of its leaves, proceeds to its source, and ends either at that source or at its other leaf.

When these conditions hold, the decrease is exactly one and the updated support is a P3-factor.

Proof. Suppose r ordinary components are visited. The cycle has exactly r+1 unselected edges connecting its r+1 distinct components. A selected path in an ordinary P3 contains at most one reversed edge. It contains exactly one if and only if it starts at a leaf and has one of the two shapes stated in condition 2. A leaf-to-leaf path contains one reversed and one forward edge; a leaf-to-source path contains just the reversed edge. A source-to-leaf path contains no reversed edge.

The T path contains at most two reversed edges, with equality exactly for condition 1. Therefore the total number q of reversed selected edges is at most r+2, whereas the number k of unselected edges is r+1. The difference k-q is negative precisely when equality q=r+2 holds. That equality is equivalent to conditions 1 and 2, and gives k-q=-1. Every divergence is preserved. The initial weight is 2n/3+1, so the new weight is 2n/3 and the ROOT-R06 identity gives a P3-factor. This proves both directions for the specified class.

Testing the opposite cycle orientation corresponds to interchanging its entry and exit data. No directed-cycle or induced-cycle hypothesis is needed.

## 4. A finite exact search for this class

The theorem gives a source-aware search with explicit state, not an assumed matching equivalence. For each of the eight ordered core pairs (u,v), seek an external route from v back to u. Start with an unselected edge incident with v. On arrival at a leaf l of an ordinary component (l,x,r), choose one of exactly three possible exits:

- traverse the selected edge l-x backwards, then use x's unselected third edge;
- traverse l-x-r, then use either one of the two unselected edges incident with r.

Reject arrivals at an ordinary source, reject any entry into T except the chosen final vertex u, and reject any revisit to an ordinary component. Stop successfully on reaching u. Distinct components and the selected-path shapes ensure that the lifted route and the core path are a simple cycle. Conversely, the transit theorem shows that every decreasing cycle in the single-pass class is generated by one of these searches.

A search state must include the set of already visited ordinary components. Keeping only the current vertex or deleting a repeated-vertex segment without checking component usage is not justified. The three available exits are a local branching bound, not a polynomial-time claim. With s ordinary components, search depth is at most s and the number of search branches is bounded by eight times two times the sum of 3^j for j=0,...,s, before invalid exits are removed. The factor two bounds the number of initial unselected edges at a core port; source ports have only one. This finite bound is intentionally coarse.

A certificate of success consists of the core pair, the ordered list of distinct ordinary components, their entry leaf and exit choice, and the intervening actual unselected edges. A checker reconstructs the simple cycle and checks k-q=-1 directly. Failure after complete enumeration means only that this cycle class contains no repair. It is not an UNSAT certificate for P3-factor existence or even for general simple-cycle repair.

## 5. The source-aware criterion repairs the omitted-port control

For the eighteen-vertex graph of the companion file, choose the core traversal

    1 -> 0 -> 2 -> 3,

so (u,v)=(a',c)=(1,3), one of the eight table entries. Close it by the external route

    3 - 17 -> 15 -> 16 - 7 -> 6 - 1.

Here hyphens denote unselected edges between components. In selected component (16,15,17), the path 17->15->16 starts at a leaf and exits through the other leaf. In selected component (7,6,8), the path 7->6 starts at a leaf and exits through its source's third edge 6-1. The two ordinary components are distinct. The route uses the core source port 3 at its start.

Thus the resulting cycle has three unselected edges and four reversed selected edges in this orientation. Adding its unit circulation decreases the weight by one. This is the reverse orientation of the nine-cycle explicitly updated in the companion file. It yields the same six displayed P3 components.

The leaf-only auxiliary matching misses both the core source port 3 and the ordinary source exit at 6. The new criterion includes these incidences without treating arbitrary auxiliary walks as valid cycle certificates.

## 6. Exact remaining obligations

It remains open in this candidate whether a 3-connected cubic graph must supply one of these single-pass repairs for every one-defect forest. Cycles that visit a forest component in more than one disjoint selected piece are outside the theorem. Neutral updates, multiple-cycle changes, and a global minimum-support argument are also separate possibilities.

The table, necessity proof, finite search bound, and displayed control route require only finite combinatorics and the exact charged-flow cost formula. No executed search, census, verifier receipt, EvidenceLink or mathematical admission is asserted in this file. Both canonical obligations remain open; the failed divisible-two-factor strengthening is not used.
