#!/usr/bin/env python3
"""Generate deterministic labelled controls, not an isomorphism/order census."""
import itertools
import json
import random
from pathlib import Path


def partitions(n, lower=4):
    if n == 0:
        yield []
    for first in range(lower, n + 1):
        for rest in partitions(n-first, first):
            yield [first] + rest


def connected(adj, banned):
    live = set(range(len(adj))) - set(banned)
    if not live:
        return False
    reached, todo = set(), [min(live)]
    while todo:
        v = todo.pop()
        if v in reached:
            continue
        reached.add(v)
        todo.extend(adj[v] & live - reached)
    return reached == live


def main():
    rng = random.Random(466132709)
    cases, observations = [], []
    for n in (6, 12, 18):
        for lengths in partitions(n):
            cycles, start = [], 0
            for length in lengths:
                cycles.append(list(range(start, start+length)))
                start += length
            f = {tuple(sorted((c[i], c[(i+1) % len(c)]))) for c in cycles for i in range(len(c))}
            forbidden = f | {tuple(sorted((c[i], c[(i+2) % len(c)]))) for c in cycles for i in range(len(c))}
            count, seen, draws = 0, set(), 0
            target = 1 if n == 6 else 4
            while count < target and draws < 20000:
                draws += 1
                vertices = list(range(n))
                rng.shuffle(vertices)
                m = sorted(tuple(sorted(vertices[i:i+2])) for i in range(0, n, 2))
                if any(e in forbidden for e in m) or tuple(m) in seen:
                    continue
                edges = sorted(f | set(m))
                adj = [set() for _ in range(n)]
                for a, b in edges:
                    adj[a].add(b); adj[b].add(a)
                if not all(connected(adj, d) for k in range(3) for d in itertools.combinations(range(n), k)):
                    continue
                seen.add(tuple(m)); count += 1
                cases.append({'id': '-'.join(map(str, lengths)) + ':' + str(count),
                              'n': n, 'cycles': cycles, 'matching': m, 'edges': edges})
            if count != target:
                raise RuntimeError('Generation budget exhausted for ' + str(lengths))
            observations.append({'lengths': lengths, 'draws': draws, 'accepted': count})
    data = {'verdict': 'candidate_only', 'seed': 466132709,
            'scope': 'Four labelled controls per nontrivial length partition; not all graphs or isomorphism classes.',
            'complete_length_partitions': {str(n): list(partitions(n)) for n in (6, 12, 18)},
            'generation': observations, 'cases': cases}
    Path('inputs.json').write_text(json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({'cases': len(cases), 'draws': sum(x['draws'] for x in observations),
                      'partition_count': len(observations), 'status': 'PASS'}))


if __name__ == '__main__':
    main()
