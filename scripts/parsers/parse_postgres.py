#!/usr/bin/env python3
"""
CBP-1.0 Parser for PostgreSQL Benchmarks (T052, T053).
Parses pgbench progress (-P 5) and final summaries, separating
burst vs. sustained TPS and latency, and appends to master/postgres_results.csv.
"""

import sys
import re
import csv
from pathlib import Path

def parse_pgbench_log(raw_log_path: str, run_id: str, test_id: str):
    log_content = Path(raw_log_path).read_text(encoding="utf-8", errors="replace")
    master_csv = Path("d:/Projects/CloudMark/master/postgres_results.csv")

    workload_type = "select_only" if test_id == "T053" else "mixed_tpc_b"

    # Split by client execution blocks
    blocks = re.split(r"=== Running (?:Mixed OLTP|SELECT-Only): Clients=(\d+), Threads=(\d+), Duration=(\d+)s ===", log_content)
    
    rows_to_add = []

    if len(blocks) > 1:
        # blocks structure: [preamble, clients1, threads1, dur1, body1, clients2, ...]
        for i in range(1, len(blocks), 4):
            clients = int(blocks[i])
            threads = int(blocks[i+1])
            duration_sec = int(blocks[i+2])
            body = blocks[i+3]

            # Parse progress lines: progress: 5.0 s, 1250.0 tps, lat 3.200 ms
            progress_tps = []
            progress_lat = []
            for p_match in re.finditer(r"progress:\s*([\d\.]+)\s*s,\s*([\d\.]+)\s*tps,\s*lat\s*([\d\.]+)\s*ms", body):
                sec = float(p_match.group(1))
                tps = float(p_match.group(2))
                lat = float(p_match.group(3))
                progress_tps.append((sec, tps))
                progress_lat.append((sec, lat))

            # Calculate sustained TPS: second half of test (e.g. sec > duration/2)
            sustained_tps = "N/A"
            sustained_lat = "N/A"
            if progress_tps:
                midpoint = duration_sec / 2.0
                sustained_vals = [tps for sec, tps in progress_tps if sec >= midpoint]
                sustained_lat_vals = [lat for sec, lat in progress_lat if sec >= midpoint]
                if sustained_vals:
                    sustained_tps = round(sum(sustained_vals) / len(sustained_vals), 1)
                if sustained_lat_vals:
                    sustained_lat = round(sum(sustained_lat_vals) / len(sustained_lat_vals), 2)

            # Whole run TPS
            tps_match = re.search(r"tps =\s*([\d\.]+)\s*\(without initial connection time\)", body)
            whole_run_tps = float(tps_match.group(1)) if tps_match else 0.0

            # Whole run average latency
            lat_match = re.search(r"latency average =\s*([\d\.]+)\s*ms", body)
            avg_latency = float(lat_match.group(1)) if lat_match else 0.0
            if sustained_lat == "N/A":
                sustained_lat = avg_latency

            # Failed transactions
            fail_match = re.search(r"number of failed transactions:\s*(\d+)", body)
            failed_txns = int(fail_match.group(1)) if fail_match else 0

            # Scale
            scale_match = re.search(r"scaling factor:\s*(\d+)", body)
            scale = int(scale_match.group(1)) if scale_match else 10

            rows_to_add.append([
                run_id, test_id, workload_type, scale, clients, threads,
                duration_sec, whole_run_tps, sustained_tps, sustained_lat,
                failed_txns, Path(raw_log_path).name
            ])

    if rows_to_add:
        existing_keys = set()
        if master_csv.exists():
            with open(master_csv, mode="r", encoding="utf-8") as f:
                rdr = csv.reader(f)
                for r in rdr:
                    if len(r) >= 5:
                        existing_keys.add((r[0], r[1], str(r[4])))

        filtered_rows = [r for r in rows_to_add if (r[0], r[1], str(r[4])) not in existing_keys]
        if filtered_rows:
            with open(master_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(filtered_rows)
            for r in filtered_rows:
                print(f"[{test_id}] Parsed: Clients={r[4]}, WholeRunTPS={r[7]}, SustainedTPS={r[8]}, Latency={r[9]}ms, Failures={r[10]}")
        else:
            print(f"[{test_id}] Rows already present in master dataset. Skipping duplicate append.")
    else:
        print(f"[{test_id}] No pgbench blocks matched in {raw_log_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: parse_postgres.py <raw_log_path> <run_id> <test_id>")
        sys.exit(1)
    parse_pgbench_log(sys.argv[1], sys.argv[2], sys.argv[3])
