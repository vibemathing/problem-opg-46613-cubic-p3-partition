#!/usr/bin/env python3
"""One bounded fresh replay. Output directory must not already exist."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
LIMITS={'cpu_seconds':30,'wall_seconds':40,'address_space_bytes':536870912,
        'per_output_file_bytes':2097152,'worker_processes':1,'threads':1,'core_dump_bytes':0}

def restrict():
    for k,v in [(resource.RLIMIT_CPU,LIMITS['cpu_seconds']),
                (resource.RLIMIT_AS,LIMITS['address_space_bytes']),
                (resource.RLIMIT_FSIZE,LIMITS['per_output_file_bytes']),
                (resource.RLIMIT_CORE,0)]:
        resource.setrlimit(k,(v,v))

def main():
    out=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'replay')
    out.mkdir(exist_ok=False)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); clock=time.monotonic()
    with (out/'stdout.json').open('wb') as stdout,(out/'stderr.txt').open('wb') as stderr:
        child=subprocess.Popen([sys.executable,'-I','-S','checker.py'],cwd=ROOT,
               stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,preexec_fn=restrict,
               env={'PATH':os.environ.get('PATH',''),'LC_ALL':'C','OMP_NUM_THREADS':'1'})
        timed_out=False
        try: code=child.wait(timeout=LIMITS['wall_seconds'])
        except subprocess.TimeoutExpired:
            child.kill(); code=child.wait(); timed_out=True
    usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    result={'verdict':'candidate_only','kind':'same_generation_domain_execution_observation',
            'command':'python3 -I -S checker.py','python':sys.version,'started_at':start,
            'elapsed_wall_seconds':round(time.monotonic()-clock,6),'exit_code':code,
            'timed_out':timed_out,'limits':LIMITS,
            'worker_peak_rss_kib_linux':usage.ru_maxrss,'worker_user_cpu_seconds':usage.ru_utime,
            'worker_system_cpu_seconds':usage.ru_stime,
            'sha256':{n:h(ROOT/n) for n in ('input.json','checker.py','run_bounded.py')},
            'output_sha256':{n:h(out/n) for n in ('stdout.json','stderr.txt')},
            'lean_elaboration':None,'axiom_report':None,'trusted_attestation':None}
    (out/'execution.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
    raise SystemExit(0 if code==0 and not timed_out else 1)

if __name__=='__main__': main()
