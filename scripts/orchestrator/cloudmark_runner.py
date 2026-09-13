#!/usr/bin/env python3
"""
CloudMark Unified Master Benchmark Orchestrator (CBP-1.0)
Automates:
- Run lifecycle initialization
- Remote benchmark execution via SSH
- Unmodified raw log preservation (Principle 2.2)
- Automated metric parsing into master datasets
- Run reporting and burst vs sustained analysis
"""

import sys
import os
import argparse
import subprocess
import json
import csv
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path("d:/Projects/CloudMark")
RUNS_DIR = BASE_DIR / "runs"
SCRIPTS_DIR = BASE_DIR / "scripts" / "benchmark"
PARSERS_DIR = BASE_DIR / "scripts" / "parsers"
MASTER_DIR = BASE_DIR / "master"

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
    "T033": SCRIPTS_DIR / "t033_storage_sustained.sh",
    "T040": SCRIPTS_DIR / "t040_network_throughput.sh",
    "T050": SCRIPTS_DIR / "t050_postgres_env.sh",
    "T051": SCRIPTS_DIR / "t051_pg_init_s10.sh",
    "T052": SCRIPTS_DIR / "t052_pg_oltp_scale.sh",
    "T053": SCRIPTS_DIR / "t053_pg_select_scale.sh",
    "T054": SCRIPTS_DIR / "t054_pg_init_s100.sh",
    "T055": SCRIPTS_DIR / "t055_pg_monitored.sh",
}

def init_run(run_id, provider, region, plan_name, monthly_price_usd, promo=True):
    run_path = RUNS_DIR / run_id
    raw_path = run_path / "raw"
    derived_path = run_path / "derived"
    raw_path.mkdir(parents=True, exist_ok=True)
    derived_path.mkdir(parents=True, exist_ok=True)

    machine_id = f"{provider.lower()}-{region.lower()}-{plan_name.lower().replace('.', '')}-01"
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    meta = {
        "run_id": run_id,
        "machine_id": machine_id,
        "protocol_version": "CBP-1.0",
        "provider": provider,
        "region": region,
        "plan_name": plan_name,
        "created_utc": now_utc,
        "pricing": {
            "monthly_usd": float(monthly_price_usd),
            "promotional_credit": promo,
            "currency": "USD"
        }
    }

    (run_path / "metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Add to master/pricing.csv
    pricing_csv = MASTER_DIR / "pricing.csv"
    with open(pricing_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            run_id, provider, plan_name, datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "USD", round(float(monthly_price_usd)/720.0, 4), float(monthly_price_usd),
            promo, 0.0 if promo else float(monthly_price_usd), "Standard on-demand rate"
        ])

    # Add to master/runs.csv
    runs_csv = MASTER_DIR / "runs.csv"
    with open(runs_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            run_id, machine_id, "CBP-1.0", "standard", now_utc, "",
            "Ubuntu", "24.04 LTS", "", "18", "In progress"
        ])

    print(f"Initialized run directory at {run_path}")
    print(f"Recorded metadata and pricing for {run_id}")

def execute_remote(host_ip, script_path, raw_log_path, ssh_key=None):
    print(f"Connecting to root@{host_ip} and executing {script_path.name}...")
    script_content = script_path.read_text(encoding="utf-8")

    ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=15"]
    if ssh_key and Path(ssh_key).exists():
        ssh_cmd.extend(["-i", ssh_key])
    ssh_cmd.extend([f"root@{host_ip}", "bash -s"])

    proc = subprocess.Popen(
        ssh_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1
    )

    with open(raw_log_path, "w", encoding="utf-8") as raw_f:
        # Write stdin script
        proc.stdin.write(script_content)
        proc.stdin.close()

        for line in proc.stdout:
            sys.stdout.write(line)
            raw_f.write(line)
            raw_f.flush()

    proc.wait()
    print(f"\nExecution completed with return code {proc.returncode}.")
    print(f"Raw output preserved at {raw_log_path}")
    return proc.returncode == 0

def run_test(run_id, test_id, host_ip, ssh_key=None):
    if test_id not in TEST_SCRIPT_MAP:
        print(f"Unknown test_id {test_id}. Available: {list(TEST_SCRIPT_MAP.keys())}")
        return False

    script_path = TEST_SCRIPT_MAP[test_id]
    raw_log = RUNS_DIR / run_id / "raw" / f"{test_id}_raw.log"
    raw_log.parent.mkdir(parents=True, exist_ok=True)

    success = execute_remote(host_ip, script_path, raw_log, ssh_key)
    if not success:
        print(f"Warning: Test {test_id} finished with errors. Parsing raw log for diagnostic evidence.")

    # Automatically invoke appropriate parser
    trigger_parser(run_id, test_id, raw_log)
    return success

def trigger_parser(run_id, test_id, raw_log):
    meta_file = RUNS_DIR / run_id / "metadata.json"
    meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}

    if test_id == "T001":
        cmd = [
            sys.executable, str(PARSERS_DIR / "parse_t001.py"),
            str(raw_log), run_id, meta.get("machine_id", f"{run_id}-machine"),
            meta.get("provider", "Vultr"), meta.get("region", "Delhi"),
            meta.get("plan_name", "vhp-4c-8gb")
        ]
        subprocess.run(cmd)

    elif test_id in ("T010", "T011", "T012"):
        cmd = [sys.executable, str(PARSERS_DIR / "parse_cpu.py"), str(raw_log), run_id, test_id]
        subprocess.run(cmd)

    elif test_id in ("T031", "T032", "T033"):
        cmd = [sys.executable, str(PARSERS_DIR / "parse_storage.py"), str(raw_log), run_id, test_id]
        subprocess.run(cmd)

    elif test_id in ("T052", "T053"):
        cmd = [sys.executable, str(PARSERS_DIR / "parse_postgres.py"), str(raw_log), run_id, test_id]
        subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="CloudMark Benchmark Orchestrator")
    subparsers = parser.add_subparsers(dest="command")

    init_p = subparsers.add_parser("init-run")
    init_p.add_argument("run_id")
    init_p.add_argument("provider")
    init_p.add_argument("region")
    init_p.add_argument("plan_name")
    init_p.add_argument("monthly_price_usd", type=float)
    init_p.add_argument("--promo", action="store_true", default=True)

    test_p = subparsers.add_parser("run-test")
    test_p.add_argument("run_id")
    test_p.add_argument("test_id")
    test_p.add_argument("host_ip")
    test_p.add_argument("--key-path", default=None)

    setup_p = subparsers.add_parser("setup-node")
    setup_p.add_argument("run_id")
    setup_p.add_argument("host_ip")
    setup_p.add_argument("--key-path", default=None)

    args = parser.parse_args()

    if args.command == "init-run":
        init_run(args.run_id, args.provider, args.region, args.plan_name, args.monthly_price_usd, args.promo)
    elif args.command == "setup-node":
        raw_log = RUNS_DIR / args.run_id / "raw" / "setup_node_raw.log"
        execute_remote(args.host_ip, SCRIPTS_DIR / "setup_node.sh", raw_log, args.key_path)
    elif args.command == "run-test":
        run_test(args.run_id, args.test_id, args.host_ip, args.key_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
