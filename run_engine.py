"""Run ONE query on ONE engine in a fresh process, write the result to Parquet, print a JSON line.

python run_engine.py <engine> <size e.g. 10m> <query> <mem e.g. 3g>
"""
import json
import os
import shutil
import sys
import time

T0 = time.perf_counter()
engine, size, query, mem = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
SALES = os.path.join(HERE, "data", f"sales_{size}")
PRODUCTS = os.path.join(HERE, "data", "products.parquet")
OUT = os.path.join(HERE, "out", engine, f"{size}_{query}")
TMP = os.path.join(HERE, "out", "tmp", engine)
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
os.makedirs(TMP, exist_ok=True)
THREADS = 8

from queries import SQL, polars_query  # noqa: E402

res = {"engine": engine, "size": size, "query": query, "mem": mem}

if engine == "duckdb":
    import duckdb
    con = duckdb.connect()
    con.execute(f"SET memory_limit = '{mem.upper()}B'")
    con.execute(f"SET threads = {THREADS}")
    con.execute(f"SET temp_directory = '{TMP}'")
    if os.environ.get("DUCKDB_NO_ORDER") == "1":
        con.execute("SET preserve_insertion_order = false")
        res["preserve_insertion_order"] = False
    con.execute(f"CREATE VIEW sales AS SELECT * FROM read_parquet('{SALES}/*.parquet')")
    con.execute(f"CREATE VIEW products AS SELECT * FROM read_parquet('{PRODUCTS}')")
    res["version"] = duckdb.__version__
    t1 = time.perf_counter()
    con.execute(f"COPY ({SQL[query]}) TO '{OUT}.parquet' (FORMAT parquet)")
    t2 = time.perf_counter()
    res["rows_out"] = con.execute(f"SELECT COUNT(*) FROM read_parquet('{OUT}.parquet')").fetchone()[0]

elif engine == "polars":
    os.environ.setdefault("POLARS_MAX_THREADS", str(THREADS))
    import polars as pl
    sales = pl.scan_parquet(f"{SALES}/*.parquet")
    products = pl.scan_parquet(PRODUCTS)
    res["version"] = pl.__version__
    t1 = time.perf_counter()
    polars_query(query, sales, products).sink_parquet(f"{OUT}.parquet")
    t2 = time.perf_counter()
    res["rows_out"] = pl.scan_parquet(f"{OUT}.parquet").select(pl.len()).collect().item()

elif engine == "spark":
    from pyspark.sql import SparkSession
    import pyspark
    spark = (SparkSession.builder.master(f"local[{THREADS}]")
             .config("spark.driver.memory", mem)
             .config("spark.local.dir", TMP)
             .config("spark.ui.enabled", "false")
             .config("spark.sql.session.timeZone", "UTC")
             .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR")
    spark.read.parquet(SALES).createOrReplaceTempView("sales")
    spark.read.parquet(PRODUCTS).createOrReplaceTempView("products")
    res["version"] = pyspark.__version__
    t1 = time.perf_counter()
    spark.sql(SQL[query]).write.mode("overwrite").parquet(OUT)
    t2 = time.perf_counter()
    res["rows_out"] = spark.read.parquet(OUT).count()
    spark.stop()
else:
    raise SystemExit(f"unknown engine {engine}")

res["setup_s"] = round(t1 - T0, 3)      # interpreter + import + session start
res["query_s"] = round(t2 - t1, 3)      # read Parquet -> compute -> write Parquet
print("RESULT " + json.dumps(res), flush=True)
