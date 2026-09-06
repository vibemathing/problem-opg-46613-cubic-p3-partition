"""Bounded generator-side tests of the C03 constructions; not a verifier."""
from collections import Counter
from itertools import combinations
import json
import resource
import sys
import time

resource.setrlimit(resource.RLIMIT_AS, (268435456, 268435456))
resource.setrlimit(resource.RLIMIT_CPU, (20, 20))
resource.setrlimit(resource.RLIMIT_FSIZE, (32768, 32768))
DEADLINE = time.monotonic() + 20

def tick():
    if time.monotonic() > DEADLINE:
        raise TimeoutError("20-second generator budget")

def adj(n, edges):
    a = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n
        a[u].add(v)
        a[v].add(u)
    return a

def petersen():
    return sorted({tuple(sorted(e)) for i in range(5) for e in
                   ((i, (i+1)%5), (i, i+5), (i+5, 5+(i+2)%5))})

def matchings(a):
    def rec(rem, m):
        tick()
        if not rem:
            yield m
            return
        u = (rem & -rem).bit_length()-1
        for v in sorted(a[u]):
            if rem >> v & 1:
                yield from rec(rem ^ (1 << u) ^ (1 << v), m+[(u, v)])
    return rec((1 << len(a))-1, [])

def spectrum(a, m):
    partner = {x: y for e in m for x, y in (e, e[::-1])}
    seen, lengths = set(), []
    for r in range(len(a)):
        if r in seen:
            continue
        previous, u, length = -1, r, 0
        while u not in seen:
            seen.add(u)
            length += 1
            choices = sorted(a[u] - {partner[u], previous})
            assert choices
            previous, u = u, choices[0]
        assert u == r
        lengths.append(length)
    return tuple(sorted(lengths))

def prism(n):
    assert n >= 4 and n % 2 == 0
    e = {tuple(sorted((r*n+i, r*n+(i+1)%n))) for r in range(2) for i in range(n)}
    e.update((i, n+i) for i in range(n))
    left = [r*n+i for r in range(2) for i in range(n) if (r+i)%2 == 0]
    return 2*n, sorted(e), left

def inflate(n, edges, left):
    a = adj(n, edges)
    right = sorted(set(range(n))-set(left))
    t = len(left)
    assert len(right) == t
    rindex = {v: i for i, v in enumerate(right)}
    e = []
    for i, v in enumerate(left):
        e.extend((9*i+u-1, 9*i+w-1) for u, w in petersen() if u and w)
        e.extend((9*i+p-1, 9*t+rindex[w]) for p, w in zip((1,4,5), sorted(a[v])))
    return 10*t, sorted(e)

def deletion_checks(a):
    count = 0
    for size in range(3):
        for deleted in combinations(range(len(a)), size):
            tick()
            remaining = set(range(len(a)))-set(deleted)
            reached = {min(remaining)}
            todo = list(reached)
            while todo:
                u = todo.pop()
                for v in (a[u] & remaining)-reached:
                    reached.add(v)
                    todo.append(v)
            assert reached == remaining
            count += 1
    return count

def check_frame(name, n, edges, left):
    a = adj(n, edges)
    t = len(left)
    quotient = Counter(spectrum(a, m) for m in matchings(a))
    predicted = Counter()
    for sp, count in quotient.items():
        assert all(x%2 == 0 for x in sp)
        lifted = tuple(sorted([5]*t+[5*(x//2) for x in sp]))
        predicted[lifted] += count * 2**t
    hn, he = inflate(n, edges, left)
    ha = adj(hn, he)
    assert len(set(he)) == 3*hn//2 and all(len(x) == 3 for x in ha)
    observed = Counter(spectrum(ha, m) for m in matchings(ha))
    assert observed == predicted
    return {"frame": name, "frame_order": n, "brick_count": t,
            "expanded_order": hn, "frame_matching_count": sum(quotient.values()),
            "expanded_matching_count": sum(observed.values()),
            "spectra": [{"lengths": list(s), "count": c} for s,c in sorted(observed.items())],
            "deletion_sets": deletion_checks(ha)}

def expanded_petersen(selected):
    a = adj(10, petersen())
    nodes = [(v,w) for v in range(10) for w in (sorted(a[v]) if v in selected else [-1])]
    edges = set()
    for v in selected:
        edges.update(frozenset(((v,x),(v,y))) for x,y in combinations(sorted(a[v]),2))
    for u,v in petersen():
        edges.add(frozenset(((u,v if u in selected else -1),
                             (v,u if v in selected else -1))))
    chosen = min(selected)
    original = [1,2,3,4,9,7,5,8,6]
    def image(x):
        if chosen < 5:
            return ((x%5+chosen)%5)+(5 if x >= 5 else 0)
        k = chosen-5
        return ((2*(x%5)+k)%5)+(5 if x < 5 else 0)
    cycle = list(map(image, original))
    assert chosen not in cycle and len(set(cycle)) == 9
    lifted = []
    for j,v in enumerate(cycle):
        if v not in selected:
            lifted.append((v,-1))
        else:
            p,q = cycle[j-1], cycle[(j+1)%9]
            middle = next(iter(a[v]-{p,q}))
            lifted.extend(((v,p),(v,middle),(v,q)))
    triangle = [(chosen,w) for w in sorted(a[chosen])]
    for c in (triangle, lifted):
        assert len(c)%3 == 0
        assert all(frozenset((c[j],c[(j+1)%len(c)])) in edges for j in range(len(c)))
    assert len(triangle+lifted) == len(set(triangle+lifted)) == len(nodes)
    assert set(triangle+lifted) == set(nodes)
    return len(nodes), len(lifted)

reports = [check_frame('K3,3', 6, [(i,j) for i in range(3) for j in range(3,6)], [0,1,2])]
for n in (4,6):
    reports.append(check_frame('prism-C'+str(n), *prism(n)))
expanded = []
for size in (1,4,7,10):
    count = 0
    for chosen in combinations(range(10), size):
        tick()
        n,length = expanded_petersen(set(chosen))
        assert n == 10+2*size and length == n-3
        count += 1
    expanded.append({'expanded_vertices':size,'labeled_subsets_checked':count,'order':n,'constructed_spectrum':[3,length]})
output = {'verdict':'candidate_only','python':sys.version.split()[0],
          'frame_checks':reports,'triangle_expansion_checks':expanded,
          'limits':{'wall_seconds':20,'cpu_seconds':20,'address_space_bytes':268435456,'output_bytes':32768,'threads':1},
          'scope':'Only the named frames and all 341 labeled Petersen expansion subsets; not all cubic graphs of these orders.',
          'limitations':['generator-side exact checks only','no formal replay or mathematical admission']}
text = json.dumps(output, indent=2)+'\n'
assert len(text.encode()) <= 32768
sys.stdout.write(text)
