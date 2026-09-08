#!/usr/bin/env python3
"""Separate consumer: successor walks, matrix flow, complete certificate checks.
No producer or historical verifier imports. Same generator trust domain.
"""
import copy,json
from collections import deque
from itertools import combinations,combinations_with_replacement,product
from pathlib import Path


def need(ok,why):
    if not ok:raise ValueError(why)


def graph(g,check_cuts=False):
    n=g['n'];need(n>0 and n%6==0,'host_order');A=[[0]*n for _ in range(n)]
    for a,b in g['edges']:
        need(a!=b and 0<=a<n and 0<=b<n and not A[a][b],'host_edge');A[a][b]=A[b][a]=1
    need(all(sum(row)==3 for row in A),'host_degree')
    need(not any(A[a][b] and A[a][c] and A[b][c] for a,b,c in combinations(range(n),3)),'host_triangle')
    need(sorted(v for e in g['matching'] for v in e)==list(range(n)),'matching_partition')
    need(all(A[a][b] for a,b in g['matching']),'matching_edge')
    need(sorted(v for c in g['cycles'] for v in c)==list(range(n)),'cycle_partition');occupied=[[0]*n for _ in range(n)]
    for c in g['cycles']:
        need(len(c)>=4,'cycle_length')
        for a,b in zip(c,c[1:]+c[:1]):occupied[a][b]=occupied[b][a]=1
    for a,b in g['matching']:
        need(not occupied[a][b],'matching_cycle_overlap');occupied[a][b]=occupied[b][a]=1
    need(A==occupied,'decomposition_edges');count=0
    if check_cuts:
        for k in range(3):
            for deleted in combinations(range(n),k):
                avail=set(range(n))-set(deleted);visited={min(avail)}
                while True:
                    more=visited|{v for u in visited for v in avail if A[u][v]}
                    if more==visited:break
                    visited=more
                need(visited==avail,'host_vertex_cut');count+=1
    return count


def flow(neighbors,supplies):
    ids={v:i for i,v in enumerate(supplies)};d=len(neighbors);s=len(supplies);N=d+s+2;source=N-2;sink=N-1;C=[[0]*N for _ in range(N)]
    for j,vs in enumerate(neighbors):
        C[source][j]=1
        for v in vs:C[j][d+ids[v]]=1
    for i in range(s):C[d+i][sink]=1
    total=0
    while True:
        pred={source:None};q=deque([source])
        while q and sink not in pred:
            u=q.popleft()
            for v,c in enumerate(C[u]):
                if c and v not in pred:pred[v]=u;q.append(v)
        if sink not in pred:return total
        v=sink
        while pred[v] is not None:
            u=pred[v];C[u][v]-=1;C[v][u]+=1;v=u
        total+=1


def rebuild(g,S):
    need(len(S)==len(set(S)) and all(type(i) is int and 0<=i<len(g['matching']) for i in S),'selected_supply')
    S=sorted(S);owners={v:i for i in S for v in g['matching'][i]};gaps=[];slots=[];untouched=[]
    for ci,c in enumerate(g['cycles']):
        successor=dict(zip(c,c[1:]+c[:1]));active=[v for v in c if v in owners]
        if not active:untouched.append({'cycle':ci,'length':len(c),'residue':len(c)%3});continue
        for a in active:
            path=[a];v=successor[a]
            while v not in owners:path.append(v);v=successor[v]
            path.append(v);d=len(path)-1;r=(d-1)%3
            gaps.append({'cycle':ci,'ends':[a,v],'owners':[owners[a],owners[v]],'distance':d,'demand':r,'path':path})
            for unit in range(r):slots.append({'gap':len(gaps)-1,'unit':unit,'ends':[owners[a],owners[v]]})
    pending=set(S);components=[]
    while pending:
        got={min(pending)}
        while True:
            more=got|{v for e in slots if got.intersection(e['ends']) for v in e['ends']}
            if got==more:break
            got=more
        pending-=got;indices=[i for i,e in enumerate(slots) if e['ends'][0] in got]
        components.append({'owners':sorted(got),'slots':indices,'vertices':len(got),'edges':len(indices),'excess':len(indices)-len(got)})
    nu=flow([s['ends'] for s in slots],S);u=sum(c['residue']!=0 for c in untouched)
    trees=sum(c['edges']<c['vertices'] for c in components);excess=sum(max(c['excess'],0) for c in components)
    kappa=len(S)+len(slots)-2*nu+3*u;need(kappa==trees+excess+3*u,'euler_rank_identity')
    return {'selected':S,'s':len(S),'D':len(slots),'u':u,'nu':nu,'tree_count':trees,'excess':excess,'kappa':kappa,
            'gaps':gaps,'slots':slots,'untouched':untouched,'components':components}


