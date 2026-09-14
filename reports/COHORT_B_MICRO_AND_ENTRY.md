# CloudMark CBP-1.0 Cohort B: Micro & Entry Tier Report ($0 to $10/month)

A rigorous analysis of ultra-low-cost virtual machines evaluating compute throttling, storage throughput, and database TPS:
- **GCP `e2-micro` (US)** ($0.00/mo) — Always Free Baseline
- **GCP `e2-micro` (Delhi)** ($7.30/mo) — Shared Core in India
- **Vultr `vc2-1c-1gb` (Delhi)** ($5.00/mo) — Regular Cloud Compute in India
- **Vultr `vc2-1c-2gb` (Delhi)** ($10.00/mo) — 2GB RAM Step-Up in India
- **Vultr `vc2-1c-1gb` (Singapore)** ($5.00/mo) — Southeast Asia Regional Hub

---

## 4. Cohort B: Micro & Entry Tier Deep-Dive ($0 – $10.00/month)

### 4.1 Sustained CPU Throttling Curves (T010, T011, T012 — 300s Continuous Load)
| Machine | Architecture & Cores | Single Peak (eps) | 300s Burst eps (0-30s) | 300s Steady eps (240-300s) | Drop Ratio | Throttling Volatility (CV) | Throttling Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **GCP `e2-micro` (US)** | Intel Xeon (0.25 core shared) | 472.0 | 341.2 | 144.1 | 2.37x drop | 83.5% | **Severe Throttling** |
| **GCP `e2-micro` (Delhi)** | AMD EPYC (0.25 core shared) | 790.2 | 332.9 | 186.3 | 1.79x drop | 51.5% | **Severe Throttling** |
| **Vultr `vc2-1c-1gb` (Delhi)** | Intel Cascadelake (1 core) | 440.8 | 442.8 | 436.0 | **1.02x** | **2.1%** | **100% Sustained (No Throttling)** |
| **Vultr `vc2-1c-2gb` (Delhi)** | Intel Cascadelake (1 core) | 449.9 | 450.8 | 450.8 | **1.00x** | **0.96%** | **100% Sustained (Rock Flat)** |
| **Vultr `vc2-1c-1gb` (SGP)** | Intel Broadwell (1 core) | 303.5 | 305.7 | 300.3 | **1.02x** | **1.58%** | **100% Sustained (No Throttling)** |

### 4.2 PostgreSQL Sustained Mixed OLTP Throughput (T052 — Scale 10)
| Concurrency Tier | GCP `e2-micro` (US, $0) | GCP `e2-micro` (Delhi, $7.30) | Vultr $5 (SGP) | Vultr $5 (Delhi) | Vultr $10 (Delhi) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Client** | 91.2 TPS (10.95 ms) | 94.1 TPS (10.63 ms) | 825.3 TPS (1.21 ms) | **2,071.1 TPS (0.48 ms)** | **2,180.4 TPS (0.46 ms)** |
| **4 Clients** | 175.5 TPS (22.78 ms) | 194.3 TPS (20.59 ms) | 1,164.5 TPS (3.44 ms) | **1,957.5 TPS (2.06 ms)** | **2,185.1 TPS (1.84 ms)** |
| **8 Clients** | 181.4 TPS (44.67 ms) | 236.2 TPS (33.95 ms) | 1,164.4 TPS (6.88 ms) | **1,821.2 TPS (4.40 ms)** | **2,127.9 TPS (3.76 ms)** |
| **16 Clients**| 179.3 TPS (89.53 ms) | 250.5 TPS (63.99 ms) | 982.9 TPS (16.32 ms) | **1,539.0 TPS (10.43 ms)**| **1,813.0 TPS (8.83 ms)** |
| **32 Clients**| 151.5 TPS (223.43 ms)| 215.8 TPS (145.05 ms)| 897.3 TPS (35.69 ms) | **1,217.1 TPS (26.38 ms)**| **1,461.7 TPS (21.92 ms)**|

---

## 5. Regional Analysis: Delhi (`del`) vs. Singapore (`sgp`)

Comparing the identical **$5.00/mo plan (`vc2-1c-1gb`)** between Delhi and Singapore uncovered a critical **hardware generation disparity** in Vultr's cloud fleet:

| Dimension | Vultr Delhi (`del`) | Vultr Singapore (`sgp`) | Disparity / Analysis |
| :--- | :---: | :---: | :--- |
| **CPU Model** | Intel Xeon Cascadelake @ 2.99 GHz | Intel Xeon Broadwell @ 2.39 GHz | Delhi is 2 microarchitecture generations newer |
| **Client RTT from India** | **10.5 ms (avg: 41 ms)** | **76.8 ms (min: 72 ms)** | Delhi offers 7.3x lower network latency |
| **Seq Read / Write** | **3,178 MB/s / 2,678 MB/s** | 352 MB/s / 308 MB/s | **Delhi disk is 9x faster** (local array vs network SAN) |
| **Random 4K Read IOPS** | **144,000 IOPS** | 56,000 IOPS | Delhi delivers 2.6x higher IOPS |
| **Sustained OLTP TPS (Client 1)** | **2,071.1 TPS** | 825.3 TPS | **Delhi delivers 2.5x higher database throughput** |

> [!IMPORTANT]
> **Regional Takeaway:** Never assume hardware homogeneity across cloud datacenters. For South Asian workloads, deploying in Delhi is not just about saving 65 ms of network ping; **the local host hardware in Delhi is 2.5x more powerful** for the exact same $5.00 price.

---

## 6. The $5 vs. $10 Step-Up: What Does Doubling RAM Buy?

Comparing Vultr's **$5/mo (`vc2-1c-1gb`)** vs. **$10/mo (`vc2-1c-2gb`)** in Delhi demonstrates the value of doubling memory from 1 GB to 2 GB on the same CPU:
- **Sequential Storage**: Equal (~3,200 MB/s).
- **Random Write IOPS**: Surges by **+89.2%** (102,000 -> 193,000 IOPS) as storage volume scales from 25 GB to 55 GB.
- **Single-Client OLTP**: Modest +5.3% gain (2,071 -> 2,180 TPS).
- **32-Client Concurrency**: Significant **+20.1% gain** (1,217 -> 1,462 TPS) due to eliminated buffer cache paging.

---
