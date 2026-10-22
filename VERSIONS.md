# Versions

## Recorded at run time

These come from the run logs in this repo, not from memory.

| Component | October 22, 2026 run (`results/`) | October 19, 2026 run (`results_duckdb156/`) | Source |
|---|---|---|---|
| DuckDB | 2.0.0 | 1.5.6 | `results/host.txt`, `results_duckdb156/versions.txt`, `version` field in every JSONL record |
| Polars | 2.0.0 | 2.0.0 | same |
| PySpark | 4.2.0 | 4.2.0 | same |
| pyarrow | 26.0.0 | 26.0.0 | same |
| psutil | not recorded | 7.2.2 | `results_duckdb156/versions.txt` |
| Python | 3.13.5 | 3.13.5 | `host.txt` |
| Java | OpenJDK 21.0.12.1 (2026-08-18) | same | `host.txt` (`java -version`) |
| Kernel | Linux 6.12.94 | same | `host.txt` |
| CPU / RAM | 8 vCPU Intel Xeon, 16002 MiB total (15 GiB), no swap | same | `host.txt` |

Java came from the Debian 13 package `openjdk-21-jre-headless` 21.0.12.1+1-1~deb13u1 (headless JRE is enough for local Spark).

## Pinned in requirements.txt but not recorded at run time

- **numpy 2.5.4.** The original run did not log the numpy version. On October 22, 2026 I installed numpy 2.5.4 with pyarrow 26.0.0 in a fresh venv and regenerated the 10M dataset with `gen_data.py`: both 10M part files came out byte-identical (same MD5) to the files the benchmark used. MD5s for every data file at all three sizes are in `data_checksums.md5`.
- **psutil 7.2.2** for the October 22 run: logged on October 19 (`results_duckdb156/versions.txt`), not logged again on October 22.
- **py4j.** Installed as a dependency of pyspark 4.2.0. Today pip resolves it to py4j 0.10.9.9. The exact version at run time was not logged.

## Files

- `requirements.txt`: October 22 run (DuckDB 2.0.0).
- `requirements-duckdb156.txt`: October 19 run (DuckDB 1.5.6).
