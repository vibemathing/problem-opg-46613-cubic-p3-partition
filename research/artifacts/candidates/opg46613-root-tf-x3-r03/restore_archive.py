"""Restore the exact bounded source/data archive. This is transport, not validation."""
import base64,hashlib,json,lzma
from pathlib import Path
H=lambda b:hashlib.sha256(b).hexdigest()
a=json.loads(Path('archive-info.json').read_text());buf=[]
for p in a['parts']:
 b=Path(p['path']).read_bytes()
 if len(b)!=p['bytes'] or H(b)!=p['sha256']:raise ValueError('part identity')
 buf.append(b)
s=b''.join(buf)
if len(s)!=a['encoded_bytes'] or H(s)!=a['encoded_sha256']:raise ValueError('encoded identity')
d=lzma.LZMADecompressor(memlimit=268435456);raw=d.decompress(base64.b85decode(s),max_length=1048576)
if not d.eof or d.unused_data:raise ValueError('bounded archive')
if len(raw)!=a['decoded_bytes'] or H(raw)!=a['decoded_sha256']:raise ValueError('decoded identity')
m=json.loads(raw)
if set(m)!=set(a['members']):raise ValueError('member set')
root=Path('replay');root.mkdir(exist_ok=True)
for name,text in m.items():
 if Path(name).name!=name or name in ('','..','.'):raise ValueError('unsafe member')
 b=text.encode();record=a['members'][name]
 if len(b)!=record['bytes'] or H(b)!=record['sha256']:raise ValueError('member identity')
 target=root/name
 if target.exists() and target.read_bytes()!=b:raise ValueError('existing member differs')
 target.write_bytes(b)
print(json.dumps({'restored_members':len(m),'sha256':H(raw),'status':'bytes_restored_not_mathematical_check'}))