def check_state(g,claimed):
    real=rebuild(g,claimed['selected'])
    for k,v in claimed.items():
        if k in real:need(v==real[k],'state_'+k)
    return real


def hall(st,cert):
    ids=cert['slot_ids'];need(len(ids)==len(set(ids)) and all(0<=i<len(st['slots']) for i in ids),'hall_ids')
    rows=[st['slots'][i]['ends'] for i in ids];neighbors=sorted({v for e in rows for v in e})
    need(neighbors==cert['neighbors'],'hall_neighbors');need(len(ids)==len(neighbors)+1 and cert['deficiency']==1,'hall_deficiency')
    need(flow(rows,neighbors)==len(ids)-1,'hall_rank')
    for k in range(len(rows)):need(flow(rows[:k]+rows[k+1:],neighbors)==len(rows)-1,'hall_not_minimal')
    degree={v:sum(e.count(v) for e in rows) for v in neighbors}
    need(min(degree.values())>=2,'hall_leaf');need(sorted(d for d in degree.values() if d>2) in ([4],[3,3]),'hall_shape')


def matching(st,rows):
    need(len(rows)==len({a for a,b in rows})==len({b for a,b in rows}),'matching_injective')
    need(all(0<=j<len(st['slots']) and e in st['slots'][j]['ends'] for j,e in rows),'matching_incidence');return dict(rows)


def factor(g,paths,S,roles=None,st=None):
    need(all(len(p)==3 for p in paths) and sorted(v for p in paths for v in p)==list(range(g['n'])),'factor_partition')
    E={tuple(sorted(e)) for e in g['edges']};selected_edges=set();centers={}
    for p in paths:
        for j in (0,1):
            edge=tuple(sorted((p[j],p[j+1])));need(edge in E,'factor_nonedge');selected_edges.add(edge)
        centers[p[1]]=p
    actual=[i for i,e in enumerate(g['matching']) if tuple(sorted(e)) in selected_edges];need(actual==sorted(S),'factor_matching_set')
    if roles is not None:
        need(set(roles)==set(map(str,S)),'factor_role_keys')
        for i in S:
            role=roles[str(i)];a,b=g['matching'][i];need((a in centers)^(b in centers),'factor_center_incidence')
            center=a if a in centers else b;leaf=b if center==a else a;p=centers[center];other=next(v for v in p if v not in (a,b))
            need(role['B']==center and role['A']==leaf and role['neighbor']==other,'factor_role')
            gap=st['gaps'][role['gap']];side=role['side'];need(side in (0,1) and gap['ends'][side]==center,'factor_gap_side')
            need((gap['path'][1] if side==0 else gap['path'][-2])==other,'factor_gap_neighbor')


def trace(g,t):
    a=check_state(g,t['before']);b=check_state(g,t['after'])
    need(t['remove']==sorted(set(a['selected'])-set(b['selected'])) and t['add']==sorted(set(b['selected'])-set(a['selected'])),'trace_set_change')
    changed={v for e in set(a['selected'])^set(b['selected']) for v in g['matching'][e]}
    need(t['changed_cycles']==[i for i,c in enumerate(g['cycles']) if set(c)&changed],'trace_cycles')
    old=matching(a,t['old_matching']);need(len(old)==a['nu'],'old_maximum')
    def key(st,j):
        x=st['slots'][j];h=st['gaps'][x['gap']];return(h['cycle'],tuple(h['path']),tuple(h['owners']),x['unit'])
    index={key(b,j):j for j in range(len(b['slots']))};retained={index[key(a,j)]:e for j,e in old.items() if key(a,j) in index and e in b['selected']}
    need(dict(t['retained_matching'])==retained,'retained_incidence');cur=dict(retained)
    for p in t['augmenting_paths']:
        need(len(p)>=2 and len(p)%2==0 and len(set(map(tuple,p)))==len(p),'augment_simple')
        need(p[0][0]=='d' and p[-1][0]=='s' and p[0][1] not in cur and p[-1][1] not in cur.values(),'augment_endpoints')
        for i in range(0,len(p),2):
            need(p[i][0]=='d' and p[i+1][0]=='s','augment_types');j,e=p[i][1],p[i+1][1]
            need(e in b['slots'][j]['ends'],'augment_incidence')
            if i+2<len(p):need(cur.get(p[i+2][1])==e,'augment_reverse')
        for i in range(0,len(p),2):cur[p[i][1]]=p[i+1][1]
        matching(b,list(map(list,cur.items())))
    new=matching(b,t['new_matching']);need(new==cur and len(new)==b['nu'],'new_maximum')
    loss=len(old)-len(retained);gain=len(new)-len(retained);need(loss==t['loss'] and gain==t['gain'],'trace_loss_gain')
    delta=b['s']-a['s']+b['D']-a['D']+3*(b['u']-a['u'])+2*loss-2*gain
    need(delta==t['delta_kappa']==b['kappa']-a['kappa'] and delta<0,'trace_balance')
    hall(a,t['minimal_hall_before']);factor(g,t['factor']['paths'],b['selected'],t['factor']['roles'],b)


