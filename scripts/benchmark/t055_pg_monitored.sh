#!/usr/bin/env bash
# CBP-1.0 / T055 — PostgreSQL + System Telemetry Monitoring
# Runs pgbench saturation test while collecting synchronized vmstat and iostat metrics

set -euo pipefail

DURATION=120
CLIENTS=16
CORES=$(nproc)

echo "========================================="
echo "=== CBP-1.0 / T055: MONITORED POSTGRESQL SATURATION ==="
echo "=== Clients: $CLIENTS, Duration: ${DURATION}s ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

LOG_DIR="/var/tmp/cloudmark_telemetry"
mkdir -p "$LOG_DIR"
VMSTAT_LOG="$LOG_DIR/vmstat.log"
IOSTAT_LOG="$LOG_DIR/iostat.log"

echo "Starting background vmstat & iostat collectors..."
vmstat 1 "$DURATION" > "$VMSTAT_LOG" 2>&1 &
VMSTAT_PID=$!

iostat -xz 1 "$DURATION" > "$IOSTAT_LOG" 2>&1 &
IOSTAT_PID=$!

echo "Executing pgbench workload (clients=$CLIENTS, threads=$CORES)..."
sudo -u postgres pgbench -c "$CLIENTS" -j "$CORES" -T "$DURATION" -P 5 -r cloudmark || true

echo "Waiting for background collectors..."
wait "$VMSTAT_PID" || true
wait "$IOSTAT_PID" || true

echo -e "\n--- System Telemetry Summary (Final 10 lines of vmstat) ---"
tail -n 10 "$VMSTAT_LOG"

echo -e "\n--- System Telemetry Summary (Final 15 lines of iostat) ---"
tail -n 15 "$IOSTAT_LOG"

echo -e "\n========================================="
echo "=== T055 COMPLETE ==="
echo "========================================="
