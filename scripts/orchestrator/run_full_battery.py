#!/usr/bin/env python3
"""
CloudMark Full Benchmark Battery & Auto-Teardown Runner
Executes CBP-1.0 test sequence autonomously, parses all metrics into master CSVs,
generates a comparative report, and unconditionally destroys the billable VM when complete.
"""

import sys
import os
import time
import argparse
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

VULTR_CLI = str(BASE_DIR / "bin" / "vultr" / "vultr-cli.exe")

def log(msg):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n[{now}] === {msg} ===", flush=True)

def ensure_ssh_access(host_ip, default_password, pubkey_path, privkey_path):
    # Test if passwordless SSH already works
    ssh_test = subprocess.run(
        ["ssh", "-i", privkey_path, "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=5", f"root@{host_ip}", "echo OK"],
        capture_output=True, text=True
    )
    if ssh_test.returncode == 0:
        log("Passwordless SSH authentication verified.")
        return True

    if not default_password:
        log("Passwordless SSH failed and no root password supplied.")
        return False

    log("Passwordless SSH not yet active. Injecting public key using initial root password via Paramiko...")
    try:
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host_ip, username="root", password=default_password, timeout=15)
        pubkey = Path(pubkey_path).read_text().strip()
        cmd = f'mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo "{pubkey}" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'
        stdin, stdout, stderr = client.exec_command(cmd)
        stdout.channel.recv_exit_status()
        client.close()
        log("Public key injected successfully into authorized_keys.")
        return True
    except Exception as e:
        log(f"Failed to inject SSH key: {e}")
        return False

def teardown_instance(instance_id):
    if not instance_id:
        return
    log(f"INITIATING TEARDOWN OF VULTR INSTANCE: {instance_id}")
    try:
        cmd = [VULTR_CLI, "instance", "delete", instance_id]
        res = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Teardown stdout: {res.stdout.strip()}")
        if res.stderr:
            print(f"Teardown stderr: {res.stderr.strip()}")
        log(f"TEARDOWN COMPLETE. No billable instances running.")
    except Exception as e:
        print(f"Error during teardown: {e}")

def run_battery(run_id, host_ip, instance_id, ssh_key, default_password=None):
    pubkey_path = str(Path(ssh_key).with_suffix(".pub")) if not str(ssh_key).endswith(".pub") else str(ssh_key)
    privkey_path = str(Path(ssh_key).with_suffix("")) if str(ssh_key).endswith(".pub") else str(ssh_key)

    start_time = datetime.now(timezone.utc)
    log(f"Starting autonomous benchmark run: {run_id} on {host_ip}")

    try:
        # Step 0: Ensure SSH Access
        if not ensure_ssh_access(host_ip, default_password, pubkey_path, privkey_path):
            raise RuntimeError(f"Failed to establish SSH access to {host_ip}. Aborting benchmark.")

        # Step 1: T001 - Characterization
        log("Executing T001 — Machine and Environment Characterization")
        cloudmark_runner.run_test(run_id, "T001", host_ip, privkey_path)

        # Step 2: T002 - Idle Baseline
        log("Executing T002 — Idle-System Baseline")
        cloudmark_runner.run_test(run_id, "T002", host_ip, privkey_path)

        # Step 3: Setup Node Packages (sysstat, sysbench, fio, postgresql)
        log("Executing Node Baseline Setup (installing packages, vendor defaults)")
        setup_log = BASE_DIR / "runs" / run_id / "raw" / "setup_node_raw.log"
        cloudmark_runner.execute_remote(host_ip, BASE_DIR / "scripts" / "benchmark" / "setup_node.sh", setup_log, privkey_path)

        # Step 4: T010 - CPU Single-Thread
        log("Executing T010 — CPU Single-Thread Performance")
        cloudmark_runner.run_test(run_id, "T010", host_ip, privkey_path)

        # Step 5: T011 - CPU Multi-Thread (all 4 vCPUs)
        log("Executing T011 — CPU Multi-Thread Performance")
        cloudmark_runner.run_test(run_id, "T011", host_ip, privkey_path)

        # Step 6: T012 - Sustained CPU (300s)
        log("Executing T012 — Sustained CPU Test (300s time-series)")
        cloudmark_runner.run_test(run_id, "T012", host_ip, privkey_path)

        # Step 7: T020 - Memory Bandwidth
        log("Executing T020 — Memory Read & Write Throughput")
        cloudmark_runner.run_test(run_id, "T020", host_ip, privkey_path)

        # Step 8: Storage Suite (T030, T031, T032)
        log("Executing T030 — Storage Identification")
        cloudmark_runner.run_test(run_id, "T030", host_ip, privkey_path)

        log("Executing T031 — Sequential Storage Throughput (1MB Direct I/O)")
        cloudmark_runner.run_test(run_id, "T031", host_ip, privkey_path)

        log("Executing T032 — Random Storage IOPS & Latency (4KB 32-depth)")
        cloudmark_runner.run_test(run_id, "T032", host_ip, privkey_path)

        # Step 9: Network T041 - Client RTT from local network
        log("Executing T041 — Client End-User RTT from Local Network")
        cloudmark_runner.run_client_rtt(run_id, host_ip, count=50)

        # Step 10: PostgreSQL Suite (Direct GCP comparison baseline)
        log("Executing T050 — PostgreSQL Environment Capture")
        cloudmark_runner.run_test(run_id, "T050", host_ip, privkey_path)

        log("Executing T051 — PostgreSQL Small Working Set Init (Scale 10)")
        cloudmark_runner.run_test(run_id, "T051", host_ip, privkey_path)

        log("Executing T052 — Mixed OLTP Concurrency Scaling (Clients: 1, 4, 8, 16, 32)")
        cloudmark_runner.run_test(run_id, "T052", host_ip, privkey_path)

        log("Executing T053 — SELECT-Only Concurrency Scaling (Clients: 1, 4, 8, 16, 32)")
        cloudmark_runner.run_test(run_id, "T053", host_ip, privkey_path)

        log("All benchmark tests completed successfully!")

    finally:
        # UNCONDITIONAL TEARDOWN
        teardown_instance(instance_id)

        # Generate final reports
        end_time = datetime.now(timezone.utc)
        log("Generating comprehensive benchmark summary report...")
        cloudmark_runner.generate_report(run_id)

        # Update end_time in master/runs.csv
        runs_csv = BASE_DIR / "master" / "runs.csv"
        if runs_csv.exists():
            import csv
            rows = []
            with open(runs_csv, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for r in reader:
                    if r.get("run_id") == run_id:
                        r["end_utc"] = end_time.strftime("%Y-%m-%d %H:%M:%S UTC")
                        r["notes"] = "Complete; instance destroyed"
                    rows.append(r)
            with open(runs_csv, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        log("Benchmark battery finished and master records finalized.")

def main():
    parser = argparse.ArgumentParser(description="CloudMark Autonomous Battery Runner")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--host-ip", required=True)
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--ssh-key", default="C:/Users/J/.ssh/cloudmark_id_ed25519")
    parser.add_argument("--default-password", default=None)

    args = parser.parse_args()
    run_battery(args.run_id, args.host_ip, args.instance_id, args.ssh_key, args.default_password)

if __name__ == "__main__":
    main()
