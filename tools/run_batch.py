"""Run run_eval.py over many measure files in parallel.

Everything after `--` is passed to run_eval.py unchanged.

Usage:
  python3 tools/run_batch.py tests/bias/measures/*.json --jobs 6 -- \
      --provider vertex --model gemini-3.1-pro-preview --gcp-project my-project --runs 1
Logs: runs/logs/<measure file>.<provider>__<model>.log
"""
import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

argv = sys.argv[1:]
rest = argv[argv.index("--") + 1:] if "--" in argv else []
ap = argparse.ArgumentParser()
ap.add_argument("measures", nargs="+")
ap.add_argument("--jobs", type=int, default=4)
a = ap.parse_args(argv[:argv.index("--")] if "--" in argv else argv)

tag = "run"
if "--provider" in rest and "--model" in rest:
    tag = f"{rest[rest.index('--provider') + 1]}__{re.sub(r'[^A-Za-z0-9._-]', '_', rest[rest.index('--model') + 1])}"
logs = ROOT / "runs/logs"
logs.mkdir(parents=True, exist_ok=True)


def one(m):
    log = logs / f"{Path(m).stem}.{tag}.log"
    with log.open("w") as f:
        rc = subprocess.run([sys.executable, str(ROOT / "tools/run_eval.py"), m, *rest],
                            stdout=f, stderr=subprocess.STDOUT).returncode
    last = log.read_text().strip().splitlines()[-1:] or [""]
    return Path(m).stem, rc, last[0]


with ThreadPoolExecutor(a.jobs) as ex:
    results = list(ex.map(one, a.measures))
for name, rc, last in sorted(results):
    print(f"{'ok  ' if rc == 0 else 'FAIL'} {name}: {last}")
bad = sum(rc != 0 for _, rc, _ in results)
print(f"{len(results) - bad}/{len(results)} measures fully accepted")
sys.exit(1 if bad else 0)
