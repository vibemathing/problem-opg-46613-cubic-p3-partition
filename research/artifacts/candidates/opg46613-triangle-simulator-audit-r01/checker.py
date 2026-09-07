#!/usr/bin/env python3
"""Fixed H/J/T audit. New exact-cover and frontier-search code; standard library only.
No old verifier modules are imported. All reported assurance is candidate_only.
"""
from __future__ import annotations
import copy
import hashlib
import itertools as it
import json
import pathlib
import platform
from functools import lru_cache

class Rejected(ValueError):
    pass

def require(ok, tag):
    if not ok:
        raise Rejected(tag)

def edge(a, b):
    return tuple(sorted((a, b)))

def adjacency(g):
    n=g['n']; es=g['edges']; ports=g['ports']
    require(type(n) is int and 3 <= n <= 100, 'order_bound')
    require(len(ports)==len(set(ports)) and all(0<=p<n for p in ports), 'ports')
    require(all(len(e)==2 and all(type(v) is int and 0<=v<n for v in e) and e[0]<e[1] for e in es), 'edge_labels')
    require(len(es)==len(set(map(tuple,es))), 'duplicate_edge')
    a=[0]*n
    for u,v in es:
        a[u]|=1<<v; a[v]|=1<<u
    require(all(a[v].bit_count()==(2 if v in ports else 3) for v in range(n)), 'degree')
    return a

def vertices(mask):
    while mask:
        b=mask & -mask; yield b.bit_length()-1; mask-=b

def flood(a, allowed, seed):
    reached=seed; front=seed
    while front:
        nxt=0
        for v in vertices(front):
            nxt |= a[v]
        front=nxt & allowed & ~reached; reached |= front
    return reached

def parts(a, mask):
    ans=[]
    while mask:
        cc=flood(a,mask,mask & -mask); ans.append(cc); mask &= ~cc
    return ans

def shortest(a, start, goal, banned=None):
    # Each layer expands an explicit integer frontier; no union-find or library calls.
    seen=1<<start; front=seen; d=0
    while front:
        if front>>goal & 1:
            return d
        nxt=0
        for v in vertices(front):
            nb=a[v]
            if banned and v in banned:
                nb &= ~(1 << (banned[1] if v==banned[0] else banned[0]))
            nxt |= nb
        front=nxt & ~seen; seen |= front; d+=1
    return None

def graph_report(g, capped=False):
    a=adjacency(g); n=g['n']; whole=(1<<n)-1
    cycles=[shortest(a,u,v,(u,v))+1 for u,v in g['edges'] if shortest(a,u,v,(u,v)) is not None]
    girth=min(cycles) if cycles else None
    colors={}; bip=True
    for start in range(n):
        if start in colors: continue
        colors[start]=0; queue=[start]
        for v in queue:
            for w in vertices(a[v]):
                if w not in colors: colors[w]=1-colors[v]; queue.append(w)
                elif colors[w]==colors[v]: bip=False
    cases=0
    if capped:
        for k in range(3):
            for ds in it.combinations(range(n),k):
                mask=whole-sum(1<<v for v in ds)
                require(flood(a,mask,mask & -mask)==mask, 'vertex_cut')
                cases+=1
    return {'n':n,'m':len(g['edges']),'girth':girth,'bipartite':bip,
            'deletion_sets_checked':cases,'port_distances':[[u,v,shortest(a,u,v)] for u,v in it.combinations(g['ports'],2)]}

def constructions(x):
    gs=x['graphs']; h=gs['H']; j=gs['J']; t=gs['T']
    for name,n in [('H',18),('J',21),('Jcap',22),('T',45),('Tcap',46),('triangle',3)]:
        require(gs[name]['n']==n, 'construction_order')
        adjacency(gs[name])
    sort=lambda es:sorted(map(tuple,es))
    hj=[e for e in h['edges'] if 0 not in e]+[[0,18],[0,19],[0,20],[1,18],[5,19],[17,20]]
    require(sort(j['edges'])==sort(hj) and j['ports']==[18,19,20], 'J_construction')
    tj=j['edges']+[[u+21,v+21] for u,v in j['edges']]+[[18+i,42+i] for i in range(3)]+[[39+i,42+i] for i in range(3)]
    require(sort(t['edges'])==sort(tj) and t['ports']==[42,43,44], 'T_construction')
    for name,base,cap in [('Jcap','J',21),('Tcap','T',45)]:
        require(sort(gs[name]['edges'])==sort(gs[base]['edges']+[[p,cap] for p in gs[base]['ports']]), 'cap_construction')
    return gs

