#!/usr/bin/env bash
# CBP-1.0 / T020 — Memory Performance
# Standardized sysbench memory read and write benchmarks

set -euo pipefail

CORES=$(nproc)

echo "========================================="
echo "=== CBP-1.0 / T020: MEMORY PERFORMANCE ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo -e "\n--- Part 1: Memory Write Throughput (threads=$CORES) ---"
sysbench memory --threads="$CORES" --memory-block-size=1M --memory-total-size=64G --memory-oper=write run

echo -e "\n--- Part 2: Memory Read Throughput (threads=$CORES) ---"
sysbench memory --threads="$CORES" --memory-block-size=1M --memory-total-size=64G --memory-oper=read run

echo -e "\n========================================="
echo "=== T020 COMPLETE ==="
echo "========================================="
