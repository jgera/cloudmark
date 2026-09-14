#!/usr/bin/env python3
"""
CloudMark GCP Benchmark Battery Runner (CBP-1.0)
Executes CBP-1.0 benchmark sequence against GCP instance (db-vm) via gcloud IAP tunnel,
parses all raw logs into master datasets, and generates the comparative report.
Preserves the Always-Free db-vm instance (DO NOT TEARDOWN).
"""

import sys
import os
import time
import argparse
import subprocess
import json
import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path

# Fix Windows console UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Force Python 3.12 for gcloud SDK to avoid Windows alias warning
os.environ["CLOUDSDK_PYTHON"] = r"C:\Users\J\AppData\Local\Programs\Python\Python312\python.exe"

GCLOUD_BIN = shutil.which("gcloud") or "gcloud.cmd"

BASE_DIR = Path("d:/Projects/CloudMark")
RUNS_DIR = BASE_DIR / "runs"
SCRIPTS_DIR = BASE_DIR / "scripts" / "benchmark"
PARSERS_DIR = BASE_DIR / "scripts" / "parsers"
MASTER_DIR = BASE_DIR / "master"

sys.path.insert(0, str(BASE_DIR / "scripts" / "orchestrator"))
import cloudmark_runner

TEST_SCRIPT_MAP = {
    "T001": SCRIPTS_DIR / "t001_characterization.sh",
    "T002": SCRIPTS_DIR / "t002_idle_baseline.sh",
    "T010": SCRIPTS_DIR / "t010_cpu_single.sh",
    "T011": SCRIPTS_DIR / "t011_cpu_multi.sh",
    "T012": SCRIPTS_DIR / "t012_cpu_sustained.sh",
    "T020": SCRIPTS_DIR / "t020_memory.sh",
    "T030": SCRIPTS_DIR / "t030_storage_id.sh",
    "T031": SCRIPTS_DIR / "t031_storage_seq.sh",
    "T032": SCRIPTS_DIR / "t032_storage_rand.sh",
    "T040": SCRIPTS_DIR / "t040_network_throughput.sh",
    "T050": SCRIPTS_DIR / "t050_postgres_env.sh",
    "T051": SCRIPTS_DIR / "t051_pg_init_s10.sh",
    "T052": SCRIPTS_DIR / "t052_pg_oltp_scale.sh",
    "T053": SCRIPTS_DIR / "t053_pg_select_scale.sh",
}

def log(msg):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n[{now}] === {msg} ===", flush=True)

def run_cmd_stream(cmd, raw_log_path=None):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1
    )
    
    log_file = None
    if raw_log_path:
        raw_log_path.parent.mkdir(parents=True, exist_ok=True)
        log_file = open(raw_log_path, "w", encoding="utf-8")
        
    try:
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            if log_file:
                log_file.write(line)
                log_file.flush()
    finally:
        if log_file:
            log_file.close()
            
    proc.wait()
    return proc.returncode

def upload_and_run(instance, zone, script_path, raw_log_path):
    # Ensure unix line endings
    content = script_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    temp_dir = BASE_DIR / "runs" / "_tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_local_file = temp_dir / script_path.name
    temp_local_file.write_bytes(content.encode("utf-8"))
    
    remote_path = f"/tmp/{script_path.name}"
    
    # SCP via IAP
    scp_cmd = [
        GCLOUD_BIN, "compute", "scp",
        str(temp_local_file),
        f"{instance}:{remote_path}",
        "--zone", zone,
        "--tunnel-through-iap",
        "--quiet"
    ]
    log(f"Uploading {script_path.name} to {instance}:{remote_path} via IAP...")
    res = subprocess.run(scp_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"SCP error ({res.returncode}):\n{res.stderr}", flush=True)
        return False
        
    # Execute via IAP
    ssh_cmd = [
        GCLOUD_BIN, "compute", "ssh",
        instance,
        "--zone", zone,
        "--tunnel-through-iap",
        "--quiet",
        "--command", f"bash {remote_path}"
    ]
    log(f"Executing {script_path.name} on {instance}...")
    rc = run_cmd_stream(ssh_cmd, raw_log_path)
    return rc == 0

def run_single_test(run_id, test_id, instance, zone, force=False):
    if test_id not in TEST_SCRIPT_MAP:
        log(f"Error: Unknown test_id {test_id}")
        return False

    raw_log = RUNS_DIR / run_id / "raw" / f"{test_id}_raw.log"
    if raw_log.exists() and raw_log.stat().st_size > 100 and not force:
        log(f"Skipping {test_id}: Raw log exists ({raw_log.stat().st_size} bytes). Use --force to re-run.")
        cloudmark_runner.trigger_parser(run_id, test_id, raw_log)
        return True

    script_path = TEST_SCRIPT_MAP[test_id]
    log(f"Running CBP-1.0 Test {test_id}: {script_path.name}")
    success = upload_and_run(instance, zone, script_path, raw_log)
    if not success:
        log(f"Warning: Test {test_id} returned non-zero code. Attempting to parse raw output anyway.")

    cloudmark_runner.trigger_parser(run_id, test_id, raw_log)
    return success

def run_battery(run_id, instance, zone, selected_tests=None, force=False):
    start_time = datetime.now(timezone.utc)
    log(f"Starting GCP CBP-1.0 Battery for {run_id} on {instance} ({zone})")

    # Sequence of standard battery
    default_sequence = [
        "T001",  # Characterization
        "T002",  # Idle baseline
        "T010",  # CPU single
        "T011",  # CPU multi
        "T012",  # CPU sustained (300s)
        "T020",  # Memory
        "T030",  # Storage id
        "T031",  # Storage seq
        "T032",  # Storage rand
        "T040",  # Network throughput
        "T050",  # PostgreSQL env
        "T051",  # PostgreSQL s10 init
        "T052",  # Mixed OLTP scale
        "T053",  # SELECT-only scale
    ]

    tests_to_run = selected_tests if selected_tests else default_sequence

    for tid in tests_to_run:
        log(f"--- Starting Stage: {tid} ---")
        run_single_test(run_id, tid, instance, zone, force=force)

    # Finalize
    end_time = datetime.now(timezone.utc)
    log("All requested tests completed. Generating summary report...")
    cloudmark_runner.generate_report(run_id)

    # Update runs.csv
    runs_csv = MASTER_DIR / "runs.csv"
    if runs_csv.exists():
        rows = []
        with open(runs_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for r in reader:
                if r.get("run_id") == run_id:
                    r["end_utc"] = end_time.strftime("%Y-%m-%d %H:%M:%S UTC")
                    r["notes"] = "Complete; persistent baseline preserved"
                rows.append(r)
        with open(runs_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    log("GCP benchmark battery execution completed successfully!")
    log(f"TARGET INSTANCE '{instance}' IS PRESERVED AND RUNNING (Always Free Tier).")

def main():
    parser = argparse.ArgumentParser(description="CloudMark GCP Battery Runner")
    parser.add_argument("--run-id", default="2026-09-14_gcp_uswest1_e2-micro_run01")
    parser.add_argument("--instance", default="db-vm")
    parser.add_argument("--zone", default="us-west1-a")
    parser.add_argument("--tests", default=None, help="Comma-separated test IDs (e.g. T001,T010)")
    parser.add_argument("--force", action="store_true", help="Force re-run even if raw log exists")

    args = parser.parse_args()
    selected = [t.strip() for t in args.tests.split(",")] if args.tests else None
    run_battery(args.run_id, args.instance, args.zone, selected, args.force)

if __name__ == "__main__":
    main()
