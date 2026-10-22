"""Check that all engines produced the same answer: row count + rounded checksums per query output."""
import sys
import duckdb

size = sys.argv[1] if len(sys.argv) > 1 else "10m"
CHECK = {
    "q1_filter_agg": "COUNT(*), SUM(orders), ROUND(SUM(revenue), 0)",
    "q2_join_agg": "COUNT(*), SUM(orders), ROUND(SUM(revenue), 0), ROUND(SUM(avg_delta), 3)",
    "q3_window_latest": "COUNT(*), SUM(order_id), ROUND(SUM(amount), 0)",
    "q4_highcard_agg": "COUNT(*), SUM(orders), ROUND(SUM(revenue), 0), MIN(first_ts), MAX(last_ts)",
}
con = duckdb.connect()
ok = True
for q, expr in CHECK.items():
    rows = {}
    for eng, path in [("duckdb", f"out/duckdb/{size}_{q}.parquet"),
                      ("polars", f"out/polars/{size}_{q}.parquet"),
                      ("spark", f"out/spark/{size}_{q}/*.parquet")]:
        try:
            rows[eng] = con.execute(f"SELECT {expr} FROM read_parquet('{path}')").fetchone()
        except Exception as e:  # missing output (failed run)
            rows[eng] = f"missing: {type(e).__name__}"
    same = len({str(v) for v in rows.values()}) == 1
    ok &= same
    print(f"{q:18s} {'MATCH' if same else 'DIFF '} {rows}")
print("ALL MATCH" if ok else "MISMATCH")
