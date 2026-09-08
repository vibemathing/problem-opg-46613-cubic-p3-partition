#!/usr/bin/env python3
"""Bounded specified-family search; not an order or isomorphism census."""
import itertools,json,time,resource
import allocation as a
resource.setrlimit(resource.RLIMIT_CPU,(25,25))
resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576))
start=time.monotonic(); deadline=start+22

def pairings(vs,L):
    if not vs:yield [];return
    u=vs[0]
    for v in vs[1:]:
        if min((u-v)%L,(v-u)%L)<3:continue
        for rest in pairings([w for w in vs if w not in (u,v)],L):yield [(u,v)]+rest

def host(L,internal):
    cs=[list(range(i*L,(i+1)*L)) for i in range(3)]
    M=[]
    for i in range(3):
        off=i*L;nxt=((i+1)%3)*L
        M += [a.edge(off+u,off+v) for u,v in internal]
        M += [a.edge(off,nxt+3),a.edge(off+1,nxt+6)]
    M=sorted(M);F={a.edge(c[j],c[(j+1)%L]) for c in cs for j in range(L)}
    return {'n':3*L,'cycles':cs,'matching':[list(e) for e in M],'edges':[list(e) for e in sorted(F|set(M))]}

def threeconn(x):
    n=x['n'];adj=[set() for _ in range(n)]
    for u,v in x['edges']:adj[u].add(v);adj[v].add(u)
    for k in (0,1,2):
        for cut in itertools.combinations(range(n),k):
            seen=set(cut);root=next(v for v in range(n) if v not in seen);seen.add(root);Q=[root]
            for v in Q:
                for w in adj[v]-seen:seen.add(w);Q.append(w)
            if len(seen)!=n:return False
    return True

stats={'local_matchings_examined':0,'three_connected_hosts':0,'cost_three_positive':0,'tested_subsets':0}; hit=None
for internal in pairings([i for i in range(14) if i not in (0,1,3,6)],14):
    if time.monotonic()>deadline:break
    x=host(14,internal);a.validate(x);stats['local_matchings_examined']+=1
    if not threeconn(x):continue
    stats['three_connected_hosts']+=1
    found=False
    # Cost <=2 already impossible by fixed cross-port geometry, but test all.
    for k in (0,1,2,3):
        for S in itertools.combinations(range(len(x['matching'])),k):
            stats['tested_subsets']+=1;y=a.system(x,S)
            if any(len(x['cycles'][j])%3 for j in y['untouched']):continue
            if sum(g['demand'] for g in y['gaps'])!=k:continue
            count,w=a.count_and_lift(x,y)
            if count:found=True;break
        if found:break
    if found:stats['cost_three_positive']+=1
    else:hit=x;break
print(json.dumps({'scope':'deterministic 3 copies of a 14-cycle with fixed ports and enumerated internal matchings',
                  'stats':stats,'candidate_no_cost_le3':hit,'elapsed_seconds':time.monotonic()-start,
                  'complete_family':False,'verdict':'candidate_only'},sort_keys=True))
