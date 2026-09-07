#!/usr/bin/env python3
"""Exact checks for the new 36-vertex cycle-quotient obstruction. No old code imports."""
import copy, hashlib, itertools, json, pathlib, sys
BASE = pathlib.Path(__file__).resolve().parent

def require(ok, label):
    if not ok:
        raise ValueError(label)

def edge(u, v):
    return (u, v) if u < v else (v, u)

def adjacency(n, es):
    a = [set() for _ in range(n)]
    for u, v in es:
        a[u].add(v); a[v].add(u)
    return a

def connected(a, removed):
    live = set(range(len(a))) - set(removed)
    reached = {min(live)}; frontier = reached.copy()
    while frontier:
        frontier = set().union(*(a[u] for u in frontier)) & live - reached
        reached |= frontier
    return reached == live

def connectivity(n, es):
    a = adjacency(n, es); count = 0
    for size in range(3):
        for removed in itertools.combinations(range(n), size):
            require(connected(a, removed), 'vertex_cut:' + str(removed)); count += 1
    return count

def factor_check(n, es, factor):
    require(all(len(t) == 3 for t in factor), 'factor_shape')
    require(sorted(v for t in factor for v in t) == list(range(n)), 'factor_coverage')
    require(all(edge(t[0], t[1]) in es and edge(t[1], t[2]) in es for t in factor), 'factor_nonedge')

def validate(x):
    n = x['n']; es = [tuple(e) for e in x['edges']]
    require(n == 36 and n % 6 == 0, 'host_order')
    require(len(es) == len(set(es)), 'duplicate_edge')
    require(all(0 <= u < v < n for u, v in es), 'host_edge_format')
    a = adjacency(n, es)
    require(len(es) == 54 and all(len(t) == 3 for t in a), 'host_cubic')
    require(not any(a[u] & a[v] for u, v in es), 'host_triangle')
    cs = x['cycles']; m = set(tuple(e) for e in x['perfect_matching'])
    require(sorted(v for c in cs for v in c) == list(range(n)), 'cycle_partition')
    require(sorted(map(len, cs)) == [7, 11, 18], 'cycle_orders')
    ce = {edge(c[i], c[(i + 1) % len(c)]) for c in cs for i in range(len(c))}
    require(sorted(v for e in m for v in e) == list(range(n)), 'matching_partition')
    require(ce.isdisjoint(m) and ce | m == set(es), 'two_factor_decomposition')
    blocks = {v:i for i,c in enumerate(cs) for v in c}
    cross = {e for e in m if blocks[e[0]] != blocks[e[1]]}
    require(cross == set(tuple(e) for e in x['cross_edges']), 'cross_edges')
    require({tuple(sorted((blocks[u],blocks[v]))) for u,v in cross} == {(0,1),(1,2)}, 'quotient_path')
    require([sum((u in c) != (v in c) for u,v in cross) for c in [cs[0],cs[2]]] == [3,3], 'three_cuts')
    middle = cs[1]
    ports = sorted(v for e in cross for v in e if v in middle)
    require([middle.index(v) for v in ports] == x['middle_port_positions'], 'port_positions')
    require({middle.index(v) % 3 for v in ports} == {0}, 'phase_alignment')
    require(x['claimed_minimum_matching_usage'] == 3, 'claimed_minimum')
    factor_check(n, set(es), x['factor'])
    used = {edge(t[i],t[i+1]) for t in x['factor'] for i in range(2)}
    require(len(used & m) == 3, 'factor_matching_usage')
    require(len((used & m) - cross) == 1, 'factor_internal_chord')
    return n, set(es), ce, m, cross

def unsat_certificate(n, es, m, budget):
    """Complete exact-cover branching; a resource exception is never UNSAT."""
    a = adjacency(n, es)
    rows = sorted((c,l,r) for c in range(n) for l,r in itertools.combinations(sorted(a[c]),2))
    rm = [sum(1 << v for v in t) for t in rows]
    cost = [int(edge(c,l) in m)+int(edge(c,r) in m) for c,l,r in rows]
    incident = [[i for i,t in enumerate(rows) if v in t] for v in range(n)]
    bad = {}; visits = 0
    def rec(mask, left):
        nonlocal visits
        if mask == 0: return []
        key = str(mask)+':'+str(left)
        if key in bad: return None
        visits += 1
        if visits > 200000: raise RuntimeError('search_node_cap')
        choices = [(v,[i for i in incident[v] if rm[i]&mask == rm[i] and cost[i]<=left]) for v in range(n) if mask>>v&1]
        pivot, ids = min(choices, key=lambda z:(len(z[1]),z[0]))
        children=[]
        for i in ids:
            ans=rec(mask^rm[i],left-cost[i])
            if ans is not None: return [rows[i]]+ans
            children.append(str(mask^rm[i])+':'+str(left-cost[i]))
        bad[key]=pivot  # Every child is reconstructed from the full graph by the consumer.
        return None
    root=str((1<<n)-1)+':'+str(budget)
    ans=rec((1<<n)-1,budget)
    require(ans is None,'unexpected_cover')
    return {'n':n,'edges':[list(e) for e in sorted(es)],'charged_matching':[list(e) for e in sorted(m & es)],
            'budget':budget,'root':root,'nodes':bad,'kind':'complete_exact_cover_failure_dag','node_count':len(bad)}