def hamilton(x):
    h=x['graphs']['H']; es=set(map(tuple,h['edges'])); cc=x['hamilton_cycles']; pairs=[]
    for c in cc:
        require(len(c)==18 and sorted(c)==list(range(18)), 'hamilton_vertices')
        require(all(edge(c[i],c[(i+1)%18]) in es for i in range(18)), 'hamilton_edges')
        pos=c.index(0); pairs.append(sorted([c[(pos-1)%18],c[(pos+1)%18]]))
    require(sorted(pairs)==[[1,5],[1,17],[5,17]], 'incident_pairs')
    require(cc[0]==list(range(18)), 'reference_cycle')
    ce={edge(i,(i+1)%18) for i in range(18)}
    chords=x['chords']; require(set(map(tuple,chords.values()))==es-ce, 'chord_complement')
    require(sorted(v for e in chords.values() for v in e)==list(range(18)), 'chord_matching')
    crosses=[]
    for u,v in it.combinations(chords,2):
        a,b=chords[u]; c,d=chords[v]
        if (a<c<b<d) or (c<a<d<b): crosses.append(''.join(sorted((u,v))))
    tree=x['interlacement_tree']
    require(len(tree)==8 and len(set(tree))==8 and all(e in crosses for e in tree), 'interlacement_edges')
    reached={'A'}
    for _ in range(9):
        reached |= {v for e in tree if any(u in reached for u in e) for v in e}
    require(reached==set(chords), 'interlacement_connected')
    return {'three_incident_pairs':pairs,'all_interlacements':sorted(crosses),'tree':tree}

def cover_solver(g, state):
    """Exact decision for each of 27 states; enumerate all boundary pair choices.
    Internal exact cover lists every center with every unordered neighbor pair.
    Memoize residual vertex masks; no old verifier computations are used.
    """
    a=adjacency(g); ps=g['ports']; n=g['n']; whole=(1<<n)-1
    require(len(state)==3 and set(state)<=set('0AB'), 'state_alphabet')
    aa=[ps[i] for i,c in enumerate(state) if c=='A']; bb=[ps[i] for i,c in enumerate(state) if c=='B']
    residue=(n-len(aa)-2*len(bb))%3
    if residue: return {'feasible':False,'reason':'residue','remainder':residue,'nodes':0,'pair_choices':0}
    active=set(aa+bb); rows=[]; incident=[[] for _ in range(n)]
    for c in range(n):
        for u,v in it.combinations(vertices(a[c]),2):
            row=(u,c,v); mask=sum(1<<z for z in row)
            if not active.intersection(row):
                rows.append((mask,row))
                for z in row: incident[z].append(len(rows)-1)
    nodes=0
    @lru_cache(None)
    def solve(mask):
        nonlocal nodes
        nodes+=1
        require(nodes<=200000, 'search_node_budget')
        if not mask: return ()
        if any(cc.bit_count()%3 for cc in parts(a,mask)): return None
        choices=None
        for v in vertices(mask):
            opts=[i for i in incident[v] if rows[i][0] & mask == rows[i][0]]
            if not opts: return None
            if choices is None or len(opts)<len(choices): choices=opts
        for i in choices:
            tail=solve(mask ^ rows[i][0])
            if tail is not None: return (rows[i][1],)+tail
        return None
    options=[sorted(set(vertices(a[p]))-active) for p in bb]; tries=0
    for endpoints in it.product(*options):
        if len(set(endpoints))!=len(endpoints): continue
        tries+=1
        remove=set(aa+bb+list(endpoints)); rem=whole-sum(1<<z for z in remove)
        answer=solve(rem)
        if answer is not None:
            return {'feasible':True,'singletons':aa,'pairs':[[p,v] for p,v in zip(bb,endpoints)],
                    'p3':[list(r) for r in answer],'nodes':nodes,'pair_choices':tries}
    return {'feasible':False,'reason':'exhausted_exact_cover','nodes':nodes,'pair_choices':tries}

def verify_certificate(g, state, cert):
    a=adjacency(g); ps=g['ports']; require(cert.get('feasible') is True, 'certificate_feasibility')
    singles=cert['singletons']; pairs=cert['pairs']; paths=cert['p3']
    require(singles==[ps[i] for i,c in enumerate(state) if c=='A'], 'A_roles')
    require([r[0] for r in pairs]==[ps[i] for i,c in enumerate(state) if c=='B'], 'B_roles')
    used=list(singles)
    for r in pairs:
        require(len(r)==2 and a[r[0]]>>r[1]&1, 'pair_nonedge'); used.extend(r)
    for r in paths:
        require(len(r)==3 and len(set(r))==3, 'P3_distinct')
        require(a[r[1]]>>r[0]&1 and a[r[1]]>>r[2]&1, 'P3_nonedge'); used.extend(r)
    require(sorted(used)==list(range(g['n'])), 'cover_partition')


