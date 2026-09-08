#!/usr/bin/env python3
"""Cycle gluing constructor. Newly written; no previous candidate code imported."""
from __future__ import annotations
import itertools as it
import json
from pathlib import Path


def partitions(n, lower=4):
    if n == 0:
        yield ()
    for first in range(lower, n + 1):
        for tail in partitions(n - first, first):
            yield (first,) + tail


def local_cover(cycle, roles):
    positions = {v: i for i, v in enumerate(cycle)}
    active = set(roles)
    if not active:
        return None if len(cycle) % 3 else {
            'singletons': [], 'pairs': [],
            'paths': [cycle[i:i+3] for i in range(0, len(cycle), 3)]}
    centers = sorted(v for v in roles if roles[v] == 'B')
    for directions in it.product((-1, 1), repeat=len(centers)):
        used, pairs = set(active), []
        for v, step in zip(centers, directions):
            w = cycle[(positions[v] + step) % len(cycle)]
            if w in used:
                break
            used.add(w)
            pairs.append([v, w])
        else:
            start = positions[min(active)]
            runs, run = [], []
            for i in range(1, len(cycle) + 1):
                v = cycle[(start + i) % len(cycle)]
                if v in used:
                    if run:
                        runs.append(run)
                        run = []
                else:
                    run.append(v)
            if all(len(r) % 3 == 0 for r in runs):
                return {'singletons': sorted(v for v in roles if roles[v] == 'A'),
                        'pairs': pairs,
                        'paths': [r[i:i+3] for r in runs for i in range(0, len(r), 3)]}
    return None


def lift(cycles, selected):
    """One A-singleton and one B-centered pair for each selected matching edge."""
    for direction in it.product((0, 1), repeat=len(selected)):
        roles = {}
        for (u, v), d in zip(selected, direction):
            roles[u], roles[v] = ('A', 'B') if d == 0 else ('B', 'A')
        pieces = [local_cover(c, {v: roles[v] for v in c if v in roles}) for c in cycles]
        if any(p is None for p in pieces):
            continue
        pairs = {u: v for p in pieces for u, v in p['pairs']}
        factor = [q for p in pieces for q in p['paths']]
        for u, v in selected:
            a, b = (u, v) if roles[u] == 'A' else (v, u)
            factor.append([a, b, pairs[b]])
        return {'factor': factor, 'pieces': pieces,
                'roles': [[v, roles[v]] for v in sorted(roles)]}
    return None


def select(cycles, matching):
    owner = {v: i for i, c in enumerate(cycles) for v in c}
    position = {v: j for c in cycles for j, v in enumerate(c)}
    residue = [len(c) % 3 for c in cycles]
    links = [(tuple(e), owner[e[0]], owner[e[1]]) for e in matching
             if owner[e[0]] != owner[e[1]]]
    if not any(residue):
        return [], 'all_zero'
    if len(cycles) == 2:
        return ([links[0][0]], 'two_12') if links else (None, 'disconnected')
    if len(cycles) == 3:
        if sorted(residue) == [0, 1, 2]:
            for e, i, j in links:
                if {residue[i], residue[j]} == {1, 2}:
                    return [e], 'three_012_direct'
        for (e, a, b), (f, c, d) in it.combinations(links, 2):
            if len({a, b, c, d}) != 3:
                continue
            middle = next(iter({a, b} & {c, d}))
            u = next(v for v in e if owner[v] == middle)
            v = next(v for v in f if owner[v] == middle)
            dist = (position[v] - position[u]) % len(cycles[middle])
            if residue == [1, 1, 1]:
                return [e, f], 'three_111'
            if residue == [2, 2, 2] and dist % 3 == 1:
                return [e, f], 'three_222'
            if sorted(residue) == [0, 1, 2] and residue[middle] == 0 and dist % 3:
                return [e, f], 'three_012_via_zero'
        return None, 'three_phase_gap'
    lengths = sorted(map(len, cycles))
    if lengths == [4, 4, 4, 6]:
        fours = {i for i, c in enumerate(cycles) if len(c) == 4}
        for (e, a, b), (f, c, d) in it.combinations(links, 2):
            if {a, b, c, d} == fours:
                return [e, f], 'four_4446'
        return None, 'small_cut_4446'
    if lengths == [4, 4, 5, 5]:
        for (e, a, b), (f, c, d) in it.combinations(links, 2):
            if len({a, b, c, d}) == 4 and residue[a] != residue[b] and residue[c] != residue[d]:
                return [e, f], 'four_4455'
        return None, 'quotient_pair_gap_4455'
    return None, 'outside_proved_classes'


def main():
    data = json.loads(Path('inputs.json').read_text())
    output = []
    for case in data['cases']:
        selected, branch = select(case['cycles'], case['matching'])
        if selected is None:
            raise ValueError('Unresolved class: ' + case['id'] + ' / ' + branch)
        lifted = lift(case['cycles'], selected)
        if lifted is None:
            raise ValueError('Local gluing failed: ' + case['id'])
        output.append({'id': case['id'], 'branch': branch,
                       'selected_matching': selected, **lifted})
    print(json.dumps({'verdict': 'candidate_only', 'cases': output}, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
