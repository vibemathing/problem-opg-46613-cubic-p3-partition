#!/usr/bin/env python3
"""New certificate consumer: unordered triples and complete branch-DAG checking.
No import from checker.py or any earlier repository verifier. Same generator domain.
"""
import copy,functools,hashlib,itertools,json,pathlib
BASE=pathlib.Path(__file__).resolve().parent

def need(b,s):
    if not b: raise ValueError(s)

def key(a,b):return tuple(sorted((a,b)))

def verify_proof(p,n,edges,matching,budget):
    need(p['n']==n and p['budget']==budget,'proof_scope')
    need(set(map(tuple,p['edges']))==edges,'proof_graph')
    need(set(map(tuple,p['charged_matching']))==matching&edges,'proof_matching')
    rows=[]
    for triple in itertools.combinations(range(n),3):
        pairs=[e for e in itertools.combinations(triple,2) if e in edges]
        for center in triple:
            ends=sorted(set(triple)-{center})
            pe=[key(center,v) for v in ends]
            if not all(e in edges for e in pe):continue
            row=[center,*ends];mask=sum(2**v for v in row)
            rows.append((row,mask,sum(e in matching for e in pe)))
    root=str(2**n-1)+':'+str(budget)
    need(p['root']==root,'proof_root')
    todo=[root];visited=set()
    while todo:
        name=todo.pop()
        if name in visited:continue
        visited.add(name)
        need(name in p['nodes'],'proof_missing_child')
        mask,left=map(int,name.split(':'));v=p['nodes'][name]
        need(0<mask<2**n and 0<=left<=budget,'proof_reached_cover_or_bad_state')
        need(0<=v<n and mask>>v&1,'proof_pivot')
        available=[(r,b,c) for r,b,c in rows if v in r and b&mask==b and c<=left]
        # No branch list is trusted: every legal P3 through the pivot is checked.
        for r,b,c in available:todo.append(str(mask^b)+':'+str(left-c))
    need(len(p['nodes'])==p['node_count'],'proof_node_count')
    return len(visited)

def factor_polynomial(n,edges,matching):
    rows=[]
    for t in itertools.combinations(range(n),3):
        for c in t:
            ends=[v for v in t if v!=c];pe=[key(c,v) for v in ends]
            if all(e in edges for e in pe):rows.append((sum(2**v for v in t),sum(e in matching for e in pe)))
    incidence=[[r for r in rows if r[0]>>v&1] for v in range(n)]
    @functools.lru_cache(None)
    def poly(mask):
        if mask==0:return (1,)
        v=(mask&-mask).bit_length()-1
        ans=[0]*(mask.bit_count()//3+1)
        for bits,cost in incidence[v]:
            if bits&mask!=bits:continue
            for i,a in enumerate(poly(mask^bits)):
                if i+cost<len(ans):ans[i+cost]+=a
        return tuple(ans)
    out=poly(2**n-1)
    return list(out),poly.cache_info().currsize

def main():
    raw=(BASE/'input.json').read_bytes();x=json.loads(raw);n=x['n']
    es=set(map(tuple,x['edges']));m=set(map(tuple,x['perfect_matching']))
    need(n==36 and len(es)==54 and len(x['edges'])==54,'host_shape')
    need(all(0<=u<v<n for u,v in es),'host_edges')
    deg=[sum(v in e for e in es) for v in range(n)]
    need(deg==[3]*n,'host_degrees')
    need(not any(all(e in es for e in itertools.combinations(t,2)) for t in itertools.combinations(range(n),3)),'host_triangle')
    # Connectivity by partition merging, not the primary frontier search.
    checks=0
    for k in range(3):
        for deleted in itertools.combinations(range(n),k):
            parts=[{v} for v in range(n) if v not in deleted]
            for u,v in es:
                if u in deleted or v in deleted:continue
                i=next(i for i,s in enumerate(parts) if u in s)
                j=next(j for j,s in enumerate(parts) if v in s)
                if i!=j:parts[i].update(parts[j]);parts.pop(j)
            need(len(parts)==1,'host_disconnected');checks+=1
    used=[];fe=set()
    for a,c,b in x['factor']:
        need(a!=b and a!=c and c!=b and key(a,c) in es and key(c,b) in es,'factor_edge')
        used.extend([a,c,b]);fe|={key(a,c),key(c,b)}
    need(sorted(used)==list(range(n)) and len(fe&m)==3,'factor_cover_or_cost')
    ce={key(c[i],c[(i+1)%len(c)]) for c in x['cycles'] for i in range(len(c))}
    cross=set(map(tuple,x['cross_edges']));pr=json.loads((BASE/'failure-certificates.json').read_bytes())
    counts={}
    scopes={'restricted_no_factor':(ce|cross,12),'full_host_at_most_two_matching_edges':(es,2)}
    for name,(ee,budget) in scopes.items():counts[name]=verify_proof(pr[name],n,ee,m,budget)
    # Attack certificate completeness rather than rejecting altered input hashes.
    names=['restricted_no_factor','full_host_at_most_two_matching_edges'];mutations=[]
    for name in names:
        q=copy.deepcopy(pr[name]); victim=next(k for k in q['nodes'] if k!=q['root'])
        del q['nodes'][victim];q['node_count']-=1
        ee,budget=scopes[name]
        try:verify_proof(q,n,ee,m,budget)
        except ValueError as exc:
            need(str(exc)=='proof_missing_child','unexpected_mutation_failure')
            mutations.append({'name':name+'_drop_residual_state','rejected':True,'failure':str(exc)})
        else:raise ValueError('certificate_mutation_accepted')
    polynomial,states=factor_polynomial(n,es,m)
    gap=json.loads((BASE/'gap-forest-stdout.json').read_text())
    normal=json.loads((BASE/'normal-form-stdout.json').read_text())
    need(all(polynomial[i]==gap['factor_counts_by_cost'][str(i)] for i in range(len(polynomial))),'gap_count_disagrees')
    need(all(polynomial[i]==normal['factor_counts_by_budget'][str(i)] for i in range(4)),'normal_form_disagrees')
    print(json.dumps({'factor_count_polynomial':polynomial,'polynomial_states':states,'total_factors':sum(polynomial),'status':'PASS','verdict':'candidate_only','method':'unordered-triple certificate verification and partition merging',
      'input_sha256':hashlib.sha256(raw).hexdigest(),'certificate_sha256':hashlib.sha256((BASE/'failure-certificates.json').read_bytes()).hexdigest(),
      'deletion_sets':checks,'checked_negative_nodes':counts,'certificate_mutations':mutations,
      'root_counterexample':False,'trust_domain':'web-candidate-generation'},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
