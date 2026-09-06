"""Generator-side exact screen, not a verifier receipt; standard library only."""
import collections,itertools,json,sys,time,resource
resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
resource.setrlimit(resource.RLIMIT_FSIZE,(16384,16384))
START=time.monotonic(); DEADLINE=START+20

def budget():
    if time.monotonic()>DEADLINE: raise TimeoutError('20-second screening limit')

def petersen():
    return sorted({tuple(sorted(e)) for i in range(5) for e in [(i,(i+1)%5),(i,i+5),(i+5,5+(i+2)%5)]})

def build():
    edges=[]
    for i in range(3):
        edges.extend((9*i+u-1,9*i+v-1) for u,v in petersen() if u and v)
        edges.extend((9*i+t-1,27+j) for j,t in enumerate((1,4,5)))
    return sorted(edges)

def adjacency(n,edges):
    adj=[set() for _ in range(n)]
    for u,v in edges:
        assert 0<=u<v<n
        adj[u].add(v);adj[v].add(u)
    return adj

def enumerate_matchings(adj):
    def visit(mask,edges):
        budget()
        if not mask:
            yield edges;return
        u=(mask&-mask).bit_length()-1
        for v in sorted(adj[u]):
            if (mask>>v)&1:
                yield from visit(mask^(1<<u)^(1<<v),edges+[(u,v)])
    return visit((1<<len(adj))-1,[])

def cycles(adj,M):
    partner={u:v for e in M for u,v in (e,e[::-1])}
    seen=set();out=[]
    for root in range(len(adj)):
        if root in seen:continue
        prev=-1;u=root;cycle=[]
        while u not in seen:
            seen.add(u);cycle.append(u)
            opts=sorted(adj[u]-{partner[u],prev})
            assert opts
            prev,u=u,opts[0]
        assert u==root
        out.append(cycle)
    return sorted(out,key=lambda c:(len(c),c))

def connected_after(adj,S):
    budget();remaining=set(range(len(adj)))-set(S)
    reached={min(remaining)};stack=list(reached)
    while stack:
        u=stack.pop()
        for v in adj[u]&remaining-reached:
            reached.add(v);stack.append(v)
    return reached==remaining

def find_p3(adj):
    triples={}
    for center,nb in enumerate(adj):
        for u,v in itertools.combinations(sorted(nb),2):
            mask=(1<<u)|(1<<center)|(1<<v)
            triples.setdefault(mask,(u,center,v))
    incident=[[(mask,p) for mask,p in sorted(triples.items()) if mask>>v&1] for v in range(len(adj))]
    def visit(rem,paths):
        budget()
        if not rem:return paths
        choices=min(([x for x in incident[v] if x[0]&rem==x[0]] for v in range(len(adj)) if rem>>v&1),key=len)
        for mask,p in choices:
            ans=visit(rem^mask,paths+[p])
            if ans is not None:return ans
        return None
    return visit((1<<len(adj))-1,[])

E=build();A=adjacency(30,E)
assert len(E)==45 and len(set(E))==45 and all(len(x)==3 for x in A)
connected_cases=0
for size in range(3):
    for S in itertools.combinations(range(30),size):
        assert connected_after(A,S);connected_cases+=1
Ms=list(enumerate_matchings(A));spectra=collections.Counter(tuple(map(len,cycles(A,M))) for M in Ms)
F=find_p3(A);assert F is not None
assert sorted(v for p in F for v in p)==list(range(30))
assert all(b in A[a] and c in A[b] for a,b,c in F)
result={'verdict':'candidate_only','python':sys.version.split()[0],'graph_order':30,'graph_size':45,'edges':E,'vertex_deletion_sets_tested':connected_cases,'perfect_matching_count':len(Ms),'cycle_spectrum_counts':[{'lengths':list(s),'count':c} for s,c in sorted(spectra.items())],'p3_factor':F,'sample_matching':Ms[0],'sample_cycles':cycles(A,Ms[0]),'algorithm':'least-uncovered-vertex perfect matching recursion; exact P3 cover recursion; deletion BFS','limits':{'timeout_seconds':20,'threads':1,'memory_bytes':268435456,'cpu_seconds':20,'maximum_output_bytes':16384},'limitations':['generator-side exact screening only','no EvidenceLink or admission','no claim of minimum counterexample order']}
output=json.dumps(result,indent=2)+'\n'
if len(output.encode('utf-8'))>16384: raise RuntimeError('output limit')
sys.stdout.write(output)
