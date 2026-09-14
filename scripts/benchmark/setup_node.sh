#!/usr/bin/env bash
# CBP-1.0 Node Baseline Setup Script
# Installs standard benchmark tools WITHOUT applying kernel or software tuning.
# Preserves out-of-the-box vendor defaults (Principle 3.2).

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0: NODE BASELINE SETUP ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a

APT_OPTS="-o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold"

echo -e "\n[0/4] Checking swap space for memory protection..."
if ! swapon --show | grep -q "/swapfile"; then
    echo "Creating 2GB swapfile..."
    fallocate -l 2G /swapfile 2>/dev/null || dd if=/dev/zero of=/swapfile bs=1M count=2048
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo "Swapfile created and activated."
fi

echo -e "\n[1/4] Updating package lists..."
apt-get update -y $APT_OPTS

echo -e "\n[2/4] Installing diagnostic and synthetic benchmark tools..."
apt-get install -y $APT_OPTS --no-install-recommends \
    sysstat \
    sysbench \
    fio \
    iperf3 \
    jq \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    procps \
    util-linux

echo -e "\n[3/4] Installing PostgreSQL 18 (or latest stable available in official repo)..."
# Configure PostgreSQL official repository if not present
if ! grep -q "apt.postgresql.org" /etc/apt/sources.list.d/* 2>/dev/null; then
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
    apt-get update -y $APT_OPTS
fi

# Attempt to install postgresql-18, falling back gracefully if repository is preparing 18
if apt-cache show postgresql-18 &>/dev/null; then
    apt-get install -y $APT_OPTS postgresql-18 postgresql-contrib-18
else
    echo "postgresql-18 package not directly found, installing default repo postgresql..."
    apt-get install -y $APT_OPTS postgresql postgresql-contrib
fi

systemctl enable postgresql
systemctl start postgresql

echo -e "\n[4/4] Verifying installed tool versions..."
echo "sysbench:   $(sysbench --version 2>&1 || echo 'N/A')"
echo "fio:        $(fio --version 2>&1 || echo 'N/A')"
echo "iperf3:     $(iperf3 --version 2>&1 | head -n 1 || echo 'N/A')"
echo "iostat:     $(iostat -V 2>&1 | head -n 1 || echo 'N/A')"
echo "PostgreSQL: $(psql --version 2>&1 || echo 'N/A')"
echo "pgbench:    $(pgbench --version 2>&1 || echo 'N/A')"

echo -e "\n========================================="
echo "=== NODE SETUP COMPLETE (NO TUNING APPLIED) ==="
echo "========================================="
