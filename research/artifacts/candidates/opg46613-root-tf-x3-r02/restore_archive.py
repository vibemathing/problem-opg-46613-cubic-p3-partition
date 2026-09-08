"""Restore fixed replay members without overwriting different existing bytes."""
import base64,hashlib,json,zlib
from pathlib import Path

def main():
 info=json.loads(Path('archive-info.json').read_text())
 encoded=b''.join(Path(p).read_bytes() for p in info['parts'])
 if hashlib.sha256(encoded).hexdigest()!=info['encoded_sha256']:raise ValueError('archive bytes')
 d=zlib.decompressobj();raw=d.decompress(base64.b64decode(encoded,validate=True),1048576)
 if not d.eof or d.unused_data or len(raw)!=info['decoded_bytes']:raise ValueError('decode bound/trailer')
 if hashlib.sha256(raw).hexdigest()!=info['decoded_sha256']:raise ValueError('decoded identity')
 obj=json.loads(raw)
 if set(obj)!=set(info['members']):raise ValueError('member names')
 for name,text in obj.items():
  if Path(name).name!=name or name.startswith('.') or not isinstance(text,str):raise ValueError('member path/type')
  data=text.encode('utf-8');expected=info['members'][name]
  if len(data)!=expected['bytes'] or hashlib.sha256(data).hexdigest()!=expected['sha256']:raise ValueError('member bytes')
  p=Path(name)
  if p.exists() and p.read_bytes()!=data:raise ValueError('refuse different existing member')
  if not p.exists():p.write_bytes(data)
 print(json.dumps({'status':'restored_exact_bytes','members':len(obj),'verdict':'candidate_only'}))
if __name__=='__main__':main()
