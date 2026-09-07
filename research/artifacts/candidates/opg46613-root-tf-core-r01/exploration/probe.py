"""Bounded discovery of positive-defect simple-cycle local minima. New code."""
import random,itertools,time,json,sys,resource
resource.setrlimit(resource.RLIMIT_CPU,(30,30))
resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
START=time.monotonic(); R=random.Random(4661326)

def conn(n,edges,removed=()):
    groups=[{v} for v in range(n) if v not in removed]
    for u,v in edges:
        if u in removed or v in removed: continue
        a=next(i for i,c in enumerate(groups) if u in c); b=next(i for i,c in enumerate(groups) if v in c)
        if a!=b:
            groups[a]|=groups[b];groups.pop(b)
    return len(groups)==1

def forest(n):
    arcs=[(0,1),(0,2),(3,2),(3,4),(2,5)]
    for c in range(6,n,3): arcs += [(c,c+1),(c,c+2)]
    return arcs

def complete(n,arcs):
    es={tuple(sorted(e)) for e in arcs}; adj=[set() for _ in range(n)]
    for a,b in es:adj[a].add(b);adj[b].add(a)
    comp=[0]*6+[v//3-1 for v in range(6,n)]
    stubs=[v for v in range(n) for _ in range(3-len(adj[v]))]
    for restart in range(30):
        s=stubs[:];R.shuffle(s);out=es.copy(); aa=[z.copy() for z in adj]
        while s:
            u=s.pop(); opts=[i for i,v in enumerate(s) if u!=v and v not in aa[u] and not aa[u]&aa[v] and comp[u]!=comp[v]]
            if not opts:break
            j=R.choice(opts);v=s.pop(j);out.add(tuple(sorted((u,v))));aa[u].add(v);aa[v].add(u)
        else:return sorted(out),aa
    return None

def improve(adj,arcs,limit=1000000):
    selected=set(arcs);nodes=0;cycles=0
    def extend(path,used,p,q,k):
        nonlocal nodes,cycles
        nodes+=1
        if nodes>limit:raise TimeoutError('cycle_node_cap')
        u=path[-1];s=path[0]
        for v in sorted(adj[u]):
            x=int((u,v) in selected);y=int((v,u) in selected);z=1-x-y
            if v==s and len(path)>2 and path[1]<path[-1]:
                cycles+=1
                if max(p+x,q+y)>k+z:return path[:],p+x,q+y,k+z
            elif v>s and v not in used:
                a=extend(path+[v],used|{v},p+x,q+y,k+z)
                if a:return a
        return None
    for s in range(len(adj)):
        ans=extend([s],{s},0,0,0)
        if ans:return ans,cycles,nodes
    return None,cycles,nodes

summary=[];found=[]
for n in [12,18,24,30]:
    a=forest(n);row={'n':n,'built':0,'cycle_limited':0,'improved':0,'no_improvement':0,'traps':0}
    for trial in range(1200):
        if time.monotonic()-START>24: break
        built=complete(n,a)
        if not built:continue
        e,adj=built;row['built']+=1
        try:ans,cc,nodes=improve(adj,a)
        except TimeoutError: row['cycle_limited']+=1;continue
        if ans:row['improved']+=1;continue
        row['no_improvement']+=1
        if not all(conn(n,e,S) for r in range(3) for S in itertools.combinations(range(n),r)):continue
        row['traps']+=1;found.append({'n':n,'edges':e,'arcs':a,'cycles':cc,'nodes':nodes});print('FOUND',n,file=sys.stderr);break
    summary.append(row)
    if found:break
out={'summary':summary,'found':found,'seed':4661326,'seconds':time.monotonic()-START}
print(json.dumps(out,separators=(',',':')))