def forbidden_BBB(x, tables):
    """All eight choices of the internal neighbor of each outer B center.
    A selected q->p forces A, never B, on that J terminal.
    """
    a=adjacency(x['graphs']['T']); out=[]
    for choices in it.product((0,1),repeat=3):
        sl=''.join('A' if v==0 else '0' for v in choices)
        sr=''.join('A' if v==1 else '0' for v in choices)
        for i,side in enumerate(choices):
            require(a[42+i]>>(18+i+21*side)&1, 'BBB_attachment')
        require(not tables['J'][sl]['feasible'] or not tables['J'][sr]['feasible'], 'BBB_leak')
        out.append({'choices':list(choices),'left':sl,'right':sr,'left_A_count':sl.count('A'),
                    'right_A_count':sr.count('A'),'left_reason':'isolated_w' if sl=='AAA' else 'residue' if sl!='000' else 'allowed',
                    'right_reason':'isolated_w' if sr=='AAA' else 'residue' if sr!='000' else 'allowed'})
    return out

def check_tables(x,tables):
    for name in ('triangle','J','T'):
        require(sorted(s for s,c in tables[name].items() if c['feasible'])==sorted(x['claimed_true_states'][name]), 'signature_truth_table')
        for s,c in tables[name].items():
            if c['feasible']: verify_certificate(x['graphs'][name],s,c)
    require(x['graphs']['J']['ports']==[18,19,20], 'J_ports')
    a=adjacency(x['graphs']['J']); require(a[0]==sum(1<<p for p in (18,19,20)), 'AAA_isolation')
    return forbidden_BBB(x,tables)

def gluing(x,tables):
    # Recheck all ordered port bijections on triangle/T against J.
    results=[]
    for left in ('triangle','T'):
        a=x['graphs'][left]; b=x['graphs']['J']; offset=a['n']
        for perm in it.permutations(range(3)):
            host={'n':a['n']+b['n'],'ports':[], 'edges':sorted(a['edges']+[[u+offset,v+offset] for u,v in b['edges']]+[list(edge(a['ports'][i],b['ports'][perm[i]]+offset)) for i in range(3)])}
            adjacency(host)
            for s,lc in tables[left].items():
                if not lc['feasible']: continue
                inv={'0':'0','A':'B','B':'A'}; right=['0']*3
                for i in range(3): right[perm[i]]=inv[s[i]]
                rs=''.join(right); rc=tables['J'][rs]
                if not rc['feasible']: continue
                paths=lc['p3']+[[z+offset for z in p] for p in rc['p3']]
                lp={p[0]:p[1] for p in lc['pairs']}; rp={p[0]:p[1] for p in rc['pairs']}
                for i,c in enumerate(s):
                    u=a['ports'][i]; v=b['ports'][perm[i]]
                    if c=='A': paths.append([u,v+offset,rp[v]+offset])
                    elif c=='B': paths.append([lp[u],u,v+offset])
                # Closed graph certificate: same edge/partition tests, no boundary.
                verify_certificate(host,'000',{'feasible':True,'singletons':[],'pairs':[],'p3':paths})
                results.append([left,list(perm),s,rs])
    return results

def replacement_control(x, tables):
    # Two successive 000-state substitutions in the eligible triangular prism.
    g={'n':6,'ports':[], 'edges':[[0,1],[0,2],[0,3],[1,2],[1,4],[2,5],[3,4],[3,5],[4,5]]}
    paths=[[0,1,2],[3,4,5]]; records=[]
    for step in range(3):
        a=adjacency(g)
        tris=[list(t) for t in it.combinations(range(g['n']),3) if all(a[u]>>v&1 for u,v in it.combinations(t,2))]
        rpt=graph_report(g,True); rpt['triangles']=tris
        verify_certificate(g,'000',{'feasible':True,'singletons':[],'pairs':[],'p3':paths})
        records.append(rpt)
        if step==2:
            require(not tris and g['n']==90, 'replacement_terminal')
            break
        tri=tris[0]; outside=[next(vertices(a[u]&~sum(1<<v for v in tri))) for u in tri]
        remain=[v for v in range(g['n']) if v not in tri]; ren={v:i for i,v in enumerate(remain)}; off=len(remain)
        es=[list(edge(ren[u],ren[v])) for u,v in g['edges'] if u in ren and v in ren]
        es += [[u+off,v+off] for u,v in x['graphs']['T']['edges']]
        es += [list(edge(ren[v],off+42+i)) for i,v in enumerate(outside)]
        keep=[p for p in paths if not set(p).intersection(tri)]
        require(sum(bool(set(p).intersection(tri)) for p in paths)==1, 'control_state_not_000')
        paths=[[ren[v] for v in p] for p in keep]+[[v+off for v in p] for p in tables['T']['000']['p3']]
        g={'n':off+45,'ports':[], 'edges':sorted(es)}
    return records

