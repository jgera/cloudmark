# CloudMark Benchmark Report: Vultr Delhi High Performance vs. GCP Free Tier Baseline

- **Run ID**: `2026-09-13_vultr_delhi_hp-4c8g-intel_run01`
- **Protocol Version**: `CBP-1.0` (Frozen Standard)
- **Comparative Baseline**: `LEGACY-GCP-001` (`CBP-0` exploratory on GCP `e2-micro`)
- **Execution Date**: 2026-09-13 (11:32:43 UTC – 12:28:05 UTC)
- **Total Machine Uptime**: ~55 minutes
- **Cost Incurred**: $0.08 (fully absorbed by $250 promotional credit)
- **Lifecycle Status**: **Instance unconditionally terminated & destroyed** (0 active instances remaining)

---

## 1. Executive Summary

This run constitutes the first complete implementation of the **CloudMark Benchmark Protocol (CBP-1.0)** on production-grade cloud infrastructure: **Vultr Delhi NCR (`del`) High Performance Intel** (4 vCPU, 8 GB RAM, 180 GB NVMe).

### Key Takeaways:
1. **PostgreSQL OLTP Throughput**:
   - Vultr peaked at **8,279.7 sustained TPS** (at 8 concurrent clients), compared to GCP's peak of **191.0 sustained TPS** (**43.3x higher throughput**).
   - Single-client mixed OLTP was **2,360.4 sustained TPS** (0.42 ms latency) vs. GCP's **90.3 TPS** (11.0 ms latency) — a **26.1x increase** in raw per-thread transactional speed.
2. **Read-Only / SELECT Performance**:
   - Single-client read reached **20,778.7 TPS** (0.05 ms latency) vs. GCP's **746.6 TPS** (**27.8x higher**).
   - Peak SELECT-only throughput reached **86,816.8 TPS** at 4 clients with **0.04 ms (40 microseconds)** latency.
3. **Burst vs. Sustained Stability**:
   - Unlike GCP `e2-micro`, which degraded by **60–88%** once CPU credits exhausted, Vultr delivered a **1.00 burst/sustained ratio** and a coefficient of variation of only **0.34%** over a 300-second sustained CPU stress test.
4. **Geographic End-User Latency**:
   - Interactive RTT from North India averaged **11.0 ms** (min 9.0 ms, max 31.0 ms, 0.0% packet loss).
5. **Reliability**:
   - **0 transaction failures** across all executed test suites (>15 million transactions processed).

---

## 2. Infrastructure Profiles

| Field | GCP Legacy Baseline (`LEGACY-GCP-001`) | Vultr Delhi NCR (`CBP-1.0`) |
| :--- | :--- | :--- |
| **Instance Type** | `e2-micro` (Shared Core) | `vhp-4c-8gb-intel` (High Performance) |
| **Region / Datacenter** | `us-west1-a` (Oregon, USA) | `del` (Delhi NCR, India) |
| **vCPUs** | 2 vCPUs (fractional burstable) | 4 vCPUs (Intel Xeon Cascadelake) |
| **Memory (RAM)** | 1.0 GB | 7.75 GB (8.0 GB Swap) |
| **Storage Type** | 30 GB `pd-standard` (Persistent HDD/SSD) | 180 GB Local NVMe SSD |
| **Sequential Read/Write** | ~30–50 MB/s (estimated standard disk) | **3,307 MB/s Read / 2,924 MB/s Write** |
| **Random 4K IOPS** | ~300–500 IOPS | **218,000 Read / 219,000 Write IOPS** |
| **OS / Kernel** | Linux (exploratory) | Ubuntu 24.04.4 LTS / Kernel `6.8.0-138-generic` |
| **PostgreSQL Version** | 18 | 18.6 (PGDG official package) |
| **Working Set** | `pgbench -i -s 10` (~150 MB) | `pgbench -i -s 10` (~150 MB) |
| **List Price** | $0.00 (Always Free Tier) | $48.00 / month ($0.067 / hour) |

---

## 3. Head-to-Head PostgreSQL Comparison (Scale 10)

### 3.1 Mixed OLTP Concurrency Scaling (`T052` - TPC-B like, 180s each)

| Concurrency (Clients) | GCP Sustained TPS | GCP Latency | Vultr Sustained TPS | Vultr Latency | Speedup vs GCP | Failures |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 client** | 90.3 TPS | 11.0 ms | **2,360.4 TPS** | **0.42 ms** | **26.1x** | 0 |
| **4 clients** | 180.6 TPS | 22.0 ms | **5,976.0 TPS** | **0.67 ms** | **33.1x** | 0 |
| **8 clients** | 191.0 TPS | 43.0 ms | **8,279.7 TPS** | **0.97 ms** | **43.3x** | 0 |
| **16 clients** | 180.1 TPS | 93.5 ms | **7,788.8 TPS** | **2.05 ms** | **43.2x** | 0 |
| **32 clients** | *Not tested* | *N/A* | **6,933.0 TPS** | **4.62 ms** | — | 0 |

