#!/usr/bin/env python3
"""Exhaustive bounded abstract tests; general proof is separate."""
from itertools import product,combinations_with_replacement
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from surgery import component_rows


def value(n,es):return sum(abs(c['vertices']-c['edges']) for c in component_rows(range(n),es))


def main():
    counts={};bounds={};total=0
    for n in range(1,4):
        pairs=list(combinations_with_replacement(range(n),2))
        for multiplicities in product(range(3),repeat=len(pairs)):
            E=[list(p) for p,m in zip(pairs,multiplicities) for _ in range(m)];old=value(n,E)
            for (a,b),m in zip(pairs,multiplicities):
                for x,y in product(range(3),repeat=2):
                    r=(x+y+1)%3
                    if m<r:continue
                    for t in (0,1):
                        es=[p[:] for p in E]
                        for _ in range(r):es.remove([a,b])
                        es += [[a,n]]*x+[[b,n]]*y+[[n,n]]*t
                        delta=value(n+1,es)-old;assert delta<=2
                        key=f'{x}{y}-t{t}';bounds[key]=max(bounds.get(key,-100),delta);counts[key]=counts.get(key,0)+1;total+=1
    print(json.dumps({'status':'PASS','verdict':'candidate_only','abstract_cases':total,
                      'range':'1..3 old owners; loop/pair multiplicities 0..2; all eligible pairs/residue splits; both new-loop cases',
                      'max_slot_potential_increase':bounds,'case_counts':counts},sort_keys=True))

if __name__=='__main__':main()
