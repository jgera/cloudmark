# CloudMark Benchmark Summary: 2026-09-14_vultr_mumbai_vc2-1c-1gb_run01
Generated: 2026-09-15 11:39:26 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_vultr_mumbai_vc2-1c-1gb_run01`
- **machine_id**: `vultr-mumbai-vc2-1c-1gb-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Vultr`
- **region**: `Mumbai`
- **plan_name**: `vc2-1c-1gb`
- **created_utc**: `2026-09-14 18:24:38 UTC`
- **pricing**: `{'monthly_usd': 5.0, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `vc2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel Xeon Processor (Cascadelake)`
- **exposed_vcpu**: `1`
- **ram_gb**: `0.93`
- **root_disk_type**: `SSD`
- **root_disk_size_gb**: `25G`
- **virt_type**: `Microsoft`
- **kernel_version**: `6.1.0-52-amd64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 454.56 | 2.2 | 2.26 | N/A |
| T011 | 1 | 453.87 | 2.2 | 2.26 | N/A |
| T012 | 1 | 455.27 | 2.2 | 2.35 | Burst/Sust=0.97, CV=1.52% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 2351.987309 | 2338.6 | 0.43 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 2301.604752 | 2322.7 | 1.73 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 2082.112877 | 2065.9 | 3.9 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 1952.925446 | 2004.9 | 7.99 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 1613.946042 | 1613.7 | 19.86 | 0 |
| T053 | select_only | 10 | 1 | 18172.497947 | 18601.7 | 0.05 | 0 |
| T053 | select_only | 10 | 4 | 15257.632221 | 15510.9 | 0.26 | 0 |
| T053 | select_only | 10 | 8 | 14693.796755 | 14673.0 | 0.54 | 0 |
| T053 | select_only | 10 | 16 | 13516.229509 | 13574.0 | 1.18 | 0 |
| T053 | select_only | 10 | 32 | 9785.038426 | 9914.9 | 3.25 | 0 |
| T053 | select_only | 10 | 1 | 18172.497947 | 18601.7 | 0.05 | 0 |
| T053 | select_only | 10 | 4 | 15257.632221 | 15510.9 | 0.26 | 0 |
| T053 | select_only | 10 | 8 | 14693.796755 | 14673.0 | 0.54 | 0 |
| T053 | select_only | 10 | 16 | 13516.229509 | 13574.0 | 1.18 | 0 |
| T053 | select_only | 10 | 32 | 9785.038426 | 9914.9 | 3.25 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 1 | 1M | 19742.46 | 0.05 |
| T020 | read | 1 | 1M | 24598.19 | 0.04 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 1261.0 | 0.0 | 1261.0 | 0.081 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 2604.0 | 0.0 | 2604.0 | 0.0 | 0.013 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 178000.0 | 0.0 | 695.0 | 0.0 | 0.714 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 194000.0 | 0.0 | 759.0 | 0.657 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 137000.0 | 58600.0 | 534.0 | 229.0 | 0.734 |