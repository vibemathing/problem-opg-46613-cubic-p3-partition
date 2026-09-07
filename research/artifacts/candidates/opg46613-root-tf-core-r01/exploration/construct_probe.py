import itertools,json
from functools import lru_cache
from pathlib import Path
E=lambda a,b:tuple(sorted((a,b)))
cycles=[list(range(7)),list(range(7,25)),list(range(25,36))]
ce={E(c[i],c[(i+1)%len(c)]) for c in cycles for i in range(len(c))}
m=[(1,5),(3,6)]+[(7+i,7+i+9) for i in [1,2,4,5,7,8]]+[(26,32),(27,33),(29,34),(30,35)]+[(0,7),(2,10),(4,13),(16,25),(19,28),(22,31)]
e=sorted(ce|set(m));adj=[set() for _ in range(36)]
for u,v in e:adj[u].add(v);adj[v].add(u)
cross=m[-6:];allowed=set(e)
rows=[(a,c,b) for c in range(36) for a,b in itertools.combinations(sorted(adj[c]),2) if E(a,c) in allowed and E(c,b) in allowed]
rb=[sum(1<<v for v in r) for r in rows];rc=[sum(E(a,b) in m for a,b in zip(r,r[1:])) for r in rows]
idx=[[i for i,r in enumerate(rows) if v in r] for v in range(36)]
@lru_cache(None)
def solve(mask,k):
 if not mask:return ()
 cand=min(([i for i in idx[v] if rb[i]&mask==rb[i] and rc[i]<=k] for v in range(36) if mask>>v&1),key=len)
 for i in cand:
  r=solve(mask^rb[i],k-rc[i])
  if r is not None:return (i,)+r
 return None
for k in range(2,7):
 z=solve((1<<36)-1,k)
 print('k',k,'factor',[rows[i] for i in z] if z else None,'states',solve.cache_info())
 if z is not None:break
x={'n':36,'edges':e,'cycles':cycles,'perfect_matching':m,'cross_edges':cross,'factor':[rows[i] for i in z]}
(Path(__file__).resolve().parent/'cycle_tree_witness.json').write_text(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n')
# direct vertex deletion BFS just exploratory
for size in range(3):
 for S in itertools.combinations(range(36),size):
  live=set(range(36))-set(S);seen={min(live)};front=list(seen)
  while front:
   u=front.pop()
   for v in (adj[u]&live)-seen:seen.add(v);front.append(v)
  assert seen==live,S
print('all vertex deletions pass','triangles',sum(1 for a,b,c in itertools.combinations(range(36),3) if b in adj[a] and c in adj[a] and c in adj[b]))
