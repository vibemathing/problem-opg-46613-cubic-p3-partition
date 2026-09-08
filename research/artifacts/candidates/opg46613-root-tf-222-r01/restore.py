#!/usr/bin/env python3
"""Restore bounded replay bytes from exact transport segments; reject conflicting files."""
from pathlib import Path
import json,base64,zlib,hashlib
ROOT=Path(__file__).resolve().parent
MAX=1048576
ARCHIVE_SHA='36925f08d86b46babec3f3bb7c3ec6e08bce10f89cc9d72ba538185e2427ef69'

def main():
    raw=b''.join((ROOT/f'replay-archive.part-{i:02d}.txt').read_bytes()for i in range(7))
    if len(raw)!=24339 or hashlib.sha256(raw).hexdigest()!=ARCHIVE_SHA:raise ValueError('archive_hash')
    a=json.loads(raw);staged=[(ROOT/'replay-archive.json',raw)];total=0
    for f in a['files']:
        name=f['name'];p=Path(name)
        if p.name!=name or p.is_absolute() or name in ('.','..'):raise ValueError('path')
        n=f['bytes']
        if type(n)is not int or not 0<=n<=MAX:raise ValueError('size')
        obj=zlib.decompressobj();b=obj.decompress(base64.b64decode(f['zlib_base64'],validate=True),n+1)
        if len(b)!=n or not obj.eof or obj.unconsumed_tail or obj.unused_data:raise ValueError('decompression')
        if hashlib.sha256(b).hexdigest()!=f['sha256']:raise ValueError('hash')
        b.decode('utf-8');total+=n
        if total>4*MAX:raise ValueError('total')
        staged.append((ROOT/name,b))
    if len({p.name for p,b in staged})!=len(staged):raise ValueError('duplicate')
    for target,b in staged:
        if target.is_symlink()or(target.exists()and target.read_bytes()!=b):raise ValueError('existing')
    for p,b in staged:
        if not p.exists():p.write_bytes(b)
    print(json.dumps({'members':len(staged)-1,'bytes':total,'archive_bytes':len(raw),'status':'PASS','verdict':'candidate_only'}))
if __name__=='__main__':main()