def primitive_check(g,q):
    a=rebuild(g,q['selected']);e=q['insert'];need(e not in a['selected'] and a['u']==0,'primitive_domain');loc=[]
    for v in g['matching'][e]:
        j,h=next((j,h) for j,h in enumerate(a['gaps']) if v in h['path'][1:-1]);k=h['path'].index(v)
        loc.append((j,h,((k-1)%3,(h['distance']-k-1)%3)))
    need(loc[0][0]!=loc[1][0],'primitive_distinct_gaps');comp={v:c for c in a['components'] for v in c['owners']}
    if q['rule']=='tree_bicycle_cycle_transfer':
        need(a['tree_count']==a['excess']==1,'primitive_components');ok=False
        for j in (0,1):
            tr,bc=loc[j],loc[1-j]
            if bc[1]['demand']!=1 or bc[2]!=(0,0) or sum(tr[2])-tr[1]['demand']!=2:continue
            vs={tr[1]['owners'][k] for k in (0,1) if tr[2][k]}
            if tr[1]['demand']:vs.update(tr[1]['owners'])
            tree=comp[next(iter(vs))];bike=comp[bc[1]['owners'][0]]
            if tree['excess']!=-1 or not vs.issubset(tree['owners']) or bike['excess']!=1:continue
            got={bike['owners'][0]};es=[x['ends'] for x in a['slots'] if x['gap']!=bc[0]]
            while True:
                more=got|{v for edge in es if got.intersection(edge) for v in edge}
                if more==got:break
                got=more
            if got==set(bike['owners']):ok=True
        need(ok,'primitive_transfer_hypotheses')
    elif q['rule']=='excess_three_to_tree_bicycle':
        need(a['tree_count']==0 and a['excess']==3,'primitive_components')
        need(all(h['demand']==1 and r==(0,0) for j,h,r in loc),'primitive_low_splits')
        omit={j for j,h,r in loc};es=[x['ends'] for x in a['slots'] if x['gap'] not in omit]
        need(flow(es,a['selected'])==len(a['selected']),'primitive_removal_rank')
    elif q['rule']=='three_tree_merge':
        need(a['tree_count']==3 and a['excess']==0,'primitive_components')
        need(all(h['demand']==0 and r==(1,1) for j,h,r in loc),'primitive_high_splits')
        touched={v for j,h,r in loc for v in h['owners']};need(all(touched.intersection(c['owners']) for c in a['components'] if c['excess']==-1),'primitive_tree_coverage')
    else:raise ValueError('primitive_rule')
    b=rebuild(g,sorted(set(a['selected'])|{e}));need(q['before']==a['kappa'] and q['after']==b['kappa']<a['kappa'],'primitive_gain')


def abstract_crosscheck():
    def rank(n,edges):
        used={0}
        for a,b in edges:used|={m|(1<<v) for m in list(used) for v in (a,b) if not (m>>v)&1}
        return max(m.bit_count() for m in used)
    def val(n,es):return n+len(es)-2*rank(n,es)
    count=0
    for n in range(1,4):
        pp=list(combinations_with_replacement(range(n),2))
        for mul in product(range(3),repeat=len(pp)):
            es=[list(p) for p,m in zip(pp,mul) for _ in range(m)];old=val(n,es)
            for (a,b),m in zip(pp,mul):
                for x,y in product(range(3),repeat=2):
                    r=(x+y+1)%3
                    if m<r:continue
                    for loops in (0,1):
                        new=es.copy()
                        for _ in range(r):new.remove([a,b])
                        new += [[a,n]]*x+[[b,n]]*y+[[n,n]]*loops
                        need(val(n+1,new)-old<=2,'abstract_activation');count+=1
    return count


