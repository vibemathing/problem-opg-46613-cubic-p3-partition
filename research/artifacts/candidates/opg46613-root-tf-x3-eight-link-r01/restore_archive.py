"""Restore exact replay bytes only; this action is not mathematical verification."""
from pathlib import Path
import base64,hashlib,json,lzma
p=Path(__file__).resolve().parent
m=json.loads((p/'archive-info.json').read_text())
h=lambda b:hashlib.sha256(b).hexdigest()
s=b''.join((p/n).read_bytes() for n in m['segments'])
assert len(s)==m['encoded_bytes'] and h(s)==m['encoded_sha256']
z=lzma.LZMADecompressor(memlimit=128*1024**2)
b=z.decompress(base64.b85decode(s),max_length=4*1024**2)
assert z.eof and not z.unused_data and len(b)==m['decoded_bytes'] and h(b)==m['decoded_sha256']
d=json.loads(b);assert set(d)==set(m['members'])
q=p/'replay';q.mkdir(exist_ok=True)
for n,text in d.items():
 assert Path(n).name==n and n not in ('.','..')
 v=text.encode();assert len(v)==m['members'][n]['bytes'] and h(v)==m['members'][n]['sha256']
 f=q/n
 if f.exists():assert f.read_bytes()==v,'refuse to overwrite different replay bytes'
 else:f.write_bytes(v)
print(json.dumps({'restored_members':len(d),'status':'exact-byte-restoration-only'}))
