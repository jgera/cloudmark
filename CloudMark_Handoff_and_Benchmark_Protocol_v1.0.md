# CloudMark Benchmarking Project

## Handoff, Baseline Record, and Cross-Provider Benchmark Protocol

**Document version:** 1.0  
**Protocol family:** CBP (Cloud Benchmark Protocol)  
**Current formal protocol:** CBP-1.0  
**Prepared:** 2026-09-13  
**Status:** Active working handoff  
**Primary purpose:** Engineering comparison now; reproducible cross-provider dataset and possible research use later.

---

## 1. Project Purpose

CloudMark is a long-term, provider-neutral effort to measure and compare the real performance of cloud virtual machines, VPS platforms, free-tier instances, paid instances, and eventually dedicated/bare-metal or self-hosted servers.

The project began as an engineering exercise to understand PostgreSQL performance on a very small Google Cloud free-tier VM. It should now be treated as a structured benchmarking dataset rather than a one-off server comparison.

The project has four goals:

1. **Engineering:** identify which infrastructure provides the best practical performance for workloads such as Django + PostgreSQL + Redis + Celery.
2. **Economic:** compare real performance per unit cost rather than advertised vCPU/RAM specifications alone.
3. **Operational:** measure sustained performance, burst behavior, variability, latency, and saturation points.
4. **Research:** preserve enough metadata, raw output, repeatability, and protocol discipline that the growing dataset may later support a rigorous comparative study or academic paper.

The protocol must remain usable across providers. It must not be silently modified to favor a particular platform.

---

## 2. Core Principles

### 2.1 Same protocol across providers

The same core test definitions should be used for:

- Google Cloud Platform
- Vultr
- Oracle Cloud Infrastructure
- Hetzner
- AWS
- Azure
- other VPS/cloud providers
- rented dedicated servers
- owned bare-metal servers
- office/self-hosted systems

Provider-specific diagnostics may be added, but they must be clearly marked as **supplementary** and must not replace the common core tests.

### 2.2 Raw data and derived data must remain separate

**Raw data** means exact, unmodified command output.

Examples:

- `lscpu`
- `free -h`
- `lsblk`
- `fio --output-format=json`
- `sysbench`
- `vmstat`
- `iostat`
- `pgbench`
- `ping`
- `iperf3`

Raw files must not be edited to make them easier to read.

**Derived data** means values calculated from raw output:

- mean TPS
- median latency
- standard deviation
- coefficient of variation
- burst/sustained ratio
- price/TPS
- IOPS/$
- scaling efficiency
- normalized scores

If a derived value is later corrected, the raw data must remain unchanged.

### 2.3 Sustained performance is more important than headline burst performance

Cloud instances may temporarily perform far above their sustainable level.

Therefore the dataset should distinguish at least:

- `burst_tps`
- `sustained_tps`
- `whole_run_tps`
- `burst_latency_ms`
- `sustained_latency_ms`

A provider should not receive an unfair advantage because a short test happened to run entirely inside a CPU or storage burst window.

### 2.4 Unexpected results must be preserved

If a result looks strange:

- do not delete it;
- do not silently rerun until a preferred value appears;
- mark it as anomalous;
- investigate;
- retain both the anomalous run and the repeat run.

Variability is itself useful data.

### 2.5 Protocol changes require version changes

Examples:

- CBP-0 — exploratory/legacy testing
- CBP-1.0 — first frozen standardized protocol
- CBP-1.1 — backward-compatible refinement
- CBP-2.0 — substantial methodology change

Never overwrite an old result because the protocol improved.

---

# 3. Agent Operating Instructions

An AI agent taking over this project must follow these rules.

## 3.1 Work one test at a time

For every benchmark step:

1. State the **test ID** and **protocol version**.
2. Explain briefly what is being measured and why.
3. Give only the commands needed for that test.
4. State exactly which output/files must be preserved.
5. Wait for the user to return the result.
6. Analyse the returned output.
7. Extract quantitative metrics.
8. Update the cumulative benchmark record.
9. Note any anomaly or methodological concern.
10. Only then proceed to the next test.

