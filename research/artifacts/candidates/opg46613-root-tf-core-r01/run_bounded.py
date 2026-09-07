#!/usr/bin/env python3
"""Linux bounded local candidate execution. Observations, never admission."""
import datetime,hashlib,json,pathlib,resource,subprocess,sys,time
B=pathlib.Path(__file__).resolve().parent
SCRIPTS=[('checker.py','primary',25),('normal_form.py','normal-form',20),('gap_forest.py','gap-forest',30),('verify_certificates.py','secondary',25)]
def cap(cpu):
    resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu));resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
    resource.setrlimit(resource.RLIMIT_FSIZE,(2097152,2097152));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
observations=[]
for script,stem,cpu in SCRIPTS:
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();timed=False
    with (B/(stem+'-stdout.json')).open('wb') as out,(B/(stem+'-stderr.txt')).open('wb') as err:
        try:r=subprocess.run([sys.executable,'-I','-S',script],cwd=B,stdout=out,stderr=err,preexec_fn=lambda:cap(cpu),timeout=cpu+10,check=False);exitcode=r.returncode
        except subprocess.TimeoutExpired:exitcode=None;timed=True
    observations.append({'program':script,'command':'python3 -I -S '+script,'start':start,'elapsed_wall_seconds':round(time.monotonic()-t,6),
      'exit_code':exitcode,'timed_out':timed,'limits':{'cpu_seconds':cpu,'wall_seconds':cpu+10,'address_space_bytes':536870912,'per_output_bytes':2097152,'worker_processes':1,'threads':1},'python':sys.version,'source_sha256':sha(B/script),
      'stdout_sha256':sha(B/(stem+'-stdout.json')),'stderr_sha256':sha(B/(stem+'-stderr.txt'))})
    if timed or exitcode!=0:break
record={'verdict':'candidate_only','kind':'same_generation_domain_execution_observations','runs':observations,'file_sha256':{f:sha(B/f) for f in ['input.json','run_bounded.py','failure-certificates.json']},'lean':{'executed':False,'elaboration':None,'axiom_audit':None},'trusted_attestation':None}
(B/'execution.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps(record,sort_keys=True,separators=(',',':')))
if len(observations)!=len(SCRIPTS) or any(r['exit_code']!=0 for r in observations):sys.exit(1)
