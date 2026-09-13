#!/usr/bin/env bash
# CBP-1.0 / T040 — Server Network Throughput
# Benchmark network throughput independent of user client geography

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0 / T040: SERVER NETWORK THROUGHPUT ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

# Primary test: iperf3 against standard public servers if reachable
IPERF_SERVERS=("speedtest.serverius.net" "bouygues.iperf.fr")

TESTED=false
for srv in "${IPERF_SERVERS[@]}"; do
    echo "Attempting iperf3 to $srv (port 5201)..."
    if iperf3 -c "$srv" -t 10 -P 4 2>&1; then
        TESTED=true
        break
    else
        echo "Server $srv was busy or unreachable, trying next..."
    fi
done

if [ "$TESTED" = false ]; then
    echo "Public iperf3 servers busy. Performing fallback network speed test via curl download..."
    curl -o /dev/null -s -w 'Speed Download: %{speed_download} bytes/sec (%{size_download} bytes in %{time_total}s)\n' https://proof.ovh.net/files/100Mb.dat || true
fi

echo -e "\n========================================="
echo "=== T040 COMPLETE ==="
echo "========================================="
