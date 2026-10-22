
### duckdb1g (6 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 150m | q3_window_latest | duckdb | 3/3 | 17.79 | 17.43 | 0.13 | 1.29, 1.29 |  |
| 150m | q4_highcard_agg | duckdb | 3/3 | 22.06 | 21.68 | 0.07 | 1.24, 1.27 |  |

Pre-run system state: available memory 5.6 to 11.0 GiB, CPU busy 2 to 21% (3 s window), load1 6.4 to 9.3. First run 2026-10-19T10:30:09, last run 2026-10-19T10:32:58.

### duckdb1g_noorder (6 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 150m | q3_window_latest | duckdb | 3/3 | 14.85 | 14.53 | 0.07 | 1.30, 1.30 |  |
| 150m | q4_highcard_agg | duckdb | 3/3 | 15.15 | 14.91 | 0.07 | 1.24, 1.25 |  |

Pre-run system state: available memory 10.4 to 11.0 GiB, CPU busy 1 to 19% (3 s window), load1 5.7 to 6.7. First run 2026-10-19T10:33:15, last run 2026-10-19T10:34:47.

### main (132 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 10m | q1_filter_agg | duckdb | 5/5 | 0.21 | 0.11 | 0.07 | 0.10, 0.10 |  |
| 10m | q1_filter_agg | polars | 5/5 | 0.27 | 0.08 | 0.10 | 0.32, 0.37 |  |
| 10m | q1_filter_agg | spark | 5/5 | 8.07 | 2.22 | 5.07 | 1.15, 1.24 |  |
| 10m | q2_join_agg | duckdb | 5/5 | 0.32 | 0.21 | 0.07 | 0.10, 0.10 |  |
| 10m | q2_join_agg | polars | 5/5 | 0.33 | 0.15 | 0.09 | 0.55, 0.59 |  |
| 10m | q2_join_agg | spark | 5/5 | 9.14 | 3.16 | 5.08 | 1.30, 1.55 |  |
| 10m | q3_window_latest | duckdb | 5/5 | 0.54 | 0.41 | 0.07 | 0.54, 0.54 |  |
| 10m | q3_window_latest | polars | 5/5 | 1.81 | 1.61 | 0.09 | 1.20, 1.21 |  |
| 10m | q3_window_latest | spark | 5/5 | 12.16 | 5.79 | 5.09 | 3.01, 3.01 |  |
| 10m | q4_highcard_agg | duckdb | 5/5 | 0.54 | 0.37 | 0.07 | 0.81, 0.81 |  |
| 10m | q4_highcard_agg | polars | 5/5 | 0.38 | 0.18 | 0.10 | 0.42, 0.43 |  |
| 10m | q4_highcard_agg | spark | 5/5 | 10.10 | 4.10 | 5.01 | 2.34, 2.45 |  |
| 50m | q1_filter_agg | duckdb | 3/3 | 0.48 | 0.33 | 0.07 | 0.15, 0.15 |  |
| 50m | q1_filter_agg | polars | 3/3 | 0.47 | 0.28 | 0.09 | 0.76, 0.90 |  |
| 50m | q1_filter_agg | spark | 3/3 | 9.05 | 3.10 | 4.98 | 1.70, 1.76 |  |
| 50m | q2_join_agg | duckdb | 3/3 | 0.82 | 0.66 | 0.07 | 0.14, 0.14 |  |
| 50m | q2_join_agg | polars | 3/3 | 0.66 | 0.46 | 0.10 | 1.53, 1.59 |  |
| 50m | q2_join_agg | spark | 3/3 | 12.01 | 6.20 | 4.97 | 1.49, 1.68 |  |
| 50m | q3_window_latest | duckdb | 3/3 | 1.94 | 1.73 | 0.07 | 2.10, 2.10 |  |
| 50m | q3_window_latest | polars | 2/3 | 9.30 | 9.03 | 0.09 | 4.47, 4.54 | watchdog: tree RSS 4.54 GiB > budget 4.5 GiB |
| 50m | q3_window_latest | spark | 3/3 | 24.26 | 18.01 | 5.14 | 3.74, 3.75 |  |
| 50m | q4_highcard_agg | duckdb | 3/3 | 2.19 | 1.97 | 0.07 | 3.21, 3.29 |  |
| 50m | q4_highcard_agg | polars | 3/3 | 1.12 | 0.86 | 0.09 | 1.64, 1.65 |  |
| 50m | q4_highcard_agg | spark | 2/3 | 19.84 | 13.87 | 5.00 | 3.52, 5.30 | watchdog: tree RSS 5.30 GiB > budget 4.5 GiB |
| 150m | q1_filter_agg | duckdb | 3/3 | 1.01 | 0.83 | 0.07 | 0.26, 0.26 |  |
| 150m | q1_filter_agg | polars | 3/3 | 0.89 | 0.72 | 0.10 | 0.95, 1.11 |  |
| 150m | q1_filter_agg | spark | 3/3 | 10.00 | 4.36 | 4.86 | 1.85, 1.87 |  |
| 150m | q2_join_agg | duckdb | 3/3 | 1.88 | 1.71 | 0.06 | 0.23, 0.23 |  |
| 150m | q2_join_agg | polars | 3/3 | 1.30 | 1.09 | 0.09 | 1.89, 1.98 |  |
| 150m | q2_join_agg | spark | 3/3 | 15.43 | 9.63 | 4.84 | 1.65, 1.75 |  |
| 150m | q3_window_latest | duckdb | 3/3 | 9.09 | 8.84 | 0.07 | 3.47, 3.55 |  |
| 150m | q3_window_latest | polars | 0/3 | - | - | - | -, 4.66 | watchdog: tree RSS 4.51 GiB > budget 4.5 GiB; watchdog: tree RSS 4.62 GiB > budget 4.5 GiB; watchdog: tree RSS 4.66 GiB > budget 4.5 GiB |
| 150m | q3_window_latest | spark | 2/3 | 60.84 | 54.28 | 4.79 | 3.76, 7.46 | watchdog: tree RSS 7.46 GiB > budget 4.5 GiB |
| 150m | q4_highcard_agg | duckdb | 3/3 | 9.61 | 9.36 | 0.09 | 3.36, 3.50 |  |
| 150m | q4_highcard_agg | polars | 0/3 | - | - | - | -, 4.57 | watchdog: tree RSS 4.53 GiB > budget 4.5 GiB; watchdog: tree RSS 4.56 GiB > budget 4.5 GiB |
| 150m | q4_highcard_agg | spark | 3/3 | 40.22 | 33.59 | 5.12 | 3.67, 3.69 |  |

