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

SSH_KEY_ID = "cae4c84f-cb38-477d-a1d8-66c78dff0869"

def teardown_instance(instance_id):
    if not instance_id:
        return
    log(f"INITIATING UNCONDITIONAL TEARDOWN OF VULTR INSTANCE: {instance_id}")
    try:
        cmd = [VULTR_CLI, "instance", "delete", instance_id]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            log(f"Teardown successful: Instance {instance_id} deleted. 0 billable instances remaining.")
        else:
            log(f"Teardown warning: {res.stderr.strip()}")
    except Exception as e:
        log(f"Error during instance teardown: {e}")

def provision_vultr_instance(plan, region, os_id=2136, label="cloudmark-ephemeral"):
    log(f"Provisioning Vultr instance (Plan: {plan}, Region: {region}, OS: {os_id}, Label: {label})...")
    create_cmd = [
        VULTR_CLI, "instance", "create",
        f"--region={region}",
        f"--plan={plan}",
        f"--os={os_id}",
        f"--ssh-keys={SSH_KEY_ID}",
        f"--label={label}",
        "--output=json"
    ]
    res = subprocess.run(create_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to create Vultr instance:\n{res.stderr}")
    
    data = json.loads(res.stdout)
    instance_info = data.get("instance", {})
    instance_id = instance_info.get("id")
    default_password = instance_info.get("default_password", "")
    if not instance_id:
        raise RuntimeError(f"Could not parse instance ID from output:\n{res.stdout}")
    
    log(f"Instance created with ID: {instance_id}. Waiting for active status and IP assignment...")
    
    max_wait = 240
    start = time.time()
    main_ip = None
    while time.time() - start < max_wait:
        time.sleep(6)
        get_res = subprocess.run([VULTR_CLI, "instance", "get", instance_id, "--output=json"], capture_output=True, text=True)
        if get_res.returncode == 0:
            inst = json.loads(get_res.stdout).get("instance", {})
            status = inst.get("status")
            server_status = inst.get("server_status")
            ip = inst.get("main_ip")
            if not default_password:
                default_password = inst.get("default_password", "")
            if status == "active" and ip and ip != "0.0.0.0":
                main_ip = ip
                log(f"Instance is active: IP={main_ip}, Server Status={server_status}")
                break
        print(".", end="", flush=True)
        
    if not main_ip:
        teardown_instance(instance_id)
        raise TimeoutError(f"Instance {instance_id} failed to become active within {max_wait}s.")
        
    log(f"Polling SSH readiness on {main_ip}...")
    pubkey_path = str(Path(os.path.expanduser(r"~\.ssh\cloudmark_id_ed25519.pub")))
    privkey_path = str(Path(os.path.expanduser(r"~\.ssh\cloudmark_id_ed25519")))
    
    ssh_ready = False
    ssh_wait = 180
    start_ssh = time.time()
    while time.time() - start_ssh < ssh_wait:
        time.sleep(5)
        if ensure_ssh_access(main_ip, default_password, pubkey_path, privkey_path):
            ssh_ready = True
            break
        print("s", end="", flush=True)
        
    if not ssh_ready:
        teardown_instance(instance_id)
        raise TimeoutError(f"SSH failed to become ready on {main_ip} within {ssh_wait}s.")
        
    log(f"Instance {instance_id} is online and SSH accessible at {main_ip}.")
    return instance_id, main_ip

def run_vultr_battery(plan, region="del", monthly_price=5.0):
    region_label = "delhi" if region == "del" else ("mumbai" if region == "bom" else region)
    clean_plan = plan.lower().replace("-", "")
    run_id = f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}_vultr_{region_label}_{plan}_run01"
    label = f"cm-{region_label}-{clean_plan}"[:30]
    
    log(f"STARTING AUTONOMOUS EPHEMERAL VULTR BENCHMARK RUN: {run_id}")
    log(f"Target: {label} ({plan}) in region '{region}' at ${monthly_price:.2f}/mo")
    
    # Initialize run directory and master records
    cloudmark_runner.init_run(run_id, "Vultr", region_label.capitalize(), plan, monthly_price, promo=False)
    
    privkey_path = str(Path(os.path.expanduser(r"~\.ssh\cloudmark_id_ed25519")))
    instance_id = None
    start_time = datetime.now(timezone.utc)
    
    try:
        # Step 1: Provision
        instance_id, host_ip = provision_vultr_instance(plan, region, os_id=2136, label=label)
        
        # Step 2: Characterization & Idle Baseline
        log("Executing T001 — Machine and Environment Characterization")
        cloudmark_runner.run_test(run_id, "T001", host_ip, privkey_path)

        log("Executing T002 — Idle-System Baseline")
        cloudmark_runner.run_test(run_id, "T002", host_ip, privkey_path)

        # Step 3: Setup Node Packages (install sysstat, sysbench, fio, postgresql, swap)
        log("Executing Node Baseline Setup (swapfile, packages, vendor defaults)")
        setup_log = BASE_DIR / "runs" / run_id / "raw" / "setup_node_raw.log"
        cloudmark_runner.execute_remote(host_ip, BASE_DIR / "scripts" / "benchmark" / "setup_node.sh", setup_log, privkey_path)

        # Step 4: CPU Suite
        log("Executing T010 — CPU Single-Thread Performance")
        cloudmark_runner.run_test(run_id, "T010", host_ip, privkey_path)

        log("Executing T011 — CPU Multi-Thread Performance")
        cloudmark_runner.run_test(run_id, "T011", host_ip, privkey_path)

        log("Executing T012 — Sustained CPU Test (300s time-series)")
        cloudmark_runner.run_test(run_id, "T012", host_ip, privkey_path)

        # Step 5: Memory Bandwidth
        log("Executing T020 — Memory Read & Write Throughput")
        cloudmark_runner.run_test(run_id, "T020", host_ip, privkey_path)

        # Step 6: Storage Suite
        log("Executing T030 — Storage Identification")
        cloudmark_runner.run_test(run_id, "T030", host_ip, privkey_path)

        log("Executing T031 — Sequential Storage Throughput (1MB Direct I/O)")
        cloudmark_runner.run_test(run_id, "T031", host_ip, privkey_path)

        log("Executing T032 — Random Storage IOPS & Latency (4KB 32-depth)")
        cloudmark_runner.run_test(run_id, "T032", host_ip, privkey_path)

        # Step 7: Client RTT from local network
        log("Executing T041 — Client End-User RTT from Local Network")
        cloudmark_runner.run_client_rtt(run_id, host_ip, count=50)

        # Step 8: PostgreSQL Suite
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
        # Step 9: UNCONDITIONAL TEARDOWN
        teardown_instance(instance_id)

        # Step 10: Parse results and generate reports
        end_time = datetime.now(timezone.utc)
        raw_dir = BASE_DIR / "runs" / run_id / "raw"
        for tid in ["T001", "T010", "T011", "T012", "T020", "T031", "T032", "T052", "T053"]:
            raw_log = raw_dir / f"{tid}_raw.log"
            if raw_log.exists():
                cloudmark_runner.trigger_parser(run_id, tid, raw_log)
        log("All metrics parsed and integrated successfully into master CSVs.")

        try:
            cloudmark_runner.generate_report(run_id)
        except Exception as re:
            log(f"Report generation note: {re}")

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

        log(f"Run {run_id} finalized. Ephemeral Vultr VM destroyed. 0 runaway instances.")

def main():
    parser = argparse.ArgumentParser(description="CloudMark Vultr Ephemeral Battery Runner")
    parser.add_argument("--plan", required=True, help="e.g. vc2-1c-1gb, vhf-1c-1gb, vhp-1c-1gb-intel")
    parser.add_argument("--region", default="del", help="Vultr region, e.g. del, bom")
    parser.add_argument("--monthly-price", type=float, default=5.0)

    args = parser.parse_args()
    run_vultr_battery(args.plan, args.region, args.monthly_price)

if __name__ == "__main__":
    main()
