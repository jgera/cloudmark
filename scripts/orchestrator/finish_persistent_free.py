#!/usr/bin/env python3
"""
CloudMark Persistent Free Tier - Complete PostgreSQL Benchmark (T050 - T053)
Executes database scaling on the permanent Frankfurt Free Tier node, parses all metrics,
and updates all reports while preserving the instance permanently.
"""

import sys
import os
import time
import subprocess
import json
import csv
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

RUN_ID = "2026-09-16_vultr_frankfurt_vc2-1c-0.5gb-free_run01"
HOST_IP = "136.244.82.152"
PRIVKEY_PATH = str(Path(os.path.expanduser(r"~\.ssh\cloudmark_id_ed25519")))

def log(msg):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n[{now}] === {msg} ===", flush=True)

def main():
    log(f"Resuming PostgreSQL suite for persistent Free Tier run: {RUN_ID} on {HOST_IP}")

    # Step 1: Run T050
    log("Executing T050 — PostgreSQL Environment Capture")
    cloudmark_runner.run_test(RUN_ID, "T050", HOST_IP, PRIVKEY_PATH)

    # Step 2: Run T051
    log("Executing T051 — PostgreSQL Working Set Init & Size")
    cloudmark_runner.run_test(RUN_ID, "T051", HOST_IP, PRIVKEY_PATH)

    # Step 3: Run T052
    log("Executing T052 — Mixed OLTP Concurrency Scaling (Clients: 1, 4, 8, 16, 32)")
    cloudmark_runner.run_test(RUN_ID, "T052", HOST_IP, PRIVKEY_PATH)

    # Step 4: Run T053
    log("Executing T053 — SELECT-Only Concurrency Scaling (Clients: 1, 4, 8, 16, 32)")
    cloudmark_runner.run_test(RUN_ID, "T053", HOST_IP, PRIVKEY_PATH)

    log("PostgreSQL benchmark tests completed successfully on Free Tier node!")

    # Step 5: Update master/runs.csv
    end_time = datetime.now(timezone.utc)
    runs_csv = BASE_DIR / "master" / "runs.csv"
    if runs_csv.exists():
        rows = []
        with open(runs_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for r in reader:
                if r.get("run_id") == RUN_ID:
                    r["end_utc"] = end_time.strftime("%Y-%m-%d %H:%M:%S UTC")
                    r["notes"] = "Complete; persistent free baseline preserved"
                rows.append(r)
        with open(runs_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        log("master/runs.csv updated with completion status.")

    # Step 6: Generate single-run summary
    try:
        cloudmark_runner.generate_report(RUN_ID)
        log("Single-run summary generated.")
    except Exception as re:
        log(f"Report generation note: {re}")

    # Step 7: Compile all publication reports
    try:
        import compile_all_reports
        compile_all_reports.compile_reports()
        log("All publication reports recompiled successfully.")
    except Exception as ce:
        log(f"Report compile note: {ce}")

    log("==================================================================")
    log(f"VULTR FREE TIER PERMANENT NODE IS PRESERVED AND READY FOR USE!")
    log(f"Public IP   : {HOST_IP}")
    log(f"Location    : Frankfurt, Germany (fra)")
    log(f"SSH Command : ssh -i {PRIVKEY_PATH} root@{HOST_IP}")
    log("==================================================================")

if __name__ == "__main__":
    main()