#### Concurrency Behavior Analysis:
* **Saturation Point**: Both platforms hit their mixed OLTP saturation ceiling at **8 clients**. On GCP, throughput stalled at ~191 TPS due to shared-core CPU starvation and storage queueing. On Vultr, throughput hit **8,279.7 TPS** at 8 clients with sub-millisecond latency (0.97 ms), before lock contention on the account branch accounts led to minor queueing at 16 and 32 clients.
* **Latency Profile**: At 8 clients, Vultr delivered transactions in **0.97 ms**, compared to GCP's **43.0 ms** — a **44x reduction in transaction queueing time**.

---

### 3.2 SELECT-Only Concurrency Scaling (`T053` - Read Ceiling, 120s each)

| Concurrency (Clients) | GCP Sustained TPS | GCP Latency | Vultr Sustained TPS | Vultr Latency | Speedup vs GCP | Failures |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 client** | 746.6 TPS | 1.35 ms | **20,778.7 TPS** | **0.05 ms** | **27.8x** | 0 |
| **4 clients** | *Not tested* | *N/A* | **86,816.8 TPS** | **0.04 ms** | — | 0 |
| **8 clients** | *Not tested* | *N/A* | **69,477.1 TPS** | **0.11 ms** | — | 0 |
| **16 clients** | *Not tested* | *N/A* | **63,268.7 TPS** | **0.25 ms** | — | 0 |
| **32 clients** | *Not tested* | *N/A* | **64,260.1 TPS** | **0.50 ms** | — | 0 |

* **Read Peak**: At 4 clients (matching the 4 physical vCPUs), PostgreSQL served **86,816 queries/sec** directly out of RAM at **40 microseconds** mean latency.

---

## 4. Compute, Memory & Storage Subsystem Deep Dive

### 4.1 CPU Performance (`T010`, `T011`, `T012`)
* **Single-Thread**: 472.04 events/sec (`sysbench cpu --cpu-max-prime=20000`).
* **Multi-Thread (4 Cores)**: 1,888.52 events/sec.
* **Scaling Efficiency**: **1.0002** (perfect linear 4-core scaling).
* **300-Second Sustained Stress**:
  - Burst EPS (0–30s): 1,887.2 eps
  - Sustained EPS (240–300s): 1,887.8 eps
  - **Burst/Sustained Ratio**: **1.00x** (zero observable degradation or throttling).
  - **Coefficient of Variation**: **0.34%** (extremely consistent hypervisor CPU allocation).

### 4.2 Memory Bandwidth (`T020`)
* **Sequential Write**: **47,792.01 MiB/s** (~47.8 GB/s) at 0.08 ms latency.
* **Sequential Read**: **91,955.48 MiB/s** (~92.0 GB/s) at 0.04 ms latency.

### 4.3 Storage Subsystem (`T031`, `T032`)
* **Sequential Throughput (1MB block, Direct I/O)**:
  - Read: **3,307 MB/s** (3.3 GB/s)
  - Write: **2,924 MB/s** (2.9 GB/s)
* **Random 4K IOPS (Queue Depth 32, 4 Jobs, Direct I/O)**:
  - Random Read: **218,000 IOPS** (850 MB/s, 0.58 ms latency)
  - Random Write: **219,000 IOPS** (855 MB/s, 0.58 ms latency)
  - Mixed 70/30: **215,700 IOPS** (843 MB/s total throughput)

---

## 5. Network & Geographic End-User Latency (`T041`)

* **Client Location**: North India
* **Target Datacenter**: Vultr Delhi NCR (`del`)
* **ICMP Packets**: 50 sent, 50 received (**0.0% packet loss**)
* **Round Trip Time (RTT)**:
  - Minimum: **9.0 ms**
  - Average: **11.0 ms**
  - Maximum: **31.0 ms**

This low latency (11 ms) confirms that local Indian cloud regions provide interactive round-trip times an order of magnitude faster than Western regions (e.g. GCP `us-west1` which typically observes 180–230 ms RTT from India).

---

## 6. Economic Efficiency (Cost per Transaction)

| Metric | GCP `e2-micro` | Vultr Delhi `vhp-4c-8gb-intel` |
| :--- | :--- | :--- |
| **Monthly List Price** | $0.00 (Free Tier) | $48.00 / month |
| **Peak Mixed Sustained TPS** | 191.0 TPS | 8,279.7 TPS |
| **Sustained Mixed TPS per $1/mo** | $\infty$ (Free) | **172.5 TPS / $** |
| **Peak SELECT TPS per $1/mo** | $\infty$ (Free) | **1,808.7 TPS / $** |
| **Actual Cash Paid for Test Run** | $0.00 | **$0.08** (covered by $250 credit) |

While free tiers offer infinite efficiency on paper ($/TPS), they hit a hard wall at ~190 transactions/second with high latency. For commercial production workloads (e.g. Django + PostgreSQL multi-tenant apps), the Vultr High Performance instance delivers **8,280 sustained OLTP transactions/second** for $48/month, providing abundant headroom.

---

## 7. Lifecycle & Resource Verification

* **Instance ID**: `56e328fe-db32-44ae-9ef5-93680d51c24a`
* **Teardown Action**: Automatically triggered via `vultr_ops` CLI inside the runner's `finally` handler.
* **Teardown Verification**: Confirmed via `vultr-cli instance list` (`TOTAL 0` instances active).
* **Billing Impact**: 0 active resources left running.
