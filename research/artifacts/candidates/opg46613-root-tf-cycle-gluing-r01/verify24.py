#!/usr/bin/env python3
"""Separate complete cost-polynomial consumer and finite <=2 certificate."""
from itertools import combinations
from functools import lru_cache
from pathlib import Path
import hashlib,json,resource
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
resource.setrlimit(resource.RLIMIT_FSIZE,(2097152,2097152))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))

def demand(ok,code):
    if not ok:raise ValueError(code)

def key(a,b):return tuple(sorted((a,b)))

def audit(c):
    n=c['n'];E={tuple(e) for e in c['edges']};M={tuple(e) for e in c['matching']}
    demand(n==24 and len(E)==len(c['edges'])==36,'graph_size')
    demand(all(0<=u<v<n for u,v in E),'graph_labels')
    deg=[sum(v in e for e in E) for v in range(n)]
    demand(deg==[3]*n,'graph_degree')
    matrix=[[int(key(u,v) in E) if u!=v else 0 for v in range(n)] for u in range(n)]
    demand(not any(matrix[a][b] and matrix[a][d] and matrix[b][d] for a,b,d in combinations(range(n),3)),'graph_triangle')
    deletion_cases=0
    # Repeated block union, separate from producer reached-set propagation.
    for size in range(3):
        for deleted in combinations(range(n),size):
            blocks=[{v} for v in range(n) if v not in deleted]
            for u,v in E:
                if u in deleted or v in deleted:continue
                i=next(i for i,s in enumerate(blocks) if u in s)
                j=next(i for i,s in enumerate(blocks) if v in s)
                if i!=j:
                    blocks[i]|=blocks[j];blocks.pop(j)
            demand(len(blocks)==1,'graph_connectivity');deletion_cases+=1
    cycles=c['cycles']
    demand(list(map(len,cycles))==[8,8,8] and sorted(sum(cycles,[]))==list(range(n)),'cycle_cover')
    F={key(x[i],x[(i+1)%8]) for x in cycles for i in range(8)}
    demand(len(M)==12 and sorted(v for e in M for v in e)==list(range(n)),'perfect_matching')
    demand(not(F&M) and F|M==E,'cycle_matching_decomposition')
    demand(len(c['factor'])==8 and sorted(sum(c['factor'],[]))==list(range(n)),'factor_cover')
    used={key(p[i],p[i+1]) for p in c['factor'] for i in (0,1)}
    demand(used<=E and len(used&M)==3,'factor_edges')
    rows=[[] for _ in range(n)]
    for a,b,d in combinations(range(n),3):
        vs=(a,b,d)
        for center in vs:
            ends=[v for v in vs if v!=center]
            edges=(key(center,ends[0]),key(center,ends[1]))
            if all(e in E for e in edges):
                mask=sum(1<<v for v in vs);cost=sum(e in M for e in edges)
                for v in vs:rows[v].append((mask,cost))
    @lru_cache(None)
    def poly(mask):
        if poly.cache_info().currsize>100000:raise RuntimeError('state_budget')
        if not mask:return (1,)
        v=(mask&-mask).bit_length()-1;out=[0]*9
        for block,cost in rows[v]:
            if block&mask==block:
                for k,count in enumerate(poly(mask^block)):
                    out[k+cost]+=count
        while len(out)>1 and out[-1]==0:out.pop()
        return tuple(out)
    polynomial=poly((1<<n)-1)
    demand(polynomial[:3]==(0,0,0) and polynomial[3]>0,'cost_bound')
    owner={v:i for i,x in enumerate(cycles) for v in x}
    pos={v:j for x in cycles for j,v in enumerate(x)}
    cert=[];ml=sorted(M)
    for size in range(3):
        for indices in combinations(range(len(ml)),size):
            S=[ml[i] for i in indices]
            incident={i:[] for i in range(3)}
            for u,v in S:
                if owner[u]!=owner[v]:
                    incident[owner[u]].append((u,v));incident[owner[v]].append((v,u))
            isolated=next((i for i in range(3) if not incident[i]),None)
            if isolated is not None:
                cert.append({'S_indices':list(indices),'reason':'isolated_nondisible_cycle','cycle':isolated})
            else:
                middle=next(i for i in range(3) if len(incident[i])==2)
                u,v=[p[0] for p in incident[middle]]
                d=(pos[v]-pos[u])%8
                demand(d%3!=1,'unexpected_compatible_ports')
                cert.append({'S_indices':list(indices),'reason':'AA_gap_remainder','middle':middle,
                             'ports':[u,v],'gap_distances':[d,8-d]})
    demand(len(cert)==79,'subset_coverage')
    return {'bits':c['bits'],'factor_polynomial':polynomial,'total_factors':sum(polynomial),
            'states':poly.cache_info().currsize,'vertex_deletions':deletion_cases},cert

raw=Path('explore24.stdout.json').read_bytes();data=json.loads(raw)
results=[];certificate=None
for c in data['cases']:
    r,cert=audit(c);results.append(r)
    if c['bits']==[0,0,0]:certificate=cert
# Mutate the compact restriction proof, not just its content hash.
def certificate_valid(cert,c):
    reference=audit(c)[1]
    return cert==reference
demand(certificate_valid(certificate,data['cases'][0]),'valid_certificate_rejected')
bad=list(certificate);bad.pop()
demand(not certificate_valid(bad,data['cases'][0]),'omitted_case_accepted')
bad=json.loads(json.dumps(certificate));j=next(i for i,r in enumerate(bad) if r['reason']=='AA_gap_remainder')
bad[j]['gap_distances'][0]=1
demand(not certificate_valid(bad,data['cases'][0]),'forged_gap_accepted')
print(json.dumps({'verdict':'candidate_only','status':'PASS','input_sha256':hashlib.sha256(raw).hexdigest(),
      'cases':results,'cost_at_most_two_certificate_for_case_000':certificate,
      'certificate_mutations_rejected':['omitted_subset','forged_gap'],
      'warning':'Restricted cost UNSAT only; all eight hosts have displayed P3-factors.',
      'trusted_attestation':None},sort_keys=True,separators=(',',':')))
