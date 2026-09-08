#!/usr/bin/env python3
"""Bounded fresh replays, sanitized observations, no trusted receipt or attestation."""
from pathlib import Path
import subprocess,resource,sys,os,time,json,hashlib,datetime,shutil
ROOT=Path(__file__).resolve().parent
STAGES=['audit.py','direct_cover.py','certificate_check.py','local_states.py','search222.py']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bounds():
    resource.setrlimit(resource.RLIMIT_CPU,(25,25));resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
    resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576));resource.setrlimit(resource.RLIMIT_CORE,(0,0))

def main():
    os.chdir(ROOT);records=[]
    for name in STAGES:
        out=ROOT/(name[:-3]+'.stdout.json');err=ROOT/(name[:-3]+'.stderr.txt')
        start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
        code="import sys,runpy;sys.path.insert(0,'.');runpy.run_path("+repr(name)+",run_name='__main__')"
        cmd=[sys.executable,'-I','-S','-c',code];timeout=False
        with out.open('wb')as o,err.open('wb')as e:
            p=subprocess.Popen(cmd,stdout=o,stderr=e,preexec_fn=bounds(),env={'PATH':os.environ.get('PATH',''),'PYTHONHASHSEED':'0','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
            try:exit_code=p.wait(timeout=35)
            except subprocess.TimeoutExpired:p.kill();exit_code=p.wait();timeout=True
        record={'stage':name,'started_at':start,'elapsed_wall_seconds':round(time.monotonic()-t,6),
          'exit_code':exit_code,'timed_out':timeout,'command':['python3','-I','-S','-c',code],
          'limits':{'cpu_seconds':25,'wall_seconds':35,'address_space_bytes':536870912,'per_file_output_bytes':1048576,'worker_processes':1,'threads':1},
          'source_sha256':sha(ROOT/name),'stdout_sha256':sha(out),'stderr_sha256':sha(err)}
        records.append(record)
        if exit_code or timeout:break
    names=STAGES+['allocation.py','run_bounded.py','objects.json','allocation-results.json','negative-42.json','initial-search-failure.json']+[n[:-3]+s for n in STAGES for s in ('.stdout.json','.stderr.txt')]
    hashes={n:sha(ROOT/n)for n in names}
    obj={'kind':'same_generation_domain_execution_observation','python':sys.version,'stages':records,'file_sha256':hashes,
         'lean_executable_present':bool(shutil.which('lean')),'lean_executed':False,'trusted_attestation':None,'verdict':'candidate_only'}
    (ROOT/'execution.json').write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'exit_codes':[r['exit_code']for r in records],'all_stages':len(records)==len(STAGES),'verdict':'candidate_only'}))
    if len(records)!=len(STAGES)or any(r['exit_code']for r in records):raise SystemExit(1)
if __name__=='__main__':main()
