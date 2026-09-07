#!/usr/bin/env python3
"""Run this fixed checker with explicit Linux resource and output limits."""
from pathlib import Path
import datetime
import hashlib
import json
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (25, 25))
    resource.setrlimit(resource.RLIMIT_AS, (256*1024*1024, 256*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024*1024, 1024*1024))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

if __name__ == '__main__':
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    begin = time.monotonic()
    timed_out = False
    with (ROOT/'stdout.json').open('wb') as out, (ROOT/'stderr.txt').open('wb') as err:
        try:
            completed = subprocess.run([sys.executable,'-I','-S','checker.py'],cwd=ROOT,
                    stdout=out,stderr=err,timeout=35,preexec_fn=limits,check=False)
            code = completed.returncode
        except subprocess.TimeoutExpired:
            code, timed_out = None, True
    use = resource.getrusage(resource.RUSAGE_CHILDREN)
    sha = lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
    record = {'verdict':'candidate_only','kind':'same_generation_domain_execution_observation',
        'started_at':started,'command':'python3 -I -S checker.py','python':sys.version,
        'limits':{'cpu_seconds':25,'wall_seconds':35,'address_space_bytes':268435456,
                  'per_output_file_bytes':1048576,'worker_processes':1,'threads':1,'core_dump_bytes':0},
        'exit_code':code,'timed_out':timed_out,'elapsed_wall_seconds':round(time.monotonic()-begin,6),
        'worker_user_cpu_seconds':use.ru_utime,'worker_system_cpu_seconds':use.ru_stime,
        'worker_peak_rss_kib_linux':use.ru_maxrss,
        'file_sha256':{p:sha(p) for p in ('witness.json','checker.py','run_bounded.py','stdout.json','stderr.txt')},
        'lean_execution':{'executed':False,'elaboration_report':None,'axiom_report':None,'status':'pending_unverified'},
        'historical_programs_or_raw_outputs_recovered':False,
        'admission':False}
    (ROOT/'execution.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(record,indent=2))
    sys.exit(0 if code==0 and not timed_out else 1)
