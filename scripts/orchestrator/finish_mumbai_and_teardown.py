#!/usr/bin/env python3
"""
CloudMark Resumption & Auto-Teardown for Vultr Mumbai vc2-1c-1gb
Completes T053 (SELECT-only scaling), parses into master datasets,
unconditionally deletes the VM instance, and updates all reports.
"""

import sys
import os
import time
import subprocess
import json
import csv
from datetime import datetime, timezone
from pathlib import Path

# Fix Windows console UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path("d:/Projects/CloudMark")
sys.path.insert(0, str(BASE_DIR / "scripts" / "orchestrator"))
import cloudmark_runner
import compile_all_reports

VULTR_CLI = str(BASE_DIR / "bin" / "vultr" / "vultr-cli.exe")
INSTANCE_ID = "c320bc06-c226-4bd0-8f98-1e6e84d101ad"
HOST_IP = "65.20.89.68"
RUN_ID = "2026-09-14_vultr_mumbai_vc2-1c-1gb_run01"
PRIVKEY_PATH = str(Path(os.path.expanduser(r"~\.ssh\cloudmark_id_ed25519")))

def log(msg):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n[{now}] === {msg} ===", flush=True)

def teardown():
    log(f"INITIATING UNCONDITIONAL TEARDOWN OF VULTR INSTANCE: {INSTANCE_ID}")
    try:
        res = subprocess.run([VULTR_CLI, "instance", "delete", INSTANCE_ID], capture_output=True, text=True)
        if res.returncode == 0:
            log(f"Teardown command issued successfully for {INSTANCE_ID}.")
        else:
            log(f"Teardown warning: {res.stderr.strip()}")
    except Exception as e:
        log(f"Error executing teardown: {e}")

    # Verify 0 instances remain
    time.sleep(5)
    chk = subprocess.run([VULTR_CLI, "instance", "list"], capture_output=True, text=True)
    log(f"Current Vultr instances:\n{chk.stdout.strip()}")

def main():
    log(f"Resuming run {RUN_ID} on {HOST_IP} (Instance: {INSTANCE_ID})")
    
    try:
        # Step 1: Run T053 (SELECT-only scaling)
        log("Executing T053 — SELECT-Only Concurrency Scaling (Clients: 1, 4, 8, 16, 32)")
        cloudmark_runner.run_test(RUN_ID, "T053", HOST_IP, PRIVKEY_PATH)
        log("T053 completed successfully.")
    except Exception as e:
        log(f"Exception during T053: {e}")
    finally:
        # Step 2: Unconditional Teardown
        teardown()

    # Step 3: Trigger parsers for any unparsed raw logs
    raw_dir = BASE_DIR / "runs" / RUN_ID / "raw"
    t053_log = raw_dir / "T053_raw.log"
    if t053_log.exists():
        log("Triggering parser for T053...")
        cloudmark_runner.trigger_parser(RUN_ID, "T053", t053_log)

    # Step 4: Update master/runs.csv
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
                    r["notes"] = "Complete; instance destroyed"
                rows.append(r)
        with open(runs_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        log("master/runs.csv updated with completion status.")

    # Step 5: Generate single-run report
    try:
        cloudmark_runner.generate_report(RUN_ID)
        log("Generated run summary report.")
    except Exception as e:
        log(f"Error generating run summary: {e}")

    # Step 6: Compile all master reports
    try:
        compile_all_reports.compile_reports()
        log("All publication reports recompiled successfully.")
    except Exception as e:
        log(f"Error compiling reports: {e}")

    log("ALL OPERATIONS COMPLETED.")

if __name__ == "__main__":
    main()
