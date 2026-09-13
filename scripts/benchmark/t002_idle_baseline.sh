#!/usr/bin/env bash
# CBP-1.0 / T002 — Idle-System Baseline
# CloudMark Benchmark Suite

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0 / T002: IDLE-SYSTEM BASELINE ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo -e "\n--- UPTIME & LOAD AVERAGE ---"
uptime

echo -e "\n--- MEMORY & SWAP (free -h) ---"
free -h

echo -e "\n--- VMSTAT SAMPLING (1s x 10 intervals) ---"
vmstat 1 10

echo -e "\n--- IOSTAT SAMPLING (1s x 10 intervals) ---"
if command -v iostat &>/dev/null; then
    iostat -xz 1 10
else
    echo "iostat not found, installing sysstat may be required"
fi

echo -e "\n========================================="
echo "=== T002 IDLE BASELINE COMPLETE ==="
echo "========================================="
