# 7. Scott Nolan: energy bottlenecks

**Scott Nolan · Playlist position 7 · [Recording](https://www.youtube.com/watch?v=wisccQYTRQc)**

The lecture traces a proposed chain of constraints from AI deployment to electricity, nuclear generation, and fuel supply. Nolan is developing an enrichment business, so his identification of the decisive bottleneck is both an engineering thesis and a commercial perspective. The chapter tests the chain rather than treating it as the only possible energy future.

A proposed data center has a signed accelerator order but no firm date for its electricity connection. Its planners consider grid supply, a local generation portfolio, and postponing part of the load. One supplier promises abundant annual energy; another promises dependable delivery at the required location. Those offers are not equivalent. The decision requires a time-indexed chain from equipment and permits to power and useful computing.

Carry this hypothetical project through the chapter. Its state contains computing capacity, hourly power supply, stored energy, and prerequisite completion dates. A bottleneck is defined relative to the project's required service date and workload. Improving a component matters only if it relaxes a constraint on that service.

## 1. Follow the dependency chain [00:08](https://www.youtube.com/watch?v=wisccQYTRQc&t=8s)

The introduction situates model development within data centers and power systems. At [07:31](https://www.youtube.com/watch?v=wisccQYTRQc&t=451s), Nolan describes his engineering and investment background and the investigation that led him to nuclear fuel. The methodological lesson is to ask which upstream condition must hold before a downstream capability can be delivered.

A **bottleneck** is a binding constraint on an explicitly defined objective over a given horizon. It need not be the most expensive component. A low-cost transformer that cannot arrive for two years can delay a high-value facility. Bottlenecks can move after an intervention, and one region's bottleneck need not bind another region.

Let $Q$ be useful computing service, $C$ available computing capacity, $E$ available energy over the period, and $e$ energy per service unit. A basic constraint is $Q\le\min(C,E/e)$. Fuel supply matters through additional links only if the chosen generation path depends on that fuel. The existence of those links does not establish that all alternatives are inferior.

### A constraint must bind before relaxing it helps

Suppose computing equipment can supply 100 service units per day, while available electricity supports only 60. Raising equipment capacity to 150 changes neither the minimum nor delivered service. Raising electricity to support 90 units can raise service to 90, assuming no omitted constraint binds first. Once electricity supports 120, computing becomes the binding limit at 100. This is why the bottleneck can move after a successful intervention.

The energy constraint is necessary but too coarse for an always-on service. A year's worth of energy arriving during the wrong hours cannot run equipment continuously without storage or flexible scheduling. Add delivery location, time, voltage and connection requirements, reliability, and the permitted shape of demand. A batch training job that can pause differs from a voice service that must respond immediately. The same energy resource can be useful to one workload and inadequate for another.

This distinction makes a practical research method: write a dependency graph and ask what observation would prove each proposed bottleneck is binding. A vendor's difficulty supplying one input does not establish that this input determines the customer's completion date. The planner must compare all critical prerequisites, including ones outside the vendor's business.

## 2. Stranded power and the difference between energy and firm capacity [12:55](https://www.youtube.com/watch?v=wisccQYTRQc&t=775s)

Nolan describes locating flexible computing near power that lacked nearby demand, then argues that new generation is needed as demand grows. **Stranded energy** is energy whose economic use is constrained by location, transmission, timing, or lack of demand. It is not necessarily free, continuous, or suitable for every workload.

**Nameplate capacity** is rated power output. **Capacity factor** is actual energy generated divided by the energy that continuous rated operation would have produced over the same period. **Firm capacity** concerns dependable contribution when the system needs power. Annual average output alone does not establish firm supply.

**Worked example.** A 100 MW IT load with PUE 1.2 requires 120 MW of facility power. Continuous annual consumption is $120\times8760=1{,}051{,}200$ MWh, about 1.051 TWh. A hypothetical solar system with 25% capacity factor would need 480 MW nameplate merely to match annual energy, before storage losses and curtailment. It would not thereby supply 120 MW every hour.

To bridge 12 hours at 120 MW, storage must deliver 1,440 MWh. If usable state-of-charge range is 80% and discharge efficiency is 90%, required nameplate stored energy is $1440/(0.8\times0.9)=2000$ MWh. Charging losses and multi-day weather gaps add requirements. This illustrative calculation is not a full least-cost design; a portfolio of generation, transmission, storage, and flexible demand can change the answer.

### The storage state makes the missing time dimension explicit

Let $S_t$ be stored energy at the start of hour $t$, in MWh. Let $c_t$ be average charging power and $d_t$ average delivered discharging power in MW during that hour. With charge efficiency $\eta_c$ and discharge efficiency $\eta_d$, the hourly state update is $S_{t+1}=S_t+\eta_c c_t\Delta t-d_t\Delta t/\eta_d$, where $\Delta t$ is one hour. Stored energy must remain between zero and its usable capacity, while charge and discharge powers have separate equipment limits.

If generation is $g_t$, imports are $i_t$, and load is $\ell_t$, the instantaneous accounting condition is $g_t+i_t+d_t\ge\ell_t+c_t$, allowing excess to be curtailed. Summing this condition over a year discards the state constraints. That is precisely why matching annual energy is insufficient. A design can have enough annual generation and still exhaust storage during a long low-output period.

The following minimal balance check omits charging and models only a specified outage. It accepts delivered load, duration, usable storage fraction, and discharge efficiency. It returns nameplate energy in MWh. It has no external effects and cannot establish the adequacy of a yearly supply portfolio.

```python
def storage_required(load_mw, hours, usable_fraction, efficiency):
    if load_mw < 0 or hours < 0:
        raise ValueError("Load and duration must be nonnegative")
    if not 0 < usable_fraction <= 1 or not 0 < efficiency <= 1:
        raise ValueError("Fractions must lie in (0, 1]")
    return load_mw * hours / (usable_fraction * efficiency)


capacity = storage_required(120, 12, 0.8, 0.9)
assert abs(capacity - 2000) < 1e-9
assert storage_required(120, 0, 0.8, 0.9) == 0
assert abs(storage_required(120, 24, 0.8, 0.9) - 2 * capacity) < 1e-9
print(round(capacity, 1))
```

Run `python labs/check_chapters.py 7`; it prints `2000.0`. A battery with this energy capacity still needs at least 120 MW of discharge capability for the example. Energy capacity determines how long it can sustain output; power capacity determines how fast it can deliver it. The distinction mirrors model storage versus memory bandwidth in compute systems: sufficient quantity is not sufficient delivery rate.

## 3. Nuclear generation and fuel are different industries [16:03](https://www.youtube.com/watch?v=wisccQYTRQc&t=963s)

Nolan argues for nuclear's role in reliable low-carbon electricity, then shifts upstream to fuel. At [18:31](https://www.youtube.com/watch?v=wisccQYTRQc&t=1111s), he outlines mining, conversion, enrichment, deconversion, and fabrication. Enrichment changes isotopic composition; it is not itself an electricity-generating reactor. A functioning fuel supply chain does not by itself solve reactor licensing, construction, financing, or grid connection.

**Primary-source clarification.** The [NRC identifies an operating URENCO USA enrichment facility in New Mexico](https://www.nrc.gov/facilities-safety/fuel-cycle-facilities/new-fuel-cycle-facility-licensing/gas-centrifuge-enrichment-facility-licensing). Therefore a statement that the United States has essentially no enrichment must distinguish U.S. location from U.S.-owned technology and companies, and distinguish conventional fuel from HALEU. The lecture's small market-share figure lacks enough denominator detail to use as a general measure of domestic physical production.

[DOE defines HALEU](https://www.energy.gov/ne/articles/what-high-assay-low-enriched-uranium-haleu) as uranium enriched above 5% and below 20% in uranium-235. Some advanced reactor designs use it; not all small modular reactors have identical fuel requirements. Supply analysis needs the specific reactor design, fuel specification, delivery date, and qualified fabrication route.

**Environmental interpretation.** Nuclear power has low lifecycle greenhouse-gas emissions, but operational emissions and lifecycle emissions are not identical. A universal ranking such as “lowest carbon” requires a defined dataset, technology, and boundary. Accident-related direct radiation deaths, evacuation consequences, chronic health effects, and modeled avoided fossil-fuel harm are also different quantities. The recording's brief comparisons do not establish all of them.

For the data center, selecting a nuclear supply path creates several distinct dependencies. A reactor must exist or be built, operate under its license, receive qualified fuel, deliver power through an available connection, and satisfy the commercial agreement. Fuel that arrives before the reactor is ready does not supply electricity. A completed reactor without a qualified fuel route is also insufficient. Map the path using service milestones rather than collapsing it into one category called nuclear capacity.

Supplier ownership, physical location, qualified output, and delivery availability answer different questions. A domestic facility operated by a foreign-owned company can contribute domestic physical capacity without satisfying a policy goal for domestically owned technology. The NRC source above supports the location-and-operation distinction; it does not resolve every strategic objective. Clear denominators prevent a discussion of one objective from becoming a misleading claim about another.

## 4. Infrastructure primitives and staged learning [21:48](https://www.youtube.com/watch?v=wisccQYTRQc&t=1308s)

The conversation connects Bitcoin-era infrastructure to later AI uses. Nolan emphasizes a reusable primitive—making a basic capability cheaper or more available—rather than the first application alone. Launch capacity and fuel services are his examples. A pivot can preserve hard-won engineering knowledge even when the customer-facing application changes.

**Teaching model.** Let $K$ be fixed infrastructure cost, $v$ variable cost per unit, and $q$ cumulative service delivered. Average cost is $AC(q)=K/q+v$. Spreading fixed cost over more output lowers average cost, but only if utilization, maintenance, and customer demand support the larger volume. This is an accounting effect, not proof of a technological learning curve.

For a hypothetical reusable test facility costing 1 million units with 1,000 units of variable cost per experiment, average cost is 11,000 at 100 experiments and 2,000 at 1,000 experiments. If only 100 experiments are valuable, doing 900 useless ones does not create an economic gain. The denominator must count useful service.

The derivative $dAC/dq=-K/q^2$ is negative for positive fixed cost and output. This decline follows entirely from spreading the same fixed cost over more units. A technological learning curve makes a different claim: unit input requirements decline with accumulated experience. Both mechanisms can occur together, but one can exist without the other. A facility operating unchanged machinery at higher utilization can lower average cost without learning a better process.

For the recurring project, a reusable planning primitive might be a source-linked database of interconnection milestones, equipment lead times, and contractual dependencies. Its value comes from reducing repeated research and revealing inconsistent assumptions across candidate sites. A model that extracts dates should preserve the document version and whether a date is promised, permitted, planned, or completed. Treating all dates as interchangeable can create an apparently precise but unusable schedule.

At [31:01](https://www.youtube.com/watch?v=wisccQYTRQc&t=1861s), Nolan recommends selecting important unsolved problems where one's skills are unusually useful. For a solo builder, the analogous opportunity may be measurement, planning software, document extraction, or operational coordination within an infrastructure workflow rather than owning the physical plant.

## 5. Funding, execution, and what an award proves [32:08](https://www.youtube.com/watch?v=wisccQYTRQc&t=1928s)

The interview details forming a team, selecting a Kentucky site, and aligning private investment with government support. [DOE's January 5, 2026 announcement](https://www.energy.gov/articles/us-department-energy-awards-27-billion-restore-american-uranium-enrichment) independently lists a 900-million-dollar award for General Matter to create domestic HALEU enrichment capacity. An award supports the existence of a funded program; it does not demonstrate completed facilities, delivered fuel, or realized future hiring.

**Teaching extension: construction time and economics.** Let $C_t$ be cost in year $t$, $E_t$ generated electricity in that year, $r$ the annual discount rate, and $T$ the analysis horizon in years. A levelized cost calculation divides discounted lifecycle costs by discounted energy production:

$$\mathrm{LCOE}=\frac{\sum_{t=0}^T C_t/(1+r)^t}{\sum_{t=0}^T E_t/(1+r)^t}.$$

Here $C_t$ is cost in year $t$, $E_t$ generated electricity, $r$ the discount rate, and $T$ the analysis horizon. The [EIA methodology](https://www.eia.gov/outlooks/aeo/electricity_generation/pdf/LCOE_methodology.pdf) provides the primary reference. LCOE alone does not price hour-by-hour usefulness, grid integration, or delivery risk.

If 1 billion units is committed now and receives no offsetting cash flow for three years, its capitalized amount at 8% is $10^9(1.08)^3\approx1.260$ billion. That 260-million difference illustrates the cost of time; it is not a complete construction-finance model. A cheaper nominal design that arrives much later can lose economically to a more expensive design available when needed.

### What the levelized number is solving

Under the simplified discounted model, suppose electricity is sold at a constant real price $p$ per MWh. Discounted revenue is $p\sum_t E_t/(1+r)^t$. Setting that equal to discounted costs and solving for $p$ gives the LCOE expression. It is therefore the constant unit price that balances the two discounted streams under the model's assumptions. All costs, prices, and the discount rate must use consistent real or nominal conventions.

Two portfolios can have the same LCOE and different value to the data center. One may produce when the facility needs power; another may require storage, transmission, or curtailed demand. Conversely, a higher-LCOE source can reduce the need for costly backup. The [EIA methodology](https://www.eia.gov/outlooks/aeo/electricity_generation/pdf/LCOE_methodology.pdf) supplies the cost framework; the project's hourly service requirement supplies an additional adequacy question.

The government award discussed in the recording reduces one financing uncertainty. It does not set the completion date of every dependent project. Distinguish an announced award, an executed agreement, funded work, a completed facility, qualified output, and delivered service. Each milestone is evidence about a different transition. In the project graph, money can enable a task without proving that the task has finished.

## 6. Timelines, alternative paths, and the closing questions [42:36](https://www.youtube.com/watch?v=wisccQYTRQc&t=2556s)

Nolan distinguishes nearer-term power procurement from nuclear capacity expected later. He discusses space-based possibilities as speculative, then recounts early SpaceX iteration and the experience gained while a company scales. The later questions address public acceptance, European policy, uranium-producing countries, and the historical loss of U.S.-owned enrichment capacity.

Treat the assertions about national energy outcomes as hypotheses requiring generation and emissions data. A map comparing two countries at one moment does not identify the causal effect of one policy; weather, demand, imports, industrial structure, and fuel prices confound the comparison. The useful research question is what generation would have occurred under a clearly specified counterfactual.

**Original project.** Build an infrastructure lead-time model with nodes for permitting, equipment, construction, fuel qualification, and interconnection. Record a source and uncertainty interval for each duration. Calculate the critical path and examine which one-month reduction most advances service delivery. Keep speculative dates visibly separate from contractual or completed milestones.

For parallel prerequisites of 12, 18, and nine months followed by six months of integration, completion takes 24 months. Reducing the nine-month prerequisite to one month changes nothing. Reducing the 18-month prerequisite to 14 saves four months. Reducing it below 12 exposes a different critical path. This is a precise way to distinguish valuable acceleration from impressive local progress.

Uncertain durations require scenarios rather than adding every best-case date. Shared causes such as financing or permitting changes can delay several tasks together. Independent random sampling would understate such correlated schedule risk. A useful first model reports an optimistic, central, and adverse scenario with named common causes, then updates the evidence as milestones become observable.

**Limits.** Annual energy, storage duration, average cost, and critical-path calculations each answer a narrow question. They do not establish a complete generation portfolio, a national-policy counterfactual, or an investment return. The lecture's fuel thesis is one conditional path through the dependency graph; alternatives should be compared at a common delivery date, location, reliability requirement, and cost boundary.

## Exercises and worked solutions

1. A 50 MW IT load has PUE 1.3 and runs at that load continuously. Find annual facility energy.
2. Why does a 90% capacity factor not guarantee 90% availability during a particular peak-demand week?
3. A project's parallel prerequisites take 12, 18, and 9 months, followed by 6 months of integration. Which prerequisite should be shortened first?
4. What would falsify the claim that fuel supply is the binding constraint on a proposed data-center project?

<details><summary>Solutions and discussion</summary>

1. Multiply the IT draw by PUE to obtain facility power $50(1.3)=65$ MW. Multiplying by 8,760 hours gives 569,400 MWh, or 0.5694 TWh. This assumes that load and PUE remain constant. A changing workload requires integrating actual facility power over time; nameplate power alone is insufficient.
2. Construct a counterexample in which almost all annual downtime occurs during the selected peak week. Annual generation can still yield a 90% capacity factor while availability during that week is very low. Capacity factor constrains an annual energy integral, not the temporal location of output. Dependable capacity requires a reliability analysis tied to the demand periods of interest.
3. Integration begins only after all three prerequisites, so its start is the maximum duration, 18 months. Adding six gives 24. Shorten the 18-month branch first; after it reaches 12, another branch becomes critical. If shortening costs differ, compare cost per month of actual completion-date improvement rather than cost per month removed from an arbitrary task.
4. Find a counterfactual in which additional qualified fuel does not advance delivered service: for example, interconnection remains unavailable after fuel delivery. That shows fuel is not the binding timing constraint in that scenario. Alternatively, demonstrate a feasible portfolio that meets the same service requirement without the fuel path. Merely naming another technology is insufficient; its date, capacity, reliability, and economics must satisfy the project's stated constraints.

</details>

## Primary sources and attribution

- [Stanford recording](https://www.youtube.com/watch?v=wisccQYTRQc) — Nolan's energy and company-building thesis.
- [NRC enrichment-facility history](https://www.nrc.gov/facilities-safety/fuel-cycle-facilities/new-fuel-cycle-facility-licensing/gas-centrifuge-enrichment-facility-licensing) — domestic-facility clarification.
- [DOE HALEU explanation](https://www.energy.gov/ne/articles/what-high-assay-low-enriched-uranium-haleu) — fuel terminology.
- [DOE enrichment awards](https://www.energy.gov/articles/us-department-energy-awards-27-billion-restore-american-uranium-enrichment) — independently checked award.
- [EIA LCOE methodology](https://www.eia.gov/outlooks/aeo/electricity_generation/pdf/LCOE_methodology.pdf) — economic reference.

**Coverage note.** The source sequence is retained through the closing fuel-history discussion. Energy/storage arithmetic, financing calculations, critical-path exercise, and causal-analysis cautions are independent additions. The chapter does not provide enrichment process instructions or represent investment advice.
