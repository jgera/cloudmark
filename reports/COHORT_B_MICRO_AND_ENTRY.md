# CloudMark CBP-1.0 Cohort B: Micro & Entry Tier Report ($0 to $10/month)

A rigorous analysis of ultra-low-cost virtual machines evaluating compute throttling, storage throughput, and database TPS:
- **GCP `e2-micro` (US)** ($0.00/mo) — Always Free Baseline
- **GCP `e2-micro` (Delhi)** ($7.30/mo) — Shared Core in India
- **Vultr `vc2-1c-1gb` (Delhi)** ($5.00/mo) — Regular Cloud Compute in Delhi
- **Vultr `vc2-1c-1gb` (Mumbai)** ($5.00/mo) — Regular Cloud Compute in Mumbai
- **Vultr `vc2-1c-2gb` (Delhi)** ($10.00/mo) — 2GB RAM Step-Up in Delhi
- **Vultr `vc2-1c-1gb` (Singapore)** ($5.00/mo) — Southeast Asia Regional Hub

---

## 4. Cohort B: Micro & Entry Tier Deep-Dive ($0 – $10.00/month)

### 4.1 Sustained CPU Throttling Curves (T010, T011, T012 — 300s Continuous Load)
| Machine | Architecture & Cores | Single Peak (eps) | 300s Burst eps (0-30s) | 300s Steady eps (240-300s) | Drop Ratio | Throttling Volatility (CV) | Throttling Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **GCP `e2-micro` (US)** | Intel Xeon (0.25 core shared) | 472.0 | 341.2 | 144.1 | 2.37x drop | 83.5% | **Severe Throttling** |
| **GCP `e2-micro` (Delhi)** | AMD EPYC (0.25 core shared) | 790.2 | 332.9 | 186.3 | 1.79x drop | 51.5% | **Severe Throttling** |
| **Vultr `vc2-1c-1gb` (Mumbai)** | Intel Cascadelake (1 core) | 454.6 | 454.6 | 455.3 | **0.97x** | **1.52%** | **100% Sustained (Rock Flat)** |
| **Vultr `vc2-1c-1gb` (Delhi)** | Intel Cascadelake (1 core) | 440.8 | 442.8 | 436.0 | **1.02x** | **2.10%** | **100% Sustained (No Throttling)** |
| **Vultr `vc2-1c-2gb` (Delhi)** | Intel Cascadelake (1 core) | 449.9 | 450.8 | 450.8 | **1.00x** | **0.96%** | **100% Sustained (Rock Flat)** |
| **Vultr `vc2-1c-1gb` (SGP)** | Intel Broadwell (1 core) | 303.5 | 305.7 | 300.3 | **1.02x** | **1.58%** | **100% Sustained (No Throttling)** |

### 4.2 PostgreSQL Sustained Mixed OLTP Throughput (T052 — Scale 10)
| Concurrency Tier | GCP `e2-micro` (US, $0) | GCP `e2-micro` (Delhi, $7.30) | Vultr $5 (SGP) | Vultr $5 (Delhi) | Vultr $5 (Mumbai) | Vultr $10 (Delhi) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Client** | 91.2 TPS (10.95 ms) | 94.1 TPS (10.63 ms) | 825.3 TPS (1.21 ms) | 2,071.1 TPS (0.48 ms) | **2,338.6 TPS (0.43 ms)** | 2,180.4 TPS (0.46 ms) |
| **4 Clients** | 175.5 TPS (22.78 ms) | 194.3 TPS (20.59 ms) | 1,164.5 TPS (3.44 ms) | 1,957.5 TPS (2.06 ms) | **2,322.7 TPS (1.73 ms)** | 2,185.1 TPS (1.84 ms) |
| **8 Clients** | 181.4 TPS (44.67 ms) | 236.2 TPS (33.95 ms) | 1,164.4 TPS (6.88 ms) | 1,821.2 TPS (4.40 ms) | 2,065.9 TPS (3.90 ms) | **2,127.9 TPS (3.76 ms)** |
| **16 Clients**| 179.3 TPS (89.53 ms) | 250.5 TPS (63.99 ms) | 982.9 TPS (16.32 ms) | 1,539.0 TPS (10.43 ms)| **2,004.9 TPS (7.99 ms)** | 1,813.0 TPS (8.83 ms) |
| **32 Clients**| 151.5 TPS (223.43 ms)| 215.8 TPS (145.05 ms)| 897.3 TPS (35.69 ms) | 1,217.1 TPS (26.38 ms)| **1,613.7 TPS (19.86 ms)**| 1,461.7 TPS (21.92 ms)|

