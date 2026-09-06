"""Candidate-side common-cycle to P3-factor construction and bounded audits.

No cycle-existence theorem is tested here. Input cycles are supplied explicitly.
Uses only the Python standard library; run with -S and external resource limits.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import sys
import time
from collections import Counter

R_EDGES = ((0,1),(0,5),(1,2),(1,6),(2,3),(2,7),(3,8),(4,6),(4,7),(5,7),(5,8),(6,8))
PORTS = (0,3,4)
SUBSETS = ((3,4),(1,5),(2,4),(3,5),(4,5),(2,5),(2,3),(1,3),(1,4))
PERMS = tuple(itertools.permutations((3,4,5)))
UUU = ((0,1,2),(4,7,5),(3,8,6))
UAB_PATHS = ((1,6,4),(2,7,5))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def automorphisms() -> dict[tuple[int, int], tuple[int, ...]]:
    lookup = {frozenset(s): i for i,s in enumerate(SUBSETS)}
    edges = {frozenset(e) for e in R_EDGES}
    result = {}
    for permutation in PERMS:
        sigma = dict(zip((3,4,5), permutation))
        mapping = tuple(lookup[frozenset(sigma.get(x,x) for x in s)] for s in SUBSETS)
        require(len(set(mapping)) == 9, 'not bijective')
        require({frozenset((mapping[u],mapping[v])) for u,v in R_EDGES} == edges, 'not an automorphism')
        key = mapping[0],mapping[3]
        require(key not in result, 'duplicate ordered port choice')
        result[key] = mapping
    require(set(result) == set(itertools.permutations(PORTS,2)), 'missing port choice')
    return result

MAPS = automorphisms()


def construct(n: int, edges: tuple[tuple[int,int],...], cycle: tuple[int,...],
              retained: frozenset[int], offset: int = 0):
    require(n >= 4 and len(cycle) >= 3, 'small input')
    require(len(set(cycle)) == len(cycle) and all(0 <= u < n for u in cycle), 'invalid cycle labels')
    require(retained <= set(cycle) and len(retained) % 3 == 0, 'retained set not eligible/on cycle')
    graph = [set() for _ in range(n)]
    edge_set = set()
    for u,v in edges:
        require(0 <= u < n and 0 <= v < n and u != v, 'invalid frame edge')
        e = tuple(sorted((u,v)))
        require(e not in edge_set, 'duplicate frame edge')
        edge_set.add(e); graph[u].add(v); graph[v].add(u)
    require(all(len(a) == 3 for a in graph), 'not a cubic frame')
    require(all(cycle[(i+1)%len(cycle)] in graph[u] for i,u in enumerate(cycle)), 'cycle uses nonedge')
    # Expanded labels are (frame vertex, -1) for retained singletons, or (v, R-label).
    vertices = {(u,-1) for u in retained}
    expanded = set()
    port = {}
    choices = tuple(itertools.permutations(PORTS))
    for u in range(n):
        if u in retained:
            continue
        vertices.update((u,j) for j in range(9))
        expanded.update(frozenset(((u,a),(u,b))) for a,b in R_EDGES)
        permutation = choices[(u + sum(retained) + offset) % 6]
        port[u] = dict(zip(sorted(graph[u]),permutation))
    def endpoint(u,v):
        return (u,-1) if u in retained else (u,port[u][v])
    for u,v in edges:
        expanded.add(frozenset((endpoint(u,v),endpoint(v,u))))
    selected = set()
    incoming = {u:[] for u in range(n)}
    outgoing = {u:[] for u in range(n)}
    value = 0
    for i,u in enumerate(cycle):
        value = (value - (u in retained)) % 3
        v = cycle[(i+1)%len(cycle)]
        if value:
            a,b = (u,v) if value == 1 else (v,u)
            selected.add(frozenset((endpoint(a,b),endpoint(b,a))))
            outgoing[a].append(b); incoming[b].append(a)
    require(value == 0, 'cycle flow did not close')
    signatures = Counter()
    for u in range(n):
        if u in retained:
            require((len(incoming[u]),len(outgoing[u])) in ((1,0),(0,2)), 'retained role')
            continue
        if not incoming[u] and not outgoing[u]:
            paths = UUU
            signatures['UUU'] += 1
        else:
            require(len(incoming[u]) == len(outgoing[u]) == 1, 'brick role')
            a,b = port[u][incoming[u][0]],port[u][outgoing[u][0]]
            mapping = MAPS[a,b]
            paths = tuple(tuple(mapping[j] for j in p) for p in UAB_PATHS)
            selected.add(frozenset(((u,mapping[3]),(u,mapping[8]))))
            signatures[f'A{a}B{b}'] += 1
        for a,b,c in paths:
            selected.add(frozenset(((u,a),(u,b))))
            selected.add(frozenset(((u,b),(u,c))))
    # Check the actual expanded graph and actual selected components, not just flow signs.
    require(selected <= expanded, 'selected nonedge')
    full = {v:set() for v in vertices}; chosen = {v:set() for v in vertices}
    for e in expanded:
        a,b = tuple(e); full[a].add(b);full[b].add(a)
    require(all(len(a) == 3 for a in full.values()), 'expanded graph not cubic')
    for e in selected:
        a,b = tuple(e);chosen[a].add(b);chosen[b].add(a)
    unseen = set(vertices); triples = []
    while unseen:
        root = min(unseen); unseen.remove(root); stack = [root]; component = {root}
        while stack:
            u = stack.pop()
            for v in chosen[u] & unseen:
                unseen.remove(v);component.add(v);stack.append(v)
        require(len(component) == 3, 'component is not a triple')
        centers = [v for v in component if len(chosen[v]) == 2]
        require(len(centers) == 1 and sorted(len(chosen[v]) for v in component) == [1,1,2], 'component is not P3')
        b = centers[0]; a,c = sorted(chosen[b]); triples.append((a,b,c))
    return sorted(triples), signatures


def audit() -> dict[str,object]:
    deadline = time.monotonic()+30
    counts = {}; signature_totals = Counter(); digest = hashlib.sha256()
    for n in (6,8,10,12):
        edges = tuple((i,(i+1)%n) for i in range(n)) + tuple((i,i+n//2) for i in range(n//2))
        count = 0
        for mask in range(1<<n):
            retained = frozenset(i for i in range(n) if mask>>i&1)
            if len(retained)%3:
                continue
            for offset in range(6):
                triples, signatures = construct(n,edges,tuple(range(n)),retained,offset)
                digest.update((json.dumps(triples,separators=(',',':'))+'\n').encode())
                signature_totals.update(signatures); count += 1
            require(time.monotonic()<deadline,'incomplete audit: deadline')
        counts[str(n)] = count
    petersen = R_EDGES + ((9,0),(9,3),(9,4))
    cycle = (0,1,2,3,8,6,4,7,5)
    examples = []
    for offset in range(6):
        triples, signatures = construct(10,petersen,cycle,frozenset(range(9)),offset)
        examples.append(triples)
        signature_totals.update(signatures)
    require(set(signature_totals) == {'UUU'} | {f'A{a}B{b}' for a,b in MAPS}, 'untested local signature')
    rejected = []
    invalid = (('nonmultiple',frozenset((0,)),cycle),('off-cycle',frozenset((0,1,9)),cycle),
               ('repeated-cycle-vertex',frozenset(),cycle+(0,)),('nonedge-cycle',frozenset(),(0,2,1)))
    for name,retained,c in invalid:
        try:
            construct(10,petersen,c,retained)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted invalid input: '+name)
    return {'verdict':'candidate_only','python':sys.version.split()[0],
            'frame_counts_by_order':counts,'petersen_nine_cycle_cases':6,
            'total_cases':sum(counts.values())+6,'all_cases_produce_p3_factors':True,
            'seven_local_signature_counts':dict(sorted(signature_totals.items())),
            'factor_stream_sha256':digest.hexdigest(),'petersen_example':examples[0],
            'rejected_inputs':rejected,
            'limitations':['supplied-cycle construction tests, not a test of universal cyclability',
                           'no registered verifier receipt or mathematical admission',
                           'six heterogeneous port assignments per retained subset, not all global assignments']}

if __name__ == '__main__':
    print(json.dumps(audit(),sort_keys=True,indent=2))
