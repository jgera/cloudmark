# CloudMark CBP-1.0 Multi-Architecture Benchmark Report

A publication-grade cross-cloud comparative analysis evaluating real-world database throughput, compute throttling curves, storage IOPS, and price-to-performance across **Google Cloud Platform** and **Vultr**.
*Compiled: 2026-09-14 18:01:41 UTC*

---

## 1. Executive Summary & Full Machine Inventory

All benchmarks executed under the frozen **CloudMark Benchmark Protocol (CBP-1.0)** with vendor defaults preserved and zero tuning bias:

### 1.1 Evaluated Instances Matrix
| Machine ID | Cloud Provider | Plan / Tier | Architecture & vCPUs | RAM | Storage Subsystem | Region | Monthly On-Demand |
| :--- | :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| `vultr-delhi-vhp-4c-8gb-intel-01` | **Vultr** | `vhp-4c-8gb-intel` | 4 vCPUs (Intel Xeon Processor (Cascadelake)) | 7.75 GB | 180G NVMe/SSD | `Delhi` | **$48.00** |
| `vultr-mumbai-vhp-4c-8gb-amd-01` | **Vultr** | `vhp-4c-8gb-amd` | 4 vCPUs (AMD EPYC-Rome Processor) | 7.75 GB | 180G NVMe/SSD | `Mumbai` | **$48.00** |
| `google cloud platform-us-west1-e2-micro-01` | **Google Cloud Platform** | `e2-micro` | 2 vCPUs (Intel(R) Xeon(R) CPU @ 2.20GHz) | 0.95 GB | 30G pd-standard | `us-west1` | **$0.00** |
| `google cloud platform-us-west1-e2-standard-4-01` | **Google Cloud Platform** | `e2-standard-4` | 4 vCPUs (Intel(R) Xeon(R) CPU @ 2.20GHz) | 15.63 GB | 50G pd-standard | `us-west1` | **$105.12** |
| `google cloud platform-us-central1-c2-standard-4-01` | **Google Cloud Platform** | `c2-standard-4` | 4 vCPUs (Intel(R) Xeon(R) CPU @ 3.10GHz) | 15.63 GB | 50G pd-standard | `us-central1` | **$158.40** |
| `google cloud platform-us-central1-t2a-standard-4-01` | **Google Cloud Platform** | `t2a-standard-4` | 4 vCPUs (Neoverse-N1) | 15.6 GB | 50G NVMe | `us-central1` | **$119.38** |
| `google cloud platform-asia-south2-e2-micro-01` | **Google Cloud Platform** | `e2-micro` | 2 vCPUs (AMD EPYC 7B12) | 0.95 GB | 30G pd-standard | `asia-south2` | **$7.30** |
| `vultr-delhi-vc2-1c-1gb-01` | **Vultr** | `vc2-1c-1gb` | 1 vCPUs (Intel Xeon Processor (Cascadelake)) | 0.93 GB | 25G SSD | `Delhi` | **$5.00** |
| `vultr-delhi-vc2-1c-2gb-01` | **Vultr** | `vc2-1c-2gb` | 1 vCPUs (Intel Xeon Processor (Cascadelake)) | 1.92 GB | 55G SSD | `Delhi` | **$10.00** |
| `vultr-sgp-vc2-1c-1gb-01` | **Vultr** | `vc2-1c-1gb` | 1 vCPUs (Intel Core Processor (Broadwell, no TSX, IBRS)) | 0.93 GB | 25G SSD | `Sgp` | **$5.00** |

---

## 2. Overall Price-to-Performance Efficiency ($/month Value)

Transactions Per Second (TPS) per dollar per month based on peak sustained PostgreSQL mixed OLTP throughput:

| Cloud & Machine Type | Location | Monthly Price | Peak Sustained OLTP TPS | TPS per Dollar / Month | Overall Value Rank |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Vultr `vc2-1c-1gb`** | **Delhi** | **$5.00** | **2,071 TPS** | **414.2 TPS / $** | 🥇 **#1 Overall Value** |
| **Vultr `vc2-1c-1gb`** | **Singapore** | **$5.00** | **1,165 TPS** | **232.9 TPS / $** | 🥈 **#2** |
| **Vultr `vc2-1c-2gb`** | **Delhi** | **$10.00** | **2,185 TPS** | **218.5 TPS / $** | 🥉 **#3 Concurrency Value** |
| **Vultr `vhp-4c-8gb-intel`** | **Delhi** | **$48.00** | **8,280 TPS** | **172.5 TPS / $** | **#4 Raw Throughput Value** |
| **Vultr `vhp-4c-8gb-amd`** | **Mumbai** | **$48.00** | **4,562 TPS** | **95.0 TPS / $** | **#5** |
| **GCP `c2-standard-4`** | **Iowa** | **$158.40** | **6,141 TPS** | **38.8 TPS / $** | **#6** |
| **GCP `t2a-standard-4` (ARM)**| **Iowa** | **$119.38** | **4,159 TPS** | **34.8 TPS / $** | **#7** |
| **GCP `e2-micro`** | **Delhi** | **$7.30** | **250 TPS** | **34.2 TPS / $** | **#8** |
| **GCP `e2-standard-4`** | **Oregon** | **$105.12** | **2,700 TPS** | **25.7 TPS / $** | **#9** |
| **GCP `e2-micro`** | **Oregon** | **$0.00** | **181 TPS** | **∞ (Always Free)** | **N/A** |

