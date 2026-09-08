#!/usr/bin/env python3
"""New bounded generator-side observations, not registered verifier receipts."""
import datetime,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path

LIMITS={'cpu_seconds':25,'wall_seconds':35,'address_space_bytes':536870912,'per_file_bytes':1048576,'core_dump_bytes':0,'workers':1,'threads':1}
STAGES=['search_hosts.py','audit.py','local_switches.py','check.py']


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(25,25))
    resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
    resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))


def main():
    os.chdir(Path(__file__).resolve().parent)
    obs={'verdict':'candidate_only','kind':'same_generation_domain_execution_observation','python':sys.version,
         'limits':LIMITS,'lean_execution':False,'axiom_report':None,'trusted_attestation':None,
         'source_sha256':{p.name:digest(p) for p in sorted(Path('.').glob('*.py'))},
         'prior_objects_sha256':digest('../opg46613-root-tf-222-r01/objects.json'),'stages':[]}
    for stage in STAGES:
        stem=stage[:-3];out=stem+'-stdout.json';err=stem+'-stderr.txt';started=datetime.datetime.now(datetime.timezone.utc).isoformat();start=time.monotonic();timed_out=False
        with open(out,'wb') as stdout,open(err,'wb') as stderr:
            p=subprocess.Popen([sys.executable,'-I','-S',stage],stdout=stdout,stderr=stderr,stdin=subprocess.DEVNULL,preexec_fn=limits,
                               env={'PATH':os.environ.get('PATH',''),'PYTHONHASHSEED':'0','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
            while True:
                pid,status,usage=os.wait4(p.pid,os.WNOHANG)
                if pid:break
                if time.monotonic()-start>35:
                    timed_out=True;p.kill();pid,status,usage=os.wait4(p.pid,0);break
                time.sleep(.025)
            p.returncode=os.waitstatus_to_exitcode(status)
        row={'command':'python3 -I -S '+stage,'started_at':started,'elapsed_wall_seconds':round(time.monotonic()-start,6),'exit_code':p.returncode,
             'timed_out':timed_out,'user_cpu_seconds':usage.ru_utime,'system_cpu_seconds':usage.ru_stime,'peak_rss_kib_linux':usage.ru_maxrss,
             'stdout':out,'stderr':err,'stdout_sha256':digest(out),'stderr_sha256':digest(err)}
        obs['stages'].append(row)
        Path('execution.json').write_text(json.dumps(obs,indent=2,sort_keys=True)+'\n')
        print(stage,'exit',p.returncode,'wall',row['elapsed_wall_seconds'],flush=True)
        if p.returncode or timed_out:raise SystemExit(1)
    obs['data_sha256']={p:digest(p) for p in ['new-hosts.json','audit-data.json']}
    Path('execution.json').write_text(json.dumps(obs,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
