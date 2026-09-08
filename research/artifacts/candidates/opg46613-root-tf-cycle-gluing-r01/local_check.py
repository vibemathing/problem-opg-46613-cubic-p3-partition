#!/usr/bin/env python3
"""Exact-cover check of cycle splitting, separate from constructor.local_cover."""
from itertools import combinations, product
from functools import lru_cache
import hashlib
import json


def exact(L, roles):
    active = set(roles)
    rows = [[] for _ in range(L)]
    def add(vertices, kind, center=None):
        mask = sum(1 << v for v in vertices)
        for v in vertices:
            rows[v].append((mask, (kind, tuple(vertices), center)))
    for v, role in roles.items():
        if role == 'A':
            add([v], 'A')
        elif role == 'B':
            for w in ((v-1) % L, (v+1) % L):
                if w not in active:
                    add([v,w], 'B', v)
    for center in range(L):
        p = [(center-1) % L, center, (center+1) % L]
        if not (set(p) & active):
            add(p, 'P3', center)
    @lru_cache(None)
    def count(mask):
        if count.cache_info().currsize > 5000:
            raise RuntimeError('local_node_budget')
        if not mask:
            return 1
        # Pick a vertex with the fewest surviving rows, not a residual path rule.
        live = [v for v in range(L) if mask >> v & 1]
        options = min(([r for r in rows[v] if r[0] & mask == r[0]] for v in live), key=len)
        return sum(count(mask ^ r[0]) for r in options)
    return count((1 << L)-1), count.cache_info().currsize


def predicted(L, roles):
    letters = list(roles.values())
    a, b = letters.count('A'), letters.count('B')
    if (L-a-2*b) % 3:
        return 0
    if not letters:
        return 3
    if len(letters) == 1:
        return 1 if a else 2
    u, v = sorted(roles)
    d = (v-u) % L
    if a == 2:
        return int(d % 3 == 1)
    if b == 2:
        return 2 if d % 3 == 2 else 1
    return int(d % 3 != 0)


def main():
    stream, tested, feasible, states = hashlib.sha256(), 0, 0, 0
    kinds = {}
    # One endpoint at zero uses the rotation automorphism of the same cycle.
    for L in range(4, 61):
        tests = [{}] + [{0:r} for r in 'AB']
        tests += [{0:a,d:b} for d in range(1,L) for a,b in product('AB', repeat=2)]
        for roles in tests:
            count, used = exact(L, roles)
            expected = predicted(L, roles)
            if count != expected:
                raise ValueError(('local_formula_mismatch', L, roles, count, expected))
            row = [L, sorted(roles.items()), count]
            stream.update((json.dumps(row,separators=(',',':'))+'\n').encode())
            tested += 1
            feasible += bool(count)
            states += used
            key = ''.join(roles[v] for v in sorted(roles)) or 'empty'
            kinds[key] = kinds.get(key,0)+1
    # Exact negative examples are cycle-boundary failures, not cubic host examples.
    negatives = [
        {'L':6,'roles':[[0,'A'],[3,'B']],'reason':'both gaps demand two extensions but only one B'},
        {'L':8,'roles':[[0,'A'],[2,'A']],'reason':'nonzero residual path remainders'},
        {'L':4,'roles':[[0,'A']],'reason':None}]
    # Third entry is a positive control guarding against an always-UNSAT checker.
    results = [exact(x['L'], dict(x['roles']))[0] for x in negatives]
    if results != [0,0,1]:
        raise ValueError('negative_positive_control_mismatch')
    print(json.dumps({'verdict':'candidate_only','status':'PASS',
          'cycle_lengths':[4,60], 'tests':tested,'feasible':feasible,
          'exact_cover_states_total':states,'kind_counts':kinds,
          'complete_test_stream_sha256':stream.hexdigest(),
          'local_controls':[{**x,'count':c} for x,c in zip(negatives,results)],
          'scope':'all specified local states on lengths 4..60, not an all-length proof or host UNSAT',
          'trusted_attestation':None},sort_keys=True,separators=(',',':')))

if __name__ == '__main__':
    main()
