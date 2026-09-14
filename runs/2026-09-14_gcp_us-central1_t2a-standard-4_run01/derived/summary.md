# CloudMark Benchmark Summary: 2026-09-14_gcp_us-central1_t2a-standard-4_run01
Generated: 2026-09-14 07:57:57 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_gcp_us-central1_t2a-standard-4_run01`
- **machine_id**: `google cloud platform-us-central1-t2a-standard-4-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Google Cloud Platform`
- **region**: `us-central1`
- **plan_name**: `t2a-standard-4`
- **created_utc**: `2026-09-14 07:06:54 UTC`
- **pricing**: `{'monthly_usd': 119.38, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `t2a`
- **cpu_arch**: `aarch64`
- **cpu_model**: `Neoverse-N1`
- **exposed_vcpu**: `4`
- **ram_gb**: `15.6`
- **root_disk_type**: `NVMe`
- **root_disk_size_gb**: `50G`
- **virt_type**: `google`
- **kernel_version**: `6.1.0-53-cloud-arm64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 1292.32 | 0.77 | 0.78 | N/A |
| T011 | 4 | 5172.01 | 0.77 | 0.78 | 1.0005 |
| T012 | 4 | 5171.62 | 0.77 | 0.78 | Burst/Sust=1.0, CV=0.05% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 1064.635992 | 1073.1 | 0.93 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 2629.0688 | 2621.8 | 1.53 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 3829.280997 | 3900.7 | 2.05 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 4132.510103 | 4135.7 | 3.87 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 4061.900209 | 4159.3 | 7.71 | 0 |
| T053 | select_only | 10 | 1 | 14606.8159 | 14666.0 | 0.07 | 0 |
| T053 | select_only | 10 | 4 | 41613.165712 | 42014.9 | 0.09 | 0 |
| T053 | select_only | 10 | 8 | 36248.307235 | 35888.4 | 0.22 | 0 |
| T053 | select_only | 10 | 16 | 36098.031336 | 36244.0 | 0.44 | 0 |
| T053 | select_only | 10 | 32 | 33979.613537 | 34132.8 | 0.94 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 4 | 1M | 59916.09 | 0.07 |
| T020 | read | 4 | 1M | 58678.84 | 0.07 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 240.0 | 0.0 | 240.0 | 0.124 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 240.0 | 0.0 | 240.0 | 0.0 | 0.043 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 7714.0 | 0.0 | 30.1 | 0.0 | 16.58 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 7537.0 | 0.0 | 29.4 | 16.97 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 5271.0 | 2266.0 | 20.6 | 8.85 | 16.974 |