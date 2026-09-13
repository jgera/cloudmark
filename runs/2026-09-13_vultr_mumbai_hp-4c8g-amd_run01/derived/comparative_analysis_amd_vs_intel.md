# CloudMark Architecture Benchmark: Intel Xeon Cascadelake vs. AMD EPYC-Rome

- **Run ID**: `2026-09-13_vultr_mumbai_hp-4c8g-amd_run01`
- **Comparative Baseline**: `2026-09-13_vultr_delhi_hp-4c8g-intel_run01` (Intel Xeon Cascadelake)
- **Historical Reference**: `LEGACY-GCP-001` (GCP `e2-micro`)
- **Protocol Version**: `CBP-1.0`
- **Instance Plan**: `vhp-4c-8gb-amd` ($48.00 / month, identical price tier to Intel)
- **Execution Window**: 2026-09-13 (18:39:55 UTC – 19:22:46 UTC, ~43 mins total)
- **Lifecycle Status**: **Instance unconditionally terminated & destroyed** (0 active instances remaining)
- **Net Billing Incurred**: ~$0.23 (covered by promotional credit)

---

## 1. Executive Summary: The "Synthetic vs. Application" Paradox

This run delivers one of the most critical engineering and research insights of the CloudMark project: **synthetic compute benchmarks do not predict database OLTP performance.**

| Benchmark Dimension | Intel Xeon Cascadelake (Delhi) | AMD EPYC-Rome (Mumbai) | Winner / Delta |
| :--- | :--- | :--- | :--- |
| **Synthetic CPU (Single-Core `T010`)** | 472.0 events/sec | **1,348.1 events/sec** | **AMD +186% (2.86x faster)** |
| **Synthetic CPU (4 vCPUs `T011`)** | 1,888.5 events/sec | **5,412.3 events/sec** | **AMD +187% (2.87x faster)** |
| **Sustained Stability (`T012` CV%)** | **0.34% CV** (1.00x burst/sust) | 0.64% CV (1.01x burst/sust) | **Tie** (Both zero throttling) |
| **Memory Write Bandwidth (`T020`)** | **47,792 MiB/s** (0.08 ms) | 18,634 MiB/s (0.20 ms) | **Intel +156% (2.56x faster)** |
| **Memory Read Bandwidth (`T020`)** | 91,955 MiB/s (0.04 ms) | **156,756 MiB/s** (0.02 ms) | **AMD +70% (1.70x faster)** |
| **Storage 4K Random Write IOPS (`T032`)** | **219,000 IOPS** (0.58 ms) | 124,000 IOPS (1.02 ms) | **Intel +77% (1.77x faster)** |
| **PostgreSQL Mixed OLTP Peak (`T052`)** | **8,279.7 sustained TPS** | 4,561.9 sustained TPS | **Intel +81% (1.81x faster)** |
| **PostgreSQL SELECT-Only Peak (`T053`)** | **86,816.8 sustained TPS** | 40,771.8 sustained TPS | **Intel +113% (2.13x faster)** |
| **Client RTT from North India (`T041`)** | **11.0 ms avg** (31 ms max) | 42.0 ms avg (108 ms max) | **Delhi +282% lower latency** |

### Why Did AMD Dominate Synthetic CPU but Lose in PostgreSQL?
1. **Transaction Durability & NVMe Latency**: In PostgreSQL OLTP (`pgbench` TPC-B like), every transaction requires a WAL (write-ahead log) flush and synchronous commit (`fsync`). The Intel node in Delhi achieved **0.58 ms 4K random write latency** (219k IOPS), whereas the Mumbai AMD host exhibited **1.02 ms latency** (124k IOPS) — almost double the disk commit latency.
2. **Memory Write Bottlenecks**: OLTP workloads continuously update dirty buffers in PostgreSQL `shared_buffers`. The Intel instance demonstrated **47.8 GB/s** memory write speed vs AMD's **18.6 GB/s**, giving Intel an advantage when mutating in-memory page buffers.
3. **Instruction Set & IPC Behavior**: Sysbench CPU calculates primes in tight mathematical loops where AMD EPYC-Rome's execution pipeline excels. PostgreSQL, however, is branch-heavy, pointer-chasing, cache-locality sensitive, and heavily dependent on memory bus commit latencies.

---

## 2. Head-to-Head PostgreSQL Comparison (Scale 10)

### 2.1 Mixed OLTP Concurrency Scaling (`T052` - 180s per tier)

