#!/usr/bin/env python3
"""Restore exact replay bytes; refuses unknown paths and mismatching existing files."""
from pathlib import Path
import base64,hashlib,json,sys,zlib
ROOT=Path(__file__).resolve().parent
STAGES=('generate','constructor','verify','local_check','explore24','verify24')
ALLOWED={'inputs.json','exploratory/verify24-initial.py','exploratory/verify24-initial-execution.json'}
ALLOWED|={s+suffix for s in STAGES for suffix in ('.stdout.json','.stderr.txt','-execution.json')}
MAX_FILE=1048576
MAX_TOTAL=8388608

def main():
    archive=ROOT/'replay-data.json'
    if archive.stat().st_size>MAX_TOTAL:raise ValueError('archive_size')
    x=json.loads(archive.read_bytes())
    if x.get('format')!='lossless-replay-bytes-v1':raise ValueError('archive_format')
    names=[e['name'] for e in x['files']]
    if set(names)!=ALLOWED or len(names)!=len(ALLOWED):raise ValueError('archive_names')
    staged=[];total=0
    for e in x['files']:
        n=e['bytes']
        if type(n) is not int or not 0<=n<=MAX_FILE:raise ValueError('file_size')
        compressed=base64.b64decode(e['zlib_base64'],validate=True)
        obj=zlib.decompressobj();raw=obj.decompress(compressed,n+1)
        if len(raw)!=n or not obj.eof or obj.unused_data or obj.unconsumed_tail:raise ValueError('decompression_boundary')
        if hashlib.sha256(raw).hexdigest()!=e['sha256']:raise ValueError('file_hash')
        total+=n
        if total>MAX_TOTAL:raise ValueError('total_size')
        target=ROOT/e['name']
        if target.is_symlink() or target.parent.is_symlink() or not target.resolve().is_relative_to(ROOT):raise ValueError('path_boundary')
        if target.exists() and target.read_bytes()!=raw:raise ValueError('existing_mismatch:'+e['name'])
        staged.append((target,raw))
    if total!=x['total_decoded_bytes']:raise ValueError('total_count')
    for target,raw in staged:
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            with target.open('xb') as f:f.write(raw)
    print(json.dumps({'status':'PASS','files':len(staged),'decoded_bytes':total,'verdict':'candidate_only'},sort_keys=True))
if __name__=='__main__':main()
