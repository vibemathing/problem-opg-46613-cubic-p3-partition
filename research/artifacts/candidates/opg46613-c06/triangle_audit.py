"""Candidate-side triangle gluing, contraction, and finite boundary tests."""
from __future__ import annotations
import hashlib
import itertools
import json
import sys
import time
from collections import Counter


def need(condition, message):
    if not condition:
        raise ValueError(message)


def three_connected(graph):
    vertices = set(graph)
    if len(vertices) < 4:
        return False
    for size in range(3):
        for cut in itertools.combinations(sorted(vertices),size):
            todo = vertices - set(cut)
            stack = [min(todo)];todo.remove(stack[0])
            while stack:
                u = stack.pop()
                new = graph[u] & todo;todo.difference_update(new);stack.extend(new)
            if todo:
                return False
    return True


def build(n, edges, cycle, retained, offset):
    need(len(retained)%3 == 0 and retained <= set(cycle),'invalid retained set')
    need(len(set(cycle)) == len(cycle),'repeated cycle vertex')
    frame = {u:set() for u in range(n)}
    for a,b in edges:
        need(a != b and b not in frame[a],'invalid frame edge')
        frame[a].add(b);frame[b].add(a)
    need(all(len(a)==3 for a in frame.values()),'noncubic frame')
    graph = {}; selected = set(); ports = {}
    choices = tuple(itertools.permutations(range(3)))
    for u in frame:
        if u in retained:
            graph[u,-1] = set()
        else:
            ports[u] = dict(zip(sorted(frame[u]),choices[(u+sum(retained)+offset)%6]))
            for j in range(3):
                graph[u,j] = {(u,k) for k in range(3) if k != j}
    def end(u,v):
        return (u,-1) if u in retained else (u,ports[u][v])
    for u,v in edges:
        a,b=end(u,v),end(v,u);graph[a].add(b);graph[b].add(a)
    incoming = {u:[] for u in frame};outgoing={u:[] for u in frame};value=0
    for i,u in enumerate(cycle):
        v=cycle[(i+1)%len(cycle)]
        need(v in frame[u],'cycle nonedge')
        value=(value-(u in retained))%3
        if value:
            a,b=(u,v) if value==1 else (v,u)
            outgoing[a].append(b);incoming[b].append(a)
            selected.add(frozenset((end(a,b),end(b,a))))
    need(value==0,'nonclosing flow')
    signatures=Counter()
    for u in frame:
        if u in retained:
            need((len(incoming[u]),len(outgoing[u])) in ((1,0),(0,2)),'retained role')
        elif not incoming[u] and not outgoing[u]:
            selected.update((frozenset(((u,0),(u,1))),frozenset(((u,1),(u,2)))))
            signatures['UUU']+=1
        else:
            need(len(incoming[u])==len(outgoing[u])==1,'triangle role')
            a=ports[u][incoming[u][0]];b=ports[u][outgoing[u][0]];c=3-a-b
            need(len({a,b,c})==3,'repeated port')
            selected.add(frozenset(((u,b),(u,c))))
            signatures[f'A{a}B{b}']+=1
    chosen={u:set() for u in graph}
    for edge in selected:
        a,b=tuple(edge);need(b in graph[a],'selected nonedge');chosen[a].add(b);chosen[b].add(a)
    unseen=set(graph);triples=[]
    while unseen:
        root=min(unseen);unseen.remove(root);stack=[root];component={root}
        while stack:
            u=stack.pop();new=chosen[u]&unseen;unseen.difference_update(new);component.update(new);stack.extend(new)
        need(len(component)==3 and sorted(len(chosen[u]) for u in component)==[1,1,2],'not P3')
        center=next(u for u in component if len(chosen[u])==2)
        a,c=sorted(chosen[center]);triples.append((a,center,c))
    return graph,sorted(triples),signatures