def main():
    controls=json.loads(Path('../opg46613-root-tf-222-r01/objects.json').read_text());rows=json.loads(Path('new-hosts.json').read_text())['cases'];data=json.loads(Path('audit-data.json').read_text());deletions=0
    for row in rows:
        deletions+=graph(row['graph'],True);factor(row['graph'],row['factor'],row['selected']);need(row['global_minimum_kappa']==0,'global_minimum_claim');need(rebuild(row['graph'],row['selected'])['kappa']==0,'positive_normalization')
    for t in data['controls']:trace(controls[t['graph_ref']],t)
    need(check_state(controls['control24'],data['neutral_control24'])['kappa']==3,'neutral_step')
    for q in data['sampled_states']:check_state(rows[q['graph']]['graph'],q['state'])
    for q in data['activation_cases']:
        g=rows[q['graph']]['graph'];a=rebuild(g,q['selected']);b=rebuild(g,sorted(set(q['selected'])|{q['insert']}))
        need(any(x['cycle']==q['bad_cycle'] and x['residue'] for x in a['untouched']),'activation_bad_cycle');need(a['kappa']==q['before'] and b['kappa']==q['after']<a['kappa'],'activation_descent')
    for q in data['hall_certificates']:hall(rebuild(rows[q['graph']]['graph'],q['selected']),q['hall'])
    for q in data['two_edge_222_states']:
        st=check_state(rows[q['graph']]['graph'],q['state']);need(st['kappa'] in (0,3) and st['u']==0,'two_edge_upper_bound')
    for q in data['primitive_cases']:primitive_check(rows[q['graph']]['graph'],q)
    tests=[];t=data['controls'][0];g=controls['control24']
    def reject(name,operation,tag):
        try:operation()
        except ValueError as e:
            need(str(e)==tag,'mutation_wrong_failure_'+name);tests.append({'name':name,'first_failure':str(e),'rejected':True});return
        raise ValueError('mutation_accepted_'+name)
    def altered(key,value):
        st=copy.deepcopy(t['before']);st[key]=value;return lambda:check_state(g,st)
    reject('duplicate_supply',altered('selected',[0,0,3]),'selected_supply');reject('nonmatching_supply',altered('selected',[0,99]),'selected_supply')
    for label,key in [('wrong_demand','demand'),('wrong_distance','distance')]:
        st=copy.deepcopy(t['before']);st['gaps'][0][key]+=1;reject(label,lambda st=st:check_state(g,st),'state_gaps')
    st=copy.deepcopy(t['before']);st['gaps'][0]['path'][-1]=23;reject('wrong_wrap_endpoint',lambda:check_state(g,st),'state_gaps')
    st=copy.deepcopy(t['before']);st['slots']=st['slots'][1:];reject('erase_demand_unit',lambda:check_state(g,st),'state_slots')
    st=copy.deepcopy(t['before']);st['slots'].append(st['slots'][0]);reject('duplicate_demand_unit',lambda:check_state(g,st),'state_slots')
    reject('fake_maximum_rank',altered('nu',3),'state_nu');reject('false_zero_conflict',altered('kappa',0),'state_kappa')
    h=copy.deepcopy(t['minimal_hall_before']);h['neighbors']=h['neighbors'][:-1];reject('erase_hall_neighbor',lambda:hall(t['before'],h),'hall_neighbors')
    h=copy.deepcopy(t['minimal_hall_before']);h['slot_ids']=h['slot_ids'][:-1];reject('fake_deficient_set',lambda:hall(t['before'],h),'hall_deficiency')
    bad=copy.deepcopy(t);bad['factor']['paths'].pop();reject('missing_P3',lambda:trace(g,bad),'factor_partition')
    bad=copy.deepcopy(t);bad['factor']['paths'][0][0]=bad['factor']['paths'][0][1];reject('duplicate_P3_vertex',lambda:trace(g,bad),'factor_partition')
    bad=copy.deepcopy(t);bad['factor']['roles']['0']['B']=0;reject('reverse_AB_roles',lambda:trace(g,bad),'factor_role')
    bad=copy.deepcopy(t);bad['loss']+=1;reject('invent_matching_loss',lambda:trace(g,bad),'trace_loss_gain')
    bad=copy.deepcopy(t);bad['delta_kappa']=-9;reject('fake_exchange_gain',lambda:trace(g,bad),'trace_balance')
    bad=copy.deepcopy(t);bad['add']=[];reject('omit_simultaneous_additions',lambda:trace(g,bad),'trace_set_change')
    bad=copy.deepcopy(t);bad['changed_cycles']=[];reject('omit_changed_cycle',lambda:trace(g,bad),'trace_cycles')
    badg=copy.deepcopy(g);badg['matching'][0]=[0,1];reject('matching_not_partition',lambda:graph(badg),'matching_partition')
    count=abstract_crosscheck()
    print(json.dumps({'status':'PASS','verdict':'candidate_only','new_host_vertex_deletion_sets':deletions,'separate_implementation_abstract_cases':count,
                      'activation_cases':len(data['activation_cases']),'minimal_Hall_certificates':len(data['hall_certificates']),'primitive_cases':len(data['primitive_cases']),
                      'mutations':tests,'old_subset_censuses_repeated':False,'trusted_attestation':None},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
