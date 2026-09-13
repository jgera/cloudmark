#!/usr/bin/env bash
# CBP-1.0 / T010 — CPU Single-Thread Performance
# Standardized sysbench cpu test on 1 thread

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0 / T010: CPU SINGLE-THREAD ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo "Running sysbench CPU test (threads=1, max-prime=20000, time=60s)..."
sysbench cpu --threads=1 --cpu-max-prime=20000 --time=60 run

echo "========================================="
echo "=== T010 COMPLETE ==="
echo "========================================="
