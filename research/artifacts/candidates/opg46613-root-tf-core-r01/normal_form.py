#!/usr/bin/env python3
"""Fixed-M normal-form search, distinct from exact cover and failure-DAG replay.
Exhausts matching-edge usage <=3 only, on the fixed input; not a root solver claim.
"""
import hashlib,itertools,json,pathlib,resource,time
BASE=pathlib.Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
resource.setrlimit(resource.RLIMIT_FSIZE,(2097152,2097152))
START=time.monotonic()
def need(ok,label):
    if not ok:raise ValueError(label)
def ek(u,v):return tuple(sorted((u,v)))
def cycle_covers(cycle,roles):
    n=len(cycle); active={i for i,v in enumerate(cycle) if v in roles}
    if not active:
        if n%3:return []
        return [([],[[cycle[(j+s)%n],cycle[(j+s+1)%n],cycle[(j+s+2)%n]] for j in range(0,n,3)]) for s in range(3)]
    b=[i for i in active if roles[cycle[i]]=='B']; out=[]
    for steps in itertools.product((-1,1),repeat=len(b)):
        occupied=set(active);pairs=[]
        for i,s in zip(b,steps):
            j=(i+s)%n
            if j in occupied:break
            occupied.add(j);pairs.append((cycle[i],cycle[j]))
        else:
            start=min(occupied);segment=[];triples=[];valid=True
            for d in range(1,n+1):
                j=(start+d)%n
                if j in occupied:
                    if len(segment)%3:valid=False;break
                    triples.extend(segment[k:k+3] for k in range(0,len(segment),3));segment=[]
                else:segment.append(cycle[j])
            if valid:out.append((pairs,triples))
    return out

def run():
    raw=(BASE/'input.json').read_bytes();x=json.loads(raw)
    n=x['n'];es=set(map(tuple,x['edges']));m=sorted(map(tuple,x['perfect_matching']));cycles=x['cycles']
    need(sorted(v for e in m for v in e)==list(range(n)),'matching_not_perfect')
    need(sorted(v for c in cycles for v in c)==list(range(n)),'cycle_partition')
    ce={ek(c[i],c[(i+1)%len(c)]) for c in cycles for i in range(len(c))}
    need(ce.isdisjoint(m) and ce|set(m)==es,'fixed_M_decomposition')
    counts={};patterns={};witness=None
    for budget in range(4):
        counts[budget]=0;patterns[budget]=0
        for ids in itertools.combinations(range(len(m)),budget):
            for orient in itertools.product((0,1),repeat=budget):
                patterns[budget]+=1;roles={};partners={}
                for i,o in zip(ids,orient):
                    a,b=m[i] if o==0 else m[i][::-1]
                    roles[a]='A';roles[b]='B';partners[b]=a
                options=[cycle_covers(c,roles) for c in cycles]
                if not all(options):continue
                for pieces in itertools.product(*options):
                    factor=[t for pairs,ts in pieces for t in ts]
                    for pairs,ts in pieces:
                        factor.extend([[w,b,partners[b]] for b,w in pairs])
                    need(sorted(v for t in factor for v in t)==list(range(n)),'factor_cover')
                    used={ek(t[i],t[i+1]) for t in factor for i in range(2)}
                    need(used<=es and len(used&set(m))==budget,'factor_edges_or_cost')
                    counts[budget]+=1
                    if witness is None:witness={'cost':budget,'factor':factor,'roles':roles}
                if time.monotonic()-START>18:raise TimeoutError('normal_form_deadline')
    need(witness is not None and witness['cost']==3,'unexpected_minimum')
    print(json.dumps({'status':'PASS','verdict':'candidate_only','method':'matching subset/orientation plus cyclic gap tiling',
      'matching_patterns_by_budget':patterns,'factor_counts_by_budget':counts,'minimum_in_checked_range':3,
      'first_factor':witness,'input_sha256':hashlib.sha256(raw).hexdigest(),
      'scope':'Complete cost-0-through-3 search on one graph, not a graph-order census or general existence proof.'},sort_keys=True,separators=(',',':')))
if __name__=='__main__':run()
