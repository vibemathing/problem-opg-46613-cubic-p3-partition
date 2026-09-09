import base64,hashlib,json,lzma
from pathlib import Path
root=Path(__file__).resolve().parent
info=json.loads((root/'archive-info.json').read_text())
encoded=''.join(p.read_text()for p in sorted(root.glob('replay-*.txt'))).encode()
assert len(encoded)==info['encoded_bytes'] and hashlib.sha256(encoded).hexdigest()==info['encoded_sha256']
raw=lzma.decompress(base64.b85decode(encoded),memlimit=134217728)
assert len(raw)==info['decoded_bytes'] and hashlib.sha256(raw).hexdigest()==info['decoded_sha256']
items=json.loads(raw);assert set(items)==set(info['members'])
out=root/'replay';out.mkdir(exist_ok=True)
for name,text in items.items():
    assert Path(name).name==name and name not in ('.','..')
    b=text.encode();d=info['members'][name]
    assert len(b)==d['bytes'] and hashlib.sha256(b).hexdigest()==d['sha256']
    p=out/name
    if p.exists():assert p.read_bytes()==b,'do not overwrite a changed replay'
    else:p.write_bytes(b)
print(json.dumps({'restored':len(items),'byte_transport_only':True}))
