"""Seeded synthetic star schema: sales fact + products dimension, written as Parquet.

Usage: python gen_data.py <rows_millions>   e.g. 10  -> data/sales_10m/*.parquet
Deterministic: same seed, same rows. Written in 5M-row chunks to keep generator memory small.
"""
import os
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

SEED = 20261019
CHUNK = 5_000_000
N_PRODUCTS = 50_000
N_STORES = 500
STATUSES = np.array(["completed", "shipped", "processing", "cancelled", "returned"])
STATUS_P = [0.55, 0.20, 0.12, 0.08, 0.05]
CATEGORIES = np.array(["electronics", "books", "home", "clothing", "grocery",
                       "toys", "sports", "beauty", "garden", "auto"])

def write_products(root):
    path = os.path.join(root, "products.parquet")
    if os.path.exists(path):
        return
    rng = np.random.default_rng(SEED)
    t = pa.table({
        "product_id": np.arange(N_PRODUCTS, dtype=np.int32),
        "category": rng.choice(CATEGORIES, N_PRODUCTS),
        "brand": np.char.add("brand_", rng.integers(0, 2_000, N_PRODUCTS).astype(str)),
        "list_price": np.round(rng.uniform(2.0, 500.0, N_PRODUCTS), 2),
    })
    pq.write_table(t, path)

def write_sales(root, rows):
    out = os.path.join(root, f"sales_{rows // 1_000_000}m")
    os.makedirs(out, exist_ok=True)
    n_customers = max(1_000_000, rows // 10)   # ~10 orders per customer
    start = np.datetime64("2026-01-01T00:00:00", "s").astype(np.int64)
    span = 270 * 24 * 3600                       # Jan..Sep 2026
    for i, lo in enumerate(range(0, rows, CHUNK)):
        n = min(CHUNK, rows - lo)
        rng = np.random.default_rng([SEED, i])
        t = pa.table({
            "order_id": np.arange(lo, lo + n, dtype=np.int64),
            "ts": pa.array(start + rng.integers(0, span, n), pa.timestamp("s")),
            "customer_id": rng.integers(0, n_customers, n, dtype=np.int32),
            "product_id": rng.integers(0, N_PRODUCTS, n, dtype=np.int32),
            "store_id": rng.integers(0, N_STORES, n, dtype=np.int16),
            "qty": rng.integers(1, 10, n, dtype=np.int16),
            "price": np.round(rng.uniform(1.0, 500.0, n), 2),
            "status": rng.choice(STATUSES, n, p=STATUS_P),
        })
        pq.write_table(t, os.path.join(out, f"part-{i:04d}.parquet"),
                       row_group_size=1_000_000, compression="snappy")
    return out

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    rows = int(sys.argv[1]) * 1_000_000
    os.makedirs(root, exist_ok=True)
    write_products(root)
    print(write_sales(root, rows))