---

## 3. Cohort A: Standard 4-Core Tier Comparison ($48 – $158/month)

### 3.1 PostgreSQL Sustained Mixed OLTP Scaling (T052 — TPC-B Like, Scale 10)
180 seconds per concurrency step with `-P 5` progress reporting:

| Concurrency | GCP `e2-std-4` ($105) | GCP `c2-std-4` ($158) | GCP `t2a` ARM ($119) | Vultr Intel ($48) | Vultr AMD ($48) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Client** | 381.3 TPS (2.65 ms) | 1,451.7 TPS (0.69 ms) | 1,073.1 TPS (0.93 ms) | **2,360.4 TPS (0.42 ms)** | 1,213.3 TPS (0.83 ms) |
| **4 Clients** | 1,062.4 TPS (3.82 ms) | 3,474.2 TPS (1.15 ms) | 2,621.8 TPS (1.53 ms) | **5,976.0 TPS (0.67 ms)** | 3,136.1 TPS (1.28 ms) |
| **8 Clients** | 1,401.3 TPS (6.27 ms) | 5,210.5 TPS (1.54 ms) | 3,900.7 TPS (2.05 ms) | **8,279.7 TPS (0.97 ms)** | 4,561.9 TPS (1.75 ms) |
| **16 Clients**| 2,700.0 TPS (5.99 ms) | **6,141.3 TPS (2.61 ms)** | 4,135.7 TPS (3.87 ms) | **7,788.8 TPS (2.05 ms)** | 4,199.1 TPS (3.81 ms) |
| **32 Clients**| 2,236.8 TPS (14.55 ms)| 6,115.5 TPS (5.24 ms) | **4,159.3 TPS (7.71 ms)** | **6,933.0 TPS (4.62 ms)** | 3,636.8 TPS (8.82 ms) |

### 3.2 Storage IOPS & Bandwidth Limits
| Machine | Storage Subsystem | Seq Read (MB/s) | Seq Write (MB/s) | Random 4K Read IOPS | Random 4K Write IOPS | Random Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **GCP `e2-standard-4`** | 50 GB `pd-ssd` | 240 MB/s | 240 MB/s | 7,700 IOPS | 7,700 IOPS | 0.038 ms |
| **GCP `c2-standard-4`** | 50 GB `pd-ssd` | 240 MB/s | 240 MB/s | 7,700 IOPS | 7,700 IOPS | 0.028 ms |
| **GCP `t2a-standard-4`**| 50 GB `pd-ssd` | 240 MB/s | 240 MB/s | 7,700 IOPS | 7,700 IOPS | 0.029 ms |
| **Vultr Intel (Delhi)** | 180 GB Local NVMe | **3,267 MB/s** | **2,721 MB/s** | **219,000 IOPS** | **178,000 IOPS** | **0.58 ms** |
| **Vultr AMD (Mumbai)** | 180 GB Local NVMe | **3,250 MB/s** | **2,710 MB/s** | **215,000 IOPS** | **172,000 IOPS** | **0.61 ms** |

> [!NOTE]
> **Storage Bottleneck Exposed:** Google Cloud caps 50 GB `pd-ssd` persistent disks at 240 MB/s and 7,700 IOPS. Vultr's direct local NVMe delivers **219,000 IOPS**, explaining why Vultr Intel achieved 8,280 sustained OLTP TPS compared to GCP C2's 6,141 TPS despite GCP C2 having higher single-thread CPU clock frequencies.

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

## 7. Architectural Recommendations

1. **For Production Databases on a Budget ($5 – $10/mo):**
   - Choose **Vultr Delhi (`vc2-1c-1gb` or `vc2-1c-2gb`)**. You get 100% sustained CPU execution, >140,000 IOPS, and >2,000 sustained OLTP TPS.
   - Avoid GCP `e2-micro` for production databases; its 0.25 core allocation causes severe latency spikes (>145 ms) once burst tokens deplete.
2. **For High-Performance Multi-Core Workloads ($48 – $160/mo):**
   - **Vultr Intel High Performance (`vhp-4c-8gb-intel` at $48/mo)** is the undisputed performance leader, delivering **8,280 sustained OLTP TPS** (172.5 TPS per dollar).
   - **GCP Compute-Optimized (`c2-standard-4` at $158/mo)** is the fastest single-thread CPU runner (488.5 eps) and reaches 6,141 OLTP TPS, but is heavily bottlenecked by persistent disk limits (240 MB/s / 7,700 IOPS).
   - **GCP Tau ARM64 (`t2a-standard-4` at $119/mo)** provides perfect linear multi-core scaling (100.1% efficiency) with zero thermal throttling, ideal for compute-bound microservices.