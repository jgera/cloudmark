# CloudMark Benchmark Summary: 2026-09-14_gcp_uswest1_e2-micro_run01
Generated: 2026-09-14 04:50:16 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_gcp_uswest1_e2-micro_run01`
- **machine_id**: `google cloud platform-us-west1-e2-micro-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Google Cloud Platform`
- **region**: `us-west1`
- **plan_name**: `e2-micro`
- **created_utc**: `2026-09-14 03:50:32 UTC`
- **pricing**: `{'monthly_usd': 0.0, 'promotional_credit': True, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `e2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel(R) Xeon(R) CPU @ 2.20GHz`
- **exposed_vcpu**: `2`
- **ram_gb**: `0.95`
- **root_disk_type**: `pd-standard`
- **root_disk_size_gb**: `30G`
- **virt_type**: `KVM`
- **kernel_version**: `6.1.0-53-cloud-amd64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 190.82 | 5.22 | 3.19 | N/A |
| T011 | 2 | 117.83 | 16.97 | 223.34 | 0.3087 |
| T012 | 2 | 75.75 | 26.4 | 223.34 | Burst/Sust=2.4, CV=83.5% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 211.255945 | 91.2 | 10.95 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 180.499382 | 175.5 | 22.78 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 191.738015 | 181.4 | 44.67 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 191.373321 | 179.3 | 89.53 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 158.909921 | 151.5 | 223.43 | 0 |
| T053 | select_only | 10 | 1 | 1099.852422 | 789.7 | 1.24 | 0 |
| T053 | select_only | 10 | 4 | 1822.547242 | 1717.0 | 2.29 | 0 |
| T053 | select_only | 10 | 8 | 1754.032798 | 1650.1 | 4.8 | 0 |
| T053 | select_only | 10 | 16 | 1616.382288 | 1487.6 | 11.61 | 0 |
| T053 | select_only | 10 | 32 | 1414.149745 | 1439.4 | 22.09 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 2 | 1M | 15514.9 | 0.13 |
| T020 | read | 2 | 1M | 6093.26 | 0.32 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 101.0 | 0.0 | 102.0 | 0.462 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 120.0 | 0.0 | 120.0 | 0.0 | 0.077 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 152.0 | 0.0 | 0.6 | 0.0 | 0.047 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 304.0 | 0.0 | 1.19 | 0.892 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 124.0 | 55.0 | 0.49 | 0.21 | 4.39 |