def capped(n, es, side):
    side=set(side); labels=sorted(side); relabel={v:i for i,v in enumerate(labels)}; z=len(labels)
    inside=[edge(relabel[u],relabel[v]) for u,v in es if u in side and v in side]
    ports=[u if u in side else v for u,v in es if (u in side)!=(v in side)]
    require(len(ports)==3 and len(set(ports))==3,'cap_ports')
    return z+1, inside+[edge(relabel[u],z) for u in ports]

def main():
    raw=(BASE/'input.json').read_bytes();x=json.loads(raw)
    n,es,ce,m,cross=validate(x)
    counts={'host':connectivity(n,es)};caps=[]
    for name,side in [('left',x['cycles'][0]),('right',x['cycles'][2])]:
        for complement in [False,True]:
            ss=set(range(n))-set(side) if complement else set(side)
            nn,ee=capped(n,es,ss);aa=adjacency(nn,ee)
            require(all(len(a)==3 for a in aa),'cap_cubic')
            require(not any(aa[u]&aa[v] for u,v in ee),'cap_triangle')
            cases=connectivity(nn,ee)
            caps.append({'cut':name,'complement':complement,'n':nn,'mod6':nn%6,'deletion_sets':cases})
    restricted=ce|cross
    proofs={'restricted_no_factor':unsat_certificate(n,restricted,m,12),
            'full_host_at_most_two_matching_edges':unsat_certificate(n,es,m,2)}
    mutations=[]
    def test(name, edit, expected):
        y=copy.deepcopy(x);edit(y)
        try: validate(y)
        except ValueError as error:
            require(str(error)==expected,'mutation_wrong_failure:'+name)
            mutations.append({'name':name,'failure':str(error),'rejected':True})
        else:raise ValueError('mutation_survived:'+name)
    test('duplicate_edge',lambda y:y['edges'].append(y['edges'][0]),'duplicate_edge')
    test('delete_edge',lambda y:y['edges'].pop(),'host_cubic')
    test('loop',lambda y:y['edges'].__setitem__(0,[0,0]),'host_edge_format')
    test('wrong_order',lambda y:y.__setitem__('n',35),'host_order')
    test('repeated_cycle_vertex',lambda y:y['cycles'][0].__setitem__(0,1),'cycle_partition')
    test('omit_matching_edge',lambda y:y['perfect_matching'].pop(),'matching_partition')
    test('invent_cross_edge',lambda y:y['cross_edges'].append([0,25]),'cross_edges')
    test('false_port_position',lambda y:y['middle_port_positions'].__setitem__(0,1),'port_positions')
    test('claim_minimum_two',lambda y:y.__setitem__('claimed_minimum_matching_usage',2),'claimed_minimum')
    test('repeat_factor_vertex',lambda y:y['factor'][0].__setitem__(0,0),'factor_coverage')
    test('wrong_factor_center',lambda y:y['factor'].__setitem__(0,[0,1,6]),'factor_nonedge')
    test('omit_factor_block',lambda y:y['factor'].pop(),'factor_coverage')
    output={'verdict':'candidate_only','status':'PASS','n':n,'edges':len(es),'triangle_free':True,
            'deletion_sets':counts,'caps':caps,'cycle_lengths':list(map(len,x['cycles'])),
            'middle_ports':x['middle_port_positions'],'restricted_graph_edges':len(restricted),
            'restricted_graph_is_cubic':False,'full_host_has_factor':True,'minimum_matching_usage':3,
            'factor':x['factor'],'proof_node_counts':{k:v['node_count'] for k,v in proofs.items()},
            'mutations':mutations,'input_sha256':hashlib.sha256(raw).hexdigest(),
            'scope':'One specified root-domain positive graph; no root nonexistence claim or order census.'}
    (BASE/'failure-certificates.json').write_text(json.dumps(proofs,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(output,sort_keys=True,separators=(',',':')))

if __name__=='__main__': main()
