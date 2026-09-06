"""Bounded candidate-side mutation tests and the frozen C02 negative control."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import tempfile
import time
from collections import Counter
from pathlib import Path
import check_factor_cover12 as checker

EDGES18 = ((0,1),(0,5),(0,9),(1,2),(1,6),(2,3),(2,7),(3,8),(3,17),
           (4,6),(4,7),(4,13),(5,7),(5,8),(6,8),(9,10),(9,14),(10,11),
           (10,15),(11,12),(11,16),(12,13),(12,17),(13,14),(14,15),(15,16),(16,17))
P3 = ((0,1,2),(4,7,5),(3,8,6),(9,10,11),(12,13,14),(15,16,17))


def run(certificate: Path) -> dict[str, object]:
    deadline = time.monotonic() + 35
    data = certificate.read_bytes()
    if len(data) > checker.MAX_BYTES:
        raise ValueError("input budget")
    rows = data.decode('ascii').splitlines()
    parts = rows[1].split('\t')
    bad_witness = '\t'.join((parts[0], parts[1], parts[1]))
    wrong_footer = rows[-1].replace('3327:2448', '3327:2447')
    mutations = {
        'missing-DONE': rows[:-1],
        'omitted-first-case': rows[:1] + rows[2:],
        'duplicate-first-case': rows[:2] + rows[1:],
        'bad-complement-witness': rows[:1] + [bad_witness] + rows[2:],
        'incorrect-footer': rows[:-1] + [wrong_footer],
    }
    rejected = {}
    with tempfile.TemporaryDirectory(prefix='candidate-control-', dir='.') as directory:
        for name, modified in mutations.items():
            path = Path(directory) / (name + '.tsv')
            path.write_text('\n'.join(modified) + '\n', encoding='ascii')
            try:
                checker.run(path, 12)
            except ValueError as error:
                rejected[name] = str(error)
            else:
                raise ValueError('checker accepted mutation: ' + name)
            if time.monotonic() >= deadline:
                raise ValueError('overall mutation deadline')
    graph = [set() for _ in range(18)]
    for u,v in EDGES18:
        graph[u].add(v); graph[v].add(u)
    if len(EDGES18) != 27 or any(len(a) != 3 for a in graph):
        raise ValueError('negative-control cubicity')
    deletion_count = 0
    for size in range(3):
        for deleted in itertools.combinations(range(18), size):
            deletion_count += 1
            remaining = set(range(18)) - set(deleted)
            root = min(remaining); seen = {root}; stack = [root]
            while stack:
                u = stack.pop()
                for v in graph[u] & remaining - seen:
                    seen.add(v); stack.append(v)
            if seen != remaining:
                raise ValueError('negative-control connectivity')
    counts = Counter()
    mate = [-1]*18
    def enumerate_matchings(remaining):
        if not remaining:
            unused = set(range(18)); sizes = []
            while unused:
                root = unused.pop(); stack = [root]; size = 0
                while stack:
                    u = stack.pop(); size += 1
                    for v in (graph[u] - {mate[u]}) & unused:
                        unused.remove(v); stack.append(v)
                sizes.append(size)
            counts[tuple(sorted(sizes))] += 1
            return
        u = min(remaining)
        for v in sorted(graph[u] & remaining):
            mate[u],mate[v] = v,u
            enumerate_matchings(remaining - {u,v})
    enumerate_matchings(set(range(18)))
    if counts != Counter({(5,13):16,(4,5,9):6,(5,6,7):4}):
        raise ValueError('negative-control spectrum mismatch')
    if sorted(v for path in P3 for v in path) != list(range(18)) or any(b not in graph[a] or c not in graph[b] for a,b,c in P3):
        raise ValueError('P3 positive control invalid')
    return {'verdict':'candidate_only', 'certificate_sha256':hashlib.sha256(data).hexdigest(),
            'rejected_mutations':rejected, 'negative_control':{'order':18,'edges':[list(e) for e in EDGES18],
            'deletion_sets':deletion_count,'perfect_matchings':sum(counts.values()),
            'spectra':[{ 'lengths':list(s), 'count':counts[s]} for s in sorted(counts)],
            'p3_factor':[list(p) for p in P3]},
            'limitations':['generator-side audit; no registered verifier receipt or root admission']}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('certificate',type=Path)
    args=parser.parse_args()
    print(json.dumps(run(args.certificate),sort_keys=True,indent=2))
