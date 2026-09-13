#!/usr/bin/env bash
# CBP-1.0 / T052 — Mixed OLTP Concurrency Scaling (TPC-B like)
# Scales clients across: 1, 4, 8, 16, 32
# Includes periodic progress reporting (-P 5) to capture burst vs steady-state sustained TPS

set -euo pipefail

DURATION=180
CLIENTS_SERIES=(1 4 8 16 32)
CORES=$(nproc)

echo "========================================="
echo "=== CBP-1.0 / T052: MIXED OLTP SCALING (Scale 10) ==="
echo "=== Duration per test: ${DURATION}s, Interval: 5s ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

for c in "${CLIENTS_SERIES[@]}"; do
    # Assign threads as min(c, CORES)
    threads=$(( c < CORES ? c : CORES ))
    if [ "$threads" -lt 1 ]; then threads=1; fi

    echo -e "\n------------------------------------------------------------"
    echo "=== Running Mixed OLTP: Clients=$c, Threads=$threads, Duration=${DURATION}s ==="
    echo "------------------------------------------------------------"

    sudo -u postgres pgbench -c "$c" -j "$threads" -T "$DURATION" -P 5 -r cloudmark

    # Brief rest interval between concurrency steps to stabilize thermal/caching state
    sleep 5
done

echo -e "\n========================================="
echo "=== T052 COMPLETE ==="
echo "========================================="
