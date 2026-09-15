#!/usr/bin/env python3
"""
CBP-1.0 Parser for Memory Benchmark (T020).
Extracts read and write throughput (MiB/s), total operations, and average latency.
Appends metrics to master/memory_results.csv.
"""

import sys
import re
import csv
from pathlib import Path

def parse_memory_log(raw_log_path: str, run_id: str, test_id: str = "T020"):
    log_content = Path(raw_log_path).read_text(encoding="utf-8", errors="replace")
    master_csv = Path("d:/Projects/CloudMark/master/memory_results.csv")

    rows_to_add = []

    # Split into Part 1 (Write) and Part 2 (Read)
    parts = re.split(r"--- Part \d+:\s*(.+?) ---", log_content)
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            part_title = parts[i].strip()
            part_body = parts[i+1]

            operation = "write" if "write" in part_title.lower() else "read"

            # Threads
            thd_match = re.search(r"Number of threads:\s*(\d+)", part_body)
            threads = int(thd_match.group(1)) if thd_match else 1

            # Throughput in MiB/sec
            tp_match = re.search(r"\(([\d\.]+)\s*MiB/sec\)", part_body)
            throughput_mb_s = float(tp_match.group(1)) if tp_match else 0.0

            # Total transferred
            trans_match = re.search(r"([\d\.]+)\s*MiB transferred", part_body)
            total_transferred_mb = float(trans_match.group(1)) if trans_match else 0.0

            # Latency average
            lat_match = re.search(r"avg:\s*([\d\.]+)", part_body)
            avg_lat_ms = float(lat_match.group(1)) if lat_match else 0.0

            rows_to_add.append([
                run_id, test_id, operation, threads, "1M",
                total_transferred_mb, throughput_mb_s, avg_lat_ms,
                Path(raw_log_path).name
            ])

    if rows_to_add:
        existing_keys = set()
        if master_csv.exists():
            with open(master_csv, mode="r", encoding="utf-8") as f:
                for r in csv.reader(f):
                    if len(r) >= 3:
                        existing_keys.add((r[0], r[1], r[2]))

        filtered_rows = [r for r in rows_to_add if (r[0], r[1], r[2]) not in existing_keys]
        if filtered_rows:
            with open(master_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(filtered_rows)
            for r in filtered_rows:
                print(f"[{test_id}] Parsed: Oper={r[2]}, Threads={r[3]}, Throughput={r[6]} MiB/s, Latency={r[7]} ms")
        else:
            print(f"[{test_id}] Memory rows already present in master dataset. Skipping duplicate append.")
    else:
        print(f"[{test_id}] No memory test parts matched in {raw_log_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: parse_memory.py <raw_log_path> <run_id> [test_id]")
        sys.exit(1)
    tid = sys.argv[3] if len(sys.argv) > 3 else "T020"
    parse_memory_log(sys.argv[1], sys.argv[2], tid)