def contract_all_triangles(graph):
    triangles=[]
    for u in sorted(graph):
        for v in sorted(graph[u]):
            if v > u:
                triangles.extend((u,v,w) for w in sorted(graph[u]&graph[v]) if w > v)
    need(len(set(itertools.chain.from_iterable(triangles)))==3*len(triangles),'overlapping triangles')
    cells=[tuple(t) for t in triangles];covered=set(itertools.chain.from_iterable(cells))
    singletons=sorted(set(graph)-covered);cells.extend((u,) for u in singletons)
    label={u:i for i,c in enumerate(cells) for u in c};edges=Counter()
    for u in graph:
        for v in graph[u]:
            if u<v and label[u]!=label[v]:
                edges[tuple(sorted((label[u],label[v])))]+=1
    if len(cells)==2:
        need(all(len(c)==3 for c in cells) and edges==Counter({(0,1):3}),'wrong two-cell exception')
        return 'triangular-prism',len(singletons)
    need(all(m==1 for m in edges.values()),'parallel quotient edges')
    quotient={i:set() for i in range(len(cells))}
    for u,v in edges:
        quotient[u].add(v);quotient[v].add(u)
    need(all(len(a)==3 for a in quotient.values()) and three_connected(quotient),'quotient not simple cubic 3-connected')
    return 'simple-cubic-3-connected',len(singletons)


def run():
    deadline=time.monotonic()+35;stream=hashlib.sha256();signatures=Counter();types=Counter();cases=0
    frame_counts={};connectivity_controls=0
    def case(n,edges,cycle,retained,offset,check_full=False):
        nonlocal cases,connectivity_controls
        graph,triples,local=build(n,edges,cycle,retained,offset)
        kind,uncovered=contract_all_triangles(graph)
        need(uncovered%3==0,'nondivisible uncovered count')
        signatures.update(local);types[kind]+=1;cases+=1
        if check_full:
            need(three_connected(graph),'expanded graph loses connectivity');connectivity_controls+=1
        stream.update((json.dumps(triples,separators=(',',':'))+'\n').encode())
        need(time.monotonic()<deadline,'incomplete audit: deadline')
    for n in (4,6,8,10,12):
        edges=tuple((u,(u+1)%n) for u in range(n))+tuple((u,u+n//2) for u in range(n//2))
        before=cases
        for mask in range(1<<n):
            retained=frozenset(u for u in range(n) if mask>>u&1)
            if len(retained)%3==0:
                for offset in range(6):
                    case(n,edges,tuple(range(n)),retained,offset,mask==0 and offset==0)
        frame_counts[str(n)]=cases-before
    petersen=((0,1),(0,5),(1,2),(1,6),(2,3),(2,7),(3,8),(4,6),(4,7),(5,7),(5,8),(6,8),(9,0),(9,3),(9,4))
    cycle=(0,1,2,3,8,6,4,7,5);before=cases
    for mask in range(1<<9):
        retained=frozenset(u for u in range(9) if mask>>u&1)
        if len(retained)%3==0:
            for offset in range(6):case(10,petersen,cycle,retained,offset,mask==511)
    petersen_cases=cases-before
    # A planar 12-prism, with twenty-one retained vertices; this is a bounded sample.
    edges=tuple((u,(u+1)%12) for u in range(12))+tuple((u+12,(u+1)%12+12) for u in range(12))+tuple((u,u+12) for u in range(12))
    cycle=tuple(range(12))+tuple(range(23,11,-1));before=cases
    for omitted in itertools.islice(itertools.combinations(range(24),3),40):
        for offset in (0,5):case(24,edges,cycle,frozenset(set(range(24))-set(omitted)),offset,omitted==(0,1,2))
    planar_samples=cases-before
    need(set(signatures)=={'UUU'}|{f'A{a}B{b}' for a,b in itertools.permutations(range(3),2)},'missed local state')
    return {'verdict':'candidate_only','python':sys.version.split()[0],'frame_case_counts':frame_counts,
            'petersen_cycle_cases':petersen_cases,'planar_twenty_one_retained_samples':planar_samples,
            'total_cases':cases,'quotient_types':dict(types),'full_vertex_deletion_controls':connectivity_controls,
            'local_signatures':dict(sorted(signatures.items())),'factor_stream_sha256':stream.hexdigest(),
            'limitations':['explicit supplied cycles only; no exhaustive planar or cubic graph census',
                           'source cyclability theorems are external proof dependencies',
                           'local generator-side audit, not a registered verifier receipt']}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
