#!/usr/bin/env python3
"""Independent C02 audit. Python standard library only; no candidate code imported.
Enumeration method: all C(27,9) edge subsets, not the candidate's matching recursion.
Connectivity method: Boolean transitive closure, not its deletion BFS.
This is a computational audit, not a Lean or repository admission receipt.
"""
from __future__ import annotations
import hashlib,itertools,json,math,pathlib,platform,time,sys
if sys.flags.optimize:
    raise SystemExit("Run without -O: assertion-based checks must remain enabled.")
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parent
EDGE=lambda u,v: (min(u,v),max(u,v))
P_EDGES=sorted({EDGE(i,(i+1)%5) for i in range(5)}|{(i,i+5) for i in range(5)}|{EDGE(i+5,(i+2)%5+5) for i in range(5)})
BRICK=sorted((u-1,v-1) for u,v in P_EDGES if 0 not in (u,v))
PORTS=(0,3,4)

def validate(n,es):
    assert len(es)==len(set(es)), 'duplicate edge'
    assert all(0<=u<v<n for u,v in es), 'loop / label / noncanonical edge'
    deg=Counter(v for e in es for v in e)
    assert all(deg[v]==3 for v in range(n)), 'not cubic'

def connected(n,es,deleted=()):
    blocked=sum(1<<v for v in deleted)
    live=((1<<n)-1)^blocked
    if not live:return False
    reach=[(1<<u) if live>>u&1 else 0 for u in range(n)]
    for u,v in es:
        if (live>>u&1) and (live>>v&1):
            reach[u]|=1<<v;reach[v]|=1<<u
    for k in range(n):
        for u in range(n):
            if reach[u]>>k&1:reach[u]|=reach[k]
    return all(reach[u]==live for u in range(n) if live>>u&1)

def components(n,es):
    adj=[set() for _ in range(n)]
    for u,v in es:adj[u].add(v);adj[v].add(u)
    unseen=set(range(n));out=[]
    while unseen:
        start=min(unseen);todo=[start];seen={start}
        while todo:
            v=todo.pop()
            for w in adj[v]-seen:seen.add(w);todo.append(w)
        unseen-=seen;out.append(sorted(seen))
    return sorted(out,key=lambda c:(len(c),c))

def p3_valid(n,es,triples):
    used=[v for p in triples for v in p]
    return all(len(p)==3 for p in triples) and sorted(used)==list(range(n)) and all(EDGE(p[0],p[1]) in es and EDGE(p[1],p[2]) in es for p in triples)