Do not dump the entire benchmark battery on the user at once.

## 3.2 Do not tune before measuring the default system

The first benchmark pass should represent the provider's normal/default configuration as closely as practical.

Do not change kernel tunables, PostgreSQL parameters, filesystem settings, CPU governors, or provider settings merely to increase scores before the default baseline is collected.

Tuned tests may be added later as a separate experiment.

## 3.3 Do not infer capacity directly from TPS

Generic benchmark TPS is not equal to:

- users;
- requests per second;
- school/customer count;
- registered accounts.

Any capacity estimate must state the workload assumptions used.

## 3.4 Prefer transparent, standard tools

Preferred tools include:

- `lscpu`
- `uname`
- `free`
- `vmstat`
- `iostat`
- `lsblk`
- `fio`
- `sysbench`
- `iperf3`
- `ping`
- PostgreSQL
- `pgbench`
- provider CLI/API where needed

Opaque "one-click benchmark scripts" may be used only as supplementary tests when their methodology is understood.

---

# 4. Dataset Organization

Recommended top-level structure:

```text
CloudMark/
├── README.md
├── protocol/
│   ├── CBP-1.0.md
│   └── CHANGELOG.md
├── runs/
│   ├── LEGACY-GCP-001/
│   │   ├── metadata.json
│   │   ├── raw/
│   │   ├── derived/
│   │   └── notes.md
│   ├── 2026-09-vultr-delhi-hp-4c8g-r01/
│   └── ...
├── master/
│   ├── machines.csv
│   ├── runs.csv
│   ├── cpu_results.csv
│   ├── memory_results.csv
│   ├── storage_results.csv
│   ├── network_results.csv
│   ├── postgres_results.csv
│   └── pricing.csv
└── analysis/
    ├── notebooks/
    ├── figures/
    └── tables/
```

## 4.1 Run ID convention

Recommended format:

```text
YYYY-MM-DD_provider_region_plan_runNN
```

Examples:

```text
2026-09-13_vultr_delhi_hp-4c8g_run01
2026-09-20_oci_home-a1-2c12g_run01
2026-09-25_gcp_us-west1_e2-micro_run01
```

The legacy GCP result should retain a special ID:

```text
LEGACY-GCP-001
```

---

# 5. Required Metadata for Every Run

At minimum record:

| Group     | Required field                           |
| --------- | ---------------------------------------- |
| Identity  | run_id                                   |
| Protocol  | protocol_version                         |
| Provider  | provider                                 |
| Location  | region                                   |
| Location  | zone / availability domain if applicable |
| Instance  | instance_family                          |
| Instance  | exact_plan_or_shape                      |
| CPU       | exposed_vcpu_count                       |
| CPU       | provider_cpu_classification              |
| CPU       | cpu_model                                |
| CPU       | cpu_architecture                         |
| CPU       | virtualization_type if visible           |
| Memory    | ram_gb                                   |
| Storage   | root_disk_type                           |
| Storage   | root_disk_size_gb                        |
| Storage   | extra_disk_type/size if used             |
| OS        | distribution                             |
| OS        | OS version                               |
| Kernel    | kernel version                           |
| Database  | PostgreSQL version                       |
| Time      | run start UTC                            |
| Time      | run end UTC                              |
| Economics | hourly price at test date                |
| Economics | monthly-equivalent price at test date    |
| Economics | currency                                 |
| Economics | promotional/free-tier status             |
| Network   | public IPv4/IPv6 state                   |
| Notes     | relevant provider limits                 |
| Integrity | raw_output_paths                         |

Where a provider does not disclose a field, record it as `unknown`, not as an inferred fact.

---

# 6. Test Profiles

CloudMark should support two execution profiles.

## 6.1 Engineering / Scout Profile

Purpose:

- quickly understand a machine;
- compare likely purchasing options;
- locate obvious bottlenecks.

Characteristics:

- normally one run per test;
- shorter sustained workloads;
- enough concurrency points to identify the approximate saturation region;
- results may guide which tests deserve deeper repetition.

Scout results are useful but should not automatically be treated as publication-grade.

