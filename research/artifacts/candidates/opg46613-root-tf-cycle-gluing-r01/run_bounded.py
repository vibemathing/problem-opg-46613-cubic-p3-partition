#!/usr/bin/env python3
"""One serial, resource-bounded candidate execution; no verifier identity assumed."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
LIMITS = {'cpu_seconds': 30, 'wall_seconds': 40, 'address_space_bytes': 536870912,
          'per_output_file_bytes': 2097152, 'worker_processes': 1, 'threads': 1}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def restricted():
    os.setsid()
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    resource.setrlimit(resource.RLIMIT_AS, (536870912, 536870912))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2097152, 2097152))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('generate', 'constructor', 'verify', 'local_check'):
        raise SystemExit('Choose generate, constructor, verify, or local_check')
    stage = sys.argv[1]
    source = ROOT / (stage + '.py')
    before = {source.name: digest(source), 'run_bounded.py': digest(Path(__file__))}
    for name in ('inputs.json', 'constructor.stdout.json', 'local_cases.json'):
        if (ROOT / name).exists():
            before[name] = digest(ROOT / name)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.monotonic()
    timed_out = False
    out_path, err_path = ROOT / (stage+'.stdout.json'), ROOT / (stage+'.stderr.txt')
    with out_path.open('wb') as out, err_path.open('wb') as err:
        p = subprocess.Popen([sys.executable, '-I', '-S', source.name], cwd=ROOT,
                             stdout=out, stderr=err, preexec_fn=restricted,
                             env={'PATH': os.environ.get('PATH',''), 'OMP_NUM_THREADS': '1',
                                  'OPENBLAS_NUM_THREADS': '1', 'PYTHONHASHSEED': '0'})
        try:
            code = p.wait(timeout=40)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(p.pid, signal.SIGKILL)
            code = p.wait()
    record = {'verdict': 'candidate_only', 'trust_domain': 'web-candidate-generation',
              'command': 'python3 -I -S '+source.name, 'python': sys.version,
              'started_at': started, 'elapsed_wall_seconds': round(time.monotonic()-tick, 6),
              'exit_code': code, 'timed_out': timed_out, 'limits': LIMITS,
              'route': 'CPU: small exact finite combinatorics; no GPU screening or floating-point result',
              'input_sha256': before,
              'output_sha256': {out_path.name: digest(out_path), err_path.name: digest(err_path)},
              'lean_elaboration': None, 'trusted_attestation': None}
    (ROOT / (stage+'-execution.json')).write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'stage': stage, 'exit_code': code, 'wall_seconds': record['elapsed_wall_seconds']}))
    raise SystemExit(0 if code == 0 else 1)


if __name__ == '__main__':
    main()
