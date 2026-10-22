# Polars sort + unique, 150M rows

[Linux run](https://github.com/Vleyked/engine-bench/actions/runs/39762377323), October 22, 2026. Ubuntu 24.04 runner, 4 vCPUs, 15983 MiB RAM, no swap; 8 engine threads as in the original runner. Python 3.13.5 and the pinned packages are recorded in [host.txt](host.txt). Spark was not run.

The original `bench.py` and `run_engine.py` were used unchanged, with the same 4.5 GiB RSS cap, 50 ms sampling, 1 GiB system-memory floor and fresh processes. Three repetitions per Polars setting. The added query is `q3_sort_unique_latest`.

| 150M query | Spill budget | Finished | Wall seconds, median | Peak RSS GiB, range |
|---|---|---|---|---|
| Window | default | 0/3 | — | 4.55–4.62, killed |
| Sort + unique | default | 0/3 | — | 4.55–4.78, killed |
| Window | 3072 MB | 0/3 | — | 4.55–4.57, killed |
| Sort + unique | 3072 MB | 0/3 | — | 4.51–4.63, killed |
| Window | 1024 MB | 0/3 | — | 4.56–4.62, killed |
| Sort + unique | 1024 MB | 3/3 | 90.58 | 2.50–2.74 |
| DuckDB window | 3 GB engine limit | 1/1 | 17.56 | 3.03 |

Raw records: [default.jsonl](default.jsonl), [ooc3g.jsonl](ooc3g.jsonl), [ooc1g.jsonl](ooc1g.jsonl), [duckdb.jsonl](duckdb.jsonl). The 10M default runs are included too. Generate tables with `python summarize.py results/dedup_linux`.

All 33 generated input files matched the repository's MD5s. Bidirectional `EXCEPT ALL` against DuckDB found no missing or extra rows at 10M or 150M; the latter produced 14,999,347 rows. See [checksums.txt](checksums.txt) and [validation.json](validation.json). The fixture tests also cover ties, nulls, empty input and multiple files.

The [workflow and full-output check](https://github.com/Vleyked/engine-bench/tree/876c8bf135d35883d8be760164230d6f20fa112d) preserve the commands used. Timings are from this host, not the original VM. The existing harness initializes `min_sys_avail` to 1e9 bytes, so that recorded field is capped at 0.93 GiB; the RSS measurements and watchdog checks are unaffected.
