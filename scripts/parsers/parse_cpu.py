#!/usr/bin/env python3
"""
CBP-1.0 Parser for CPU Benchmarks (T010, T011, T012).
Extracts events/sec, mean latency, p95 latency, multicore scaling efficiency,
and appends derived metrics to master/cpu_results.csv.
"""

import sys
import re
import csv
from pathlib import Path

def parse_cpu_log(raw_log_path: str, run_id: str, test_id: str):
    log_content = Path(raw_log_path).read_text(encoding="utf-8", errors="replace")

    # Extract thread count
    thread_match = re.search(r"Number of threads:\s*(\d+)", log_content)
    thread_count = int(thread_match.group(1)) if thread_match else 1

    # Extract events per second
    eps_match = re.search(r"events per second:\s*([\d\.]+)", log_content)
    events_per_sec = float(eps_match.group(1)) if eps_match else 0.0

    # Extract average latency
    avg_lat_match = re.search(r"avg:\s*([\d\.]+)", log_content)
    mean_lat_ms = float(avg_lat_match.group(1)) if avg_lat_match else 0.0

    # Extract 95th percentile latency
    p95_match = re.search(r"95th percentile:\s*([\d\.]+)", log_content)
    p95_lat_ms = float(p95_match.group(1)) if p95_match else 0.0

    # Scaling efficiency calculation (if T011, compare with T010 if present in master)
    scaling_eff = "N/A"
    master_csv = Path("d:/Projects/CloudMark/master/cpu_results.csv")
    if test_id == "T011" and master_csv.exists() and thread_count > 1:
        with open(master_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("run_id") == run_id and row.get("test_id") == "T010":
                    single_score = float(row.get("events_per_sec", 0))
                    if single_score > 0:
                        scaling_eff = round(events_per_sec / (single_score * thread_count), 4)
                    break

    # Append to master/cpu_results.csv
    with open(master_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            run_id, test_id, "sysbench_cpu", thread_count,
            events_per_sec, mean_lat_ms, p95_lat_ms, scaling_eff,
            Path(raw_log_path).name
        ])

    print(f"[{test_id}] Parsed: Threads={thread_count}, Events/sec={events_per_sec}, MeanLat={mean_lat_ms}ms, P95Lat={p95_lat_ms}ms, ScalingEff={scaling_eff}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: parse_cpu.py <raw_log_path> <run_id> <test_id>")
        sys.exit(1)
    parse_cpu_log(sys.argv[1], sys.argv[2], sys.argv[3])
