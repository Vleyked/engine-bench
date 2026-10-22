"""Orchestrate fresh-process runs sequentially with a memory watchdog.

python bench.py --sizes 10m --reps 3 [--engines duckdb,polars,spark] [--queries ...] [--tag name]

For every run it records: wall time of the whole process, the engine-reported setup/query time,
peak RSS of the process tree (psutil, sampled every 50 ms), system available memory and load
before the run, exit status. The watchdog kills the process tree if tree RSS exceeds --budget-gib
or system available memory drops under --floor-gib, so a hungry engine cannot take the box down.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime

import psutil

HERE = os.path.dirname(os.path.abspath(__file__))
# Interpreter for the engine processes: $BENCH_PYTHON, else ./.venv/bin/python if present, else this interpreter.
_VENV_PY = os.path.join(HERE, ".venv", "bin", "python")
PY = os.environ.get("BENCH_PYTHON") or (_VENV_PY if os.path.exists(_VENV_PY) else sys.executable)
GIB = 1024 ** 3


def tree_rss(p):
    total = 0
    try:
        procs = [p] + p.children(recursive=True)
    except psutil.NoSuchProcess:
        return 0
    for q in procs:
        try:
            total += q.memory_info().rss
        except psutil.NoSuchProcess:
            pass
    return total


def wait_for_room(min_avail_gib, max_busy_pct):
    """Wait until enough memory is free and the CPU is quiet (busy % over a 3 s window).
    Load average lags by minutes after our own runs, so instantaneous CPU busy is the gate."""
    while True:
        avail = psutil.virtual_memory().available / GIB
        busy = psutil.cpu_percent(interval=3)
        if avail >= min_avail_gib and busy <= max_busy_pct:
            return avail, busy
        print(f"  waiting: avail={avail:.2f} GiB cpu_busy={busy:.0f}%", flush=True)
        time.sleep(2)


def run_one(engine, size, query, mem, budget, floor, timeout, env_extra):
    env = dict(os.environ, **env_extra)
    t0 = time.perf_counter()
    proc = subprocess.Popen([PY, os.path.join(HERE, "run_engine.py"), engine, size, query, mem],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, cwd=HERE)
    p = psutil.Process(proc.pid)
    peak, min_avail, killed = 0, 1e9, None
    while proc.poll() is None:
        rss = tree_rss(p)
        peak = max(peak, rss)
        avail = psutil.virtual_memory().available
        min_avail = min(min_avail, avail)
        if rss > budget * GIB:
            killed = f"watchdog: tree RSS {rss / GIB:.2f} GiB > budget {budget} GiB"
        elif avail < floor * GIB:
            killed = f"watchdog: system available {avail / GIB:.2f} GiB < floor {floor} GiB"
        elif time.perf_counter() - t0 > timeout:
            killed = f"watchdog: timeout {timeout}s"
        if killed:
            for q in p.children(recursive=True) + [p]:
                try:
                    q.kill()
                except psutil.NoSuchProcess:
                    pass
            break
        time.sleep(0.05)
    out, err = proc.communicate()
    wall = time.perf_counter() - t0
    rec = {"engine": engine, "size": size, "query": query, "mem": mem,
           "wall_s": round(wall, 3), "peak_rss_gib": round(peak / GIB, 3),
           "min_sys_avail_gib": round(min_avail / GIB, 2), "exit": proc.returncode}
    line = next((l for l in out.splitlines() if l.startswith("RESULT ")), None)
    if line and not killed and proc.returncode == 0:
        rec.update({k: v for k, v in json.loads(line[7:]).items() if k not in rec})
        rec["status"] = "ok"
    else:
        rec["status"] = killed or "error"
        tail = [l for l in err.splitlines() if l.strip()][-6:]
        rec["stderr_tail"] = tail
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="10m")
    ap.add_argument("--engines", default="duckdb,polars,spark")
    ap.add_argument("--queries", default="q1_filter_agg,q2_join_agg,q3_window_latest,q4_highcard_agg")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--mem", default="3g")
    ap.add_argument("--budget-gib", type=float, default=4.5)
    ap.add_argument("--floor-gib", type=float, default=1.0)
    ap.add_argument("--min-avail-gib", type=float, default=5.0)
    ap.add_argument("--max-busy-pct", type=float, default=30.0)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--tag", default="run")
    ap.add_argument("--env", default="", help="KEY=VAL,KEY2=VAL2 passed to the engine process")
    a = ap.parse_args()
    env_extra = dict(kv.split("=", 1) for kv in a.env.split(",") if kv)
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    path = os.path.join(HERE, "results", f"{a.tag}.jsonl")
    engines = a.engines.split(",")
    with open(path, "a") as f:
        for size in a.sizes.split(","):
            for rep in range(1, a.reps + 1):
                for qi, query in enumerate(a.queries.split(",")):
                    # rotate engine order per rep/query so no engine always runs first
                    k = (rep + qi) % len(engines)
                    for engine in engines[k:] + engines[:k]:
                        avail, busy = wait_for_room(a.min_avail_gib, a.max_busy_pct)
                        load1 = os.getloadavg()[0]
                        rec = run_one(engine, size, query, a.mem, a.budget_gib, a.floor_gib, a.timeout, env_extra)
                        rec.update({"rep": rep, "pre_avail_gib": round(avail, 2), "pre_load1": round(load1, 2), "pre_cpu_busy_pct": round(busy, 1),
                                    "started": datetime.now().isoformat(timespec="seconds"), **env_extra})
                        f.write(json.dumps(rec) + "\n")
                        f.flush()
                        print(f"{size} r{rep} {query:18s} {engine:7s} {rec['status']:>4s} "
                              f"wall={rec['wall_s']:7.2f}s q={rec.get('query_s', '-')} "
                              f"rss={rec['peak_rss_gib']:.2f}GiB rows={rec.get('rows_out', '-')} "
                              f"avail0={avail:.1f} busy0={busy:.0f}% load0={load1:.1f}", flush=True)
    print("wrote", path)


if __name__ == "__main__":
    main()
