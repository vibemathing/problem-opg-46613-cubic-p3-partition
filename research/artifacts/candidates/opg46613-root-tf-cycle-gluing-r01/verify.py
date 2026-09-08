#!/usr/bin/env python3
"""Separate unordered-triple weighted exact-cover consumer; imports no producer."""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations
import hashlib
import json
from pathlib import Path

class Invalid(ValueError):
    pass

def require(condition, code):
    if not condition:
        raise Invalid(code)

def pair(u, v):
    return (u, v) if u < v else (v, u)

def path_key(p):
    return (min(p[0], p[2]), p[1], max(p[0], p[2]))

def graph(case):
    n, raw = case['n'], case['edges']
    require(isinstance(n, int) and n > 0 and n % 6 == 0, 'root_order')
    es = [tuple(e) for e in raw]
    require(len(es) == len(set(es)), 'duplicate_edge')
    require(all(len(e) == 2 and all(type(x) is int for x in e) and 0 <= e[0] < e[1] < n for e in es), 'edge_labels_or_loop')
    require(len(es) == 3*n//2, 'edge_count')
    E = set(es)
    adjacency = [0]*n
    for u, v in es:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    require(all(row.bit_count() == 3 for row in adjacency), 'cubic')
    require(not any((adjacency[u] & adjacency[v]) for u, v in es), 'triangle')
    # Bit-vector wave propagation is separate from the generator's set DFS.
    deletion_cases = 0
    for k in range(3):
        for removed in combinations(range(n), k):
            live = ((1 << n)-1) ^ sum(1 << v for v in removed)
            reached = live & -live
            frontier = reached
            while frontier:
                expansion = 0
                while frontier:
                    bit = frontier & -frontier
                    expansion |= adjacency[bit.bit_length()-1]
                    frontier ^= bit
                frontier = expansion & live & ~reached
                reached |= frontier
            require(reached == live, 'vertex_connectivity')
            deletion_cases += 1
    cycles = case['cycles']
    require(all(len(c) >= 4 for c in cycles), 'cycle_length')
    require(sorted(v for c in cycles for v in c) == list(range(n)), 'cycle_cover')
    F = {pair(c[i], c[(i+1) % len(c)]) for c in cycles for i in range(len(c))}
    require(len(F) == n and F <= E, 'cycle_edges')
    M = {tuple(e) for e in case['matching']}
    require(len(M) == n//2 and sorted(v for e in M for v in e) == list(range(n)), 'matching_cover')
    require(M <= E and not (M & F) and M | F == E, 'matching_decomposition')
    return E, F, M, deletion_cases

def factor(n, E, paths):
    require(all(len(p) == 3 and len(set(p)) == 3 for p in paths), 'path_distinct')
    require(all(pair(p[0], p[1]) in E and pair(p[1], p[2]) in E for p in paths), 'path_nonedge')
    require(sorted(v for p in paths for v in p) == list(range(n)), 'factor_cover')
    return {pair(p[i], p[i+1]) for p in paths for i in (0, 1)}

def consume(case, result, host=None):
    E, F, M, deleted = graph(case) if host is None else host
    n = case['n']
    S = {tuple(e) for e in result['selected_matching']}
    require(len(S) == len(result['selected_matching']) and S <= M and len(S) <= 2, 'selected_subset')
    support = factor(n, E, result['factor'])
    require(support & M == S, 'selected_usage')
    roles = dict(result['roles'])
    require(len(roles) == len(result['roles']) and set(roles) == {v for e in S for v in e}, 'role_domain')
    require(all({roles[u], roles[v]} == {'A', 'B'} for u, v in S), 'matching_roles')
    require(len(result['pieces']) == len(case['cycles']), 'piece_count')
    internal_paths, Bpairs = [], {}
    for c, pieces in zip(case['cycles'], result['pieces']):
        a = pieces['singletons']
        bp = pieces['pairs']
        ps = pieces['paths']
        require(sorted(a) == sorted(v for v in c if roles.get(v) == 'A'), 'singleton_roles')
        require(all(len(p) == 2 for p in bp) and sorted(p[0] for p in bp) == sorted(v for v in c if roles.get(v) == 'B'), 'pair_center_roles')
        require(all(p[1] not in roles and pair(*p) in F for p in bp), 'pair_incidence')
        require(all(len(p) == 3 and pair(p[0],p[1]) in F and pair(p[1],p[2]) in F for p in ps), 'internal_path')
        used = a + [v for p in bp for v in p] + [v for p in ps for v in p]
        require(sorted(used) == sorted(c), 'local_cover')
        Bpairs.update(bp)
        internal_paths.extend(ps)
    rebuilt = list(internal_paths)
    for u, v in S:
        a, b = (u, v) if roles[u] == 'A' else (v, u)
        rebuilt.append([a, b, Bpairs[b]])
    require(sorted(map(path_key, rebuilt)) == sorted(map(path_key, result['factor'])), 'gluing_equality')
    return deleted

def minimum_matching_usage(n, E, M):
    """Generate rows from unordered triples, not cycle gaps or port assignments."""
    rows = [[] for _ in range(n)]
    for vertices in combinations(range(n), 3):
        for center in vertices:
            ends = [v for v in vertices if v != center]
            edges = (pair(ends[0], center), pair(center, ends[1]))
            if all(e in E for e in edges):
                mask = sum(1 << v for v in vertices)
                cost = sum(e in M for e in edges)
                require(cost <= 1, 'matching_path_cost')
                for v in vertices:
                    rows[v].append((mask, cost, [ends[0], center, ends[1]]))
    @lru_cache(None)
    def solve(mask):
        if solve.cache_info().currsize > 200000:
            raise RuntimeError('exact_cover_node_budget')
        if not mask:
            return 0, ()
        v = (mask & -mask).bit_length()-1
        best, witness = n+1, ()
        for block, cost, path in rows[v]:
            if block & mask == block:
                subcost, subwitness = solve(mask ^ block)
                if cost + subcost < best:
                    best, witness = cost + subcost, (tuple(path),) + subwitness
        return best, witness
    cost, witness = solve((1 << n)-1)
    require(cost <= n, 'no_factor')
    factor(n, E, witness)
    return cost, [list(p) for p in witness], solve.cache_info().currsize

def main():
    inp = Path('inputs.json').read_bytes()
    constructed = Path('constructor.stdout.json').read_bytes()
    data, output = json.loads(inp), json.loads(constructed)
    require(len(data['cases']) == len(output['cases']), 'case_count')
    rows, hosts = [], []
    for case, result in zip(data['cases'], output['cases']):
        require(case['id'] == result['id'], 'case_identity')
        host = graph(case)
        consume(case, result, host)
        cost, witness, states = minimum_matching_usage(case['n'], host[0], host[2])
        require(cost == len(result['selected_matching']), 'minimum_cost_disagreement')
        rows.append({'id': case['id'], 'minimum_M_edges': cost,
                     'exact_cover_states': states, 'other_factor': witness,
                     'vertex_deletions': host[3]})
        hosts.append(host)
    # Partition completeness checked by a different fixed-length Cartesian enumeration.
    coverage = {}
    for n in (6, 12, 18):
        expected = set()
        def collect(prefix, remain):
            if remain == 0:
                expected.add(tuple(prefix))
                return
            for v in range(4, remain+1):
                if not prefix or v >= prefix[-1]:
                    collect(prefix+[v], remain-v)
        collect([], n)
        declared = {tuple(p) for p in data['complete_length_partitions'][str(n)]}
        require(declared == expected, 'partition_completeness')
        require({tuple(map(len,c['cycles'])) for c in data['cases'] if c['n'] == n} == expected, 'sample_pattern_coverage')
        coverage[str(n)] = sorted(map(list, expected))
    mutations = []
    base, cert = data['cases'][-1], output['cases'][-1]
    def reject(name, expected, alter_case=None, alter_result=None):
        c, r = deepcopy(base), deepcopy(cert)
        if alter_case:
            alter_case(c)
        if alter_result:
            alter_result(r)
        try:
            consume(c, r)
        except Invalid as err:
            require(str(err) == expected, 'mutation_wrong_failure:' + name + ':' + str(err))
            mutations.append({'mutation':name, 'first_failure':str(err), 'rejected':True})
        else:
            raise Invalid('mutation_accepted:' + name)
    reject('delete_host_edge', 'edge_count', lambda c:c['edges'].pop())
    reject('duplicate_host_edge', 'duplicate_edge', lambda c:c['edges'].append(c['edges'][0]))
    reject('loop_host_edge', 'edge_labels_or_loop', lambda c:c['edges'].__setitem__(0,[0,0]))
    reject('outside_vertex', 'edge_labels_or_loop', lambda c:c['edges'].__setitem__(0,[0,c['n']]))
    reject('wrong_modulus', 'root_order', lambda c:c.__setitem__('n',17))
    reject('remove_matching_edge', 'matching_cover', lambda c:c['matching'].pop())
    reject('repeat_cycle_vertex', 'cycle_cover', lambda c:c['cycles'][0].__setitem__(1,c['cycles'][0][0]))
    reject('cycle_nonedge', 'cycle_edges', lambda c:c['cycles'][0].__setitem__(slice(1,3),list(reversed(c['cycles'][0][1:3]))))
    reject('repeat_path_vertex', 'path_distinct', alter_result=lambda r:r['factor'][0].__setitem__(0,r['factor'][0][1]))
    bad = next(v for v in range(base['n']) if v not in cert['factor'][0] and pair(v,cert['factor'][0][1]) not in hosts[-1][0])
    reject('nonedge_path', 'path_nonedge', alter_result=lambda r:r['factor'][0].__setitem__(0,bad))
    reject('missing_factor_block', 'factor_cover', alter_result=lambda r:r['factor'].pop())
    reject('forged_selected_edge', 'selected_subset', alter_result=lambda r:r['selected_matching'].append([0,1]))
    # Choose a nonzero-cost certificate for role mutations.
    base_index = next(i for i,r in enumerate(output['cases']) if r['roles'])
    base, cert = data['cases'][base_index], output['cases'][base_index]
    reject('same_roles_on_matching', 'matching_roles', alter_result=lambda r:r['roles'][0].__setitem__(1,'B' if r['roles'][0][1]=='A' else 'A'))
    pi = next(i for i,p in enumerate(cert['pieces']) if p['pairs'])
    reject('reverse_B_center', 'pair_center_roles', alter_result=lambda r:r['pieces'][pi]['pairs'][0].reverse())
    ai = next(i for i,p in enumerate(cert['pieces']) if p['singletons'])
    reject('erase_A_singleton', 'singleton_roles', alter_result=lambda r:r['pieces'][ai]['singletons'].pop())
    summary = {'verdict':'candidate_only', 'status':'PASS', 'scope':'85 fixed labelled hosts, not an isomorphism or graph-order census',
               'inputs_sha256':hashlib.sha256(inp).hexdigest(),
               'constructor_output_sha256':hashlib.sha256(constructed).hexdigest(),
               'cases':rows, 'partition_coverage':coverage,
               'minimum_cost_histogram':dict(sorted(Counter(r['minimum_M_edges'] for r in rows).items())),
               'vertex_deletions_total':sum(r['vertex_deletions'] for r in rows),
               'mutations':mutations, 'trusted_attestation':None}
    print(json.dumps(summary,sort_keys=True,separators=(',',':')))

if __name__ == '__main__':
    main()
