
### duckdb1g (6 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 150m | q3_window_latest | duckdb | 3/3 | 14.97 | 14.77 | 0.08 | 1.12, 1.12 |  |
| 150m | q4_highcard_agg | duckdb | 3/3 | 13.94 | 13.77 | 0.08 | 1.08, 1.08 |  |

Pre-run system state: available memory 10.4 to 10.9 GiB, CPU busy 1 to 13% (3 s window), load1 5.5 to 6.2. First run 2026-10-22T10:47:11, last run 2026-10-22T10:48:38.

### duckdb1g_noorder (6 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 150m | q3_window_latest | duckdb | 3/3 | 14.94 | 14.75 | 0.09 | 1.12, 1.12 |  |
| 150m | q4_highcard_agg | duckdb | 3/3 | 13.88 | 13.70 | 0.08 | 1.08, 1.08 |  |

Pre-run system state: available memory 10.1 to 10.9 GiB, CPU busy 2 to 18% (3 s window), load1 5.1 to 6.6. First run 2026-10-22T10:48:56, last run 2026-10-22T10:50:23.

### main (132 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 10m | q1_filter_agg | duckdb | 5/5 | 0.21 | 0.08 | 0.09 | 0.21, 0.21 |  |
| 10m | q1_filter_agg | polars | 5/5 | 0.27 | 0.08 | 0.10 | 0.32, 0.39 |  |
| 10m | q1_filter_agg | spark | 5/5 | 8.61 | 2.38 | 5.27 | 1.17, 1.39 |  |
| 10m | q2_join_agg | duckdb | 5/5 | 0.32 | 0.18 | 0.09 | 0.16, 0.16 |  |
| 10m | q2_join_agg | polars | 5/5 | 0.37 | 0.15 | 0.10 | 0.57, 0.61 |  |
| 10m | q2_join_agg | spark | 5/5 | 9.15 | 3.15 | 5.20 | 1.46, 1.61 |  |
| 10m | q3_window_latest | duckdb | 5/5 | 0.60 | 0.40 | 0.09 | 0.65, 0.66 |  |
| 10m | q3_window_latest | polars | 5/5 | 1.83 | 1.66 | 0.10 | 1.20, 1.20 |  |
| 10m | q3_window_latest | spark | 4/5 | 12.74 | 6.06 | 5.27 | 2.94, 3.01 | watchdog: system available 0.97 GiB < floor 1.0 GiB |
| 10m | q4_highcard_agg | duckdb | 5/5 | 0.54 | 0.33 | 0.10 | 0.92, 0.94 |  |
| 10m | q4_highcard_agg | polars | 5/5 | 0.42 | 0.20 | 0.10 | 0.43, 0.44 |  |
| 10m | q4_highcard_agg | spark | 5/5 | 10.67 | 4.24 | 5.12 | 2.32, 3.99 |  |
| 50m | q1_filter_agg | duckdb | 3/3 | 0.43 | 0.28 | 0.09 | 0.55, 0.58 |  |
| 50m | q1_filter_agg | polars | 3/3 | 0.54 | 0.28 | 0.10 | 0.76, 0.85 |  |
| 50m | q1_filter_agg | spark | 3/3 | 10.90 | 3.97 | 5.78 | 1.65, 1.66 |  |
| 50m | q2_join_agg | duckdb | 3/3 | 0.70 | 0.52 | 0.09 | 0.33, 0.34 |  |
| 50m | q2_join_agg | polars | 3/3 | 0.86 | 0.56 | 0.10 | 1.55, 1.58 |  |
| 50m | q2_join_agg | spark | 3/3 | 13.28 | 6.92 | 5.44 | 1.55, 1.62 |  |
| 50m | q3_window_latest | duckdb | 3/3 | 2.33 | 2.10 | 0.11 | 2.19, 2.19 |  |
| 50m | q3_window_latest | polars | 3/3 | 10.36 | 10.06 | 0.11 | 4.46, 4.46 |  |
| 50m | q3_window_latest | spark | 3/3 | 29.06 | 21.81 | 5.74 | 3.77, 3.81 |  |
| 50m | q4_highcard_agg | duckdb | 3/3 | 2.04 | 1.70 | 0.10 | 2.98, 3.00 |  |
| 50m | q4_highcard_agg | polars | 3/3 | 1.30 | 1.01 | 0.10 | 1.63, 1.64 |  |
| 50m | q4_highcard_agg | spark | 3/3 | 23.34 | 16.33 | 5.62 | 3.60, 3.66 |  |
| 150m | q1_filter_agg | duckdb | 3/3 | 0.87 | 0.65 | 0.11 | 0.77, 0.78 |  |
| 150m | q1_filter_agg | polars | 3/3 | 0.96 | 0.68 | 0.15 | 0.94, 0.96 |  |
| 150m | q1_filter_agg | spark | 3/3 | 10.77 | 4.80 | 5.28 | 1.85, 1.93 |  |
| 150m | q2_join_agg | duckdb | 3/3 | 1.47 | 1.29 | 0.12 | 0.42, 0.42 |  |
| 150m | q2_join_agg | polars | 3/3 | 1.46 | 1.18 | 0.09 | 1.96, 1.97 |  |
| 150m | q2_join_agg | spark | 3/3 | 16.10 | 10.16 | 5.05 | 1.61, 1.85 |  |
| 150m | q3_window_latest | duckdb | 3/3 | 7.92 | 7.66 | 0.08 | 3.01, 3.02 |  |
| 150m | q3_window_latest | polars | 0/3 | - | - | - | -, 4.66 | watchdog: tree RSS 4.52 GiB > budget 4.5 GiB; watchdog: tree RSS 4.65 GiB > budget 4.5 GiB; watchdog: tree RSS 4.66 GiB > budget 4.5 GiB |
| 150m | q3_window_latest | spark | 2/3 | 46.29 | 39.49 | 5.28 | 3.74, 7.50 | watchdog: tree RSS 7.51 GiB > budget 4.5 GiB |
| 150m | q4_highcard_agg | duckdb | 3/3 | 7.91 | 7.73 | 0.08 | 3.01, 3.03 |  |
| 150m | q4_highcard_agg | polars | 1/3 | 4.21 | 3.81 | 0.12 | 4.49, 4.55 | watchdog: tree RSS 4.50 GiB > budget 4.5 GiB; watchdog: tree RSS 4.55 GiB > budget 4.5 GiB |
| 150m | q4_highcard_agg | spark | 3/3 | 39.70 | 33.03 | 5.10 | 4.40, 4.46 |  |

Pre-run system state: available memory 5.0 to 11.2 GiB, CPU busy 0 to 24% (3 s window), load1 0.2 to 8.5. First run 2026-10-22T10:03:23, last run 2026-10-22T10:46:53.

### polars_ooc3g (6 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 150m | q3_window_latest | polars | 0/3 | - | - | - | -, 4.66 | watchdog: tree RSS 4.57 GiB > budget 4.5 GiB; watchdog: tree RSS 4.62 GiB > budget 4.5 GiB; watchdog: tree RSS 4.66 GiB > budget 4.5 GiB |
| 150m | q4_highcard_agg | polars | 3/3 | 4.67 | 4.40 | 0.10 | 4.18, 4.30 |  |

Pre-run system state: available memory 10.3 to 10.8 GiB, CPU busy 2 to 5% (3 s window), load1 4.7 to 5.7. First run 2026-10-22T10:50:30, last run 2026-10-22T10:51:07.