## 6.2 Research / Standard Profile

Purpose:

- formal cross-provider comparison;
- statistical analysis;
- publication-quality dataset.

Characteristics:

- fixed test definitions;
- at least 3 repeated runs per primary measurement;
- preferably 5 or more for high-variance/shared-cloud experiments;
- multiple times of day when practical;
- ideally multiple independently provisioned instances for a plan/provider;
- raw logs retained;
- exact software versions retained;
- test order documented;
- no selective deletion of weak results.

Where possible, repeat the same configuration on different physical hosts by reprovisioning the VM. This is valuable because cloud-plan variability can be a research result in its own right.

---

# 7. CBP-1.0 Core Test Sequence

The following is the planned standardized sequence. The agent must still execute it **one test at a time**.

---

## T001 — Machine and Environment Characterization

Purpose:

- establish exactly what has been provisioned;
- identify CPU architecture/model;
- identify virtualization environment;
- establish OS/kernel/memory/storage basics.

Typical evidence:

```bash
uname -a
cat /etc/os-release
lscpu
nproc
free -h
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,ROTA,MODEL
df -hT
systemd-detect-virt
```

Preserve complete raw output.

---

## T002 — Idle-System Baseline

Purpose:

- establish CPU, memory, swap, and I/O state before stress testing.

Typical evidence:

```bash
uptime
free -h
vmstat 1 10
iostat -xz 1 10
```

Record whether the server is truly idle and whether swap/I/O activity already exists.

---

## T010 — CPU Single-Thread Performance

Purpose:

- estimate performance of latency-sensitive serial work;
- relevant to many SQL queries and application request paths.

Preferred standard tool: `sysbench` or another transparent benchmark frozen by protocol version.

Record:

- exact command;
- events/sec;
- total time;
- latency distribution when available.

---

## T011 — CPU Multi-Thread Performance

Purpose:

- measure aggregate CPU throughput using all exposed vCPUs.

Use the same benchmark family as T010 with a standardized thread count.

Record:

- thread count;
- events/sec;
- latency;
- scaling relative to single-thread performance.

Derived metric:

```text
multicore_scaling_efficiency =
multi_thread_score / (single_thread_score × thread_count)
```

---

## T012 — Sustained CPU Test

Purpose:

- distinguish initial burst performance from sustainable compute;
- expose shared-core throttling or host contention.

The test should be long enough to reach steady state.

For research runs, preserve time-series output rather than only the final average.

Derived fields may include:

- first-30-second score;
- final-5-minute score;
- burst/sustained ratio;
- coefficient of variation.

---

## T020 — Memory Performance

Purpose:

- characterize memory throughput and latency proxies;
- capture RAM capacity separately from CPU/storage.

Record:

- benchmark method;
- working-set size;
- read/write throughput;
- thread count.

Memory benchmark methodology must remain identical across x86 and ARM where possible.

---

## T030 — Storage Identification

Before running `fio`, determine:

- local/remote/cloud block device;
- filesystem;
- apparent rotational/non-rotational state;
- mount options;
- available space.

Do not assume "NVMe" merely from marketing text; record what the guest sees and separately record the provider's advertised storage class.

---

## T031 — Sequential Storage Throughput

Purpose:

- measure large-block sequential read/write performance.

Record:

- block size;
- queue depth;
- test file size;
- runtime;
- read MB/s;
- write MB/s;
- latency.

The test file must be large enough to reduce trivial cache effects.

---

## T032 — Random Storage IOPS and Latency

Purpose:

- evaluate database-relevant random I/O.

A standardized 4 KiB random profile should be included.

Record:

- read IOPS;
- write IOPS;
- mixed IOPS if tested;
- mean latency;
- percentile latency where available;
- queue depth;
- jobs;
- runtime.

---

## T033 — Sustained Storage Behavior

Purpose:

- detect storage burst credits or throttling;
- distinguish short synthetic peaks from longer-term database capability.

Use a controlled workload and retain time-series behavior.

Avoid unnecessarily destructive write volumes.

---

## T040 — Server Network Throughput

Purpose:

- establish available network throughput independent of user geography.

