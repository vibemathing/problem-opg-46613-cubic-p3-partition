"""Bounded exploratory parity test; not a graph census or root proof."""
import functools, itertools, json, resource, time
resource.setrlimit(resource.RLIMIT_CPU,(15,15))
resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
start=time.monotonic()
def count(n,edges):
 a=[set() for _ in range(n)]
 for u,v in edges:a[u].add(v);a[v].add(u)
 rows=[(1<<c)|(1<<l)|(1<<r) for c in range(n) for l,r in itertools.combinations(a[c],2)]
 inc=[[p for p in rows if p>>v&1] for v in range(n)]
 @functools.lru_cache(None)
 def rec(mask):
  if not mask:return 1
  if time.monotonic()-start>12:raise TimeoutError('deadline')
  ids=min(([p for p in inc[v] if p&mask==p] for v in range(n) if mask>>v&1),key=len)
  return sum(rec(mask^p) for p in ids)
 return rec((1<<n)-1),rec.cache_info().currsize
samples=[]
from pathlib import Path
x=json.loads((Path(__file__).parent/'input.json').read_text())
samples.append(('G36',x['n'],x['edges']))
h=[(i,(i+1)%18) for i in range(18)]+[(0,5),(1,8),(2,13),(3,10),(4,15),(6,11),(7,14),(9,16),(12,17)]
samples.append(('Hamilton18',18,h))
e=[(i,j) for i in range(3) for j in range(3,6)]
samples.append(('K33',6,e))
g=[(0,1),(2,1),(0,3),(2,10),(1,17),(0,15),(2,8),(9,22),(16,23)]
for t in (3,10,17):g += [(t+i,t+(i+1)%5) for i in range(5)]+[(t+5,t+1),(t+5,t+3),(t+6,t+2),(t+6,t+4)]
samples.append(('layer24',24,g))
out=[]
for name,n,es in samples:
 c,s=count(n,es);out.append({'name':name,'n':n,'count':c,'states':s})
print(json.dumps({'scope':'four labeled inputs only; no universal parity inference','results':out,'elapsed':time.monotonic()-start},sort_keys=True))
