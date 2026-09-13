#!/usr/bin/env bash
# CBP-1.0 / T051 — Small Working-Set Initialization (Scale 10)
# Initializes pgbench database at scale 10 and captures table sizes

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0 / T051: POSTGRESQL INIT SCALE 10 ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo "Initializing pgbench database (scale 10) on database 'cloudmark'..."
sudo -u postgres pgbench -i -s 10 -I dtgvp cloudmark

echo -e "\n--- Database & Relation Sizes ---"
sudo -u postgres psql -d cloudmark -c "
SELECT 
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
    pg_size_pretty(pg_relation_size(relid)) AS data_size,
    pg_size_pretty(pg_indexes_size(relid)) AS index_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
"

echo -e "\n--- Total Database Size ---"
sudo -u postgres psql -d cloudmark -t -A -c "SELECT pg_size_pretty(pg_database_size('cloudmark'));"

echo -e "\n========================================="
echo "=== T051 COMPLETE ==="
echo "========================================="
