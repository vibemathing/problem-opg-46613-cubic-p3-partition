#!/usr/bin/env python3
"""Frozen allocation experiments; independent of all prior constructors."""
import allocation as a
import itertools,json,hashlib,copy,time
from collections import Counter
from pathlib import Path

def hist(values):return {str(k):v for k,v in sorted(Counter(values).items())}

def main():
    x=json.loads(Path('objects.json').read_text());g=x['control24'];g42=x['new42']
    a.validate(g);a.validate(g42)
    counts=[];phis=[];factors={};three=Counter()
    for mask in range(4096):
        S=[i for i in range(12) if mask>>i&1];y=a.system(g,S)
        k,w=a.count_and_lift(g,y);d=a.deficiency(g,y)
        a.need((d['conflict']==0)==bool(k),'feasibility_equivalence')
        counts.append(k);phis.append(d['conflict'])
        if k:
            factors[str(mask)]=w
            if len(S)==3:
                active=set(v for i in S for v in g['matching'][i]);h=tuple(sorted(sum(v in active for v in c) for c in g['cycles']))
                a.need(h in ((1,1,4),(1,2,3)),'three_edge_classification');three[str(h)]+=k
    mask=9;neighbors=[{'toggle':i,'new_mask':mask^(1<<i),'conflict':phis[mask^(1<<i)]}for i in range(12)]
    a.need(phis[mask]>0 and all(t['conflict']>=phis[mask]for t in neighbors),'strict_descent_trap')
    target=min((int(k)for k in factors),key=lambda k:((k^mask).bit_count(),k))
    a.need((mask^target).bit_count()==2,'escape_distance')
    trail=[mask];cur=mask
    for i in range(12):
        if (mask^target)>>i&1:cur^=1<<i;trail.append(cur)
    negative=[];cost4=0;w4=None
    for k in range(5):
        for S in itertools.combinations(range(21),k):
            y=a.system(g42,S);d=a.deficiency(g42,y);count,w=a.count_and_lift(g42,y)
            a.need((d['conflict']==0)==bool(count),'42_agreement')
            if k<=3:
                a.need(not count,'cost_three_obstruction');negative.append([sum(1<<i for i in S),d['demand'],d['matched'],len(d['untouched_bad'])])
            else:
                cost4+=count
                if count and w4 is None:w4={'S':list(S),**w}
    a.need(w4 is not None,'positive_host')
    local=[]
    for u,v in itertools.product([0,1],[3,6]):
        for e in [[2,9],[4,8],[5,12],[7,11],[10,13]]:
            p=sorted([u,v,*e]);ds=[(p[(j+1)%4]-p[j])%14 for j in range(4)];r=[(d-1)%3 for d in ds]
            one=[j for j in range(4) if r[j]]
            reason='total_demand_not_one' if sum(r)!=1 else 'only_demand_bounded_by_two_A_ports'
            if sum(r)==1:a.need(set([p[one[0]],p[(one[0]+1)%4]])=={u,v},'local_obstruction')
            local.append({'external_A':[u,v],'chord':e,'positions':p,'r':r,'reason':reason})
    port_free=[]
    ports={0,1,3,6};chords=[[2,9],[4,8],[5,12],[7,11],[10,13]]
    for lo in range(14):
        for hi in range(lo,14):
            interval=set(range(lo,hi+1))
            if interval&ports:continue
            boundary={(lo-1)%14,(hi+1)%14}
            witness=next((e for e in chords if len(set(e)&interval)==1 and not set(e)&boundary),None)
            a.need(witness is not None,'port_free_interval_cut')
            port_free.append([lo,hi,*witness])
    a.need(len(port_free)==32,'interval_count')
    results={'connectivity_port_free_intervals':port_free,'control24_counts':counts,'control24_conflicts':phis,'three_edge_factor_types':dict(three),
      'control24_total':sum(counts),'control24_feasible_subsets':sum(k>0 for k in counts),
      'trap':{'mask':mask,'S':[0,3],'system':a.system(g,[0,3]),'deficiency':a.deficiency(g,a.system(g,[0,3])),
              'all_toggle_neighbors':neighbors,'escape_masks':trail,'escape_conflicts':[phis[t]for t in trail],
              'escape_factor':factors[str(target)]},
      'new42_restricted_negative':negative,'new42_cost4_count':cost4,'new42_cost4_witness':w4,
      'new42_twenty_local_cases':local,'verdict':'candidate_only'}
    Path('allocation-results.json').write_text(json.dumps(results,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'PASS','control24_total':sum(counts),'control24_feasible_subsets':sum(k>0 for k in counts),
        'three_edge_types':dict(three),'new42_subsets_cost_le3':len(negative),'new42_cost4_factor_count':cost4,
        'trap_masks':trail,'trap_conflicts':[phis[t]for t in trail],
        'verdict':'candidate_only'},sort_keys=True))
if __name__=='__main__':main()
