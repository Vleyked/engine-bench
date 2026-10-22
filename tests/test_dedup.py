import random
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import polars as pl

from queries import SQL, polars_query


SCHEMA = {
    "customer_id": pl.Int32,
    "order_id": pl.Int64,
    "ts": pl.Datetime("ms"),
    "qty": pl.Int16,
    "price": pl.Float64,
}
OUTPUT_SCHEMA = {name: SCHEMA[name] for name in ("customer_id", "order_id", "ts")}
OUTPUT_SCHEMA["amount"] = pl.Float64
Sale = tuple[int | None, int | None, datetime | None, int | None, float | None]


class DedupTests(unittest.TestCase):
    def assert_matches_sql(self, parts: list[list[Sale]]) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = []
            for index, rows in enumerate(parts):
                path = root / f"sales-{index}.parquet"
                pl.DataFrame(rows, schema=SCHEMA, orient="row").write_parquet(path)
                paths.append(str(path))
            sales = pl.scan_parquet(paths)
            output = root / "result.parquet"
            polars_query("q3_sort_unique_latest", sales, pl.LazyFrame()).sink_parquet(
                output, engine="streaming"
            )
            actual = pl.read_parquet(output).sort("customer_id", nulls_last=True)
            with duckdb.connect() as connection:
                connection.read_parquet(paths).create_view("sales")
                expected = connection.execute(
                    f"{SQL['q3_window_latest']} ORDER BY customer_id NULLS LAST"
                ).fetchall()
            self.assertEqual(actual.schema, OUTPUT_SCHEMA)
            self.assertEqual(actual.rows(), expected)

    def test_edge_cases(self) -> None:
        early = datetime(2026, 1, 1)
        late = datetime(2026, 1, 2)
        cases: dict[str, list[Sale]] = {
            "unsorted_groups_and_ties": [
                (2, 40, early, 2, 1.5),
                (1, 30, late, 3, 2.5),
                (2, 10, late, 4, 3.5),
                (1, 50, early, 5, 4.5),
                (1, 20, late, 6, 5.5),
            ],
            "singleton": [(7, 1, late, 2, 3.5)],
            "null_ordering_and_values": [
                (1, 100, None, 2, 3.5),
                (1, 10, early, 3, 4.5),
                (2, None, late, 4, 5.5),
                (2, 20, late, None, 6.5),
                (3, 30, None, 5, 7.5),
                (3, 40, None, 6, None),
                (None, 50, early, 7, 8.5),
                (None, 60, late, 8, 9.5),
                (4, None, None, 9, 10.5),
            ],
            "empty": [],
        }
        for name, rows in cases.items():
            with self.subTest(name=name):
                self.assert_matches_sql([rows])

    def test_ties_across_parquet_files(self) -> None:
        generator = random.Random(20261019)
        start = datetime(2026, 1, 1)
        rows: list[Sale] = [
            (
                generator.randrange(37),
                order_id,
                start + timedelta(days=generator.randrange(5)),
                generator.randrange(1, 10),
                generator.randrange(1, 2000) / 4,
            )
            for order_id in range(1200)
        ]
        generator.shuffle(rows)
        self.assert_matches_sql([rows[index::4] for index in range(4)])


if __name__ == "__main__":
    unittest.main()
