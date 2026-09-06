"""Generator-side exact screen, not a verifier receipt; standard library only."""
import collections,itertools,json,sys,time,resource
resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
resource.setrlimit(resource.RLIMIT_FSIZE,(16384,16384))
START=time.monotonic(); DEADLINE=START+20

def budget():
    if time.monotonic()>DEADLINE: raise TimeoutError('20-second C02 screening limit')

def petersen():
    return sorted({tuple(sorted(e)) for i in range(5) for e in [(i,(i+1)%5),(i,i+5),(i+5,5+(i+2)%5)]})

def build():
    # Petersen minus vertex 0 uses labels 0..8 (original j -> j-1).
    # Mobius ladder on 0..9: cycle plus opposite chords; delete vertex 0.
    # Its remaining original j -> j+8, using labels 9..17.
    ladder = {tuple(sorted((i,(i+1)%10))) for i in range(10)}
    ladder.update((i,i+5) for i in range(5))
    edges = [(u-1,v-1) for u,v in petersen() if u and v]
    edges += [(u+8,v+8) for u,v in ladder if u and v]
    edges += [(0,9),(3,17),(4,13)]
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

E=build();A=adjacency(18,E)
assert len(E)==27 and len(set(E))==27 and all(len(x)==3 for x in A)
connected_cases=0
for size in range(3):
    for S in itertools.combinations(range(18),size):
        assert connected_after(A,S);connected_cases+=1
Ms=list(enumerate_matchings(A));spectra=collections.Counter(tuple(map(len,cycles(A,M))) for M in Ms)
F=find_p3(A);assert F is not None
assert sorted(v for p in F for v in p)==list(range(18))
assert all(b in A[a] and c in A[b] for a,b,c in F)
result={'verdict':'candidate_only','python':sys.version.split()[0],'graph_order':18,'graph_size':27,'edges':E,'vertex_deletion_sets_tested':connected_cases,'perfect_matching_count':len(Ms),'cycle_spectrum_counts':[{'lengths':list(s),'count':c} for s,c in sorted(spectra.items())],'p3_factor':F,'sample_matching':Ms[0],'sample_cycles':cycles(A,Ms[0]),'algorithm':'least-uncovered-vertex perfect matching recursion; exact P3 cover recursion; deletion BFS','limits':{'timeout_seconds':20,'threads':1,'memory_bytes':268435456,'cpu_seconds':20,'maximum_output_bytes':16384},'limitations':['generator-side exact screening only','no EvidenceLink or admission','no claim of minimum counterexample order']}
output=json.dumps(result,indent=2)+'\n'
if len(output.encode('utf-8'))>16384: raise RuntimeError('output limit')
sys.stdout.write(output)
