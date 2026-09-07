#!/usr/bin/env python3
"""Bounded eight-wiring pressure test of the next 2-factor spectrum (8,8,8)."""
from itertools import product, combinations
from functools import lru_cache
import json
import resource
resource.setrlimit(resource.RLIMIT_CPU, (20,20))
resource.setrlimit(resource.RLIMIT_AS, (536870912,536870912))
resource.setrlimit(resource.RLIMIT_FSIZE, (2097152,2097152))
resource.setrlimit(resource.RLIMIT_CORE, (0,0))

def run(bits):
    cycles = [list(range(8*i,8*i+8)) for i in range(3)]
    F = {tuple(sorted((c[j],c[(j+1)%8]))) for c in cycles for j in range(8)}
    M = set()
    for i,b in enumerate(bits):
        a=8*i;d=8*((i+1)%3)
        M.update([(a+2,a+5),(a+4,a+7)])
        targets=(3,6) if not b else (6,3)
        M.update(tuple(sorted((a+j,d+k))) for j,k in enumerate(targets))
    E=F|M
    adj=[set() for _ in range(24)]
    for u,v in E:
        adj[u].add(v);adj[v].add(u)
    assert len(E)==36 and len(M)==12 and all(len(s)==3 for s in adj)
    assert not any(adj[u]&adj[v] for u,v in E)
    failed=[]
    for k in range(3):
        for deleted in combinations(range(24),k):
            live=set(range(24))-set(deleted)
            reached={min(live)}
            while True:
                new=reached|{w for v in reached for w in adj[v] if w in live}
                if new==reached:break
                reached=new
            if reached!=live:failed.append(list(deleted))
    paths=[]
    for c in range(24):
        for u,v in combinations(sorted(adj[c]),2):
            cost=int(tuple(sorted((u,c))) in M)+int(tuple(sorted((c,v))) in M)
            paths.append((frozenset((u,c,v)),cost,(u,c,v)))
    @lru_cache(None)
    def opt(live):
        if not live:return (0,())
        if opt.cache_info().currsize>100000:raise RuntimeError('node_budget')
        v=min(live)
        best=(100,())
        for block,cost,p in paths:
            if v in block and block<=live:
                sub,w=opt(live-block)
                if sub+cost<best[0]:best=(sub+cost,(p,)+w)
        return best
    minimum,factor=opt(frozenset(range(24)))
    return {'bits':list(bits),'n':24,'cycles':cycles,'matching':sorted(M),'edges':sorted(E),
            'vertex_cut_failures':failed,'minimum_M_edges':minimum,'factor':factor,
            'states':opt.cache_info().currsize}
print(json.dumps({'verdict':'candidate_only','scope':'eight specified wirings, not graph-order census',
                  'cases':[run(bits) for bits in product((0,1),repeat=3)]},sort_keys=True,separators=(',',':')))
