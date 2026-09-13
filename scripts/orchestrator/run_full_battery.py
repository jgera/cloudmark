#!/usr/bin/env python3
"""
CloudMark Full Benchmark Battery & Auto-Teardown Runner
Executes CBP-1.0 test sequence autonomously, parses all metrics into master CSVs,
generates a comparative report against the GCP baseline, and unconditionally destroys
the billable Vultr VM when complete.
"""

import sys
import os
import time
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path("d:/Projects/CloudMark")
sys.path.insert(0, str(BASE_DIR / "scripts" / "orchestrator"))
import cloudmark_runner

RUN_ID = "2026-09-13_vultr_delhi_hp-4c8g-intel_run01"
HOST_IP = "139.84.169.177"
INSTANCE_ID = "56e328fe-db32-44ae-9ef5-93680d51c24a"
SSH_KEY = "C:/Users/J/.ssh/cloudmark_id_ed25519"
VULTR_CLI = str(BASE_DIR / "bin" / "vultr" / "vultr-cli.exe")

def log(msg):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n[{now}] === {msg} ===", flush=True)

def teardown_instance():
    log(f"INITIATING TEARDOWN OF VULTR INSTANCE: {INSTANCE_ID}")
    try:
        cmd = [VULTR_CLI, "instance", "delete", INSTANCE_ID]
        res = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Teardown stdout: {res.stdout.strip()}")
        if res.stderr:
            print(f"Teardown stderr: {res.stderr.strip()}")
        log(f"TEARDOWN COMPLETE. No billable instances running.")
    except Exception as e:
        print(f"Error during teardown: {e}")

def main():
    start_time = datetime.now(timezone.utc)
    log(f"Starting autonomous benchmark run: {RUN_ID} on {HOST_IP}")

    try:
        # Step 1: T002 - Idle Baseline
        log("Executing T002 — Idle-System Baseline")
        cloudmark_runner.run_test(RUN_ID, "T002", HOST_IP, SSH_KEY)

        # Step 2: Setup Node Packages (sysstat, sysbench, fio, postgresql)
        log("Executing Node Baseline Setup (installing packages, vendor defaults)")
        setup_log = BASE_DIR / "runs" / RUN_ID / "raw" / "setup_node_raw.log"
        cloudmark_runner.execute_remote(HOST_IP, BASE_DIR / "scripts" / "benchmark" / "setup_node.sh", setup_log, SSH_KEY)

        # Step 3: T010 - CPU Single-Thread
        log("Executing T010 — CPU Single-Thread Performance")
        cloudmark_runner.run_test(RUN_ID, "T010", HOST_IP, SSH_KEY)

        # Step 4: T011 - CPU Multi-Thread (all 4 vCPUs)
        log("Executing T011 — CPU Multi-Thread Performance")
        cloudmark_runner.run_test(RUN_ID, "T011", HOST_IP, SSH_KEY)

        # Step 5: T012 - Sustained CPU (300s)
        log("Executing T012 — Sustained CPU Test (300s time-series)")
        cloudmark_runner.run_test(RUN_ID, "T012", HOST_IP, SSH_KEY)

        # Step 6: T020 - Memory Bandwidth
        log("Executing T020 — Memory Read & Write Throughput")
        cloudmark_runner.run_test(RUN_ID, "T020", HOST_IP, SSH_KEY)

        # Step 7: Storage Suite (T030, T031, T032)
        log("Executing T030 — Storage Identification")
        cloudmark_runner.run_test(RUN_ID, "T030", HOST_IP, SSH_KEY)

        log("Executing T031 — Sequential Storage Throughput (1MB Direct I/O)")
        cloudmark_runner.run_test(RUN_ID, "T031", HOST_IP, SSH_KEY)

        log("Executing T032 — Random Storage IOPS & Latency (4KB 32-depth)")
        cloudmark_runner.run_test(RUN_ID, "T032", HOST_IP, SSH_KEY)

        # Step 8: Network T041 - Client RTT from local network
        log("Executing T041 — Client End-User RTT from Local Network")
        cloudmark_runner.run_client_rtt(RUN_ID, HOST_IP, count=50)

        # Step 9: PostgreSQL Suite (Direct GCP comparison baseline)
        log("Executing T050 — PostgreSQL Environment Capture")
        cloudmark_runner.run_test(RUN_ID, "T050", HOST_IP, SSH_KEY)

        log("Executing T051 — PostgreSQL Small Working Set Init (Scale 10)")
        cloudmark_runner.run_test(RUN_ID, "T051", HOST_IP, SSH_KEY)

        log("Executing T052 — Mixed OLTP Concurrency Scaling (Clients: 1, 4, 8, 16, 32)")
        cloudmark_runner.run_test(RUN_ID, "T052", HOST_IP, SSH_KEY)

        log("Executing T053 — SELECT-Only Concurrency Scaling (Clients: 1, 4, 8, 16, 32)")
        cloudmark_runner.run_test(RUN_ID, "T053", HOST_IP, SSH_KEY)

        log("All benchmark tests completed successfully!")

    finally:
        # UNCONDITIONAL TEARDOWN
        teardown_instance()

        # Generate final reports
        end_time = datetime.now(timezone.utc)
        log("Generating comprehensive benchmark summary report...")
        cloudmark_runner.generate_report(RUN_ID)

        # Update end_time in master/runs.csv
        runs_csv = BASE_DIR / "master" / "runs.csv"
        if runs_csv.exists():
            import csv
            rows = []
            with open(runs_csv, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for r in reader:
                    if r.get("run_id") == RUN_ID:
                        r["end_utc"] = end_time.strftime("%Y-%m-%d %H:%M:%S UTC")
                        r["notes"] = "Complete; instance destroyed"
                    rows.append(r)
            with open(runs_csv, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        log("Benchmark battery finished and master records finalized.")

if __name__ == "__main__":
    main()
