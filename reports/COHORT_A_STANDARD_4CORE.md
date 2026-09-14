# CloudMark CBP-1.0 Cohort A: Standard 4-Core Tier Report

A rigorous multi-architecture benchmark comparing 4-core virtual machines across **Google Cloud** and **Vultr**:
- **GCP `e2-standard-4`** ($105.12/mo) — Intel Xeon 2.2 GHz shared
- **GCP `c2-standard-4`** ($158.40/mo) — Intel Xeon Cascadelake 3.8 GHz Compute-Optimized
- **GCP `t2a-standard-4`** ($119.38/mo) — Ampere Altra Neoverse-N1 ARM64 3.0 GHz
- **Vultr `vhp-4c-8gb-intel`** ($48.00/mo) — Intel Xeon Cascadelake 2.99 GHz in Delhi
- **Vultr `vhp-4c-8gb-amd`** ($48.00/mo) — AMD EPYC Rome 2.59 GHz in Mumbai

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
