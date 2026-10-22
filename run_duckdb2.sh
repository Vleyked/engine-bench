#!/usr/bin/env bash
# 2026-10-22 rerun on DuckDB 2.0.0: same plan as run_all.sh + run_extra.sh, needs150 run last (it needs ~10 GiB free).
set -u
cd "$(dirname "$0")"
PY=${PY:-.venv/bin/python}
{
  echo "=== host"; date -Is; uname -r; lscpu | grep -E "Model name|^CPU\(s\)"; free -m; cat /proc/loadavg
  java -version 2>&1 | head -1; $PY -V
  $PY -c "import duckdb,polars,pyspark,pyarrow;print('duckdb',duckdb.__version__,'polars',polars.__version__,'pyspark',pyspark.__version__,'pyarrow',pyarrow.__version__)"
} > results/host.txt 2>&1
$PY bench.py --sizes 10m --reps 5 --tag main --min-avail-gib 5
$PY bench.py --sizes 50m,150m --reps 3 --tag main --min-avail-gib 5
$PY bench.py --sizes 150m --reps 3 --engines duckdb --queries q3_window_latest,q4_highcard_agg --mem 1g --tag duckdb1g
$PY bench.py --sizes 150m --reps 3 --engines duckdb --queries q3_window_latest,q4_highcard_agg --mem 1g \
    --env DUCKDB_NO_ORDER=1 --tag duckdb1g_noorder
$PY bench.py --sizes 150m --reps 3 --engines polars --queries q3_window_latest,q4_highcard_agg \
    --env POLARS_OOC_MEMORY_BUDGET_MB=3072 --min-avail-gib 5 --tag polars_ooc3g
echo CORE_DONE
