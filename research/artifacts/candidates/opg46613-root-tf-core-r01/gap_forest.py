#!/usr/bin/env python3
"""Exact fixed-M subset criterion via a gap-demand multigraph; no old imports.
Enumerates all subsets of the 18-edge matching of ONE graph, not graph orders.
"""
import hashlib,itertools,json,pathlib,resource,time
B=pathlib.Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_CPU,(30,30))
resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
resource.setrlimit(resource.RLIMIT_FSIZE,(2097152,2097152))
def require(p,s):
    if not p:raise ValueError(s)
def criterion(cycles,matching,ids,detail=False):
    owner={v:i for i in ids for v in matching[i]}
    force={i:0 for i in ids};adj={i:[] for i in ids};mult=1;gaps=[];edges=[];untouched=0
    for ci,c in enumerate(cycles):
        active=[j for j,v in enumerate(c) if v in owner]
        if not active:
            if len(c)%3:return (0,None)
            mult*=3;untouched+=1;continue
        for t,p in enumerate(active):
            q=active[(t+1)%len(active)];d=(q-p)%len(c) or len(c)
            r=(d-1)%3;u=owner[c[p]];v=owner[c[q]]
            if detail:gaps.append({'cycle':ci,'ports':[c[p],c[q]],'distance':d,'demand':r,'owners':[u,v]})
            if r==2:force[u]+=1;force[v]+=1
            if r==1:
                k=len(edges);edges.append((u,v));adj[u].append(k);adj[v].append(k)
    if any(x>1 for x in force.values()):return (0,None)
    remaining=set(ids);comps=[]
    while remaining:
        todo=[min(remaining)];vs=set();ee=set()
        while todo:
            u=todo.pop()
            if u in vs:continue
            vs.add(u)
            for k in adj[u]:
                ee.add(k);a,b=edges[k];todo.append(b if a==u else a)
        remaining-=vs;f=sum(force[u] for u in vs);v=len(vs);e=len(ee)
        if f==1 and e==v-1:kind='tree_with_one_forced_vertex'
        elif f==0 and e==v:kind='unicyclic_without_forcing';mult*=2
        else:return (0,None)
        if detail:comps.append({'owners':sorted(vs),'gap_edges':[list(edges[k]) for k in sorted(ee)],'forces':f,'kind':kind})
    return mult,({'selected_matching_indices':list(ids),'gaps':gaps,'forced_incidence_counts':force,'components':comps,'untouched_cycles':untouched} if detail else None)

def main():
    start=time.monotonic();raw=(B/'input.json').read_bytes();x=json.loads(raw)
    m=sorted(map(tuple,x['perfect_matching']));cs=x['cycles'];hist={i:0 for i in range(len(m)+1)};feasible=hist.copy();first=None;checked=0
    for mask in range(1<<len(m)):
        ids=[i for i in range(len(m)) if mask>>i&1];ways,_=criterion(cs,m,ids)
        hist[len(ids)]+=ways;feasible[len(ids)]+=bool(ways);checked+=1
        if ways and (first is None or len(ids)<len(first['selected_matching_indices'])):_,first=criterion(cs,m,ids,True)
        if checked%4096==0 and time.monotonic()-start>26:raise TimeoutError('subset_search_deadline')
    out={'status':'PASS','verdict':'candidate_only','method':'gap-demand multigraph components','matching':m,'subsets_checked':checked,
      'feasible_subsets_by_cost':feasible,'factor_counts_by_cost':hist,'total_factors':sum(hist.values()),'first_minimum_certificate':first,
      'input_sha256':hashlib.sha256(raw).hexdigest(),'scope':'Complete matching-subset search on one fixed graph; no graph-order census or universal selection theorem.'}
    require(checked==262144 and sum(hist.values())==9360 and hist[0]==hist[1]==hist[2]==0 and hist[3]==76,'cross_check_mismatch')
    print(json.dumps(out,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