| Clients | GCP `e2-micro` (Free) | Intel Xeon Delhi ($48) | AMD EPYC Mumbai ($48) | Intel vs AMD Delta | Failures |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 90.3 TPS (11.0 ms) | **2,360.4 TPS** (0.42 ms) | 1,213.3 TPS (0.83 ms) | Intel **+94.5%** | 0 |
| **4** | 180.6 TPS (22.0 ms) | **5,976.0 TPS** (0.67 ms) | 3,136.1 TPS (1.28 ms) | Intel **+90.6%** | 0 |
| **8** | 191.0 TPS (43.0 ms) | **8,279.7 TPS** (0.97 ms) | 4,561.9 TPS (1.75 ms) | Intel **+81.5%** | 0 |
| **16** | 180.1 TPS (93.5 ms) | **7,788.8 TPS** (2.05 ms) | 4,199.1 TPS (3.81 ms) | Intel **+85.5%** | 0 |
| **32** | *Not tested* | **6,933.0 TPS** (4.62 ms) | 3,636.8 TPS (8.82 ms) | Intel **+90.6%** | 0 |

* **Saturation Ceiling**: Both x86 architectures reach their maximum OLTP saturation at **8 concurrent clients**.
* **Latency Profile**: At peak throughput (8 clients), Intel completes transactions in **0.97 ms** compared to AMD's **1.75 ms** and GCP's **43.0 ms**.

---

### 2.2 SELECT-Only Concurrency Scaling (`T053` - 120s per tier)

| Clients | GCP `e2-micro` (Free) | Intel Xeon Delhi ($48) | AMD EPYC Mumbai ($48) | Intel vs AMD Delta | Failures |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 746.6 TPS (1.35 ms) | **20,778.7 TPS** (0.05 ms) | 10,223.5 TPS (0.10 ms) | Intel **+103%** | 0 |
| **4** | *Not tested* | **86,816.8 TPS** (0.04 ms) | 40,771.8 TPS (0.09 ms) | Intel **+113%** | 0 |
| **8** | *Not tested* | **69,477.1 TPS** (0.11 ms) | 36,401.1 TPS (0.22 ms) | Intel **+91%** | 0 |
| **16** | *Not tested* | **63,268.7 TPS** (0.25 ms) | 39,028.9 TPS (0.41 ms) | Intel **+62%** | 0 |
| **32** | *Not tested* | **64,260.1 TPS** (0.50 ms) | 38,912.3 TPS (0.82 ms) | Intel **+65%** | 0 |

---

## 3. Storage & Network Subsystem Comparison

### 3.1 Storage Performance (`T031`, `T032`)
* **Sequential Read (1MB Direct I/O)**:
  - Intel (Delhi): 3,307 MB/s
  - AMD (Mumbai): **6,460 MB/s** (AMD's storage controller achieved 6.4 GB/s sequential read)
* **Sequential Write (1MB Direct I/O)**:
  - Intel (Delhi): **2,924 MB/s**
  - AMD (Mumbai): 2,878 MB/s
* **Random 4K IOPS (Queue Depth 32, 4 Jobs)**:
  - Intel (Delhi): **218k Read / 219k Write IOPS** (0.58 ms latency)
  - AMD (Mumbai): **127k Read / 124k Write IOPS** (1.02 ms latency)

### 3.2 Geographic Interactive Latency (`T041`)
* **To Delhi (`del`)**:
  - Min: 9 ms, **Avg: 11 ms**, Max: 31 ms (0% packet loss)
* **To Mumbai (`bom`)**:
  - Min: 32 ms, **Avg: 42 ms**, Max: 108 ms (2% packet loss)

For interactive North Indian web traffic, routing through Delhi provides **almost 4x lower latency** than Mumbai.

---

## 4. Economic Value: Real Transactions per Dollar

| Architecture | Monthly Cost | Peak Mixed OLTP | Peak SELECT Read | Mixed TPS / $1/mo | SELECT TPS / $1/mo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GCP `e2-micro`** | $0.00 | 191 TPS | 747 TPS | $\infty$ | $\infty$ |
| **Vultr AMD EPYC (Mumbai)** | $48.00 | 4,562 TPS | 40,772 TPS | **95.0 TPS / $** | **849.4 TPS / $** |
| **Vultr Intel Xeon (Delhi)** | $48.00 | 8,280 TPS | 86,817 TPS | **172.5 TPS / $** | **1,808.7 TPS / $** |

At the identical $48/month price point, the **Intel Xeon High Performance plan in Delhi delivers 1.8x to 2.1x better real-world database economic value** than the AMD EPYC plan in Mumbai.

---

## 5. Teardown Confirmation

* **Instance ID**: `ed0f5d95-aa2c-4f16-b330-f3f098a295d4`
* **Teardown Command**: Executed via automated handler at 19:22:45 UTC.
* **Verification**: `vultr-cli instance list` reports `TOTAL 0`.
* **Billing Impact**: 0 running machines remaining.