### 4.3 PostgreSQL Sustained SELECT-Only Scaling (T053 — Scale 10)
| Concurrency Tier | GCP `e2-micro` (US, $0) | GCP `e2-micro` (Delhi, $7.30) | Vultr $5 (SGP) | Vultr $5 (Delhi) | Vultr $5 (Mumbai) | Vultr $10 (Delhi) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Client** | 789.7 TPS (1.24 ms) | 971.8 TPS (1.01 ms) | 9,224.7 TPS (0.11 ms) | **19,475.2 TPS (0.05 ms)** | 18,601.7 TPS (0.05 ms) | **21,048.0 TPS (0.05 ms)** |
| **4 Clients** | 1,717.0 TPS (2.29 ms) | 2,325.4 TPS (1.68 ms) | 8,076.3 TPS (0.50 ms) | 15,287.2 TPS (0.26 ms) | 15,510.9 TPS (0.26 ms) | **16,933.3 TPS (0.24 ms)** |
| **8 Clients** | 1,650.1 TPS (4.80 ms) | 2,248.5 TPS (3.52 ms) | 8,120.8 TPS (0.98 ms) | 14,442.4 TPS (0.55 ms) | 14,673.0 TPS (0.54 ms) | **15,547.8 TPS (0.51 ms)** |
| **16 Clients**| 1,487.6 TPS (11.61 ms)| 2,290.7 TPS (6.95 ms) | 7,418.1 TPS (2.16 ms) | 13,695.9 TPS (1.17 ms) | 13,574.0 TPS (1.18 ms) | **15,067.2 TPS (1.06 ms)** |
| **32 Clients**| 1,439.4 TPS (22.09 ms)| 2,120.5 TPS (15.17 ms)| 6,317.1 TPS (5.08 ms) | 9,308.0 TPS (3.44 ms) | 9,914.9 TPS (3.25 ms) | **11,508.8 TPS (2.85 ms)** |

---

## 5. Regional Analysis: The India Domestic Triangle (Delhi vs. Mumbai vs. Singapore)

Evaluating identical **$5.00/mo plans (`vc2-1c-1gb`)** across Vultr's South Asian and Southeast Asian locations reveals profound hardware generational differences:

| Benchmark Dimension | Vultr Delhi (`del`) | Vultr Mumbai (`bom`) | Vultr Singapore (`sgp`) | Regional Disparity / Verdict |
| :--- | :---: | :---: | :---: | :--- |
| **CPU Architecture** | Intel Xeon Cascadelake | Intel Xeon Cascadelake | Intel Xeon Broadwell | Delhi & Mumbai are 2 generations newer than Singapore |
| **Client Ping from India** | **10.5 ms min (41 ms avg)** | **32.0 ms min (37 ms avg)** | 72.0 ms min (77 ms avg) | **Domestic India ping is 2.1x–7x lower** than Singapore |
| **Sequential Storage Read** | **3,178 MB/s** | 2,604 MB/s | 352 MB/s | **India host disks are 7.4x–9.0x faster** than Singapore SAN |
| **Sequential Storage Write**| **2,678 MB/s** | 1,261 MB/s | 308 MB/s | Delhi leads sequential write throughput |
| **Random 4K Read IOPS** | 144,000 IOPS | **178,000 IOPS** | 56,000 IOPS | Mumbai leads raw read IOPS (+23.6% over Delhi) |
| **Random 4K Write IOPS**| 102,000 IOPS | **194,000 IOPS** | 37,000 IOPS | **Mumbai write IOPS is +90.2% higher** than Delhi |
| **Peak Sustained Mixed OLTP**| 2,071.1 TPS (0.48 ms) | **2,338.6 TPS (0.43 ms)** | 1,164.5 TPS (3.44 ms) | **Mumbai is 13% faster than Delhi and 2.0x faster than SGP** |
| **32-Client Sustained OLTP** | 1,217.1 TPS (26.38 ms) | **1,613.7 TPS (19.86 ms)** | 897.3 TPS (35.69 ms) | Mumbai sustains +32.6% higher throughput under heavy concurrency |
| **Peak SELECT-Only Read** | **19,475.2 TPS** | 18,601.7 TPS | 9,224.7 TPS | Delhi & Mumbai deliver double the read capability of Singapore |

> [!IMPORTANT]
> **India Domestic Triangle Takeaways:**
> 1. **Mumbai (`bom`) is the Highest Performing $5.00 Node:** Thanks to phenomenal random write IOPS (194k IOPS) and ultra-consistent low-latency disk arrays, Mumbai achieved **2,338.6 sustained OLTP TPS**, holding up better under 32 concurrent clients (1,614 TPS vs Delhi's 1,217 TPS).
> 2. **Delhi (`del`) is the Lowest Latency Node for North India:** If client network round-trip time is paramount, Delhi offers single-digit pings (10.5 ms min) and near-identical CPU performance (2,071 OLTP TPS).
> 3. **Singapore (`sgp`) Suffers from Legacy Hardware:** Vultr Singapore's entry tier operates on older Intel Broadwell silicon paired with network SAN storage, resulting in less than half the database throughput (825–1,164 TPS) at higher round-trip latency (72–77 ms).

---

## 6. The $5 vs. $10 Step-Up: What Does Doubling RAM Buy?

Comparing Vultr's **$5/mo (`vc2-1c-1gb`)** vs. **$10/mo (`vc2-1c-2gb`)** in Delhi demonstrates the value of doubling memory from 1 GB to 2 GB on the same CPU:
- **Sequential Storage**: Equal (~3,200 MB/s).
- **Random Write IOPS**: Surges by **+89.2%** (102,000 -> 193,000 IOPS) as storage volume scales from 25 GB to 55 GB.
- **Single-Client OLTP**: Modest +5.3% gain (2,071 -> 2,180 TPS).
- **32-Client Concurrency**: Significant **+20.1% gain** (1,217 -> 1,462 TPS) due to eliminated buffer cache paging.

---
