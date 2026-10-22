import hashlib
import json
import logging
import os
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import duckdb

import bench


logger = logging.getLogger(__name__)
RESULTS = Path("results/faster_dedup")
CANDIDATES = ("q3_max_join_latest", "q3_max_sort_latest")
BASELINE = "q3_sort_unique_latest"
CAP_GIB = 4.5
TIMEOUT_SECONDS = 120


def validate_output(path: Path) -> dict[str, int]:
    with duckdb.connect() as connection:
        connection.execute("SET memory_limit = '2GB'")
        connection.execute("SET threads = 8")
        connection.execute("SET temp_directory = 'out/tmp/validation'")
        connection.read_parquet("out/duckdb/150m_q3_window_latest.parquet").create_view("expected")
        connection.read_parquet(str(path)).create_view("actual")
        counts = {
            "rows": connection.execute("SELECT count(*) FROM actual").fetchone()[0],
            "missing": connection.execute("SELECT count(*) FROM (SELECT * FROM expected EXCEPT ALL SELECT * FROM actual)").fetchone()[0],
            "extra": connection.execute("SELECT count(*) FROM (SELECT * FROM actual EXCEPT ALL SELECT * FROM expected)").fetchone()[0],
        }
    if counts["missing"] or counts["extra"]:
        raise ValueError(f"Output mismatch for {path}: {counts}")
    return counts


def checksums() -> None:
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
    (RESULTS / "checksums.txt").write_text(f"All {checked} generated files match data_checksums.md5.\n")


def screen(budget: str) -> None:
    tag = f"screen_{budget}"
    command = [sys.executable, "bench.py", "--sizes", "150m", "--engines", "polars",
               "--queries", ",".join(CANDIDATES), "--reps", "1", "--budget-gib", str(CAP_GIB),
               "--timeout", str(TIMEOUT_SECONDS), "--tag", f"faster_dedup/{tag}"]
    if budget != "default":
        command += ["--env", f"POLARS_OOC_MEMORY_BUDGET_MB={budget}"]
    subprocess.run(command, check=True)
    records = [json.loads(line) for line in (RESULTS / f"{tag}.jsonl").read_text().splitlines()]
    validation = []
    for record in records:
        if record["status"] != "ok":
            continue
        query = record["query"]
        validation.append({"query": query, "budget": budget,
                           **validate_output(Path(f"out/polars/150m_{query}.parquet"))})
    (RESULTS / f"{tag}_validation.json").write_text(json.dumps(validation, indent=2) + "\n")


def compare() -> None:
    screened = [json.loads(line) for path in RESULTS.glob("screen_*.jsonl")
                for line in path.read_text().splitlines()]
    successful = [record for record in screened if record["status"] == "ok"]
    if not successful:
        raise RuntimeError("No candidate completed under the cap")
    winner = min(successful, key=lambda record: record["wall_s"])
    query = winner["query"]
    budget = winner.get("POLARS_OOC_MEMORY_BUDGET_MB")
    (RESULTS / "selected.json").write_text(json.dumps(winner, indent=2) + "\n")
    logger.info("Selected %s with spill budget %s", query, budget or "default")
    records = []
    validation = []
    with (RESULTS / "comparison.jsonl").open("w") as stream:
        for repetition in range(1, 4):
            names = [BASELINE, query] if repetition % 2 else [query, BASELINE]
            for name in names:
                setting = "1024" if name == BASELINE else budget
                environment = {"POLARS_OOC_MEMORY_BUDGET_MB": setting} if setting else {}
                available, busy = bench.wait_for_room(5.0, 30.0)
                load = os.getloadavg()[0]
                record = bench.run_one("polars", "150m", name, "3g", CAP_GIB, 1.0, TIMEOUT_SECONDS, environment)
                record.update({"rep": repetition, "pre_avail_gib": round(available, 2),
                               "pre_load1": round(load, 2), "pre_cpu_busy_pct": round(busy, 1),
                               "started": datetime.now().isoformat(timespec="seconds"), **environment})
                stream.write(json.dumps(record) + "\n")
                stream.flush()
                records.append(record)
                logger.info("%s", record)
                if record["status"] != "ok":
                    raise RuntimeError(f"Repeat failed: {record}")
                validation.append({"query": name, "rep": repetition,
                                   **validate_output(Path(f"out/polars/150m_{name}.parquet"))})
                (RESULTS / "validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    medians = {name: statistics.median(record["wall_s"] for record in records if record["query"] == name)
               for name in (BASELINE, query)}
    (RESULTS / "comparison.json").write_text(json.dumps(medians, indent=2) + "\n")
    if medians[query] >= medians[BASELINE]:
        raise RuntimeError(f"No speed improvement: {medians}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if sys.argv[1] == "checksums":
        checksums()
    elif sys.argv[1] == "screen":
        screen(sys.argv[2])
    elif sys.argv[1] == "compare":
        compare()
    else:
        raise ValueError(sys.argv[1])