Preferred:

- `iperf3` against documented endpoints where possible;
- multiple endpoints when provider routing could bias a single result.

Record upload and download separately.

---

## T041 — End-User RTT / Geographic Latency

Purpose:

- measure real interactive network latency from defined client locations.

The current primary client geography is North India.

For every client endpoint record:

- client city/region;
- ISP if known;
- IPv4 or IPv6;
- packet count;
- min RTT;
- average RTT;
- maximum RTT;
- packet loss.

This test should be kept conceptually separate from server throughput.

---

# 8. PostgreSQL Benchmark Protocol

PostgreSQL is a primary workload in CloudMark because it represents practical OLTP/database infrastructure rather than only synthetic CPU scores.

Use the same major PostgreSQL version whenever practical.

For CBP-1.0, PostgreSQL 18 is the preferred reference because the original GCP baseline used PostgreSQL 18.

If a future architecture/package repository cannot reasonably use PostgreSQL 18, record the version explicitly and do not silently treat the run as perfectly equivalent.

---

## T050 — PostgreSQL Environment Capture

Record:

- PostgreSQL exact version;
- `pgbench` exact version;
- database configuration relevant to performance;
- data directory filesystem;
- PostgreSQL service state;
- major non-default settings, if any.

The initial comparison should use near-default configuration unless a separate tuned profile is explicitly defined.

---

## T051 — Small Working-Set Initialization

Reference initialization:

```bash
pgbench -i -s 10
```

Record actual database size after initialization.

Purpose:

- maintain continuity with the original GCP benchmark;
- characterize a relatively cache-friendly workload.

---

## T052 — Mixed OLTP Concurrency Scaling

Builtin pgbench TPC-B-like workload.

Core concurrency series:

```text
1
4
8
16
32
```

If performance is still increasing materially at 32 clients, extend to:

```text
64
128
```

only as justified.

### Sustained-run principle

The test must be long enough to separate burst and steady-state behavior.

A research-grade run should retain periodic progress output so the steady-state interval can be calculated from the raw time series.

Do not report only the whole-run average on burstable machines.

Required fields:

- clients;
- worker threads/jobs;
- duration;
- total transactions;
- failed transactions;
- whole-run TPS;
- whole-run latency;
- sustained TPS;
- sustained latency;
- time-series TPS;
- time-series latency.

---

## T053 — SELECT-Only Concurrency Scaling

Use the same client levels as the mixed workload where practical.

Purpose:

- characterize cache/read ceiling;
- separate CPU/cache performance from write/WAL behavior.

Required fields mirror T052.

---

## T054 — Larger PostgreSQL Working Set

A small scale-10 database can fit largely in memory on larger machines.

Therefore a second working-set size is required for serious comparisons.

Candidate CBP-1.0 larger scale:

```text
scale 100
```

If the resulting dataset remains too small relative to a machine's memory, a larger scale may be added, but the scale must be recorded and results at different scales must not be merged as if identical.

Purpose:

- expose storage behavior;
- reduce unrealistic cache-only results;
- compare RAM-rich and RAM-constrained systems.

---

## T055 — PostgreSQL + System Monitoring

Run selected pgbench saturation tests while collecting:

```bash
vmstat
iostat
```

and, when useful:

- PostgreSQL statistics;
- CPU utilization;
- I/O wait;
- swap activity;
- device utilization.

Purpose:

- identify whether a throughput ceiling is predominantly CPU-, memory-, WAL-, storage-, or queueing-related.

---

## T056 — Remote PostgreSQL Test

Optional but useful for application realism.

Run pgbench from a remote client over a secure route.

Keep this separate from the local-server benchmark because it includes WAN latency.

Purpose:

- quantify local-server capability versus real remote application experience.

---

# 9. Existing GCP Baseline — LEGACY-GCP-001

This is the first historical observation in the CloudMark project.

It must be preserved, but it predates the frozen CBP-1.0 methodology.

## 9.1 Environment