Pre-run system state: available memory 9.5 to 11.0 GiB, CPU busy 1 to 20% (3 s window), load1 1.9 to 11.1. First run 2026-10-19T10:01:51, last run 2026-10-19T10:24:24.

### needs150 (12 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 150m | q3_window_latest | polars | 0/3 | - | - | - | -, 9.54 | watchdog: tree RSS 9.04 GiB > budget 9.0 GiB; watchdog: tree RSS 9.17 GiB > budget 9.0 GiB; watchdog: tree RSS 9.54 GiB > budget 9.0 GiB |
| 150m | q3_window_latest | spark | 3/3 | 46.83 | 39.87 | 5.18 | 3.83, 7.44 |  |
| 150m | q4_highcard_agg | polars | 3/3 | 3.82 | 3.53 | 0.12 | 4.71, 4.76 |  |
| 150m | q4_highcard_agg | spark | 3/3 | 39.05 | 32.19 | 5.62 | 4.50, 5.38 |  |

Pre-run system state: available memory 10.1 to 11.0 GiB, CPU busy 2 to 19% (3 s window), load1 7.3 to 9.8. First run 2026-10-19T10:25:14, last run 2026-10-19T10:29:52.

### polars_ooc3g (6 runs)

| size | query | engine | ok/runs | wall s (median) | query s (median) | setup s (median) | peak RSS GiB (median, max) | failures |
|---|---|---|---|---|---|---|---|---|
| 150m | q3_window_latest | polars | 0/3 | - | - | - | -, 4.82 | watchdog: tree RSS 4.53 GiB > budget 4.5 GiB; watchdog: tree RSS 4.57 GiB > budget 4.5 GiB; watchdog: tree RSS 4.82 GiB > budget 4.5 GiB |
| 150m | q4_highcard_agg | polars | 3/3 | 4.73 | 4.44 | 0.10 | 4.17, 4.25 |  |

Pre-run system state: available memory 10.2 to 11.0 GiB, CPU busy 2 to 6% (3 s window), load1 5.2 to 9.6. First run 2026-10-19T10:35:07, last run 2026-10-19T10:35:43.
