# 4. Amin Vahdat: delivering value per gigawatt

**Amin Vahdat · Playlist position 4 · [Recording](https://www.youtube.com/watch?v=VeTqsCpcDgg)**

A research group rents a cluster for a week-long training run. The devices are busy, yet checkpoints repeatedly restart, workers wait for data, and the final model arrives late. Buying twice as many devices might accelerate arithmetic while increasing the number of components that can interrupt the job. The relevant question is how much verified progress the group receives for its power, money, and elapsed time.

Treat the cluster as a pipeline from provisioned power to scheduled execution to retained progress to completed tasks. Each section changes one part of that pipeline: failures reduce retained progress; imbalance limits execution; procurement determines available capacity; networking connects the workers; specialization changes efficiency for a workload. All numerical cluster data and formal developments below are original teaching constructions.

## 1. Capacity is an input, not an outcome [02:06](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=126s)

Vahdat resists judging infrastructure by capital expenditure or gigawatts alone. A large accelerator fleet has little value if it cannot be scheduled, if failures repeatedly interrupt useful computation, or if its users are waiting on storage and CPUs. The interviewer offers utilization figures; Vahdat redirects the discussion toward actual delivered value. Those figures should not be read as audited cross-company comparisons.

**Power** is a rate of energy use, measured in watts. **Energy** is power integrated over time. One gigawatt sustained for one hour consumes one gigawatt-hour. **Utilization** requires an explicit denominator: allocated devices, busy cycles, achieved floating-point operations, and useful completed tasks are different measures. **Goodput** counts useful progress or output after excluding wasted work under a stated definition.

**Teaching decomposition.** Let $P$ be provisioned IT power, $\eta$ nominal computation per joule, $u$ the fraction usable after allocation and scheduling, $g$ the fraction of executed work retained as useful progress, and $w$ useful computation required per completed task. A simplified throughput model is

$$Q=\frac{P\eta ug}{w}.$$

The factors must be measured without double counting losses. If $u$ already includes time lost to failed jobs, $g$ cannot subtract that same loss again. This equation is a bookkeeping device, not a universal performance law.

**Worked example.** Two equal-power systems have $(u,g)=(0.8,0.9)$ and $(0.6,0.98)$. At equal $\eta$ and $w$, their effective factors are 0.72 and 0.588. The first produces about 22.4% more useful output despite its worse progress-retention factor. To choose a system, measure the complete product rather than one attractive statistic.

### Keep the units and losses attached to the pipeline

In the throughput equation, $P$ is joules per second, $\eta$ is nominal operations per joule, and $w$ is retained useful operations per task. Their product and ratio therefore yield tasks per second. The dimensionless factors $u$ and $g$ describe different losses. If a device is idle because no job is assigned, charge the loss to scheduling. If it repeats arithmetic after a failed checkpoint, charge the loss to progress retention. A metric called “GPU utilization” rarely makes this distinction by itself.

Suppose the rented cluster has nominal capacity of 100 task-equivalents per hour. Scheduling makes 80 available, and restarts retain 90% of executed progress, leaving 72 completed-task equivalents. Improving scheduling to 90% produces 81, a gain of nine. Improving retention alone to 98% produces 78.4, a gain of 6.4. Cost and feasibility determine which intervention is preferable; ranking the percentages alone does not.

The multiplicative decomposition can be inspected through relative changes. Holding the other terms fixed, a 10% relative improvement in $u$ gives a 10% relative improvement in $Q$. Raising $u$ from 0.8 to 0.9 is a 12.5% relative increase, not ten percent. Near the upper bound of one, a factor has little remaining headroom. This makes the model useful for locating an opportunity, provided the factors are causally separable enough for the proposed intervention.

## 2. Reliability is a workload-dependent resource tradeoff [09:42](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=582s)

The lecture contrasts highly available customer services with training jobs that may accept interruption in exchange for greater capacity. It then explains why synchronous distributed computation is sensitive to individual failures. Many workers participate in one coordinated step; one missing participant can stop progress unless the software and hardware provide recovery.

**Numerical correction.** Using a 365-day year, allowed downtime is $8760(1-A)$ hours for availability $A$. At 99%, downtime is 87.6 hours; at 99.9%, 8.76 hours; at 99.999%, 0.0876 hours, or **5.256 minutes**. The recording's approximately 30-second phrase for five nines is arithmetically incorrect. Availability percentages also omit outage duration distributions and correlated failures.

**Teaching model.** If each of $n$ components is independently available with probability $a$ and every component is required, whole-system availability is $a^n$. For $a=0.999$ and $n=1000$, this is about 0.368. Independence is unrealistic for shared power or networking, and real systems use repair, redundancy, and reconfiguration. The model nevertheless shows why excellent component reliability is not sufficient for a large tightly coupled system.

**Checkpointing extension.** Let $c$ be checkpoint time, $\tau$ time between checkpoints, and $M$ mean time between job-interrupting failures. Under infrequent uniformly located failures and negligible restart overhead, the wasted-time fraction is approximately

$$f(\tau)=\frac c\tau+\frac{\tau}{2M}.$$

The first term is checkpoint overhead; the second is expected lost work per failure times failure frequency. Setting $f'(\tau)=0$ gives $\tau^*=\sqrt{2cM}$. With $c=2$ minutes and $M=1000$ minutes, the optimum is about 63.2 minutes. This approximation requires checkpoints to be small relative to the interval and the interval small relative to failure time; correlated failures and recovery cost require a richer model.

### Why the optimum is a square root

Over a long run, checkpointing every $\tau$ minutes spends approximately a fraction $c/\tau$ saving state. A failure uniformly located between checkpoints loses on average $\tau/2$ minutes of work. Multiplying by failure frequency $1/M$ gives the second term. Doubling the interval halves checkpoint overhead but doubles expected lost work. The optimum balances these opposing effects rather than minimizing either alone.

Differentiate to obtain $f'(\tau)=-c/\tau^2+1/(2M)$. Setting this to zero yields the square-root solution. Since $f''(\tau)=2c/\tau^3>0$ for positive times, it is a minimum. At that point the two loss terms are equal: with the numerical inputs each is approximately 0.0316, giving total modeled waste of 6.32%. An interval of ten minutes instead wastes about 20.5%; an interval of 200 minutes wastes about 11%.

If checkpoints become four times faster, the optimal interval halves. If interruptions become four times less frequent, it doubles. Both directions are sensible: cheap saving encourages frequent saving, while rare failure permits longer work intervals. A constant restart cost adds a separate approximate term proportional to $1/M$ and does not change this elementary optimum, but correlated failures, incomplete checkpoints, and interval-dependent restart behavior can change it.

```python
from math import sqrt


def checkpoint_plan(checkpoint_minutes, mtbf_minutes):
    if checkpoint_minutes <= 0 or mtbf_minutes <= 0:
        raise ValueError("Times must be positive")
    interval = sqrt(2 * checkpoint_minutes * mtbf_minutes)
    waste = checkpoint_minutes / interval + interval / (2 * mtbf_minutes)
    return interval, waste


interval, waste = checkpoint_plan(2, 1000)
assert 63.24 < interval < 63.25
assert abs(waste - sqrt(4 / 1000)) < 1e-12
assert checkpoint_plan(0.5, 1000)[0] == interval / 2
print(round(interval, 2), round(100 * waste, 2))
```

Run `python labs/check_chapters.py 4`; it prints `63.25 6.32`. The pure function accepts times in the same units and returns an interval plus a dimensionless waste fraction. It does not schedule checkpoints or inspect a real cluster. A restore drill is needed to establish that a checkpoint contains enough consistent state to resume useful work.

Independent component availability also deserves scrutiny. For a synchronous job that requires every worker, one shared power failure can disable all workers together. Adding nominally redundant devices behind the same power or network dependency does not create independent redundancy. A failure-domain map identifies components that can fail together; job placement and recovery should be evaluated against that map, not just per-device failure statistics.

## 3. System balance and moving bottlenecks [14:08](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=848s)

Vahdat emphasizes that computation, memory capacity, memory bandwidth, networking, CPUs, and storage must be proportioned to the workload. He invokes Amdahl's historical system-balance thinking. Do not turn an old numerical rule into a universal modern hardware ratio. The correct ratios depend on the amount and location of data moved by the actual algorithm.

Let a task require $F$ floating-point operations, $B_m$ bytes transferred from memory, and $B_n$ bytes transferred over a network. Let the respective capacities be $R_f$, $R_m$, and $R_n$ per second. Even with perfect overlap, execution time satisfies

$$T\ge\max(F/R_f,\ B_m/R_m,\ B_n/R_n).$$

If these phases cannot overlap, their times may instead add. The bound explains why improving a nonlimiting resource can leave runtime unchanged. For mixture-of-experts models, activating fewer parameters can reduce arithmetic while leaving difficult memory and communication demands.

**Worked example.** A task requires 20 ms of arithmetic, 50 ms of memory movement, and 10 ms of networking at the installed capacities. Under ideal overlap, the lower bound is 50 ms. Doubling arithmetic capacity lowers its contribution to 10 ms but leaves the bound unchanged. Doubling memory bandwidth lowers the bound to 25 ms. Real performance needs measurement because overlap and software overhead may invalidate the idealization.

For the week-long job, record a trace of step time decomposed into useful device work, communication, input preparation, and waiting. The lower bound is useful because no scheduling cleverness can make a required transfer exceed its physical capacity. It is not a prediction that the lower bound is achieved. Dependencies can force phases to execute sequentially, and many small transfers can be dominated by per-message latency rather than total bytes divided by bandwidth.

The [Roofline technical report](https://digital.library.unt.edu/ark:/67531/metadc934195/) supplies a related computation-versus-memory view. Define arithmetic intensity as operations performed per byte moved from a specified memory level. The level matters: bytes moved within a fast cache are not equivalent to bytes arriving from remote storage. Improving data reuse can raise intensity, moving a workload toward the compute limit without buying more arithmetic units.

The bottleneck can move after a successful fix. Once memory movement drops from 50 to 25 ms, arithmetic at 20 ms is close behind. A second bandwidth doubling lowers the memory contribution to 12.5 ms, making arithmetic the limiting term in the ideal model. Investment should be reevaluated after each substantial change; the first bottleneck is not a permanent identity of the application.

## 4. Procurement is planning under uncertainty [20:31](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=1231s)

The lecture describes long lead times and the need to commit before demand is known. Land, grading, buildings, utility agreements, chips, and memory are different commitments. Some can be prepared early at modest cost; others create large irreversible obligations. The value of shortening a lead time is therefore partly the value of postponing a forecast until better information arrives.

**Teaching derivation.** Let $D$ be uncertain future demand and $q$ committed capacity. Let $c_u$ be the cost per unit of unmet demand and $c_o$ the cost per unit of excess capacity. Write $(x)_+=\max(x,0)$ for the positive part and $\mathbb E$ for expectation over demand. Expected mismatch cost is

$$J(q)=c_u\mathbb E[(D-q)_+]+c_o\mathbb E[(q-D)_+],$$

where $(x)_+=\max(x,0)$. For a continuous demand distribution with cumulative distribution function $F_D$, the derivative is $-c_u[1-F_D(q)]+c_oF_D(q)$. Thus the optimum satisfies $F_D(q^*)=c_u/(c_u+c_o)$.

If shortage costs four times as much as excess, the optimal commitment is the 80th percentile, not the mean forecast. This single-period model omits financing, demand response, capacity resale, and staged expansion. It makes the asymmetry explicit rather than concealing it in an arbitrary safety margin.

The derivative has a direct operational interpretation. Buying one more small unit saves shortage cost only in states where demand exceeds committed capacity, with probability $1-F_D(q)$. It creates excess cost only in states where demand is lower, with probability $F_D(q)$. At the optimum the expected marginal saving equals expected marginal cost. This argument explains the percentile without requiring the demand distribution to be symmetric.

For an illustrative uniform demand distribution from 60 to 100 device units, the 80th percentile is 92. Committing to the mean, 80, would underweight the specified shortage penalty. If uncertainty narrows to 70 through 90 while the same cost ratio applies, the optimum is 86. Better information can reduce the excess buffer while preserving the preferred probability of coverage. Shorter procurement lead times create value partly by making such information available before commitment.

A commitment is not always all-or-nothing. Reserving a site option, completing design work, or negotiating a contingent supply agreement may preserve the ability to expand later at a smaller initial cost. The correct model then includes sequential decisions and the value of information. Do not insert an arbitrary “option value” into the one-period formula; specify the future decision, its price, and what uncertainty will be resolved first.

## 5. Optical reconfiguration and collective communication [31:31](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=1891s)

Vahdat explains optical circuit switches as programmable physical connections. In his example, a spare rack can replace a failed rack in a topology, and large jobs can receive high-bandwidth paths toward needed storage. Electrical packet switching remains part of the system. The point is matching the switching mechanism to traffic timescales, not declaring one technology universally superior.

An **all-reduce** combines values contributed by participants and returns the combined result to all of them. An **all-to-all** allows each participant to send different data to every other participant. They impose different communication demands. A topology suitable for regular reduction traffic may perform poorly for arbitrary exchange unless algorithms and placement exploit its structure.

**Research extension.** [Jouppi et al., TPU v4](https://arxiv.org/abs/2304.01433) provides a primary technical account of optical topology reconfiguration and specialized embedding support. Its measured results concern the systems and workloads in that paper; they are not a current universal ranking of TPUs versus GPUs.

Suppose reconfiguration costs $t_r$ seconds and saves $\Delta T$ per job. It is beneficial for that job only if $\Delta T>t_r$, before considering effects on other jobs. A 2-second reconfiguration that saves 20 minutes of communication is easy to amortize; one repeated for every 1-millisecond request is not. Optical topology changes need not occur at packet timescales to be useful.

For the running job, distinguish communication volume from the placement of that volume. If every worker needs a global reduction, an algorithm can combine partial results along a structured route. If each expert sends tokens to many different experts, traffic depends on routing and placement. Two jobs moving the same total bytes can have different hotspots and completion times. Topology is part of the algorithm's execution environment.

Reconfiguration also consumes an opportunity shared with other jobs. A topology that accelerates the large training run can lengthen inference requests or interfere with storage access. Evaluate the change over the admitted workload set, with declared priorities and isolation requirements. The TPU v4 paper demonstrates why co-design of topology, workload, and hardware matters; it does not eliminate this scheduling decision for another installation.

## 6. Specialization, hardware lifetime, and community constraints [37:42](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=2262s)

The questions address continued use of older hardware, dynamic replanning, robotics, and specialization. At [46:22](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=2782s), Vahdat explains that different memory/compute/network ratios can justify distinct designs for training and inference. A general device retains flexibility; a specialized device earns its advantage only on workloads it serves well.

At [55:20](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=3320s), he names energy as a particularly difficult constraint, then discusses generation, storage, and longer-horizon possibilities. At [60:01](https://www.youtube.com/watch?v=VeTqsCpcDgg&t=3601s), he discusses water, power efficiency, demand response, and community impact. These commitments and tradeoffs are reported as his account, not a site-by-site environmental audit.

**Definition.** Power usage effectiveness is $\mathrm{PUE}=P_{\rm facility}/P_{\rm IT}$, using consistent boundaries and measurement periods. Lower PUE means less facility overhead per unit of IT power. It says nothing by itself about whether the IT computation is useful, water scarcity, carbon intensity, or total energy demand. A design can have better PUE and worse local water consequences.

For a one-person frontier lab, reproduce this reasoning at small scale: profile one real workload, separate compute and I/O time, inject a recoverable failure, and measure cost per verified completion. This is a more informative infrastructure project than a dashboard showing only peak device specifications.

A lower PUE can coexist with lower useful progress. If facility power falls from 12 to 11 MW at the same 10 MW IT draw, PUE improves from 1.2 to 1.1. But if the new workload wastes twice as much device time on retries, the facility may consume more energy per completed result. Combine the boundary-consistent facility measure with useful throughput: energy per task is facility power divided by tasks per second, with matching units and time windows.

**Limits.** The pipeline assumes losses can be separated without double counting. The checkpoint model assumes sparse failures; the capacity model assumes a one-period cost structure; the bandwidth model gives a lower bound. Site water use, electricity emissions, and community effects require local measurements. No device count or single efficiency ratio establishes all of these outcomes.

## Exercises and worked solutions

1. Convert 99.99% availability into annual downtime.
2. With checkpoint cost 1 minute and mean interruption time 720 minutes, find the approximate checkpoint interval.
3. A facility draws 12 MW and IT equipment draws 10 MW. Compute PUE and facility overhead as a fraction of total power.
4. If excess capacity costs 3 per unit and shortage costs 7, which demand percentile does the simple planning model choose?

<details><summary>Solutions and discussion</summary>

1. The unavailable fraction is $1-0.9999=0.0001$. Multiplying by 8,760 hours gives 0.876 hours, then multiplying by 60 gives 52.56 minutes. The result is an annual aggregate allowance, not a guarantee that no outage lasts longer than a minute. One long outage and many brief outages can have the same availability and different consequences.
2. Substitute the times into the stationary condition to obtain $\tau=\sqrt{1440}\approx37.95$ minutes. Check the two waste terms: $1/37.95\approx0.02635$ and $37.95/1440\approx0.02635$. Their equality is an independent check on the optimum. The approximately 5.27% total waste omits restart and correlated-failure effects; it should be compared with a measured restore experiment.
3. Divide facility power by IT power: $12/10=1.2$. The overhead is the difference, 2 MW. Relative to facility power that is one sixth, or 16.7%; relative to IT it is one fifth, or 20%. A claim of “20% of total energy overhead” would therefore use the wrong denominator for these inputs. Neither fraction measures useful computation or water impact.
4. The marginal balance is $7[1-F_D(q)]=3F_D(q)$. Solving yields $F_D(q)=0.7$. More expensive shortage pushes the commitment above the median. If demand has discrete masses, an exact equality need not be available; choose a capacity whose cumulative probability crosses the critical fraction and compare adjacent feasible commitments. A percentile rule still depends on an adequately estimated demand distribution.

</details>

## Primary sources and attribution

- [Stanford recording](https://www.youtube.com/watch?v=VeTqsCpcDgg) — the operational arguments and interview examples.
- [Jouppi et al. (2023), TPU v4](https://arxiv.org/abs/2304.01433) — optical reconfiguration and hardware specialization.
- [Williams, Waterman, and Patterson (2009), Roofline, archived technical report](https://digital.library.unt.edu/ark:/67531/metadc934195/) — computation/data-movement performance model.

**Coverage note.** The interview's main progression and technical questions are retained; personal career anecdotes are compressed. Checkpoint optimization, capacity planning, and the numerical cases are authored extensions. Numerical availability claims are corrected explicitly rather than silently copied.
