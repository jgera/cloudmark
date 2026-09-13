#!/usr/bin/env bash
# CBP-1.0 / T011 — CPU Multi-Thread Performance
# Standardized sysbench cpu test using all exposed vCPUs

set -euo pipefail

CORES=$(nproc)

echo "========================================="
echo "=== CBP-1.0 / T011: CPU MULTI-THREAD ($CORES CORES) ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo "Running sysbench CPU test (threads=$CORES, max-prime=20000, time=60s)..."
sysbench cpu --threads="$CORES" --cpu-max-prime=20000 --time=60 run

echo "========================================="
echo "=== T011 COMPLETE ==="
echo "========================================="
