# Windows trials

Same generated files and pinned versions as the Linux reproduction. Windows 11 Home 10.0.26200, Ryzen 5 5600X (6 cores / 12 logical CPUs), 33455360 KiB RAM, 2048 MiB pagefile, Python 3.13.5. Polars used 8 threads. No Spark or DuckDB timings were taken here.

The original runner used this wrapper for Windows load-average metadata:

```python
import os
import psutil
import bench

os.getloadavg = psutil.getloadavg
bench.main()
```

All runs used `--engines polars --budget-gib 4.5`. The default trial ran both queries at 10M and 150M for three repetitions. The 3072 MB trial ran both at 150M for three repetitions. The 1024 MB trials ran sort + unique once, with and without `POLARS_ROW_GROUP_PREFETCH_SIZE=2`. Environment overrides are recorded in each JSONL file.

Both queries passed at 10M and exceeded the cap at 150M. The 1024 MB sort trials also reported the 512-blocking-thread warning. These trials do not establish the cause of the difference from Linux. They are included to make the platform limitation explicit.