def mutations(x,tables):
    tests=[]
    def must_reject(name, thunk):
        try: thunk()
        except Rejected as e: tests.append({'name':name,'rejected':True,'first_failure':str(e)})
        else: raise Rejected('mutation_survived:'+name)
    for name,edit,fn in [
        ('duplicate_H_edge',lambda z:z['graphs']['H']['edges'].append(z['graphs']['H']['edges'][0]),constructions),
        ('delete_H_edge',lambda z:z['graphs']['H']['edges'].pop(),constructions),
        ('repeat_Hamilton_vertex',lambda z:z['hamilton_cycles'][1].__setitem__(1,0),hamilton),
        ('Hamilton_nonedge',lambda z:z['hamilton_cycles'][1].__setitem__(slice(1,3),[8,1]),hamilton),
        ('false_interlacement',lambda z:z['interlacement_tree'].__setitem__(0,'AJ'),hamilton),
        ('drop_J_edge',lambda z:z['graphs']['J']['edges'].pop(),constructions),
        ('repeat_T_port',lambda z:z['graphs']['T']['ports'].__setitem__(1,42),constructions),
        ('delete_cap_edge',lambda z:z['graphs']['Tcap']['edges'].pop(),constructions),
        ('claim_J_AAA',lambda z:z['claimed_true_states']['J'].append('AAA'),lambda z:check_tables(z,tables)),
        ('claim_T_BBB',lambda z:z['claimed_true_states']['T'].append('BBB'),lambda z:check_tables(z,tables))]:
        z=copy.deepcopy(x); edit(z); must_reject(name,lambda z=z,fn=fn:fn(z))
    for name,s,edit in [
        ('duplicate_P3_vertex','000',lambda c:c['p3'][0].__setitem__(2,c['p3'][0][0])),
        ('omit_P3_block','000',lambda c:c['p3'].pop()),
        ('reverse_B_pair_role','0AB',lambda c:c['pairs'][0].reverse()),
        ('erase_A_singleton','0AB',lambda c:c['singletons'].clear())]:
        c=copy.deepcopy(tables['T'][s]); edit(c)
        must_reject(name,lambda c=c,s=s:verify_certificate(x['graphs']['T'],s,c))
    bad=copy.deepcopy(tables); bad['J']['AAA']={'feasible':True}
    must_reject('forge_J_AAA_in_BBB_elimination',lambda:forbidden_BBB(x,bad))
    return tests

def main():
    root=pathlib.Path(__file__).resolve().parent; raw=(root/'input.json').read_bytes(); x=json.loads(raw)
    gs=constructions(x); hc=hamilton(x)
    graph_results={name:graph_report(g,name in ('H','Jcap','Tcap')) for name,g in gs.items()}
    require(graph_results['H']['bipartite'], 'H_bipartite')
    require(all(graph_results[n]['girth']==6 for n in ('H','J','T')), 'girth_six')
    require(all(d==4 for u,v,d in graph_results['T']['port_distances']), 'T_port_distance')
    states=[''.join(s) for s in it.product('0AB',repeat=3)]
    tables={name:{s:cover_solver(gs[name],s) for s in states} for name in ('triangle','J','T')}
    exclusions=check_tables(x,tables); joins=gluing(x,tables); negative=mutations(x,tables)
    result={'verdict':'candidate_only','status':'PASS','scope':'triangle-free-reduction-audited finite objects; prose reduction remains candidate proof',
            'python':platform.python_version(),'input_sha256':hashlib.sha256(raw).hexdigest(),
            'checker_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'graphs':graph_results,'hamilton':hc,'interface_tables':tables,'T_BBB_eight_cases':exclusions,
            'gluing_cases':joins,'replacement_control':replacement_control(x,tables),'mutations':negative,'lean':'not_executed','trusted_attestation':None}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    main()
