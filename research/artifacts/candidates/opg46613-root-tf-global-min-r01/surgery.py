#!/usr/bin/env python3
"""Demand-unit graph and simultaneous subset surgery. Candidate-only.
No imports from old constructors or old verifier modules.
"""
from collections import deque


def require(ok, message):
    if not ok: raise ValueError(message)


def validate_object(g):
    n,es,mt,cs=g['n'],g['edges'],g['matching'],g['cycles']
    edge=lambda e:tuple(sorted(e))
    require(n>0 and n%6==0,'host_order')
    require(all(len(e)==2 and 0<=e[0]<n and 0<=e[1]<n and e[0]!=e[1] for e in es),'host_endpoints')
    E=set(map(edge,es));require(len(E)==len(es)==3*n//2,'host_edge_multiplicity')
    require(all(sum(v in e for e in E)==3 for v in range(n)),'host_degree')
    require(sorted(x for e in mt for x in e)==list(range(n)),'matching_partition')
    require(all(edge(e) in E for e in mt),'matching_nonedge')
    require(sorted(x for c in cs for x in c)==list(range(n)),'cycle_partition')
    require(all(len(c)>=4 for c in cs),'cycle_length')
    F={edge((c[i],c[(i+1)%len(c)])) for c in cs for i in range(len(c))}
    require(len(F)==n and F.isdisjoint(map(edge,mt)) and F|set(map(edge,mt))==E,'cycle_complement')
    adj=[set() for _ in range(n)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    require(not any(adj[a]&adj[b] for a,b in E),'host_triangle')
    return adj


def component_rows(vertices,edges):
    parent={v:v for v in vertices}
    def root(v):
        while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
        return v
    for a,b in edges:
        ra,rb=root(a),root(b)
        if ra!=rb:parent[rb]=ra
    groups={}
    for v in vertices:groups.setdefault(root(v),[]).append(v)
    out=[]
    for vs in groups.values():
        inside=set(vs);ids=[i for i,(a,b) in enumerate(edges) if a in inside]
        out.append({'owners':sorted(vs),'slots':ids,'vertices':len(vs),'edges':len(ids),'excess':len(ids)-len(vs)})
    return sorted(out,key=lambda x:x['owners'])


def state(g,selected):
    S=tuple(sorted(selected))
    require(len(set(S))==len(S) and all(type(e) is int and 0<=e<len(g['matching']) for e in S),'selected_supply')
    owner={v:e for e in S for v in g['matching'][e]};gaps=[];untouched=[];slots=[]
    for ci,c in enumerate(g['cycles']):
        positions=[i for i,v in enumerate(c) if v in owner]
        if not positions:
            untouched.append({'cycle':ci,'length':len(c),'residue':len(c)%3});continue
        for j,i in enumerate(positions):
            k=positions[(j+1)%len(positions)];d=(k-i)%len(c) or len(c)
            path=[c[(i+t)%len(c)] for t in range(d+1)];a,b=path[0],path[-1];r=(d-1)%3
            gap={'cycle':ci,'ends':[a,b],'owners':[owner[a],owner[b]],'distance':d,'demand':r,'path':path}
            gid=len(gaps);gaps.append(gap)
            for unit in range(r):slots.append({'gap':gid,'unit':unit,'ends':[owner[a],owner[b]]})
    rows=component_rows(S,[x['ends'] for x in slots]);u=sum(x['residue']!=0 for x in untouched)
    t=sum(x['edges']==x['vertices']-1 for x in rows);b=sum(max(0,x['edges']-x['vertices']) for x in rows)
    return {'selected':list(S),'gaps':gaps,'untouched':untouched,'slots':slots,'components':rows,
            's':len(S),'D':len(slots),'u':u,'tree_count':t,'excess':b,
            'nu':sum(min(x['vertices'],x['edges']) for x in rows),'kappa':t+b+3*u}


def augment(slots,selected,initial=None):
    """Record complete alternating augmentations in the changed slot graph."""
    mate={} if initial is None else dict(initial)
    require(len(set(mate.values()))==len(mate),'initial_matching')
    require(all(j<len(slots) and e in slots[j]['ends'] for j,e in mate.items()),'initial_incidence')
    paths=[]
    while True:
        inverse={e:j for j,e in mate.items()};q=deque(j for j in range(len(slots)) if j not in mate)
        parent={('d',j):None for j in q};stop=None
        while q and stop is None:
            j=q.popleft()
            for e in sorted(set(slots[j]['ends'])):
                if ('s',e) in parent:continue
                parent['s',e]=('d',j)
                if e not in inverse:stop=('s',e);break
                jj=inverse[e]
                if ('d',jj) not in parent:parent['d',jj]=('s',e);q.append(jj)
        if stop is None:break
        p=[];v=stop
        while v is not None:p.append(list(v));v=parent[v]
        p.reverse();paths.append(p)
        for i in range(0,len(p),2):mate[p[i][1]]=p[i+1][1]
    return mate,paths


def minimal_hall(st):
    slots=st['slots'];bad=next((c for c in st['components'] if c['edges']>c['vertices']),None)
    if bad is None:return None
    ids=list(bad['slots']);changed=True
    while changed:
        changed=False
        for k in ids:
            trial=[i for i in ids if i!=k];owners=sorted({v for i in trial for v in slots[i]['ends']})
            rows=component_rows(owners,[slots[i]['ends'] for i in trial])
            more=next((c for c in rows if c['edges']>c['vertices']),None)
            if more is not None:
                chosen=set(more['owners']);ids=[i for i in trial if slots[i]['ends'][0] in chosen];changed=True;break
    owners=sorted({v for i in ids for v in slots[i]['ends']})
    require(len(ids)==len(owners)+1,'hall_excess_not_one')
    return {'slot_ids':ids,'neighbors':owners,'deficiency':1}


def surgery(g,before,after):
    a=state(g,before);b=state(g,after);ma,_=augment(a['slots'],a['selected'])
    require(len(ma)==a['nu'],'rank_formula')
    def key(st,j):
        sl=st['slots'][j];gap=st['gaps'][sl['gap']]
        return(gap['cycle'],tuple(gap['path']),tuple(gap['owners']),sl['unit'])
    newkeys={key(b,j):j for j in range(len(b['slots']))}
    inherited={newkeys[key(a,j)]:e for j,e in ma.items() if key(a,j) in newkeys and e in b['selected']}
    mb,paths=augment(b['slots'],b['selected'],inherited);require(len(mb)==b['nu'],'new_rank_formula')
    loss=len(ma)-len(inherited);gain=len(mb)-len(inherited)
    change=b['s']-a['s']+b['D']-a['D']+3*(b['u']-a['u'])+2*loss-2*gain
    require(change==b['kappa']-a['kappa'],'surgery_balance')
    changed={v for e in set(before)^set(after) for v in g['matching'][e]}
    return {'before':a,'after':b,'remove':sorted(set(before)-set(after)),'add':sorted(set(after)-set(before)),
            'changed_cycles':[i for i,c in enumerate(g['cycles']) if set(c)&changed],
            'old_matching':sorted(map(list,ma.items())),'retained_matching':sorted(map(list,inherited.items())),
            'new_matching':sorted(map(list,mb.items())),'loss':loss,'gain':gain,'augmenting_paths':paths,
            'delta_kappa':change,'minimal_hall_before':minimal_hall(a)}


def factor_from_state(g,st):
    require(st['kappa']==0,'not_feasible');mate,_=augment(st['slots'],st['selected']);p3=[];role={}
    for gid,h in enumerate(st['gaps']):
        ids=[j for j,s in enumerate(st['slots']) if s['gap']==gid];used=[]
        for e in [mate[j] for j in ids]:
            side=0 if h['owners'][0]==e else 1
            require(side not in used,'duplicate_gap_side');used.append(side)
            v=h['ends'][side];w=h['path'][1] if side==0 else h['path'][-2]
            other=next(x for x in g['matching'][e] if x!=v)
            require(e not in role,'double_B');role[e]={'B':v,'A':other,'neighbor':w,'gap':gid,'side':side};p3.append([other,v,w])
        middle=h['path'][1:-1]
        if 0 in used:middle=middle[1:]
        if 1 in used:middle=middle[:-1]
        require(len(middle)%3==0,'remaining_gap');p3.extend(middle[i:i+3] for i in range(0,len(middle),3))
    for h in st['untouched']:
        c=g['cycles'][h['cycle']];p3.extend(c[i:i+3] for i in range(0,len(c),3))
    require(sorted(v for row in p3 for v in row)==list(range(g['n'])),'factor_partition')
    E={tuple(sorted(e)) for e in g['edges']}
    require(all(tuple(sorted((p[i],p[i+1]))) in E for p in p3 for i in (0,1)),'factor_edge')
    return {'paths':p3,'roles':{str(e):role[e] for e in sorted(role)}}
