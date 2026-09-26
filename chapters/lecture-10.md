# 10. Amit Jain: unified multimodal systems and the limits of world models

**Recording:** [Unified Intelligence Systems](https://www.youtube.com/watch?v=6nUl_w5W9Wk). **Reading question:** What must change when an agent needs to reason about pictures, time, and actions as well as words?

Jain describes Luma's progression from 3D capture to video and unified multimodal models, then to systems that complete creative workflows. The account supplies the chapter's sequence. Equations and controlled examples are independent extensions. Commercial scale figures, unreleased architectures, and customer outcomes are the speaker's account unless separately sourced.

A designer asks an assistant for a video of a cart moving down a ramp, then asks it to change the cart's mass while preserving the camera, markings, and geometry. A convincing answer may still violate the intervention or alter the reference object. If an engineer uses it to predict a real cart's behavior, visual plausibility is insufficient. Representation, preference, prediction, and control need separate tests.

Use this cart-editing task throughout. The system receives observations, constructs an internal state, proposes a transformation or action, and produces an artifact. Some actions change pixels; others refer to physical interventions. The model must specify which meaning applies. All numerical values below are hypothetical teaching constructions.

## 1. Differentiable representations make learning possible [03:01](https://www.youtube.com/watch?v=6nUl_w5W9Wk&t=181s)

The founding story links 3D sensing, neural rendering, and generative modeling. A differentiable representation allows a change in an output error to be propagated back to parameters. That makes it possible to fit representations to observations through gradient-based optimization.

**Definition.** Let $(x_i,y_i)$ be input-target examples for $i=1,\ldots,n$, $\theta$ adjustable parameters, $f_\theta$ a predictor, and $\ell$ its per-example loss. Let $k$ index updates, $\eta>0$ be the learning rate, and $\nabla_\theta$ denote the parameter gradient. Empirical risk and a gradient update are

$$L(\theta)=\frac1n\sum_{i=1}^n\ell(f_\theta(x_i),y_i),\qquad \theta_{k+1}=\theta_k-\eta\nabla_\theta L(\theta_k).$$

The learning rate $\eta$ controls the step. Differentiability does not ensure an informative loss, sufficient data, global convergence, or causal understanding. Deep-learning systems can also contain discrete operations handled through surrogates or gradient estimators, so the lecture's informal claim that non-differentiability makes learning impossible is too strong.

[NeRF](https://arxiv.org/abs/2003.08934) is a concrete primary example: it learns a continuous scene representation from images and camera poses for novel-view synthesis. That achievement is narrower than learning arbitrary physical dynamics. A static scene renderer is not automatically an action-conditioned simulator.

### The gradient connects error to representation

In the risk expression, $x_i$ is an input, $y_i$ its target, $n$ the number of examples, and $k$ the optimization-step index. The vector $\theta$ contains adjustable parameters. The gradient contains the partial derivative of loss with respect to each parameter. Subtracting it seeks a local decrease, with a positive learning rate specifying step size.

For a one-parameter renderer $f_\theta(x)=\theta x$, take one observation $x=2,y=6$ and squared loss $L=(2\theta-6)^2/2$. Its derivative is $2(2\theta-6)$. Starting at $\theta=1$ with learning rate 0.1 gives $\theta'=1-0.1(-8)=1.8$. Loss falls from eight to 2.88. A step size of one jumps to nine and raises loss to 72. Differentiability supplies a direction, not a guarantee that an arbitrary finite step improves the result.

For the cart, a renderer can fit observed appearances while leaving hidden surfaces uncertain. Novel-view evaluation tests transfer beyond training views. It does not test how an intervention changes motion. That needs a dynamics model and intervention evidence. Static reconstruction success cannot establish physical understanding by itself.

## 2. Data availability can overturn an elegant representation [06:00](https://www.youtube.com/watch?v=6nUl_w5W9Wk&t=360s)

Luma initially sought a large corpus through 3D capture. Jain says the team concluded that a single application's data collection could not match the scale of existing image and video data. The company therefore changed its representation and training strategy. The lesson is to design jointly around information content, collection cost, and available scale.

**Independent sample-efficiency model.** Suppose error approximately follows $E(D)=E_\infty+aD^{-\alpha}$ and data costs $cD$. A richer modality may have smaller $a$ or larger $\alpha$ but much larger $c$. Under data budget $B$, compare

$$E(B/c)=E_\infty+a(B/c)^{-\alpha}.$$

This makes the tradeoff explicit. It does not imply that the largest corpus is always best: duplicated, mislabeled, inaccessible, or irrelevant data may add little. Robotics action data can be valuable precisely because passive video does not identify the consequences of all possible actions.

**Worked example.** Two hypothetical datasets have excess error $D^{-1/2}$. If one costs 100 times as much per sample but gives a tenfold reduction in the error coefficient $a$, both yield the same excess error at a fixed budget. Higher per-sample information can offset lower scale; which regime applies is an empirical question.

Substituting the budget constraint makes excess error $ac^\alpha B^{-\alpha}$. At a fixed exponent and budget, compare $ac^\alpha$, not sample count alone. With exponent one half, multiplying sample cost by 100 multiplies this factor by ten, exactly canceled by a tenfold smaller coefficient. Different irreducible error floors would break the equality.

Passive cart videos may be cheap and diverse but fail to identify mass when appearance is unchanged. Controlled trials with known force and mass are expensive but answer the intervention question. A million observational clips do not automatically replace a missing variable. Conversely, a small clean simulator can omit visual conditions needed for deployment. Quantity, information content, and domain coverage are separate dimensions.

## 3. A download is not a preference label [10:02](https://www.youtube.com/watch?v=6nUl_w5W9Wk&t=602s)

One of the recording's most concrete lessons concerns feedback. Downloading a generated video sometimes indicated approval, but sometimes meant the user wanted to share an amusing failure. Treating every download as a positive label taught the wrong preference. Human review was needed to improve signal quality.

**Definition: proxy precision.** Let $G$ mean the user regards an output as good and $D$ mean they download it. A download-based positive label has precision

$$P(G\mid D)=\frac{P(D\mid G)P(G)}{P(D\mid G)P(G)+P(D\mid\neg G)P(\neg G)}.$$

**Worked example.** If 60% of outputs are good, good outputs are downloaded 80% of the time, and poor outputs 30% of the time, precision is $0.48/(0.48+0.12)=0.8$. One fifth of positive labels are wrong even though the proxy sounds sensible. If a viral failure increases $P(D\mid\neg G)$, this contamination rises further.

Pairwise judgments can provide more targeted supervision. Given input $x$ and candidates $y_A,y_B$, write $y_A\succ y_B$ for preference for A. Let $r_\phi$ be a learned scalar score with parameters $\phi$, and $\sigma(z)=1/(1+e^{-z})$ the logistic function. A common preference model is

$$P(y_A\succ y_B\mid x)=\sigma(r_\phi(x,y_A)-r_\phi(x,y_B)),$$

where $r_\phi$ is a learned score and $\sigma(z)=1/(1+e^{-z})$. The score's validity depends on the judging population, question, and candidate distribution. Aesthetic preference, instruction compliance, and physical validity should be evaluated separately.

### A proxy changes with its population

The download calculation multiplies each class's prevalence by its download probability, then normalizes over downloads. Good downloads contribute 0.48 of all outputs and poor downloads 0.12. If good-output prevalence falls to 0.2 while conditional download behavior stays fixed, precision falls to 0.4. A proxy can deteriorate without a change in behavior conditional on quality.

In the cart task, an absurd result may be especially shareable. Optimizing downloads could reinforce the failure an engineering customer wants eliminated. Sample downloaded and undownloaded outputs, ask a specified judging question, and measure disagreement between the proxy and target. Repeat after population or product changes; calibration need not transfer indefinitely.

In the preference expression, $y_A\succ y_B$ means the judge prefers A to B for input $x$. Adding a constant to all scores leaves their differences unchanged, so pairwise judgments do not identify an absolute score origin. More importantly, a judge asked for “most attractive” supplies no direct label for “preserves the requested physical intervention.” Define the target before fitting the reward.

## 4. Unified models and competing decompositions [16:00](https://www.youtube.com/watch?v=6nUl_w5W9Wk&t=960s)

The lecture argues that a thin bridge between a language system and an image generator limits joint reasoning. Jain favors a common processing backbone with modality-specific input and output mechanisms. Later he contrasts a collection of specialized models with an integrated model that can reason across modalities.

**Independent formalization.** Let $z_m=E_m(x_m)$ encode modality $m$ and let a shared backbone $h_\theta$ combine available representations. A modality is a signal type; its encoder maps input to a representation. Output heads map shared computation toward task-specific outputs. Let $L_{\mathrm{CE}}$ be text cross-entropy loss, $L_{\mathrm{denoise}}$ image-denoising error, and $L_{\mathrm{control}}$ a specified action loss. Nonnegative coefficients $\lambda$ set their relative weights. Different heads can use different likelihoods or losses:

$$L(\theta)=\lambda_{\mathrm{text}}L_{\mathrm{CE}}+\lambda_{\mathrm{image}}L_{\mathrm{denoise}}+\lambda_{\mathrm{action}}L_{\mathrm{control}}.$$

Cross-entropy, denoising error, and control loss have different scales and sampling rates. The coefficients $\lambda_m$ and batch mixtures affect which abilities improve. If modality gradients $g_i$ and $g_j$ have $g_i^Tg_j<0$, reducing one loss can locally worsen another. A shared architecture can enable transfer and also create interference.

[Show-o](https://arxiv.org/abs/2408.12528) is a published research example of combining multimodal understanding and generation in one transformer. It offers a checkable point of comparison, not documentation of Luma's proprietary implementation. Claims about competitors' internal architectures in the conversation are not independently established here. The analogy to a single human-brain reasoning center is also a heuristic, not a neuroscience result.

A modality is a signal type, such as text or image. An encoder maps that input into an internal representation; an output head maps shared computation toward a particular output or loss. Cross-entropy penalizes low probability on target discrete tokens. Denoising and control losses measure different errors. Their coefficients cannot be chosen meaningfully without considering units, scales, and task priorities.

Let $g_i=\nabla_\theta L_i$ and $g_j=\nabla_\theta L_j$ be two task gradients. A small descent step on task $j$ changes task $i$ by approximately $-\eta g_i^Tg_j$, where the product is a dot product. If it is negative, task $i$ worsens to first order. This explains interference without proving joint training globally harmful; shared representations can also enable transfer.

For the cart, a modular planner and generator can expose inspectable intermediate instructions. A unified model may preserve information lost when a scene is compressed into text. Compare them using the same edit constraints, inference budget, and failure categories. “Unified” describes an architecture, not a measured quality advantage.

## 5. A world model must be evaluated on consequences [18:02](https://www.youtube.com/watch?v=6nUl_w5W9Wk&t=1082s)

Creative tasks require temporal consistency, spatial relationships, editability, and continuity of intent. Let $s_t$ be internal state at time $t$, $a_t$ a defined action, and $\theta$ learned parameters. A useful definition of a world model for control is a learned transition distribution

$$\hat p_\theta(s_{t+1}\mid s_t,a_t),$$

possibly coupled to an observation decoder and reward model. Here $s_t$ is an internal state and $a_t$ an action. A video generator instead may model future frames conditioned on previous frames and a prompt. These can overlap, but an action must have a defined operational meaning before predictive video becomes a controllable simulator.

[World Models](https://arxiv.org/abs/1803.10122) and [DreamerV3](https://arxiv.org/abs/2301.04104) provide primary examples of learning representations and dynamics for policy learning. Their results concern evaluated environments; they do not establish universal real-world simulation.

**Error propagation.** Let $e_t$ be the norm of true-minus-predicted state error after $t$ steps, and $H$ the rollout horizon. Suppose a deterministic true transition is $L$-Lipschitz in state, meaning it amplifies state distance by at most factor $L\ge0$, and a learned transition has uniform one-step error at most $\epsilon\ge0$ over visited states. Then, under the same action sequence,

$$e_{t+1}\leq Le_t+\epsilon,\qquad e_H\leq\epsilon\sum_{j=0}^{H-1}L^j$$

when $e_0=0$. For $L=1$, error grows at most as $H\epsilon$; for $L>1$, this bound can grow geometrically. The uniform-error assumption is demanding, especially when a planner seeks unusual actions that exploit the model's weaknesses.

**Worked example.** With $L=1.1$, $\epsilon=0.01$, and horizon 20, the bound is $0.01(1.1^{20}-1)/0.1\approx0.573$. Small local errors do not guarantee a reliable long rollout. Evaluate held-out interventions, object persistence, conservation residuals where applicable, and closed-loop task success—not visual appeal alone.

### The hinge in the rollout bound

Let $f$ be the true transition, $\hat f$ the learned transition, and $\hat s_t$ the predicted state. Define error $e_t=\|s_t-\hat s_t\|$ using a specified norm. A transition is $L$-Lipschitz when changing state by a distance $d$ changes the next state by at most $Ld$, for the same action. Assume the learned transition differs from the true transition by at most $\epsilon$ at every relevant state and action.

Insert and subtract $f(\hat s_t,a_t)$ inside the next-state difference. The triangle inequality separates propagated state error from fresh model error. The Lipschitz condition bounds the first by $Le_t$, and uniform approximation bounds the second by $\epsilon$. Iteration from zero initial error produces the geometric sum. The crucial assumption is that accuracy holds where predicted trajectories travel, not only at training states.

```python
def rollout_bound(lipschitz, one_step_error, horizon):
    if lipschitz < 0 or one_step_error < 0:
        raise ValueError("Bounds must be nonnegative")
    if horizon < 0 or int(horizon) != horizon:
        raise ValueError("Horizon must be a nonnegative integer")
    error = 0.0
    for _ in range(horizon):
        error = lipschitz * error + one_step_error
    return error


bound = rollout_bound(1.1, 0.01, 20)
assert abs(bound - 0.01 * (1.1 ** 20 - 1) / 0.1) < 1e-12
assert abs(rollout_bound(1, 0.01, 20) - 0.2) < 1e-12
assert rollout_bound(1.1, 0.01, 0) == 0
print(round(bound, 4))
```

Run `python labs/check_chapters.py 10`; it prints `0.5727`. The function evaluates a recurrence, has no external effects, and checks the geometric expression and the $L=1$ limit. It computes an upper bound rather than a trajectory. A large bound permits large error but does not prove that every rollout fails.

The bound assumes the same actions. A controller acting on predicted states can also change its actions in response to state error, requiring additional policy assumptions. A planner may seek trajectories that exploit model weaknesses. Test its policy in an independent environment, rather than making the same learned model both planner and final judge. This connects to the evaluated policy-learning use of world models in [DreamerV3](https://arxiv.org/abs/2301.04104) without asserting universal physical simulation.

## 6. Skills, harnesses, memory, and data boundaries [21:00](https://www.youtube.com/watch?v=6nUl_w5W9Wk&t=1260s)

The studio-data discussion separates customer artifacts from interaction traces. The later slide-generation example separates domain guidance, model reasoning, and executable tools. This illustrates the distinction between model capability and the surrounding agent system.

For an iterative editor, define state $s=(g,A,H,P)$: user goal $g$, current artifacts $A$, edit history $H$, and permissions $P$. The model proposes an edit; the harness checks scope, executes it, and validates the result. A skill supplies reusable domain constraints, such as preserving an approved palette or keeping labels legible. Memory preserves decisions across iterations.

Interaction traces can still contain confidential project names, scene descriptions, and creative plans. “We exclude the image” does not logically imply “the remaining trace is non-sensitive.” A meaningful data boundary applies to all representations, embeddings, logs, and derived datasets. A certification name by itself does not prove the absence of cross-customer leakage.

For the cart editor, preserve an immutable approved reference and evaluate requested change separately from preservation. A successful file write proves that an artifact exists, not that the edit met the goal. Record which version was approved and which transformation was requested. A later color change does not implicitly authorize changed geometry. The skill specifies this procedure; the harness controls file and publication effects; the model proposes the edit. These mechanisms change runtime behavior without requiring permanent memorization of the project.

## 7. Creativity, architectural forecasts, and causal humility [40:00](https://www.youtube.com/watch?v=6nUl_w5W9Wk&t=2400s)

Jain's economic argument is that cheaper execution allows creators to explore more possibilities. His architectural forecast favors hybrid autoregressive and diffusion approaches. Neither the disappearance of pure diffusion nor a particular employment outcome follows necessarily from the argument.

The final counterfactual-history examples illustrate a critical limit. A plausible video of a world without a historical event is a visualization of assumptions. It cannot establish what would actually have happened. That requires an explicit causal model, evidence, and uncertainty about unobserved alternatives.

The copyright Q&A is the speaker's legal position, not a legal conclusion adopted by these notes. The [U.S. Copyright Office's 2025 report](https://www.copyright.gov/newsnet/2025/1060.html) distinguishes human expressive authorship in AI-assisted outputs. Copyrightability of an output, infringement of existing work, training-data use, and platform liability are separate questions. The report on copyrightability does not settle all four.

## Limits

The gradient argument is local, the data curve is empirical, and the rollout bound assumes uniform accuracy over visited states. Visual preference is not physical truth. An internal state can support prediction without being an interpretable physical coordinate system, but a claim about mass, force, or causation needs an operational mapping and independent evidence.

## Exercises

1. Recalculate download-label precision if only 20% of outputs are good while both conditional download probabilities stay fixed.
2. Derive the rollout-error bound for $L\neq1$ and explain what happens for $0\leq L<1$.
3. Two tasks have gradients $(1,0)$ and $(-2,1)$. Does an equal-weight gradient step necessarily improve both losses to first order?
4. Design a benchmark distinguishing an attractive animation from an action-conditioned physical model. Include one intervention and one out-of-distribution condition.

<details><summary>Solutions and discussion</summary>

1. Good downloads contribute $0.2(0.8)=0.16$, and poor downloads contribute $0.8(0.3)=0.24$. Divide 0.16 by their sum 0.40 to obtain precision 0.40. Most proxy positives are false. The conditional download probabilities did not change, demonstrating why prevalence matters when interpreting a feedback channel.
2. Multiply the finite geometric sum by $L$ and subtract the original sum. Intermediate terms cancel, giving $(L-1)\sum_{j=0}^{H-1}L^j=L^H-1$. Dividing and multiplying by $\epsilon$ yields the claimed expression. For $0\le L<1$, $L^H$ tends to zero and the bound approaches $\epsilon/(1-L)$. Leaving the domain where uniform accuracy holds invalidates this limiting argument.
3. Summing the gradients gives $(-1,1)$; a negative step follows $(1,-1)$ times the positive learning rate. Its dot product with task one's gradient is positive, so task one's loss increases locally. Averaging rather than summing the gradients halves the magnitude but preserves the sign. Improving a weighted aggregate need not improve every task.
4. Hold initial position and velocity fixed and intervene on applied force. Compare predicted and measured trajectories, then test a mass or friction range excluded from training. Record action semantics, units, trajectory error, applicable conservation residuals, and controller success in an independent environment. An attractive animation that ignores the intervention fails regardless of aesthetic preference.

</details>

## Primary references and coverage

- [Mildenhall et al., NeRF (2020)](https://arxiv.org/abs/2003.08934).
- [Ha and Schmidhuber, World Models (2018)](https://arxiv.org/abs/1803.10122).
- [Hafner et al., Mastering Diverse Domains through World Models (2023)](https://arxiv.org/abs/2301.04104).
- [Xie et al., Show-o (2024)](https://arxiv.org/abs/2408.12528).
- [U.S. Copyright Office, output copyrightability report announcement (2025)](https://www.copyright.gov/newsnet/2025/1060.html).

The transcript grounds the 3D-to-video pivot, feedback failure, multimodal architecture argument, studio deployment, skill example, and concluding Q&A. Visual demonstrations were described in the captions; their image quality has not been independently evaluated. Company growth figures and anecdotal industry statistics are not treated as verified measurements.