def family(q):
    assert isinstance(q,int) and q>=0
    t=6*q+5;n=2*t+8
    es=set(BRICK)
    cyc={EDGE(i,(i+1)%(2*t)) for i in range(2*t)}
    chords={(i,i+t) for i in range(t)}
    es|={(u+8,v+8) for u,v in cyc|chords if u!=0 and v!=0}
    es|={(0,9),(3,2*t+7),(4,t+8)}
    triples=[(0,1,2),(4,7,5),(3,8,6)]+[(9+3*j,10+3*j,11+3*j) for j in range((2*t-1)//3)]
    return n,sorted(es),triples

def exhaustive_matchings(n,es):
    """Iterate every n/2-edge subset. No matching generator from C01/C02."""
    masks=[(1<<u)|(1<<v) for u,v in es];out=[];subsets=0
    for ids in itertools.combinations(range(len(es)),n//2):
        subsets+=1;used=0
        for j in ids:
            b=masks[j]
            if used&b:break
            used|=b
        else:
            assert used==(1<<n)-1
            selected=set(ids)
            rest=[e for j,e in enumerate(es) if j not in selected]
            deg=Counter(v for e in rest for v in e)
            assert all(deg[v]==2 for v in range(n))
            cs=components(n,rest)
            out.append({'edge_indices':list(ids),'matching':[list(es[j]) for j in ids],
                        'complement_components':cs,'spectrum':[len(c) for c in cs]})
    assert subsets==math.comb(len(es),n//2)
    return subsets,out

def fragment_table():
    out=[];boundary_hist=Counter()
    for mask in range(1<<12):
        chosen=[e for i,e in enumerate(BRICK) if mask>>i&1]
        deg=Counter(v for e in chosen for v in e)
        for boundary in range(8):
            if not all(deg[v]+(int(bool(boundary>>PORTS.index(v)&1)) if v in PORTS else 0)==2 for v in range(9)):
                continue
            cs=components(9,chosen)
            closed5=[c for c in cs if len(c)==5 and all(deg[v]==2 for v in c)]
            bc=boundary.bit_count();boundary_hist[bc]+=1
            if bc==2:assert len(closed5)==1
            out.append({'internal_mask':mask,'boundary_mask':boundary,'boundary_count':bc,
                        'component_sizes':sorted(map(len,cs)),'closed_five_components':closed5})
    return out,boundary_hist

def main():
    start=time.perf_counter();raw=(ROOT/'inputs/C02-witness.json').read_bytes();x=json.loads(raw)
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='3e2e860d828e4045e809bc445d11cb59fd60c610'
    n=x['graph_order'];es=[tuple(e) for e in x['edges']];validate(n,es)
    fn,fe,fp=family(0);assert (fn,fe)==(n,es), 'family q=0 disagrees with repository edge list'
    deletion_tests=0
    for r in range(3):
        for d in itertools.combinations(range(n),r):
            assert connected(n,es,d), ('vertex cut',d)
            deletion_tests+=1
    assert p3_valid(n,set(es),x['p3_factor'])
    subsets,matchings=exhaustive_matchings(n,es)
    hist=Counter(tuple(m['spectrum']) for m in matchings)
    assert hist==Counter({(4,5,9):6,(5,6,7):4,(5,13):16}), hist
    sample={tuple(e) for e in x['sample_matching']}
    assert any({tuple(e) for e in m['matching']}==sample for m in matchings)
    sample_cycles=x['sample_cycles']
    assert sorted(v for c in sample_cycles for v in c)==list(range(n))
    cycle_edges={EDGE(c[i],c[(i+1)%len(c)]) for c in sample_cycles for i in range(len(c))}
    assert cycle_edges==set(es)-sample, 'saved sample cycle certificate disagrees with complement'
    cut={EDGE(0,9),EDGE(3,17),EDGE(4,13)}
    for m in matchings:
        assert len(cut.intersection(map(tuple,m['matching'])))==1
        assert 5 in m['spectrum']
    local,local_hist=fragment_table()
    # Structural family audit at several explicit parameter values; not a proof for all q.
    family_tests=[]
    for q in range(9):
        nq,eq,pq=family(q);validate(nq,eq);assert p3_valid(nq,set(eq),pq)
        # Exhaust all deletion sets for q <= 3; beyond that check construction and factor only.
        tested=0
        if q<=3:
            for r in range(3):
                for d in itertools.combinations(range(nq),r):
                    assert connected(nq,eq,d),(q,d)
                    tested+=1
        family_tests.append({'q':q,'order':nq,'edges':len(eq),'p3_blocks':len(pq),'deletion_sets_tested':tested})
    # Negative control: drop bipartiteness, replace the right brick by another Petersen-a0.
    pp=sorted(set(BRICK)|{(u+9,v+9) for u,v in BRICK}|{(p,p+9) for p in PORTS})
    validate(18,pp)
    nine=[0,1,2,3,8,6,4,7,5]
    circles=[nine,[v+9 for v in nine]]
    factor={EDGE(c[i],c[(i+1)%9]) for c in circles for i in range(9)}
    assert factor<=set(pp)
    assert sorted(map(len,components(18,sorted(factor))))==[9,9]
    assert all(connected(18,pp,d) for r in range(3) for d in itertools.combinations(range(18),r))
    # Positive control: the same matching/factor checker must accept K3,3.
    k33=[(i,j) for i in range(3) for j in range(3,6)]
    ksub,kmatch=exhaustive_matchings(6,k33)
    assert len(kmatch)==6 and all(m['spectrum']==[6] for m in kmatch)
    assert p3_valid(3,{(0,1),(0,2),(1,2)},[(0,1,2)]), 'P3 is not required to be induced'
    # Validation mutations must be rejected.
    repeated=[list(t) for t in x['p3_factor']];repeated[-1][-1]=16
    missing_edge=set(es)-{(0,1)}
    mutations={'duplicate_vertex_in_factor_rejected':not p3_valid(n,set(es),repeated),
               'nonedge_path_rejected':not p3_valid(n,missing_edge,x['p3_factor']),
               'drop_bipartiteness_allows_divisible_factor':True}
    assert all(mutations.values())
    result={'verdict':'candidate_only','audit_kind':'independent_computational_replay_no_lean_receipt',
      'source_commit':'85f4b0269addb746adad975cedd1fed07565ee96',
      'input_git_blob_sha1':'3e2e860d828e4045e809bc445d11cb59fd60c610',
      'input_sha256':hashlib.sha256(raw).hexdigest(),'python':platform.python_version(),
      'independence_scope':'fresh implementation; no generator code imported; same assistant, not independently staffed review',
      'order':n,'edges':len(es),'vertex_deletion_sets_tested':deletion_tests,
      'edge_subsets_exhaustively_tested':subsets,'perfect_matchings':len(matchings),
      'cycle_spectra':[{'lengths':list(k),'count':v} for k,v in sorted(hist.items())],
      'divisible_complements':sum(all(l%3==0 for l in m['spectrum']) for m in matchings),
      'fragment_assignments_tested':(1<<12)*8,'fragment_valid_states_by_boundary_count':dict(sorted(local_hist.items())),
      'family_tests':family_tests,'mutations':mutations,
      'positive_control':{'graph':'K3,3','edge_subsets':ksub,'matchings':len(kmatch),'all_spectra':[6]},
      'noninduced_P3_semantics_test':True,'saved_sample_matching_and_cycles_checked':True,
      'negative_control':{'construction':'(P-a0) vertex-3-sum (P-a0)','edges':pp,'cycles':circles,'spectrum':[9,9]},
      'elapsed_seconds':round(time.perf_counter()-start,3),
      'limits':'Finite audit only. No all-q proof-assistant replay, novelty test, minimality test or root conclusion.'}
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    for name,body in [('audit.json',result),('all_26_matchings.json',matchings),('fragment_states.json',local)]:
        (out/name).write_text(json.dumps(body,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
