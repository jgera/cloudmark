# CloudMark Benchmark Summary: 2026-09-14_gcp_us-west1_e2-standard-4_run01
Generated: 2026-09-14 06:13:15 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_gcp_us-west1_e2-standard-4_run01`
- **machine_id**: `google cloud platform-us-west1-e2-standard-4-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Google Cloud Platform`
- **region**: `us-west1`
- **plan_name**: `e2-standard-4`
- **created_utc**: `2026-09-14 05:21:17 UTC`
- **pricing**: `{'monthly_usd': 105.12, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `e2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel(R) Xeon(R) CPU @ 2.20GHz`
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
| T010 | 1 | 335.92 | 2.98 | 3.3 | N/A |
| T011 | 4 | 1114.29 | 3.59 | 3.96 | 0.8293 |
| T012 | 4 | 1102.99 | 3.62 | 4.1 | Burst/Sust=0.97, CV=2.35% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 391.580084 | 381.3 | 2.65 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 1031.78159 | 1062.4 | 3.82 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 1590.708194 | 1401.3 | 6.27 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 2465.077025 | 2700.0 | 5.99 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 2452.287471 | 2236.8 | 14.55 | 0 |
| T053 | select_only | 10 | 1 | 9167.465813 | 9668.3 | 0.1 | 0 |
| T053 | select_only | 10 | 4 | 31712.001673 | 32161.1 | 0.12 | 0 |
| T053 | select_only | 10 | 8 | 29623.375752 | 29813.9 | 0.27 | 0 |
| T053 | select_only | 10 | 16 | 27096.648611 | 27252.0 | 0.59 | 0 |
| T053 | select_only | 10 | 32 | 17880.972432 | 18509.2 | 1.75 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 4 | 1M | 27368.43 | 0.14 |
| T020 | read | 4 | 1M | 46140.38 | 0.09 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 240.0 | 0.0 | 240.0 | 0.231 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 240.0 | 0.0 | 240.0 | 0.0 | 0.074 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 7718.0 | 0.0 | 30.1 | 0.0 | 0.028 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 7542.0 | 0.0 | 29.5 | 0.023 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 5275.0 | 2268.0 | 20.6 | 8.86 | 0.027 |