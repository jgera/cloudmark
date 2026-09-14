# CloudMark Benchmark Summary: 2026-09-14_gcp_us-central1_c2-standard-4_run01
Generated: 2026-09-14 07:06:33 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_gcp_us-central1_c2-standard-4_run01`
- **machine_id**: `google cloud platform-us-central1-c2-standard-4-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Google Cloud Platform`
- **region**: `us-central1`
- **plan_name**: `c2-standard-4`
- **created_utc**: `2026-09-14 06:15:44 UTC`
- **pricing**: `{'monthly_usd': 158.4, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `c2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel(R) Xeon(R) CPU @ 3.10GHz`
- **exposed_vcpu**: `4`
- **ram_gb**: `15.63`
- **root_disk_type**: `pd-standard`
- **root_disk_size_gb**: `50G`
- **virt_type**: `KVM`
- **kernel_version**: `6.1.0-53-cloud-amd64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 488.53 | 2.05 | 2.07 | N/A |
| T011 | 4 | 1654.07 | 2.42 | 2.43 | 0.8465 |
| T012 | 4 | 1654.07 | 2.42 | 2.43 | Burst/Sust=1.0, CV=0.04% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 1453.184461 | 1451.7 | 0.69 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 3468.933659 | 3474.2 | 1.15 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 5190.266638 | 5210.5 | 1.54 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 6133.186693 | 6141.3 | 2.61 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 6113.098344 | 6115.5 | 5.24 | 0 |
| T053 | select_only | 10 | 1 | 20351.660541 | 20475.4 | 0.05 | 0 |
| T053 | select_only | 10 | 4 | 57488.94005 | 57588.4 | 0.07 | 0 |
| T053 | select_only | 10 | 8 | 52292.633797 | 52729.0 | 0.15 | 0 |
| T053 | select_only | 10 | 16 | 49216.018484 | 48511.0 | 0.33 | 0 |
| T053 | select_only | 10 | 32 | 47975.441354 | 47364.5 | 0.68 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 4 | 1M | 35058.26 | 0.11 |
| T020 | read | 4 | 1M | 75481.16 | 0.05 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 240.0 | 0.0 | 240.0 | 0.135 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 240.0 | 0.0 | 240.0 | 0.0 | 0.019 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 4115.0 | 0.0 | 16.1 | 0.0 | 31.089 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 4021.0 | 0.0 | 15.7 | 0.012 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 2809.0 | 1211.0 | 11.0 | 4.73 | 31.84 |