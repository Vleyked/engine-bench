import hashlib
import json
import logging
import sys
from pathlib import Path

import duckdb


logger = logging.getLogger(__name__)
RESULTS = Path("results/dedup_linux")


def verify_checksums() -> None:
    checked = 0
    for line in Path("data_checksums.md5").read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        if "sales_50m/" in name:
            continue
        with Path(name).open("rb") as stream:
            actual = hashlib.file_digest(stream, "md5").hexdigest()
        if actual != expected:
            raise ValueError(f"Checksum mismatch: {name}")
        checked += 1
    message = f"All {checked} generated data files match data_checksums.md5.\n"
    (RESULTS / "checksums.txt").write_text(message)
    logger.info(message.strip())


def verify_outputs() -> None:
    records = []
    with duckdb.connect() as connection:
        connection.execute("SET memory_limit = '2GB'")
        connection.execute("SET threads = 8")
        connection.execute("SET temp_directory = 'out/tmp/validation'")
        for size in ("10m", "150m"):
            expected = f"out/duckdb/{size}_q3_window_latest.parquet"
            actual = f"out/polars/{size}_q3_sort_unique_latest.parquet"
            connection.execute(f"CREATE OR REPLACE VIEW expected AS SELECT * FROM read_parquet('{expected}')")
            connection.execute(f"CREATE OR REPLACE VIEW actual AS SELECT * FROM read_parquet('{actual}')")
            expected_count = connection.execute("SELECT count(*) FROM expected").fetchone()[0]
            actual_count = connection.execute("SELECT count(*) FROM actual").fetchone()[0]
            missing = connection.execute("SELECT count(*) FROM (SELECT * FROM expected EXCEPT ALL SELECT * FROM actual)").fetchone()[0]
            extra = connection.execute("SELECT count(*) FROM (SELECT * FROM actual EXCEPT ALL SELECT * FROM expected)").fetchone()[0]
            record = {"size": size, "expected_rows": expected_count, "actual_rows": actual_count, "missing": missing, "extra": extra}
            records.append(record)
            logger.info("Validation %s", record)
            if missing or extra:
                raise ValueError(f"Dedup mismatch for {size}: {record}")
    (RESULTS / "validation.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if sys.argv[1] == "checksums":
        verify_checksums()
    elif sys.argv[1] == "outputs":
        verify_outputs()
    else:
        raise ValueError(sys.argv[1])
