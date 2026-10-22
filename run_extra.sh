#!/usr/bin/env bash
# D. Polars with an explicit out-of-core memory budget (env var found in the 2.0.0 binary / polars-config source)
set -u
cd "$(dirname "$0")"
PY=${PY:-.venv/bin/python}
while ! grep -q ALL_DONE results/run_all.log; do sleep 15; done
$PY bench.py --sizes 150m --reps 3 --engines polars --queries q3_window_latest,q4_highcard_agg \
    --env POLARS_OOC_MEMORY_BUDGET_MB=3072 --min-avail-gib 5 --tag polars_ooc3g
echo EXTRA_DONE
