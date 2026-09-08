#!/usr/bin/env python3
"""Exact port-incidence allocation for a supplied complementary 2-factor.
New implementation. No earlier candidate program is imported.
"""
from itertools import combinations
from functools import lru_cache

class BadInput(ValueError):
    pass

def need(p, message):
    if not p: raise BadInput(message)

def edge(u,v): return tuple(sorted((u,v)))

def validate(x):
    n=x['n']; cs=x['cycles']; es=[tuple(e) for e in x['edges']]; M=[tuple(e) for e in x['matching']]
    need(type(n) is int and n>=6 and n%6==0,'order')
    need(all(len(e)==2 and type(e[0]) is int and type(e[1]) is int and 0<=e[0]<e[1]<n for e in es),'edge_label')
    need(len(es)==len(set(es)),'duplicate_edge')
    need(all(len(c)>=4 for c in cs) and sorted(v for c in cs for v in c)==list(range(n)),'cycle_partition')
    need(len(M)==n//2 and len(set(M))==len(M) and sorted(v for e in M for v in e)==list(range(n)),'perfect_matching')
    F={edge(c[i],c[(i+1)%len(c)]) for c in cs for i in range(len(c))}
    need(F.isdisjoint(M) and set(es)==F|set(M),'factor_decomposition')
    adj=[set() for _ in range(n)]
    for u,v in es:adj[u].add(v);adj[v].add(u)
    need(all(len(a)==3 for a in adj),'cubic')
    need(all(not(adj[u]&adj[v]) for u,v in es),'triangle')
    return cs,M

def system(x,S):
    cs=x['cycles']; M=x['matching']; S=tuple(S)
    need(len(S)==len(set(S)) and all(type(i)is int and 0<=i<len(M) for i in S),'selected_matching')
    owner={v:i for i in S for v in M[i]}
    gaps=[]; untouched=[]
    for ci,c in enumerate(cs):
        pos=[j for j,v in enumerate(c) if v in owner]
        if not pos:untouched.append(ci);continue
        for j,p in enumerate(pos):
            q=pos[(j+1)%len(pos)];d=(q-p)%len(c) or len(c)
            inner=[c[(p+k)%len(c)] for k in range(1,d)]
            gaps.append({'cycle':ci,'ends':[c[p],c[q]],'owners':[owner[c[p]],owner[c[q]]],
                         'distance':d,'demand':(d-1)%3,'internal':inner})
    return {'S':list(S),'gaps':gaps,'untouched':untouched}

def slot_graph(y):
    slots=[]
    for gi,g in enumerate(y['gaps']):
        for j in range(g['demand']):slots.append((gi,j,sorted(set(g['owners']))))
    return slots

def deficiency(x,y):
    slots=slot_graph(y); to_owner={}; to_slot={};augmentations=[]
    # Alternating BFS; every successful path strictly increases cardinality.
    for root in range(len(slots)):
        todo=[root]; seenL={root}; predR={}; finish=None
        for l in todo:
            for r in slots[l][2]:
                if r in predR:continue
                predR[r]=l
                if r not in to_owner:finish=r;break
                nxt=to_owner[r]
                if nxt not in seenL:seenL.add(nxt);todo.append(nxt)
            if finish is not None:break
        if finish is not None:
            path=[];r=finish
            while True:
                l=predR[r];path.append([l,r]);old=to_slot.get(l)
                to_slot[l]=r;to_owner[r]=l
                if old is None:break
                r=old
            augmentations.append(path)
    # Maximal alternating reachability gives a Hall witness when demands fail.
    X={l for l in range(len(slots)) if l not in to_slot}; Q=list(X);N=set()
    for l in Q:
        for r in slots[l][2]:
            if r in N:continue
            N.add(r)
            if r in to_owner and to_owner[r] not in X:X.add(to_owner[r]);Q.append(to_owner[r])
    bad=[ci for ci in y['untouched'] if len(x['cycles'][ci])%3]
    nu=len(to_owner);R=len(slots)
    return {'demand':R,'supply':len(y['S']),'matched':nu,
            'conflict':R+len(y['S'])-2*nu+3*len(bad),'untouched_bad':bad,
            'Hall_slots':sorted(X),'Hall_neighbors':sorted(N),
            'augmentations':augmentations}

def count_and_lift(x,y):
    S=y['S']; bit={i:1<<j for j,i in enumerate(S)};used=0; selected=[];one=[]
    for gi,g in enumerate(y['gaps']):
        if g['demand']==2:
            for side,r in enumerate(g['owners']):
                if used&bit[r]:return 0,None
                used|=bit[r]; selected.append((gi,side))
        elif g['demand']==1:one.append(gi)
    if any(len(x['cycles'][ci])%3 for ci in y['untouched']):return 0,None
    full=(1<<len(S))-1
    @lru_cache(None)
    def rec(j,mask):
        if j==len(one):return (int(mask==full),())
        gi=one[j];total=0;witness=None
        for side,r in enumerate(y['gaps'][gi]['owners']):
            if mask&bit[r]:continue
            k,w=rec(j+1,mask|bit[r]);total+=k
            if k and witness is None:witness=((gi,side),)+w
        return total,(() if witness is None else witness)
    k,w=rec(0,used)
    if not k:return 0,None
    selected+=list(w); B={}; consumed={gi:set() for gi in range(len(y['gaps']))}; triples=[]
    for gi,side in selected:
        g=y['gaps'][gi];v=g['ends'][side];z=g['internal'][0 if side==0 else -1]
        r=g['owners'][side];need(r not in B,'double_supply');B[r]=(v,z)
        need(z not in consumed[gi],'double_gap_vertex');consumed[gi].add(z)
    for r in S:
        v,z=B[r];a,b=x['matching'][r];other=b if a==v else a;triples.append([other,v,z])
    for gi,g in enumerate(y['gaps']):
        leftover=[v for v in g['internal'] if v not in consumed[gi]]
        need(len(leftover)%3==0,'gap_residue')
        triples.extend(leftover[j:j+3] for j in range(0,len(leftover),3))
    for ci in y['untouched']:
        c=x['cycles'][ci];triples.extend(c[j:j+3] for j in range(0,len(c),3))
    validate_factor(x,triples,S)
    return k*3**len(y['untouched']),{'factor':triples,'allocation':[list(t) for t in selected],
           'roles':{str(v):('B' if v==B[r][0] else 'A') for r in S for v in x['matching'][r]}}

def validate_factor(x,ps,S=None):
    need(all(len(p)==3 and len(set(p))==3 for p in ps),'path_distinct')
    need(sorted(v for p in ps for v in p)==list(range(x['n'])),'cover')
    E=set(map(tuple,x['edges']));mi={tuple(e):i for i,e in enumerate(x['matching'])};actual=[]
    for a,b,c in ps:
        for e in (edge(a,b),edge(b,c)):
            need(e in E,'path_edge')
            if e in mi:actual.append(mi[e])
    if S is not None:need(sorted(actual)==sorted(S),'matching_usage')
    return sorted(actual)

def control():
    cs=[list(range(a,a+8)) for a in (0,8,16)]
    M=[]
    for a,b in ((0,8),(8,16),(16,0)):
        M += [edge(a+2,a+5),edge(a+4,a+7),edge(a,b+3),edge(a+1,b+6)]
    M=sorted(M);F={edge(c[i],c[(i+1)%8]) for c in cs for i in range(8)}
    return {'n':24,'cycles':cs,'matching':[list(e) for e in M],'edges':[list(e) for e in sorted(F|set(M))]}
