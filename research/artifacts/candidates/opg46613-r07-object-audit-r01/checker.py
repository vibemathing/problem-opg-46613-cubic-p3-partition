#!/usr/bin/env python3
"""Fresh fixed-object R07 audit; Python standard library only.
No old candidate/verifier module is imported. No Lean or admission claim.
Core methods: disjoint-set contraction, exhaustive cut masks, vertex-mask
matching dynamic programming, and ternary incidence-vector subtraction.
"""
from __future__ import annotations
import copy
import hashlib
import itertools
import json
import sys
from pathlib import Path


class Rejected(ValueError):
    pass


def need(ok: bool, code: str) -> None:
    if not ok:
        raise Rejected(code)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def groups(vertices, edges):
    """Connected components by equivalence-class merging, not graph traversal."""
    parent = {u: u for u in vertices}
    def root(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    for u, v in edges:
        if u in parent and v in parent:
            a, b = root(u), root(v)
            if a != b:
                parent[max(a, b)] = min(a, b)
    parts = {}
    for u in parent:
        parts.setdefault(root(u), []).append(u)
    return sorted(sorted(p) for p in parts.values())


def cycle_edges(c, host):
    need(len(c) >= 3 and len(set(c)) == len(c), 'cycle_not_simple')
    es = list(zip(c, c[1:] + c[:1]))
    need(all(edge(u, v) in host for u, v in es), 'cycle_nonedge')
    return es


def typed_vertices(n, arcs):
    out, inc = [0]*n, [0]*n
    for u, v in arcs:
        out[u] += 1
        inc[v] += 1
    need(all((out[u]-inc[u]) % 3 == 2 for u in range(n)), 'charge_mismatch')
    need(all((out[u], inc[u]) in ((2,0),(0,1),(1,2)) for u in range(n)), 'illegal_local_type')
    return {'sources':[u for u in range(n) if out[u] == 2],
            'leaves':[u for u in range(n) if out[u] == 0],
            'defects':[u for u in range(n) if inc[u] == 2],
            'rows':[[u,out[u],inc[u],out[u]-inc[u],(out[u]-inc[u])%3] for u in range(n)]}


def matching_dp(vertices, typed_edges):
    """Exact maximum cardinality on every vertex mask. Parallel edges kept
    in the input; their multiplicity does not change maximum cardinality."""
    ix = {v:i for i,v in enumerate(vertices)}
    adj = [0]*len(vertices)
    for item in typed_edges:
        a, b = (ix[v] for v in item['ends'])
        need(a != b, 'auxiliary_loop')
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    dp = [0]*(1 << len(vertices))
    for mask in range(1, len(dp)):
        low = mask & -mask
        i, rest = low.bit_length()-1, mask ^ low
        best, possible = dp[rest], adj[i] & rest
        while possible:
            j = possible & -possible
            best = max(best, 1 + dp[rest ^ j])
            possible ^= j
        dp[mask] = best
    return dp[-1], hashlib.sha256(bytes(dp)).hexdigest(), len(dp)


def audit(w):
    n, es = w['order'], [tuple(e) for e in w['edges']]
    need(n == 18 and len(es) == 27, 'host_order_or_edge_count')
    need(all(type(u) is int and type(v) is int and 0 <= u < v < n for u,v in es), 'host_edge_encoding')
    host = set(es)
    need(len(host) == len(es), 'host_duplicate_edge')
    degrees = [sum(u in e for e in es) for u in range(n)]
    need(degrees == [3]*n, 'host_not_cubic')
    triangles = [list(t) for t in itertools.combinations(range(n),3)
                 if all(edge(u,v) in host for u,v in itertools.combinations(t,2))]
    need(not triangles, 'host_triangle')
    H = w['hamilton_cycle']
    need(sorted(H) == list(range(n)), 'hamilton_coverage')
    he = {edge(u,v) for u,v in cycle_edges(H,host)}
    cp = w['chord_positions']
    need(len(cp) == 9 and sorted(x for p in cp.values() for x in p) == list(range(n)), 'chords_not_perfect_matching')
    chords = {name:edge(H[a],H[b]) for name,(a,b) in cp.items()}
    need(set(chords.values()) == host-he, 'chords_disagree')
    pairs = set()
    for a,b in itertools.combinations(sorted(cp),2):
        u,v = sorted(cp[a]); s,t = sorted(cp[b])
        if (u < s < v) != (u < t < v):
            pairs.add((a,b))
    tree = [tuple(sorted(p)) for p in w['interlacement_tree']]
    need(len(tree)==8 and len(set(tree))==8 and set(tree)<=pairs and len(groups(cp,tree))==1, 'interlacement_tree_invalid')
    # A mask and its complement describe one cut; bit zero chooses a unique side.
    cuts, cut_hist, smallest, small_side = 0, {}, 28, None
    for mask in range(1, (1 << n)-1, 2):
        size = sum(((mask >> u) ^ (mask >> v)) & 1 for u,v in es)
        cut_hist[size] = cut_hist.get(size,0)+1
        cuts += 1
        if size < smallest:
            smallest, small_side = size, [u for u in range(n) if mask >> u & 1]
    need(smallest == 3, 'edge_connectivity_not_three')
    vcuts = {'empty':0,'singleton':0,'adjacent_pair':0,'nonadjacent_pair':0}
    for r in range(3):
        for cut in itertools.combinations(range(n),r):
            key = 'empty' if r==0 else 'singleton' if r==1 else 'adjacent_pair' if tuple(cut) in host else 'nonadjacent_pair'
            vcuts[key] += 1
            need(len(groups(set(range(n))-set(cut),es))==1, 'vertex_cut')
    arcs = [tuple(a) for a in w['initial_arcs']]
    need(len(arcs)==13 and len({edge(*a) for a in arcs})==13 and all(edge(*a) in host for a in arcs), 'initial_arc_encoding')
    types = typed_vertices(n,arcs)
    label = w['exceptional_labels']
    a,ap,b,c,cpv,d = [label[k] for k in ('a','ap','b','c','cp','d')]
    need(len({a,ap,b,c,cpv,d})==6 and types['defects']==[b], 'one_defect_shape')
    need({(a,ap),(a,b),(c,cpv),(c,b),(b,d)} <= set(arcs), 'exceptional_arcs')
    components = groups(range(n),arcs)
    need(sorted(map(len,components))==[3,3,3,3,6] and len(arcs)==n-len(components), 'not_one_defect_forest')
    exceptional = sorted([a,ap,b,c,cpv,d])
    need(exceptional in components, 'exceptional_component')
    virtual = []
    for part in components:
        if part == exceptional:
            continue
        centers = sorted(set(part) & set(types['sources']))
        need(len(centers)==1, 'ordinary_component')
        virtual.append({'source':centers[0],'ends':sorted(set(part)-set(centers))})
    virtual.sort(key=lambda t:t['source'])
    leaves = types['leaves']
    real = [list(e) for e in es if all(u in leaves for u in e)]
    aux = w['auxiliary']
    need(aux['leaves']==leaves and aux['virtual_matching']==virtual, 'auxiliary_leaf_or_virtual_mismatch')
    need(aux['real_edges']==real, 'auxiliary_real_edges_not_host_induced')
    matched = [u for item in virtual for u in item['ends']]
    need(len(matched)==len(set(matched)), 'virtual_edges_not_matching')
    exposed = sorted(set(leaves)-set(matched))
    need(exposed==sorted([ap,cpv,d])==aux['exposed'], 'exposed_mismatch')
    typed = [{'kind':'real','ends':e} for e in real]+[dict(kind='virtual',**v) for v in virtual]
    isolated = sorted(set(leaves)-{u for e in typed for u in e['ends']})
    nu, dp_hash, dp_states = matching_dp(leaves,typed)
    need(nu==aux['matching_number']==len(virtual)==4, 'matching_number_mismatch')
    need((len(leaves)-len(isolated))//2==nu, 'matching_upper_bound')
    update = w['update']
    ce = cycle_edges(update['cycle'],host)
    values = {e:0 for e in es}
    for u,v in arcs:
        values[edge(u,v)] = 1 if u<v else 2
    before = [(values[edge(u,v)] * (1 if u<v else -1))%3 for u,v in ce]
    p,q,k = before.count(1),before.count(2),before.count(0)
    need((p,q,k)==(update['p'],update['q'],update['k'])==(4,2,3), 'cycle_cost_counts')
    need(update['coefficient']==-1, 'cycle_coefficient')
    new = dict(values)
    for u,v in ce:
        e = edge(u,v)
        new[e] = (new[e] + update['coefficient']*(1 if u<v else -1))%3
    after = sorted((u,v) if x==1 else (v,u) for (u,v),x in new.items() if x)
    new_types = typed_vertices(n,after)
    need(len(after)==12 and len(after)-len(arcs)==k-p and not new_types['defects'], 'update_does_not_repair')
    factor_arcs, seen = set(), []
    factor = w['p3_factor']
    for triple in factor:
        need(len(triple)==3 and len(set(triple))==3 and all(type(u) is int and 0<=u<n for u in triple), 'p3_encoding')
        l,x,r = triple
        need(edge(l,x) in host and edge(x,r) in host, 'p3_nonedge')
        factor_arcs.update(((x,l),(x,r))); seen.extend(triple)
    need(len(factor)==6 and sorted(seen)==list(range(n)), 'p3_partition')
    need(factor_arcs==set(after), 'factor_not_updated_support')
    need(all(len(t)==3 for t in groups(range(n),after)), 'updated_component_size')
    return {
      'host':{'order':n,'edge_count':len(es),'degrees':degrees,'triangles':triangles,
        'edge_cut_count':cuts,'edge_cut_histogram':cut_hist,'minimum_edge_cut':smallest,'minimum_cut_side':small_side,'vertex_deletion_cases':vcuts},
      'hamilton_certificate':{'cycle':H,'chords_by_vertex':chords,'all_interlacements':sorted(pairs),'spanning_tree':tree,'chord_cyclic_distances':{name:min(v-u,n-v+u) for name,(u,v) in cp.items()}},
      'initial_flow':{'weight':len(arcs),'types':types,'components':components},
      'auxiliary':{'vertices':leaves,'typed_edges':typed,'virtual_matching':virtual,'exposed':exposed,'isolated':isolated,'matching_number':nu,'upper_bound':(len(leaves)-len(isolated))//2,'dp_states':dp_states,'dp_sha256':dp_hash},
      'update':{'cycle':update['cycle'],'p':p,'q':q,'k':k,'coefficient':-1,'weight_change':k-p,
        'cycle_edge_rows':[[u,v,x, (x-1)%3] for (u,v),x in zip(ce,before)],'new_arcs':[list(e) for e in after],
        'new_types':new_types,'components':groups(range(n),after),'factor':factor},
      'status':'PASS', 'verdict':'candidate_only'}


def mutation_suite(w):
    tests = []
    def test(name, expected, edit):
        m = copy.deepcopy(w); edit(m)
        try:
            audit(m)
        except Rejected as err:
            need(str(err)==expected, 'mutation_wrong_rejection_'+name)
            tests.append({'mutation':name,'first_failure':str(err),'rejected':True})
        else:
            raise Rejected('mutation_accepted_'+name)
    test('delete_host_edge_0_10','host_order_or_edge_count',lambda m:m['edges'].remove([0,10]))
    test('duplicate_host_edge','host_duplicate_edge',lambda m:m['edges'].__setitem__(2,[0,1]))
    test('reverse_selected_arc_0_1','charge_mismatch',lambda m:m['initial_arcs'].__setitem__(0,[1,0]))
    test('replace_update_vertex_6_by_8','cycle_nonedge',lambda m:m['update']['cycle'].__setitem__(2,8))
    test('break_first_P3','p3_nonedge',lambda m:m['p3_factor'][0].__setitem__(1,1))
    test('invent_augmenting_edge_1_4','auxiliary_real_edges_not_host_induced',lambda m:m['auxiliary']['real_edges'].append([1,4]))
    test('drop_interlacement_tree_edge','interlacement_tree_invalid',lambda m:m['interlacement_tree'].pop())
    test('claim_matching_number_five','matching_number_mismatch',lambda m:m['auxiliary'].__setitem__('matching_number',5))
    test('repeat_update_vertex','cycle_not_simple',lambda m:m['update']['cycle'].__setitem__(2,1))
    return tests


def main():
    raw = Path(__file__).with_name('witness.json').read_bytes()
    need(len(raw)<65536, 'input_size')
    w = json.loads(raw)
    result = audit(w)
    result.update({'witness_sha256':hashlib.sha256(raw).hexdigest(),
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python':sys.version.split()[0], 'mutations':mutation_suite(w),
        'limitations':['One frozen graph, not a graph-order census.',
        'Fresh same-generation-domain audit, not a trusted-verifier receipt.',
        'General sufficient lemma has a separate written proof, not a Lean check.']})
    print(json.dumps(result,sort_keys=True,separators=(',',':')))


if __name__ == '__main__':
    try:
        main()
    except (Rejected, KeyError, TypeError, ValueError) as err:
        print(json.dumps({'status':'FAIL','error':str(err),'verdict':'candidate_only'}))
        sys.exit(1)
