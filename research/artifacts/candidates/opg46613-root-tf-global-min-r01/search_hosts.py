#!/usr/bin/env python3
"""Bounded deterministic new-host search, not an isomorphism-reduced census."""
import hashlib,json,random,sys,time
from itertools import combinations
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from surgery import validate_object,state


def connected(adj,deleted):
    available=set(range(len(adj)))-set(deleted);seen={min(available)};queue=list(seen)
    while queue:
        v=queue.pop()
        for w in (adj[v]&available)-seen:seen.add(w);queue.append(w)
    return seen==available


def make(lengths,seed):
    rng=random.Random(seed);n=sum(lengths);cs=[];base=0
    for length in lengths:cs.append(list(range(base,base+length)));base+=length
    F={tuple(sorted((c[i],c[(i+1)%len(c)]))) for c in cs for i in range(len(c))}
    forbidden=F|{tuple(sorted((c[i],c[(i+2)%len(c)]))) for c in cs for i in range(len(c))}
    for trial in range(1,2001):
        permutation=list(range(n));rng.shuffle(permutation)
        M=sorted(tuple(sorted(permutation[j:j+2])) for j in range(0,n,2))
        if any(e in forbidden for e in M):continue
        g={'n':n,'cycles':cs,'matching':list(map(list,M)),'edges':list(map(list,sorted(F|set(M))))}
        adj=validate_object(g)
        if all(connected(adj,d) for k in range(3) for d in combinations(range(n),k)):return g,trial
    raise RuntimeError('bounded_generator_exhausted')


def exact_factor(g):
    adj=[set() for _ in range(g['n'])]
    for a,b in g['edges']:adj[a].add(b);adj[b].add(a)
    rows=[(a,c,b) for c in range(g['n']) for a,b in combinations(sorted(adj[c]),2)]
    masks=[sum(1<<v for v in p) for p in rows];contains=[[i for i,p in enumerate(rows) if v in p] for v in range(g['n'])]
    nodes=0;dead=set();start=time.monotonic()
    def visit(remaining):
        nonlocal nodes
        nodes+=1
        if nodes>150000 or time.monotonic()-start>2.5:raise RuntimeError('cover_budget')
        if remaining==0:return []
        if remaining in dead:return None
        best=None
        for v in range(g['n']):
            if not (remaining>>v)&1:continue
            candidates=[i for i in contains[v] if masks[i]&remaining==masks[i]]
            if best is None or len(candidates)<len(best):best=candidates
            if not best:break
        for i in best:
            tail=visit(remaining^masks[i])
            if tail is not None:return [list(rows[i])]+tail
        dead.add(remaining);return None
    result=visit((1<<g['n'])-1)
    if result is None:raise RuntimeError('no_factor_requires_separate_complete_certificate')
    return result,nodes


def main():
    specs=[(8,11,11),(8,14,14),(8,17,17),(14,17,17),(20,20,20),(20,26,26),(8,)*6,(8,)*9,(7,8,9,12),(8,8,8,8,10)]
    output=[]
    for j,lengths in enumerate(specs):
        for rep in range(2):
            seed=46613000+100*j+rep;g,trial=make(lengths,seed);factor,nodes=exact_factor(g)
            E={tuple(sorted((p[i],p[i+1]))) for p in factor for i in (0,1)}
            S=[i for i,e in enumerate(g['matching']) if tuple(e) in E]
            assert state(g,S)['kappa']==0
            output.append({'seed':seed,'accepted_trial':trial,'graph':g,'factor':factor,'selected':S,'cover_nodes':nodes,
                           'global_minimum_kappa':0,'minimum_certificate':'explicit_factor_and_nonnegativity'})
    text=json.dumps({'verdict':'candidate_only','scope':'20 deterministic labeled positive hosts, not an isomorphism-reduced census','cases':output},sort_keys=True,separators=(',',':'))+'\n'
    Path('new-hosts.json').write_text(text)
    print(json.dumps({'status':'PASS','verdict':'candidate_only','graphs':len(output),'orders':sorted(set(x['graph']['n'] for x in output)),
                      'cycle_counts':sorted(set(len(x['graph']['cycles']) for x in output)),'positive':len(output),'root_negative_objects':0,
                      'new_hosts_sha256':hashlib.sha256(text.encode()).hexdigest(),'old_subset_censuses_repeated':False},sort_keys=True))

if __name__=='__main__':main()
