"""Print the logical and streaming physical plans for the q3 window dedup (Polars) and the DuckDB EXPLAIN.

Run from the repo root after `python gen_data.py 10`:  python plans/make_plans.py
No timing, no benchmark. Writes plans/*.txt and plans/*.dot.
"""
import os, sys
os.environ.setdefault("POLARS_MAX_THREADS", "8")
import polars as pl, duckdb
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from queries import SQL, polars_query
SALES = "data/sales_10m/*.parquet"; PRODUCTS = "data/products.parquet"
lf = polars_query("q3_window_latest", pl.scan_parquet(SALES), pl.scan_parquet(PRODUCTS))
dot = lf.show_graph(engine="streaming", plan_stage="physical", raw_output=True, show=False)
o = []
o.append(f"Polars {pl.__version__}: plans for q3_window_latest (expression exactly as in queries.py)\n")
o.append("Input: data/sales_10m/*.parquet, produced by `python gen_data.py 10`. Plan output only, nothing was timed.\n")
o.append("Generated with plans/make_plans.py.\n\n")
o.append("Expression:\n")
o.append('  amount = pl.col("qty").cast(pl.Float64) * pl.col("price")\n')
o.append('  rn = pl.int_range(pl.len()).over("customer_id", order_by=["ts", "order_id"], descending=True)\n')
o.append('  sales.filter(rn == 0).select("customer_id", "order_id", "ts", amount.alias("amount"))\n\n')
o.append("== 1. Optimized logical plan: lf.explain() ==\n" + lf.explain() + "\n\n")
o.append("== 2. Unoptimized logical plan: lf.explain(optimized=False) ==\n" + lf.explain(optimized=False) + "\n\n")
o.append("== 3. lf.explain(engine='streaming') ==\n" + lf.explain(engine="streaming") + "\n")
o.append("(In Polars 2.0 explain(streaming=True) was removed; engine='streaming' is the replacement. It prints the same logical plan.)\n\n")
o.append("== 4. Streaming PHYSICAL plan: lf.show_graph(engine='streaming', plan_stage='physical', raw_output=True) ==\n")
o.append("Graphviz DOT, also saved as plans/polars_dedup_physical_streaming.dot. Legend from Polars itself:\n")
o.append("  plain node = streaming engine node; yellow fill (0.16 0.3 1.0) = potentially memory-intensive node;\n")
o.append("  red fill (0.0 0.3 1.0) = in-memory engine fallback.\n")
o.append("Read it bottom-up (rankdir=BT): multi-scan[parquet] -> multiplexer (memory-intensive) -> select customer_id, order_id, ts\n")
o.append("  -> in-memory-map running the int_range().over(...) window (in-memory engine fallback) -> zip-broadcast with the\n")
o.append("  other multiplexer branch -> select (rn == 0) -> filter -> select.\n\n")
o.append(dot + "\n")
open("plans/polars_dedup_explain.txt", "w").write("".join(o))
open("plans/polars_dedup_physical_streaming.dot", "w").write(dot)
con = duckdb.connect(); con.execute("SET threads = 8"); con.execute("SET memory_limit = '3GB'")
con.execute(f"CREATE VIEW sales AS SELECT * FROM read_parquet('{SALES}')")
q = SQL["q3_window_latest"]
d = [f"DuckDB {duckdb.__version__}: EXPLAIN (physical plan) for q3_window_latest, SQL exactly as in queries.py\n",
     "Input: data/sales_10m/*.parquet, threads = 8, memory_limit = 3GB. Plan output only, nothing was timed.\n",
     "Generated with plans/make_plans.py.\n", q, "\n"]
d.append("\n".join(r[-1] for r in con.execute(f"EXPLAIN {q}").fetchall()) + "\n")
open("plans/duckdb_dedup_explain.txt", "w").write("".join(d))
