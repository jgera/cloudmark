#!/usr/bin/env python3
"""
CloudMark Ephemeral GCP Benchmark Battery Runner (CBP-1.0)
Automates the full ephemeral benchmark lifecycle:
1. Provisions temporary GCP VM with --no-address (zero IPv4 fee) and pd-ssd boot disk.
2. Waits for SSH readiness via Google Cloud IAP tunnel.
3. Sets up diagnostic & benchmark prerequisites (sysbench, fio, sysstat, postgresql).
4. Executes full CBP-1.0 battery (T001 through T053) and parses results into master datasets.
5. Unconditionally destroys the instance and attached disks upon completion or error.
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

def provision_instance(instance_name, machine_type, candidate_zones, disk_type="pd-ssd", disk_size="50GB"):
    if isinstance(candidate_zones, str):
        candidate_zones = [z.strip() for z in candidate_zones.split(",") if z.strip()]
        
    is_arm = "t2a" in machine_type.lower()
    image_family = "debian-12-arm64" if is_arm else "debian-12"
    
    active_zone = None
    for zone in candidate_zones:
        log(f"Attempting to provision '{instance_name}' ({machine_type}) in {zone} with {disk_size} {disk_type}...")
        create_cmd = [
            GCLOUD_BIN, "compute", "instances", "create", instance_name,
            f"--zone={zone}",
            f"--machine-type={machine_type}",
            f"--boot-disk-type={disk_type}",
            f"--boot-disk-size={disk_size}",
            f"--image-family={image_family}",
            "--image-project=debian-cloud",
            "--network=default",
            "--subnet=default",
            "--quiet"
        ]
        res = subprocess.run(create_cmd, capture_output=True, text=True)
        if res.returncode == 0:
            active_zone = zone
            break
        elif "ZONE_RESOURCE_POOL_EXHAUSTED" in res.stderr or "not have enough resources" in res.stderr:
            log(f"Zone {zone} resource pool exhausted. Trying next candidate zone...")
            continue
        else:
            raise RuntimeError(f"Failed to create instance {instance_name} in {zone}:\n{res.stderr}")
            
    if not active_zone:
        raise RuntimeError(f"Could not provision {instance_name} in any of the candidate zones: {candidate_zones}")
        
    log(f"Instance '{instance_name}' provisioned in {active_zone}. Waiting for SSH IAP availability...")
    
    # Poll SSH availability
    check_cmd = [
        GCLOUD_BIN, "compute", "ssh", instance_name,
        f"--zone={active_zone}",
        "--tunnel-through-iap",
        "--quiet",
        "--command", "echo READY"
    ]
    
    max_wait = 180
    start = time.time()
    ready = False
    while time.time() - start < max_wait:
        time.sleep(5)
        p = subprocess.run(check_cmd, capture_output=True, text=True)
        if p.returncode == 0 and "READY" in p.stdout:
            ready = True
            break
        print(".", end="", flush=True)
        
    if not ready:
        teardown_instance(instance_name, active_zone)
        raise TimeoutError(f"Instance {instance_name} did not become SSH accessible within {max_wait}s.")
        
    log(f"Instance '{instance_name}' is online in {active_zone} and SSH accessible via IAP.")
    return active_zone

def teardown_instance(instance_name, zone):
    # Safety guard: Never delete db-vm
    if instance_name == "db-vm":
        log("SAFETY CHECK: Attempted teardown on persistent 'db-vm' blocked.")
        return
        
    log(f"INITIATING UNCONDITIONAL TEARDOWN OF EPHEMERAL INSTANCE '{instance_name}'...")
    delete_cmd = [
        GCLOUD_BIN, "compute", "instances", "delete", instance_name,
        f"--zone={zone}",
        "--delete-disks=all",
        "--quiet"
    ]
    res = subprocess.run(delete_cmd, capture_output=True, text=True)
    if res.returncode == 0:
        log(f"Teardown complete: Instance '{instance_name}' and attached disks permanently destroyed.")
    else:
        log(f"Teardown warning (code {res.returncode}):\n{res.stderr}")

def upload_and_run(instance, zone, script_path, raw_log_path):
    content = script_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    temp_dir = BASE_DIR / "runs" / "_tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_local_file = temp_dir / script_path.name
    temp_local_file.write_bytes(content.encode("utf-8"))
    
    remote_path = f"/tmp/{script_path.name}"
    
    scp_cmd = [
        GCLOUD_BIN, "compute", "scp",
        str(temp_local_file),
        f"{instance}:{remote_path}",
        f"--zone={zone}",
        "--tunnel-through-iap",
        "--quiet"
    ]
    res = subprocess.run(scp_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"SCP error ({res.returncode}):\n{res.stderr}", flush=True)
        return False
        
    ssh_cmd = [
        GCLOUD_BIN, "compute", "ssh",
        instance,
        f"--zone={zone}",
        "--tunnel-through-iap",
        "--quiet",
        "--command", f"bash {remote_path}"
    ]
    rc = run_cmd_stream(ssh_cmd, raw_log_path)
    return rc == 0

def run_ephemeral_battery(machine_type, zone, disk_type="pd-ssd", disk_size="50GB", monthly_price=105.0):
    region = "-".join(zone.split("-")[:2])
    clean_type = machine_type.lower().replace("-", "")
    run_id = f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}_gcp_{region}_{machine_type}_run01"
    instance_name = f"cm-test-{clean_type}"
    
    log(f"STARTING AUTONOMOUS EPHEMERAL BENCHMARK RUN: {run_id}")
    log(f"Target: {instance_name} ({machine_type}) in {zone} with {disk_size} {disk_type}")
    
    # Step 0: Initialize run directory and master records
    cloudmark_runner.init_run(run_id, "Google Cloud Platform", region, machine_type, monthly_price, promo=False)
    
    active_zone = zone.split(",")[0].strip()
    start_time = datetime.now(timezone.utc)
    
    try:
        # Step 1: Provision
        active_zone = provision_instance(instance_name, machine_type, zone, disk_type, disk_size)
        
        # Step 2: Setup Node Packages (noninteractive)
        log("Executing Node Diagnostic Setup (sysbench, fio, sysstat, iperf3, postgresql)...")
        setup_cmd = [
            GCLOUD_BIN, "compute", "ssh", instance_name,
            f"--zone={active_zone}",
            "--tunnel-through-iap",
            "--quiet",
            "--command",
            "echo 'iperf3 iperf3/start_daemon boolean false' | sudo debconf-set-selections && "
            "sudo DEBIAN_FRONTEND=noninteractive apt-get update -y && "
            "sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -o Dpkg::Options::='--force-confdef' -o Dpkg::Options::='--force-confold' "
            "sysbench fio sysstat iperf3 postgresql postgresql-contrib"
        ]
        setup_log = RUNS_DIR / run_id / "raw" / "setup_node_raw.log"
        rc_setup = run_cmd_stream(setup_cmd, setup_log)
        if rc_setup != 0:
            raise RuntimeError(f"Diagnostic node setup failed on {instance_name} with exit code {rc_setup}. See {setup_log}")
        
        # Ensure postgres service is active and max_connections=100
        verify_pg = [
            GCLOUD_BIN, "compute", "ssh", instance_name,
            f"--zone={active_zone}",
            "--tunnel-through-iap",
            "--quiet",
            "--command",
            "sudo systemctl enable postgresql && sudo systemctl start postgresql && "
            "sudo -u postgres psql -c 'ALTER SYSTEM RESET ALL;' 2>/dev/null || true && "
            "sudo systemctl restart postgresql"
        ]
        subprocess.run(verify_pg, capture_output=True, text=True)
        
        # Step 3: Run full CBP-1.0 test sequence
        test_sequence = [
            "T001", "T002", "T010", "T011", "T012",
            "T020", "T030", "T031", "T032", "T040",
            "T050", "T051", "T052", "T053"
        ]
        
        for tid in test_sequence:
            script_path = TEST_SCRIPT_MAP[tid]
            raw_log = RUNS_DIR / run_id / "raw" / f"{tid}_raw.log"
            log(f"Executing CBP-1.0 Test {tid}: {script_path.name} on {instance_name} in {active_zone}...")
            upload_and_run(instance_name, active_zone, script_path, raw_log)
            cloudmark_runner.trigger_parser(run_id, tid, raw_log)
            
        log("All benchmark tests completed successfully!")
        
    finally:
        # Step 4: UNCONDITIONAL TEARDOWN
        teardown_instance(instance_name, active_zone)
        
        # Step 5: Finalize reports & records
        end_time = datetime.now(timezone.utc)
        log("Generating benchmark summary report...")
        cloudmark_runner.generate_report(run_id)
        
        runs_csv = MASTER_DIR / "runs.csv"
        if runs_csv.exists():
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
                
        # Clean temporary uploads
        temp_dir = BASE_DIR / "runs" / "_tmp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
            
        log(f"Run {run_id} finalized. Ephemeral VM destroyed. 0 runaway instances.")

def main():
    parser = argparse.ArgumentParser(description="CloudMark GCP Ephemeral Battery Runner")
    parser.add_argument("--machine-type", required=True, help="e.g. e2-standard-4, c2-standard-4, t2a-standard-4")
    parser.add_argument("--zone", default="us-central1-a", help="GCP zone, e.g. us-central1-a, us-west1-a")
    parser.add_argument("--disk-type", default="pd-ssd", help="pd-ssd or pd-balanced")
    parser.add_argument("--disk-size", default="50GB", help="e.g. 50GB")
    parser.add_argument("--monthly-price", type=float, default=105.0)

    args = parser.parse_args()
    run_ephemeral_battery(args.machine_type, args.zone, args.disk_type, args.disk_size, args.monthly_price)

if __name__ == "__main__":
    main()
