#!/usr/bin/env python3
"""Second consumer: explicit adjacency matrix, partition merging and full DAG checks.
Imports neither allocation.py, direct_cover.py nor any old candidate checker.
"""
import itertools,json,copy
from pathlib import Path

def require(p,msg):
    if not p:raise ValueError(msg)

def graph_check(x):
    n=x['n'];E=[tuple(e) for e in x['edges']];M=[tuple(e) for e in x['matching']]
    require(n%6==0 and n>=6,'order')
    require(len(E)==len(set(E)) and len(E)==3*n//2,'edge_count')
    require(all(0<=u<v<n for u,v in E),'edge_labels')
    A=[[False]*n for _ in range(n)]
    for u,v in E:A[u][v]=A[v][u]=True
    require(all(sum(row)==3 for row in A),'degree')
    require(not any(A[u][v] and A[v][w] and A[u][w] for u,v,w in itertools.combinations(range(n),3)),'triangle')
    require(len(M)==n//2 and sorted(v for e in M for v in e)==list(range(n)) and set(M)<=set(E),'matching')
    cycles=x['cycles'];require(sorted(v for c in cycles for v in c)==list(range(n)),'cycle_vertices')
    F=set()
    for c in cycles:
        require(len(c)>=4,'cycle_length')
        for i in range(len(c)):F.add(tuple(sorted((c[i],c[(i+1)%len(c)]))))
    require(F==set(E)-set(M),'cycle_edges')
    checked=0
    for k in (0,1,2):
        for cut in itertools.combinations(range(n),k):
            live=set(range(n))-set(cut);parts=[{v}for v in live]
            for u,v in E:
                if u not in live or v not in live:continue
                p=next(i for i,B in enumerate(parts)if u in B);q=next(i for i,B in enumerate(parts)if v in B)
                if p!=q:parts[p]|=parts[q];parts.pop(q)
            require(len(parts)==1,'vertex_cut');checked+=1
    return checked

def rows(x):
    # Neighborhood-pair generation, distinct from producer's unordered triples.
    E=set(map(tuple,x['edges']));M=set(map(tuple,x['matching']));out=[]
    for c in range(x['n']):
        neighbors=[v for v in range(x['n']) if tuple(sorted((v,c))) in E]
        for u,v in itertools.combinations(neighbors,2):
            es=[tuple(sorted((c,u))),tuple(sorted((c,v)))];cost=sum(e in M for e in es)
            out.append((frozenset((u,c,v)),cost))
    return out

def check_dag(x,cert):
    require(cert['n']==x['n'] and cert['budget']==3,'dag_scope')
    rs=rows(x);ns={(int(m,16),b):v for m,b,v in cert['nodes']}
    require(len(ns)==len(cert['nodes']),'dag_duplicate')
    root=(int(cert['root'],16),3);require(root==((1<<x['n'])-1,3),'dag_root')
    done=set();todo=[root]
    for key in todo:
        if key in done:continue
        require(key in ns,'dag_missing_child');done.add(key)
        mask,b=key;v=ns[key];live=frozenset(i for i in range(x['n'])if mask>>i&1)
        require(live and v in live and b>=0,'dag_pivot')
        for vs,cost in rs:
            if v in vs and vs<=live and cost<=b:
                child=(mask-sum(1<<u for u in vs),b-cost)
                require(child[0]!=0,'dag_contains_solution')
                require(child in ns,'dag_missing_child');todo.append(child)
    require(len(done)==len(ns),'dag_unreachable')
    return len(done)

def check_factor(x,p,S=None,roles=None):
    require(all(len(t)==3 and len(set(t))==3 for t in p),'factor_distinct')
    require(sorted(v for t in p for v in t)==list(range(x['n'])),'factor_cover')
    E=set(map(tuple,x['edges']));M=[tuple(e)for e in x['matching']];used=[];derived={}
    for u,c,v in p:
        for leaf in (u,v):
            e=tuple(sorted((leaf,c)));require(e in E,'factor_nonedge')
            if e in M:used.append(M.index(e));derived[str(c)]='B';derived[str(leaf)]='A'
    if S is not None:require(sorted(used)==sorted(S),'factor_matching')
    if roles is not None:require(roles==derived,'factor_roles')
    return used

def check_system(x,S,y):
    require(y['S']==S and len(S)==len(set(S)),'selected_duplicate')
    owner={v:i for i in S for v in x['matching'][i]};expected=[];unt=[]
    for ci,c in enumerate(x['cycles']):
        act=[v for v in c if v in owner]
        if not act:unt.append(ci);continue
        for j,v in enumerate(act):
            w=act[(j+1)%len(act)];p=c.index(v);inside=[];cur=(p+1)%len(c)
            while c[cur]!=w:inside.append(c[cur]);cur=(cur+1)%len(c)
            expected.append({'cycle':ci,'ends':[v,w],'owners':[owner[v],owner[w]],'distance':len(inside)+1,
                             'demand':len(inside)%3,'internal':inside})
    require(y=={'S':S,'gaps':expected,'untouched':unt},'gap_system')

def check_allocation(x,S,w):
    check_factor(x,w['factor'],S,w['roles'])
    # An allocation record must spend each selected owner once and no gap vertex twice.
    owner={v:i for i in S for v in x['matching'][i]};gaps=[]
    for c in x['cycles']:
        act=[j for j,v in enumerate(c)if v in owner]
        for k,p in enumerate(act):
            q=act[(k+1)%len(act)];d=(q-p)%len(c)or len(c)
            gaps.append(([c[p],c[q]],[c[(p+j)%len(c)]for j in range(1,d)]))
    spent=[];taken=[];tot=[0]*len(gaps)
    for gi,side in w['allocation']:
        require(0<=gi<len(gaps) and side in (0,1),'allocation_index');ends,inside=gaps[gi]
        require(inside,'empty_gap');v=ends[side];z=inside[0 if side==0 else -1]
        spent.append(owner[v]);taken.append(z);tot[gi]+=1
        require(w['roles'][str(v)]=='B','allocation_role')
        require(any(t[1]==v and z in (t[0],t[2]) for t in w['factor']),'allocation_factor')
    require(sorted(spent)==sorted(S) and len(taken)==len(set(taken)),'allocation_supply')
    require(tot==[len(inside)%3 for ends,inside in gaps],'allocation_demand')

def main():
    x=json.loads(Path('objects.json').read_text());r=json.loads(Path('allocation-results.json').read_text());dag=json.loads(Path('negative-42.json').read_text())
    g=x['control24'];g42=x['new42'];checks=[graph_check(g),graph_check(g42)]
    ports={0,1,3,6};seen=set()
    for lo,hi,u,v in r['connectivity_port_free_intervals']:
        interval=set(range(lo,hi+1));boundary={(lo-1)%14,(hi+1)%14}
        require(0<=lo<=hi<14 and not interval&ports,'interval_domain')
        require(tuple(sorted((u,v)))in set(map(tuple,g42['matching'])),'interval_chord')
        require(len({u,v}&interval)==1 and not {u,v}&boundary,'interval_escape')
        seen.add((lo,hi))
    all_intervals={(a,b)for a in range(14)for b in range(a,14)if not set(range(a,b+1))&ports}
    require(seen==all_intervals and len(seen)==32,'interval_exhaustion')
    nodes=check_dag(g42,dag);w=r['new42_cost4_witness'];check_allocation(g42,w['S'],w)
    trap=r['trap'];check_system(g,trap['S'],trap['system']);escape=trap['escape_factor']
    target=trap['escape_masks'][-1];S=[i for i in range(12)if target>>i&1];check_allocation(g,S,escape)
    muts=[]
    def reject(name,fn):
        try:fn()
        except ValueError as e:muts.append({'name':name,'rejected':True,'first_failure':str(e)});return
        raise ValueError('mutation_accepted:'+name)
    y=copy.deepcopy(g);y['edges'][0]=y['edges'][1];reject('duplicate_host_edge',lambda:graph_check(y))
    y=copy.deepcopy(g);y['edges'].pop();reject('delete_host_edge',lambda:graph_check(y))
    y=copy.deepcopy(g);y['matching'][0]=y['matching'][1];reject('repeated_matching_owner',lambda:graph_check(y))
    y=copy.deepcopy(g);y['matching'][0]=[0,2];reject('nonedge_in_matching',lambda:graph_check(y))
    y=copy.deepcopy(g);y['cycles'][0][1]=0;reject('cycle_repeated_vertex',lambda:graph_check(y))
    y=copy.deepcopy(trap['system']);y['S'].append(0);reject('selected_owner_twice',lambda:check_system(g,[0,3,0],y))
    y=copy.deepcopy(trap['system']);y['gaps'][0]['distance']+=1;reject('gap_distance_mutation',lambda:check_system(g,[0,3],y))
    y=copy.deepcopy(trap['system']);y['gaps'][0]['demand']=0;reject('gap_residue_mutation',lambda:check_system(g,[0,3],y))
    y=copy.deepcopy(trap['system']);y['gaps'][2]['ends'][1]=10;reject('erase_wrap_incidence',lambda:check_system(g,[0,3],y))
    y=copy.deepcopy(w);v=next(v for v in y['roles']if y['roles'][v]=='B');y['roles'][v]='A';reject('flip_center_endpoint_role',lambda:check_allocation(g42,w['S'],y))
    y=copy.deepcopy(w);y['allocation'].append(y['allocation'][0]);reject('double_extension',lambda:check_allocation(g42,w['S'],y))
    y=copy.deepcopy(w);y['factor'][0][0]=y['factor'][0][1];reject('P3_repeated_vertex',lambda:check_allocation(g42,w['S'],y))
    y=copy.deepcopy(w);y['factor'][0][0],y['factor'][1][0]=y['factor'][1][0],y['factor'][0][0];reject('P3_nonedge',lambda:check_allocation(g42,w['S'],y))
    y=copy.deepcopy(dag);y['nodes'].pop(0);reject('missing_negative_child',lambda:check_dag(g42,y))
    y=copy.deepcopy(dag);y['budget']=4;reject('wrong_negative_budget',lambda:check_dag(g42,y))
    y=copy.deepcopy(dag);y['nodes'][0][2]=x['new42']['n'];reject('invalid_negative_pivot',lambda:check_dag(g42,y))
    y=copy.deepcopy(w);y['S']=y['S'][:-1];reject('pretend_cost_three_factor',lambda:check_allocation(g42,y['S'],y))
    print(json.dumps({'status':'PASS','vertex_deletion_counts':checks,'negative42_nodes_rechecked':nodes,
          'positive42_matching_use':len(w['S']),'mutations':muts,'trust':'same_generation_domain',
          'verdict':'candidate_only'},sort_keys=True))
if __name__=='__main__':main()
