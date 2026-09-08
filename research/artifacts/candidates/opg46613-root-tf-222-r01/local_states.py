#!/usr/bin/env python3
"""Two local implementations, all roles at up to four active vertices, lengths 5/8/11/14."""
import itertools,json
from functools import lru_cache

def table(L):
    blocks=[sum(1<<((i+j)%L) for j in range(3))for i in range(L)]
    @lru_cache(None)
    def cover(mask):
        if mask==0:return 1
        first=mask&-mask
        return sum(cover(mask^b)for b in blocks if b&first and b&mask==b)
    def direct(pos,B):
        total=0;active=set(pos);bs=sorted(B)
        for neighbors in itertools.product(*[[(v-1)%L,(v+1)%L]for v in bs]):
            if len(set(neighbors))<len(neighbors) or active.intersection(neighbors):continue
            removed=sum(1<<v for v in active|set(neighbors));total+=cover(((1<<L)-1)^removed)
        return total
    def equations(pos,B):
        h=len(pos);gaps=[(pos[(j+1)%h]-pos[j])%L or L for j in range(h)];rs=[(d-1)%3 for d in gaps]
        total=0;bs=sorted(B)
        for sides in itertools.product((-1,1),repeat=len(bs)):
            units=[0]*h;used=[];okay=True
            for v,side in zip(bs,sides):
                i=pos.index(v);gi=(i-1)%h if side<0 else i
                if gaps[gi]==1:okay=False;break
                units[gi]+=1;used.append((v+side)%L)
            if okay and units==rs and len(set(used))==len(used):total+=1
        return total
    tested=0;feasible=0;summary={}
    for h in (1,2,3,4):
        yes=0;cases=0
        for pos in itertools.combinations(range(L),h):
            for role in range(1<<h):
                B={pos[j]for j in range(h)if role>>j&1};d=direct(pos,B);e=equations(pos,B)
                if d!=e:raise ValueError(('local_disagreement',L,pos,role,d,e))
                if d and (h+len(B)-L)%3:raise ValueError('residue_claim')
                yes+=bool(d);cases+=1
        summary[str(h)]={'tested':cases,'feasible':yes};tested+=cases;feasible+=yes
    return {'length':L,'tested':tested,'feasible':feasible,'by_active_count':summary}
if __name__=='__main__':
    result=[table(L)for L in (5,8,11,14)]
    print(json.dumps({'status':'PASS','scope':'all positions and all A/B words with one through four active vertices at each listed length',
                     'tables':result,'verdict':'candidate_only'},sort_keys=True))
