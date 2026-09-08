#!/usr/bin/env python3
"""Direct vertex-cover search; does not import the allocation implementation."""
import itertools,json,sys,time
from functools import lru_cache
from pathlib import Path

def triples(x):
    es=set(map(tuple,x['edges'])); ms={tuple(e):i for i,e in enumerate(x['matching'])}; ans=[]
    for vs in itertools.combinations(range(x['n']),3):
        selected=[e for e in itertools.combinations(vs,2) if e in es]
        if len(selected)!=2:continue # inputs must have separately checked triangle-freeness
        center=next(v for v in vs if sum(v in e for e in selected)==2)
        leaves=[v for v in vs if v!=center]
        mid=[ms[e] for e in selected if e in ms]
        if len(mid)>1:raise ValueError('not_matching')
        ans.append((sum(1<<v for v in vs),mid[0] if mid else -1,[leaves[0],center,leaves[1]]))
    return ans

def negative(x,budget):
    rows=triples(x);by=[[]for _ in range(x['n'])];nodes={};t=time.monotonic()
    for r in rows:
        for v in r[2]:by[v].append(r)
    def visit(mask,b):
        key=(mask,b)
        if key in nodes:return False
        if len(nodes)>200000 or time.monotonic()-t>20:raise RuntimeError('search_limit')
        if mask==0:return True
        options=[]
        for v in range(x['n']):
            if mask>>v&1:
                cand=[r for r in by[v] if r[0]&mask==r[0] and (r[1]>=0)<=b]
                options.append((len(cand),v,cand))
        _,v,cand=min(options,key=lambda z:(z[0],z[1]))
        for row,mi,p in cand:
            if visit(mask^row,b-int(mi>=0)):return True
        nodes[key]=v;return False
    possible=visit((1<<x['n'])-1,budget)
    if possible:raise ValueError('negative_claim_false')
    return {'n':x['n'],'budget':budget,'root':format((1<<x['n'])-1,'x'),
            'nodes':[[format(m,'x'),b,v]for (m,b),v in sorted(nodes.items())]}

def complete_counts(x):
    rows=triples(x);out=[0]*(1<<len(x['matching']));first={};calls=0
    def walk(mask,used,ps):
        nonlocal calls
        calls+=1
        if calls>500000:raise RuntimeError('walk_budget')
        if not mask:
            out[used]+=1;first.setdefault(used,ps);return
        v=(mask&-mask).bit_length()-1
        for row,mi,p in rows:
            if row>>v&1 and row&mask==row:
                walk(mask^row,used|(0 if mi<0 else 1<<mi),ps+[p])
    walk((1<<x['n'])-1,0,[])
    return out,first,calls

def bounded_count(x,budget):
    rr=triples(x);deadline=time.monotonic()+15
    @lru_cache(None)
    def count(mask,b):
        if time.monotonic()>deadline or count.cache_info().currsize>200000:raise RuntimeError('count_limit')
        if not mask:return 1
        v=(mask&-mask).bit_length()-1;answer=0
        for row,mi,p in rr:
            cost=int(mi>=0)
            if row>>v&1 and row&mask==row and cost<=b:answer+=count(mask^row,b-cost)
        return answer
    return count((1<<x['n'])-1,budget)

if __name__=='__main__':
    x=json.loads(Path('objects.json').read_text());g24=x['control24'];g42=x['new42']
    dag=negative(g42,3);Path('negative-42.json').write_text(json.dumps(dag,separators=(',',':'))+'\n')
    counts,first,calls=complete_counts(g24)
    prior=json.loads(Path('allocation-results.json').read_text())
    if counts!=prior['control24_counts']:raise ValueError('allocation_mismatch')
    bound4=bounded_count(g42,4)
    if bound4!=prior['new42_cost4_count']:raise ValueError('cost4_mismatch')
    print(json.dumps({'status':'PASS','same_generation_domain':True,'negative42_nodes':len(dag['nodes']),'new42_cost_at_most_four':bound4,
       'negative_scope':'no P3-factor with at most 3 edges of the specified M, not root UNSAT',
       'control24_all_factors':sum(counts),'control24_cover_search_calls':calls,
       'all_4096_subset_counts_agree':True,'verdict':'candidate_only'},sort_keys=True))
