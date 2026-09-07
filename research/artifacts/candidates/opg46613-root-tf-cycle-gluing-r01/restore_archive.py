#!/usr/bin/env python3
"""Restore the exact historical archive from committed, ordered byte segments."""
import hashlib,json,pathlib
P=pathlib.Path(__file__).resolve().parent
NAMES=([f'replay-data.part-{i:02}.txt' for i in range(4)]+
       [f'replay-data.part-{i:02}-{j}.txt' for i in (4,5) for j in range(4)]+
       ['replay-data.part-06.txt'])
EXPECTED='bb288e3c419fc26f63cd71fb610ba05f0ef23e5380c1ac4bc8cead7de4618669'
parts=[]
for name in NAMES:
    raw=(P/name).read_bytes()
    if len(raw)>4096:raise SystemExit('segment exceeds fixed bound')
    parts.append(raw)
raw=b''.join(parts)
if len(raw)!=24652 or hashlib.sha256(raw).hexdigest()!=EXPECTED:
    raise SystemExit('archive byte identity mismatch')
x=json.loads(raw)
if len(x['files'])!=21 or x['total_decoded_bytes']!=95730:
    raise SystemExit('archive shape mismatch')
target=P/'replay-data.json'
if target.exists():
    if target.read_bytes()!=raw:raise SystemExit('refuse to replace different existing archive')
else:
    with target.open('xb') as stream:stream.write(raw)
print(json.dumps({'status':'byte_restore_pass','bytes':len(raw),'sha256':EXPECTED,
                  'segments':len(parts),'mathematical_execution':False},sort_keys=True))