| Field                   | Value                                                          |
| ----------------------- | -------------------------------------------------------------- |
| Run ID                  | `LEGACY-GCP-001`                                               |
| Provider                | Google Cloud Platform                                          |
| Instance                | `e2-micro`                                                     |
| Zone                    | `us-west1-a`                                                   |
| RAM                     | approximately 1 GB                                             |
| Disk                    | 30 GB `pd-standard`                                            |
| PostgreSQL              | 18                                                             |
| pgbench scale           | 10                                                             |
| Protocol classification | `CBP-0 / legacy / exploratory`                                 |
| Status                  | valid engineering baseline; not formal statistical observation |

The earlier work identified strong burst behavior followed by a much lower steady state.

## 9.2 Existing PostgreSQL Results

| Workload      | Clients | Duration | Whole-run TPS | Estimated sustained TPS | Approx sustained latency | Failures |
| ------------- | -------:| --------:| -------------:| -----------------------:| ------------------------:| --------:|
| Mixed pgbench | 1       | 300 s    | 128.9         | **~90.3**               | ~11 ms                   | 0        |
| Mixed pgbench | 4       | 180 s    | 397.1         | **~180.6**              | ~22 ms                   | 0        |
| Mixed pgbench | 8       | 180 s    | 435.6         | **~191.0**              | ~40–46 ms                | 0        |
| Mixed pgbench | 16      | 180 s    | 413.8         | **~180.1**              | ~83–104 ms               | 0        |
| SELECT-only   | 1       | 120 s    | 2030.0        | **~746.6**              | ~1.2–1.5 ms              | 0        |

Approximate mixed-workload scaling:

```text
1 client       ~90 TPS
4 clients     ~181 TPS
8 clients     ~191 TPS
16 clients    ~180 TPS
```

This suggests a practical mixed-workload throughput peak around 4–8 simultaneously busy database clients on that VM.

## 9.3 Approximate Early Burst Values

Historical observations:

```text
Mixed c1       ~475 TPS
Mixed c4      ~1,330 TPS
Mixed c8      ~1,634 TPS
Mixed c16     ~1,448 TPS
SELECT c1     ~6,383 TPS
```

These are useful because they demonstrate why short cloud benchmarks can be misleading.

## 9.4 Limitations of LEGACY-GCP-001

The GCP run must not be treated as equivalent to future CBP-1.0 research runs because:

- test durations differed;
- results were collected during exploratory work;
- sustained values were manually estimated from post-burst intervals;
- each configuration was not systematically repeated;
- benchmark order was not formally randomized;
- full system telemetry was not consistently retained;
- CPU, memory, storage, and network subtests were not performed under a frozen common protocol;
- raw machine-readable files may not exist for every observation.

### Allowed use

Use LEGACY-GCP-001 for:

- initial engineering comparison;
- sanity checking;
- historical reference;
- measuring order-of-magnitude improvement.

### Not allowed without qualification

Do not include it in formal inferential cross-provider statistics as if it were an equivalent CBP-1.0 repeated run.

## 9.5 Planned GCP Re-run

Later, reprovision the same or equivalent `e2-micro` and run CBP-1.0 completely.

Create a new record.

Do **not** overwrite `LEGACY-GCP-001`.

This will allow comparison between:

```text
CBP-0 exploratory result
vs
CBP-1.0 standardized result
```

and will also validate whether the new protocol reaches the same engineering conclusions.

---

# 10. Immediate Next Target — Vultr Delhi NCR

The next machine should serve as the first formal CBP-1.0 implementation.

## Current state

The Vultr account currently has a **$250 promotional credit** available for benchmarking.

Initial candidate:

```text
Provider: Vultr
Region: Delhi NCR, India
Class: High Performance
CPU family: AMD-based plan
Candidate size: approximately 4 vCPU / 8 GB
```

The exact plan ID, storage allocation, advertised bandwidth, hourly price, and underlying exposed CPU model must be captured at provisioning time rather than assumed from prior discussions.

## Why this target matters

It provides:

- a much stronger machine than the GCP legacy baseline;
- a North-India region;
- a practical candidate for production workloads;
- a direct opportunity to test real price/performance rather than relying on public benchmark websites.

