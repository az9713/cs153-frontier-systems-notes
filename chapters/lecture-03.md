# 3. Joe Sullivan: the road ahead and resilience

**Joe Sullivan · Playlist position 3 · [Recording](https://www.youtube.com/watch?v=g50FHC-PzK8)**

This lecture combines personal history, an account of the Uber breach litigation, incident communication, operational resilience, and AI security. A first-person account is evidence of the speaker's perspective. It is not a substitute for a judicial opinion or an independently established incident chronology. The models below are original teaching extensions.

Consider a company whose document-processing assistant suddenly loses access to its primary database. Staff cannot tell whether this is a credential error, a destructive intrusion, or a provider outage. Restoring the service quickly matters, but reconnecting a compromised account could expose more documents. A useful response must improve both service state and knowledge of the incident, without confusing one with the other.

Use an **incident state** comprising delivered service, preserved evidence, access authority, and unresolved hypotheses. A containment action changes what an account can do. A forensic observation changes which hypotheses the team can support. A recovery action changes delivered service. Keeping these objects separate prevents the common mistake of treating a green status page as evidence that the whole incident is resolved.

## 1. Trust at the boundary of technology and government [00:09](https://www.youtube.com/watch?v=g50FHC-PzK8&t=9s)

Sullivan describes moving from prosecution into security leadership at internet companies. The recurring problem is cooperation between organizations with different incentives. A company may fear that reporting an incident creates reputational damage; investigators need disclosure to identify and prosecute wrongdoing. A technically useful channel can fail if its participants do not trust how information will be used.

The eBay discussion supplies a second example: a marketplace needs buyers and sellers to trust transactions with strangers. Security is therefore part of the service's enabling infrastructure, rather than an unrelated cost center. As platforms become more consequential, the consequences of security failures spread beyond the direct operator.

**Teaching definition.** A **security control** is a mechanism intended to prevent, detect, contain, or recover from an unwanted event. These functions are distinct. Preventing unauthorized access does not ensure recovery from a destructive event; restoring a service does not establish that copied data has been deleted.

### Trust needs a testable boundary

The document assistant may be permitted to read one project folder and create a draft summary. Giving it an identity establishes which principal made a request; giving it a narrow capability establishes which requests can succeed. Neither proves that the documents it reads are accurate or that a draft is correct. Authority, evidence quality, and task performance answer different questions.

A useful control has a failure model. A read-only credential prevents writes through the service that enforces that credential. It does not prevent a separate tool from writing elsewhere, and it does not prevent disclosure of readable data. A backup permits recovery only if it is independent enough to survive the incident, decryptable, and restorable within the target period. State these boundaries before assigning a control a reassuring name.

For the recurring incident, first preserve the evidence needed to distinguish a revoked credential from active misuse. Record identifiers, authoritative timestamps, relevant access events, and the scope of observed failures. “The database is down” is a hypothesis until the team knows whether the failure is global, account-specific, or limited to one network route. Narrowing that claim can avoid a disruptive recovery action that does not address the actual problem.

## 2. Transparency and the Uber case [08:03](https://www.youtube.com/watch?v=g50FHC-PzK8&t=483s)

Sullivan recounts his dismissal, its personal effects, and his subsequent work at Cloudflare. At [11:32](https://www.youtube.com/watch?v=g50FHC-PzK8&t=692s), he describes leadership treating incident documentation and public explanation as part of the response. At [15:04](https://www.youtube.com/watch?v=g50FHC-PzK8&t=904s), he turns to criminal charges and presents his account of internal approvals and the treatment of the attackers through a bug-bounty process.

**Independent primary-source check.** The Ninth Circuit's [amended opinion, filed November 12, 2025](https://cdn.ca9.uscourts.gov/datastore/opinions/2025/11/12/23-927.pdf), affirmed Sullivan's convictions for obstruction of justice and misprision of a felony. Its account and legal analysis must be read alongside his presentation. His favorable characterization of sentencing is not an acquittal or reversal of the convictions. These notes do not infer a general legal permission rule from the anecdote.

A **vulnerability disclosure program** defines how researchers can report weaknesses and the authorized scope of testing. A **bug bounty** adds rewards under specified conditions. Calling a payment a bounty does not by itself determine the legal status of access, copied data, disclosure, or concealment. Scope and authorization should be established before testing, with jurisdiction-specific legal advice for actual incidents.

The engineering lesson is to separate four records: what happened, what evidence supports it, who made each decision, and what obligations were assessed. A message stating “legal approved” is much less informative than a dated decision that identifies the facts, uncertainty, responsible people, and escalation triggers. Documentation supports accountability; it is not immunity.

In the case company, the initial decision record might say: “At 09:10, requests using account A received an authorization error; requests with a separately controlled diagnostic account succeeded. No evidence yet establishes deletion or disclosure. Account A is suspended pending review.” This preserves an observation, its scope, and an action. Rewriting it later as “the attacker was blocked at 09:10” would add a conclusion that was not known then.

Use an append-only correction when the interpretation changes. If later logs show a policy rotation caused the outage, record that finding with the supporting events and the time it became known. The earlier containment may have been reasonable under uncertainty even though the alarming hypothesis was false. Conversely, a good outcome does not prove a poorly supported decision was sound. Evaluate the decision against the evidence and options available at the time.

A record should also distinguish factual confidence from responsibility. Technical staff can identify affected systems; legal specialists assess actual reporting duties; authorized leaders decide among operational alternatives. A shared document can coordinate these roles without allowing a model-generated summary to invent an approval. This is an engineering design for accountability, not a legal safe harbor or a substitute for the governing rules in a particular incident.

## 3. Personal recovery and organizational resilience [26:37](https://www.youtube.com/watch?v=g50FHC-PzK8&t=1597s)

Sullivan describes nonprofit work, support from colleagues and family, and returning to professional life. These passages explain the lecture's title. At [33:32](https://www.youtube.com/watch?v=g50FHC-PzK8&t=2012s), he extends resilience from the individual to the organization: security must address loss of operations as well as loss of data.

**Availability** is the ability to obtain a service when needed. **Recovery time objective (RTO)** is the target maximum time to restore a specified service after disruption. **Recovery point objective (RPO)** is the target maximum amount of data loss measured backward in time. A backup created every day can still miss an RPO of one hour. An unreadable or untested backup provides no demonstrated recovery capability.

**Teaching model.** Let $q(t)\in[0,1]$ be the fraction of normal service delivered at time $t$ after an incident, and $v$ the value of full service per hour. Lost service value over horizon $T$ is

$$L=v\int_0^T[1-q(t)]\,dt.$$

This measures the area under the service-deficit curve. It excludes litigation, data exposure, physical effects, and reputation. Those need additional terms rather than being silently treated as zero.

**Worked example.** A service loses all operation for two hours, then runs at half capacity for four hours. The deficit is $2+4(0.5)=4$ equivalent full-outage hours. At 10,000 units per hour, the direct loss is 40,000. Restoring half service after one hour and full service after three reduces the deficit to $1+2(0.5)=2$ hours. The improvement is 20,000 before recovery costs. This makes partial restoration quantitatively visible.

**Research extension.** [NIST SP 800-61 Revision 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) places incident response within ongoing cybersecurity risk management. For a project, convert that framing into a small exercise: simulate expired credentials, loss of the primary model provider, corrupted task state, and a restore from backup. Record actual recovery times and remaining data gaps.

### Recovery is a curve, not a switch

In the service-deficit model, time is measured in hours, $T$ is the evaluation horizon, and $q(t)$ is a fraction relative to a defined normal service level. The integral sums the missing fraction over time. Multiplying by $v$, in value units per hour, produces value units. For piecewise constant service, the integral becomes a sum of interval duration times missing fraction. This makes the model executable without numerical integration machinery.

```python
def deficit_hours(intervals):
    total = 0.0
    for hours, service_fraction in intervals:
        if hours < 0 or not 0 <= service_fraction <= 1:
            raise ValueError("Invalid recovery interval")
        total += hours * (1 - service_fraction)
    return total


original = deficit_hours([(2, 0), (4, 0.5)])
improved = deficit_hours([(1, 0), (2, 0.5)])
assert original == 4 and improved == 2
assert deficit_hours([(100, 1)]) == 0
print(original, improved, (original - improved) * 10000)
```

Run `python labs/check_chapters.py 3`; the result is `4.0 2.0 20000.0`. Inputs are nonoverlapping recovery intervals in temporal order; omitted periods are outside the accounted horizon. The function returns equivalent full-outage hours and has no external effects. It does not inspect logs or establish that the declared service fractions are true. In particular, it cannot detect that “half capacity” serves only low-value jobs while urgent work remains blocked.

The RTO is a requirement against which an observed restore is checked. Suppose a restore finishes in 90 minutes, meeting a two-hour RTO, but the latest usable snapshot is six hours old. A 15-minute RPO is still violated. Frequent snapshots do not alone fix this: if encryption keys or restore instructions are unavailable, recovery may fail despite fresh data. Test the whole restoration path, including the person who must execute it and the authority they need.

Partial service can create misleading progress. If the assistant generates drafts but cannot verify citations against the restored database, counting those drafts as completed work overstates $q(t)$. Define service by accepted outcomes, then decide whether degraded operation is permissible. The recurring case therefore reconnects the same objects: delivered service must be evaluated with evidence and authority, rather than inferred from process uptime.

## 4. Generated code shifts the review constraint [44:11](https://www.youtube.com/watch?v=g50FHC-PzK8&t=2651s)

In the questions, Sullivan identifies three pressures: more generated code, contributors who cannot independently repair security flaws, and agents creating connections or services outside established workflows. His toddler analogy motivates observing what agents do with access, not merely checking whether they have credentials.

A **permission boundary** restricts possible effects. **Runtime monitoring** examines events as execution proceeds. The two complement each other: monitoring is not a replacement for least privilege, and permissions do not establish that every allowed action is sensible. A deployment process should test behavior, isolate secrets, and retain a rollback path even when the code was produced quickly.

**Teaching derivation.** Let $\lambda$ be incoming changes per hour and $\mu$ the review service rate. In an idealized M/M/1 queue with Poisson arrivals, exponentially distributed service times, one reviewer, and $\lambda<\mu$, mean time in the system is

$$W=\frac{1}{\mu-\lambda}.$$

If $\mu=10$ changes/hour and arrivals rise from 5 to 9, mean time rises from 0.2 hours to 1 hour. A further increase to 10 eliminates a finite steady-state mean in this model. Real reviews differ in size and risk, but the example explains why faster generation can increase waiting time. The intervention is not simply to produce still more code: reduce change size, automate reliable checks, prioritize by risk, and increase qualified review capacity.

**Original AI project.** Build a local change-risk dashboard using repository metadata and test evidence. It should distinguish a documentation edit from a credential-handling change and show which checks actually ran. Evaluate whether it reduces missed high-risk changes without burying reviewers in false alerts. Do not let a model-generated risk score automatically authorize production changes.

### Deriving the queueing warning

An M/M/1 model has memoryless arrivals and service times and a single service channel. Let $N$ be the number of changes in review or waiting and let $\rho=\lambda/\mu$ be utilization. In equilibrium, transitions between adjacent queue lengths balance: $P(N=n+1)\mu=P(N=n)\lambda$. Repeating gives $P(N=n)=P(N=0)\rho^n$. The geometric series sums to one only for $\rho<1$, producing $P(N=0)=1-\rho$.

The mean queue population including the item under review is $\mathbb E[N]=\rho/(1-\rho)$. Little's relation equates average population to arrival rate times mean time in the system: $\mathbb E[N]=\lambda W$. Combining them yields $W=1/(\mu-\lambda)$. This is total time, not just waiting before service. Expected service itself takes $1/\mu$ hours under the assumed exponential distribution.

For the document company, an AI coding tool can raise proposed changes from five to nine per hour while review remains ten per hour. Utilization rises from 0.5 to 0.9, and average completion delay increases fivefold. The divergence near capacity reflects variability: occasional bursts have little spare capacity with which to drain. Perfectly regular arrivals and service would have different waiting behavior, which is why the assumptions matter.

A practical intervention should target accepted changes, not proposals. Small changes can make review faster, but splitting one conceptual change into many dependent fragments can create coordination overhead. Automated tests can remove repetitive checks, but only for properties they actually verify. Risk-based prioritization can protect critical work while allowing low-risk backlog to grow. Report the backlog by risk and age; an average alone can hide the dangerous tail.

Correlated model errors also undermine apparent redundancy. If three reviewers share the same missing context or mistaken specification, agreement adds little independent evidence. A test of an actual permission boundary is stronger than three generated statements that the boundary appears secure. The important distinction is not human versus AI review but what each check can observe and falsify.

## 5. Quantum risk, release policy, and coordination [49:35](https://www.youtube.com/watch?v=g50FHC-PzK8&t=2975s)

The later questions cover quantum risks, restricted access to powerful cyber models, government involvement, insider threats, and ransomware. Sullivan gives practitioner judgments and forecasts. Model-access anecdotes and exact timelines are not independently verified here. Nor should the recording's compressed history of ransomware be treated as a complete technical history.

**Primary-source extension.** NIST finalized [FIPS 203, 204, and 205 in August 2024](https://csrc.nist.gov/News/2024/postquantum-cryptography-fips-approved). They cover a key-encapsulation mechanism and two digital-signature families designed to resist quantum attacks. Post-quantum cryptography runs on classical computers; it is different from quantum key distribution. Migration requires an inventory of cryptographic dependencies and data lifetimes, not a confident forecast of the first cryptographically relevant quantum computer.

Let $d$ be the remaining secrecy lifetime of data, $m$ the migration time, and $q$ the uncertain time until an adversary can break the vulnerable scheme. The heuristic condition $d+m>q$ indicates why waiting can be risky when encrypted material can be collected now. This is a planning model with uncertain inputs, not a date prediction.

For example, take a hypothetical ten-year secrecy requirement and a three-year migration program. If the relevant threat might arrive within thirteen years, waiting for certainty can leave already-collected ciphertext exposed during its required lifetime. These values are a scenario, not an estimate of quantum progress. Short-lived public data have a different confidentiality requirement from long-lived confidential research.

Key encapsulation establishes shared secret material; a digital signature authenticates a message or signer under a verification key. Replacing one primitive does not automatically migrate certificates, key management, backups, embedded devices, or protocols. The inventory must identify which role each algorithm plays. Authentication and confidentiality can have different failure consequences, so a single “quantum safe” checkbox conceals the work.

For the running company, the immediate useful artifact is a dependency inventory linking data lifetime, cryptographic use, owning service, upgrade path, and recovery test. This improves preparedness without requiring a confident arrival date. It also returns to the lecture's coordination theme: a technically correct migration can fail if one critical supplier or restore path remains incompatible.

At [57:27](https://www.youtube.com/watch?v=g50FHC-PzK8&t=3447s), the speaker discusses limits of perfect security and the risks around valuable intellectual property. The practical extension is to reduce concentrated authority and make unusual access visible. In the closing ransomware discussion, distinguish authorized defensive preparation from retaliatory access to someone else's systems; the latter is not authorized merely because an organization has suffered an attack.

## Limits

The deficit integral prices service loss linearly and omits external harms. The queue model idealizes variable review work. The migration inequality organizes uncertainty rather than estimating it. Personal recovery and organizational recovery can inform each other by analogy, but a queue or control metric is not a psychological model. Judicial documents establish the cited disposition; an interview and these notes do not determine obligations in another case.

## Exercises and worked solutions

1. A service is fully unavailable for 3 hours and at 80% capacity for 5 hours. Compute equivalent full-outage hours.
2. Explain why an RTO of 2 hours and an RPO of 15 minutes are independent requirements.
3. In the queue model, $\mu=12$ and $\lambda=11$. What happens if generation increases to 13 changes/hour?
4. Draft the minimum incident decision record for a suspected data leak.

<details><summary>Solutions and discussion</summary>

1. During the first interval the missing fraction is one, contributing three hours. During the second it is 0.2, contributing one hour. The total is four equivalent full-outage hours. If urgent demand occurs mainly in the first interval, constant value per hour may understate the loss; replace it with a time-dependent valuation only after defining how that value is measured.
2. Construct two counterexamples. A restore completed in one hour from yesterday's backup meets a two-hour RTO but misses a 15-minute RPO. A current replica that takes four hours to activate can meet the data-loss requirement but miss the time requirement. Testing one target therefore cannot establish the other. The test must verify both restored functionality and the age/completeness of restored state.
3. Initially $W=1/(12-11)=1$ hour, including service. At 13 arrivals per hour, $\rho=13/12>1$ and the geometric stationary distribution cannot be normalized. Do not insert the rates into the formula and report a negative waiting time; the formula's stability condition has failed. Reduce admitted work, increase qualified capacity, or change the workflow before claiming a sustainable throughput increase.
4. Record the incident identifier, event and observation times, affected assets, directly observed facts, hypotheses, evidence locations, integrity checks, containment actions, decision owners, reporting assessment, and next review time. Separate an approval from a summary that alleges approval. Add explicit triggers for reopening a decision when new evidence appears. Corrections should preserve the earlier record and explain what changed, enabling later reviewers to reconstruct the decision under its original uncertainty.

</details>

## Primary sources and attribution

- [Stanford recording](https://www.youtube.com/watch?v=g50FHC-PzK8) — Sullivan's personal and professional account.
- [United States v. Sullivan, amended Ninth Circuit opinion](https://cdn.ca9.uscourts.gov/datastore/opinions/2025/11/12/23-927.pdf) — independent judicial source for the litigation outcome.
- [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) — incident-response research extension.
- [NIST post-quantum standards announcement](https://csrc.nist.gov/News/2024/postquantum-cryptography-fips-approved) — cryptographic terminology and standards status.

**Coverage note.** Personal recovery is summarized; the core security themes and later questions are retained. Calculations, queueing analysis, the project proposal, and exercises are independently authored. The chapter deliberately does not reproduce personal addresses, identifying details of third parties, or unverified accusations from anecdotes.
