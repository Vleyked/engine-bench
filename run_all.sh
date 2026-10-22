#!/usr/bin/env bash
# Full measurement plan for Part 1. Engines run strictly one at a time.
set -u
cd "$(dirname "$0")"
PY=${PY:-.venv/bin/python}
{
  echo "=== host"; date -Is; uname -r; lscpu | grep -E "Model name|^CPU\(s\)"; free -m; cat /proc/loadavg
  java -version 2>&1 | head -1; $PY -V
} > results/host.txt 2>&1
# A. main matrix: engine knobs at 3 GB, watchdog budget 4.5 GiB process-tree RSS
$PY bench.py --sizes 10m --reps 5 --tag main --min-avail-gib 5
$PY bench.py --sizes 50m,150m --reps 3 --tag main --min-avail-gib 5
# B. how much do Polars and Spark actually need at 150M for q3/q4? (budget 9 GiB, floor 1.5 GiB)
$PY bench.py --sizes 150m --reps 3 --engines polars,spark --queries q3_window_latest,q4_highcard_agg \
    --budget-gib 9 --floor-gib 1.5 --min-avail-gib 10 --tag needs150
# C. DuckDB with a 1 GB memory_limit at 150M (spill), with and without insertion-order preservation
$PY bench.py --sizes 150m --reps 3 --engines duckdb --queries q3_window_latest,q4_highcard_agg --mem 1g --tag duckdb1g
$PY bench.py --sizes 150m --reps 3 --engines duckdb --queries q3_window_latest,q4_highcard_agg --mem 1g \
    --env DUCKDB_NO_ORDER=1 --tag duckdb1g_noorder
echo ALL_DONE