Prior network exploration from the user's North India connection found very low latency to Vultr Delhi, approximately **13 ms average RTT** in the earlier exploratory tests. This should be re-measured and stored formally under CBP-1.0.

## Required workflow

1. Provision the chosen Delhi instance.
2. Record plan/price/provider metadata before modifications.
3. Start CBP-1.0 at T001.
4. Complete tests one by one.
5. Preserve raw data.
6. Destroy unused billable resources after testing.
7. Record final actual cost/credit consumption.

---

# 11. Planned Oracle Cloud Free-Tier Benchmark

Oracle Cloud Infrastructure is an important future target because its Always Free resources provide an architectural contrast to the GCP shared-core baseline.

## 11.1 Primary target: OCI Ampere A1 Flex

As verified from Oracle's official documentation on 2026-09-13, Always Free tenancies currently receive:

```text
1,500 Ampere A1 OCPU-hours per month
9,000 GB-hours of memory per month
```

Oracle describes this as equivalent, for an Always Free tenancy, to approximately:

```text
2 OCPUs
12 GB RAM
```

using the ARM-based `VM.Standard.A1.Flex` shape.

Important:

- architecture: ARM64 / Ampere;
- benchmark binaries/packages must therefore be architecture-compatible;
- the same source-level benchmark methods should be used where possible;
- x86-specific binaries must not be substituted silently;
- PostgreSQL comparison is especially valuable because PostgreSQL runs natively on both architectures.

Oracle also documents Always Free AMD micro instances, currently up to two `VM.Standard.E2.1.Micro` instances, each in the very small micro class. These may be tested separately if available.

Oracle free-tier capacity and availability can change, and A1 capacity may be unavailable temporarily in a region. **Re-verify official limits immediately before provisioning.**

## 11.2 Oracle-specific research value

OCI A1 enables several useful comparisons:

### ARM vs x86

Compare:

- Ampere ARM64;
- AMD/Intel x86_64 cloud instances.

### Free-tier economics

Compare:

- GCP small free/shared instance;
- OCI Always Free A1;
- paid Vultr;
- later paid GCP/AWS/Hetzner plans.

### PostgreSQL efficiency

Evaluate whether PostgreSQL throughput per free-dollar / per vCPU differs substantially by architecture and provider.

### Memory effect

The OCI A1 free allocation has substantially more RAM than the original 1 GB GCP `e2-micro`, allowing analysis of:

- small working-set caching;
- large working-set behavior;
- SELECT performance;
- storage sensitivity.

## 11.3 Oracle execution plan

When ready:

1. create OCI tenancy / verify existing tenancy;
2. select home region carefully;
3. verify current Always Free eligibility;
4. provision `VM.Standard.A1.Flex` within free allowance;
5. record exact OCPU and RAM allocation;
6. record boot/block volume configuration;
7. run CBP-1.0 from T001 onward;
8. repeat PostgreSQL tests at scale 10 and scale 100;
9. compare against GCP and Vultr;
10. preserve ARM-specific installation notes but do not modify the core test semantics.

---

# 12. Additional Future Platforms

The following are planned candidate groups, not commitments.

## 12.1 Google Cloud

- rerun `e2-micro` under CBP-1.0;
- test a paid balanced 4-vCPU class later;
- optionally test a compute-optimized family;
- preserve disk class as an independent variable.

## 12.2 Hetzner Cloud

Candidate:

- Singapore region;
- CPX/shared AMD class comparable to Vultr 4 vCPU / 8 GB.

Research interest:

- provider-to-provider shared CPU variability;
- Singapore vs India user latency;
- price/performance;
- host-generation variability.

Do not assume previously observed public benchmark scores represent the provisioned machine. Measure the assigned host instance directly.

## 12.3 AWS

Potential future targets:

- burstable EC2;
- general-purpose EC2;
- Graviton ARM instance;
- Lightsail if useful.

Research interest:

- x86 vs Graviton ARM;
- burst-credit behavior;
- premium cloud pricing versus smaller VPS providers.

Exact free/trial eligibility must be verified at test time.

## 12.4 Microsoft Azure

Potential future target for a major hyperscaler comparison.

