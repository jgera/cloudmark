#!/usr/bin/env bash
# CBP-1.0 / T012 — Sustained CPU Test
# 300s duration with 5s interval reports to expose throttling / burst curves

set -euo pipefail

CORES=$(nproc)

echo "========================================="
echo "=== CBP-1.0 / T012: CPU SUSTAINED TEST (300s) ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo "Running 300s sustained sysbench CPU test with 5s progress reporting..."
sysbench cpu --threads="$CORES" --cpu-max-prime=20000 --time=300 --report-interval=5 run

echo "========================================="
echo "=== T012 COMPLETE ==="
echo "========================================="
