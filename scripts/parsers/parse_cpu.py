#!/usr/bin/env python3
"""
CBP-1.0 Parser for CPU Benchmarks (T010, T011, T012).
Extracts events/sec, mean latency, p95 latency, multicore scaling efficiency,
and time-series burst vs. sustained metrics for T012.
Appends derived metrics to master/cpu_results.csv.
"""

import sys
import re
import csv
import math
from pathlib import Path

def parse_cpu_log(raw_log_path: str, run_id: str, test_id: str):
    log_content = Path(raw_log_path).read_text(encoding="utf-8", errors="replace")

    # Extract thread count
    thread_match = re.search(r"Number of threads:\s*(\d+)", log_content)
    thread_count = int(thread_match.group(1)) if thread_match else 1

    # Extract overall events per second
    eps_match = re.search(r"events per second:\s*([\d\.]+)", log_content)
    events_per_sec = float(eps_match.group(1)) if eps_match else 0.0

    # Extract average latency
    avg_lat_match = re.search(r"avg:\s*([\d\.]+)", log_content)
    mean_lat_ms = float(avg_lat_match.group(1)) if avg_lat_match else 0.0

    # Extract 95th percentile latency
    p95_match = re.search(r"95th percentile:\s*([\d\.]+)", log_content)
    p95_lat_ms = float(p95_match.group(1)) if p95_match else 0.0

    scaling_eff = "N/A"
    master_csv = Path("d:/Projects/CloudMark/master/cpu_results.csv")

    # If T011, compute multicore scaling efficiency relative to T010
    if test_id == "T011" and master_csv.exists() and thread_count > 1:
        with open(master_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("run_id") == run_id and row.get("test_id") == "T010":
                    single_score = float(row.get("events_per_sec", 0))
                    if single_score > 0:
                        scaling_eff = round(events_per_sec / (single_score * thread_count), 4)
                    break

    # If T012, compute time-series burst vs sustained
    extra_note = ""
    if test_id == "T012":
        # Progress lines: [ 5s ] thds: 4 eps: 4200.00 lat (ms,95%): 0.95
        interval_eps = []
        for m in re.finditer(r"\[\s*(\d+)s\s*\]\s*thds:\s*\d+\s*eps:\s*([\d\.]+)", log_content):
            sec = int(m.group(1))
            eps = float(m.group(2))
            interval_eps.append((sec, eps))

        if interval_eps:
            burst_samples = [eps for sec, eps in interval_eps if sec <= 30]
            sustained_samples = [eps for sec, eps in interval_eps if sec >= 240]
            burst_eps = sum(burst_samples) / len(burst_samples) if burst_samples else events_per_sec
            sustained_eps = sum(sustained_samples) / len(sustained_samples) if sustained_samples else events_per_sec
            ratio = round(burst_eps / sustained_eps, 2) if sustained_eps > 0 else 1.0

            # Calculate coefficient of variation
            all_eps = [eps for _, eps in interval_eps]
            mean_eps = sum(all_eps) / len(all_eps)
            variance = sum((x - mean_eps) ** 2 for x in all_eps) / len(all_eps)
            cv = round((math.sqrt(variance) / mean_eps) * 100, 2) if mean_eps > 0 else 0.0

            scaling_eff = f"Burst/Sust={ratio}, CV={cv}%"
            print(f"[T012 Time Series] Burst (first 30s): {burst_eps:.1f} eps | Sustained (final 60s): {sustained_eps:.1f} eps | Ratio: {ratio}x | CV: {cv}%")

    # Append to master/cpu_results.csv
    existing_keys = set()
    if master_csv.exists():
        with open(master_csv, mode="r", encoding="utf-8") as f:
            for r in csv.reader(f):
                if len(r) >= 2:
                    existing_keys.add((r[0], r[1]))

    if (run_id, test_id) not in existing_keys:
        with open(master_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                run_id, test_id, "sysbench_cpu", thread_count,
                events_per_sec, mean_lat_ms, p95_lat_ms, scaling_eff,
                Path(raw_log_path).name
            ])
        print(f"[{test_id}] Parsed: Threads={thread_count}, Events/sec={events_per_sec}, MeanLat={mean_lat_ms}ms, P95Lat={p95_lat_ms}ms, ScalingMetric={scaling_eff}")
    else:
        print(f"[{test_id}] Row already present in master dataset. Skipping duplicate append.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: parse_cpu.py <raw_log_path> <run_id> <test_id>")
        sys.exit(1)
    parse_cpu_log(sys.argv[1], sys.argv[2], sys.argv[3])