Research interest:

- general-purpose VM performance;
- regional latency;
- price/performance;
- variability.

## 12.5 Dedicated/Bare-Metal

Later compare cloud VMs against:

- rented dedicated servers;
- owned bare-metal server;
- colocated server;
- office/self-hosted machine.

This can answer whether cloud virtualization and convenience premiums are justified at larger scale.

---

# 13. Pricing Methodology

Price changes over time.

Never replace historical price with the provider's latest price.

For every run record:

```text
price_at_test_hourly
price_at_test_monthly_equivalent
currency
price_date
tax_included_or_excluded
ipv4_extra_cost
storage_extra_cost
traffic_allowance
promotion_applied
effective_cash_cost
```

Promotional credits must be recorded separately from list price.

Example:

```text
List price: $48/month
Promotional credit used: yes
Actual cash paid for run: $0
```

For economic comparisons, use **list/on-demand price at test date** unless the research question explicitly studies promotions.

Possible derived metrics:

```text
mixed_sustained_tps_per_usd
select_tps_per_usd
random_read_iops_per_usd
cpu_score_per_usd
ram_gb_per_usd
```

A later study may also calculate performance normalized by vCPU, RAM, or hourly cost.

---

# 14. Variability and Statistical Plan

If CloudMark develops into a research dataset, single measurements are insufficient.

## Minimum preferred research design

For each major configuration:

```text
n >= 3 independent runs
```

Preferably:

```text
n = 5 or more
```

for shared CPU/VPS plans where host contention may be substantial.

Where financially practical, provision more than one independent VM of the same plan, rather than repeating every run on a single VM forever.

## Report at least

- mean;
- median;
- standard deviation;
- minimum;
- maximum;
- coefficient of variation;
- sample size.

For latency distributions, preserve percentiles where the tool reports them.

## Test-order concern

Repeated tests can be affected by:

- caches;
- burst credits;
- thermal state;
- background provider contention;
- storage cache;
- time of day.

For research-grade runs, document test order and consider randomized or rotated test ordering where appropriate.

---

# 15. Potential Research Questions

The dataset may eventually support questions such as:

### RQ1

How closely do advertised vCPU counts predict sustained compute performance across cloud/VPS providers?

### RQ2

How large is the gap between burst and sustained performance for burstable/shared cloud instances?

### RQ3

Which providers deliver the best PostgreSQL OLTP performance per unit cost?

### RQ4

How does concurrency scaling differ across providers and instance families?

### RQ5

How variable is performance across repeated runs or independently provisioned instances of the same advertised plan?

### RQ6

How do ARM64 and x86_64 instances compare for PostgreSQL and general server workloads?

### RQ7

How strongly do storage class and RAM size influence PostgreSQL performance as the working set grows?

### RQ8

For interactive SaaS workloads, when does geographic latency outweigh moderate differences in backend compute speed?

### RQ9

At what monthly cloud spend does dedicated or owned hardware become economically competitive for a stable workload?

These are candidate directions only. A future paper should select a narrow research question after the dataset is sufficiently large.

---

# 16. Publication-Readiness Requirements

Do not call the dataset research-grade merely because it contains many machines.

Before using it in a paper, aim for:

- frozen protocol version;
- raw outputs retained;
- exact commands retained;
- exact software versions retained;
- provider/region/plan metadata retained;
- multiple repeated observations;
- preferably multiple provisionings per important shared plan;
- transparent exclusion/anomaly rules;
- historical pricing evidence;
- architecture differences documented;
- statistically defensible comparisons;
- no mixing of CBP-0 and CBP-1.0 observations without explicit qualification.

The legacy GCP result is useful but should remain clearly marked.

---

# 17. Practical SaaS/Application Benchmarking — Later Phase

Synthetic infrastructure benchmarks are only the first layer.

Once the target application is available, add a separate **Application Benchmark Profile** rather than modifying CBP core infrastructure tests.

Candidate actions:

```text
login
dashboard_load
search_record
create_record
update_record
submit_attendance_like_batch
fee/status_lookup
report_generation
background_job
webhook_processing
```

