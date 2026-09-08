#!/usr/bin/env python3
"""Restore bounded fixed execution bytes; never overwrite different content."""
import base64,hashlib,json,zlib
from pathlib import Path

root=Path(__file__).resolve().parent
allowed={'new-hosts.json','audit-data.json','execution.json'}|{p+s for p in ('search_hosts','audit','local_switches','check') for s in ('-stdout.json','-stderr.txt')}
parts=[root/f'data-{i:02d}.txt' for i in range(23)]
raw=b''.join(p.read_bytes() for p in parts)
assert len(raw)==22891 and hashlib.sha256(raw).hexdigest()=='645d6c49782157a5635cc80b35d7b9131f369c0d868e4338dc121234e2877a91'
a=json.loads(raw)
assert a['format']=='bounded-zlib-base64-members-v1' and len(a['members'])==len(allowed)
assert {m['name'] for m in a['members']}==allowed
assert sum(m['bytes'] for m in a['members'])<=1048576
for m in a['members']:
    assert 0<=m['bytes']<=1048576
    d=zlib.decompressobj();b=d.decompress(base64.b64decode(m['zlib_base64'],validate=True),m['bytes']+1)
    assert d.eof and not d.unused_data and not d.unconsumed_tail
    assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
    target=root/m['name']
    if target.exists():assert target.read_bytes()==b,'existing bytes differ: '+m['name']
    else:target.write_bytes(b)
print(json.dumps({'status':'PASS','restored_members':len(allowed),'operation':'byte_restoration_not_mathematical_replay','verdict':'candidate_only'},sort_keys=True))