For Django/DRF systems record:

- requests/sec;
- median response time;
- p95;
- p99;
- error rate;
- CPU utilization;
- PostgreSQL activity;
- Redis activity;
- Celery queue behavior.

Keep application-level results separate from generic pgbench results.

---

# 18. Current Project State

## Completed

### GCP exploratory baseline

`LEGACY-GCP-001`

Useful PostgreSQL baseline exists.

### Vultr account/testing budget

A Vultr promotional balance of **$250** is currently available for testing.

## Next action

Provision the selected Vultr Delhi machine and begin:

```text
CBP-1.0
T001 — Machine and Environment Characterization
```

Do not begin with PostgreSQL immediately.

First characterize the machine so that every later result has trustworthy infrastructure metadata.

---

# 19. Copy-Paste Handoff Prompt for the Next Agent

Use the following when handing this project to a new AI agent:

> You are taking over the CloudMark cross-provider benchmarking project.
> 
> Read this handoff document completely before issuing commands.
> 
> The project is building a provider-neutral infrastructure benchmark dataset for engineering comparison now and potential academic analysis later.
> 
> The current standardized methodology is **CBP-1.0**.
> 
> Important operating rules:
> 
> - work ONE TEST AT A TIME;
> - preserve exact raw output;
> - keep raw and derived data separate;
> - do not optimize/tune the machine before establishing its default baseline;
> - distinguish burst performance from sustained performance;
> - do not silently change benchmark definitions between providers;
> - record exact provider, region, plan, CPU, RAM, storage, OS, kernel, PostgreSQL version, time, and price;
> - flag anomalies rather than deleting them;
> - never overwrite old runs;
> - do not treat `LEGACY-GCP-001` as equivalent to CBP-1.0 research-grade data;
> - do not infer user capacity directly from generic benchmark TPS.
> 
> Existing historical baseline:
> 
> - GCP `e2-micro`
> - PostgreSQL 18
> - pgbench scale 10
> - sustained mixed TPS approximately:
>   - c1: 90
>   - c4: 181
>   - c8: 191
>   - c16: 180
> - SELECT-only c1 sustained: approximately 747 TPS
> - all observed benchmark transactions: 0 failures
> 
> This baseline is `LEGACY-GCP-001 / CBP-0` and must be preserved only as a provisional historical baseline until GCP is rerun under CBP-1.0.
> 
> Current next target:
> 
> - Vultr
> - Delhi NCR
> - High Performance AMD class
> - likely around 4 vCPU / 8 GB
> - exact plan metadata must be captured after provisioning
> 
> Future targets include:
> 
> - standardized GCP e2-micro rerun;
> - Oracle Cloud Always Free Ampere A1 ARM instance;
> - Hetzner Singapore;
> - comparable AWS/Azure instances;
> - later dedicated/bare-metal systems.
> 
> Start with **CBP-1.0 / T001 — Machine and Environment Characterization** only.
> 
> Explain the purpose, provide only the commands for T001, tell me exactly what output to return/save, and then WAIT for my response.

---

# 20. Source/Provenance Notes

## Existing GCP measurements

The values in `LEGACY-GCP-001` were extracted from the prior benchmark conversation and the saved handoff titled:

`Postgress benchmark on GCP Free instance.md`

They are intentionally preserved as historical/provisional measurements.

## Oracle Free Tier facts

Oracle Free Tier details in this document were checked against Oracle's official Always Free documentation on 2026-09-13.

At that time Oracle documented:

- `VM.Standard.A1.Flex` as ARM-based Ampere A1;
- 1,500 A1 OCPU-hours/month;
- 9,000 GB-hours of memory/month;
- equivalent to 2 OCPUs + 12 GB RAM for an Always Free tenancy;
- up to two AMD `VM.Standard.E2.1.Micro` Always Free instances;
- a separate time-limited Oracle Free Trial offering.

These details are time-sensitive and must be re-verified before the Oracle benchmark is executed.

---

## End of Handoff

**Immediate next step:** provision Vultr Delhi candidate → record billing/plan metadata → run CBP-1.0 T001 only.
