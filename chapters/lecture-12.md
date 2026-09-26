# 12. Mati Staniszewski: voice systems, latency, and reliable action

**Recording:** [The Future of Voice Systems](https://www.youtube.com/watch?v=vfF011ko89o). **Reading question:** Why can a convincing voice still make a poor agent?

The lecture follows ElevenLabs from a dubbing problem to speech generation and interactive enterprise systems. Its central technical comparison is between cascaded and fused architectures. Mathematical definitions, latency budgets, and evaluation examples below extend the conversation; they are not measurements of ElevenLabs products.

A traveler asks a voice assistant to move a flight to tomorrow morning while keeping the same destination and staying below a price limit. The assistant sounds warm and confident, but mishears one digit in the booking reference. It later says “all set” while the booking tool has timed out. Neither vocal quality nor conversational fluency establishes that the correct reservation changed.

Carry this rebooking case through the chapter. The system receives audio, forms an interpretation, obtains authenticated account evidence, proposes an action, executes only an authorized transaction, and reports a verified result. Audio quality, information preservation, latency, and transaction correctness are distinct properties of that same process.

## 1. Start with a tractable component of a real problem [05:01](https://www.youtube.com/watch?v=vfF011ko89o&t=301s)

Staniszewski's motivating problem was multilingual dubbing that preserved vocal identity and emotional delivery. The initial system required transcription, translation, and speech generation. Conversations with prospective users revealed a nearer-term need: correcting narration and producing voiceovers in the original language. This allowed the team to focus research on speech generation first.

**Definition: cascaded dubbing.** Automatic speech recognition (ASR) estimates text from audio, machine translation (MT) translates text, and text-to-speech (TTS) synthesizes audio. Let source audio be $a$, transcript $x$, translated text $y$, and output audio $b$. Sum over possible text sequences $x,y$ to write a decomposition:

$$p(b\mid a)=\sum_{x,y}p_{\mathrm{TTS}}(b\mid y,a)\,p_{\mathrm{MT}}(y\mid x)\,p_{\mathrm{ASR}}(x\mid a),$$

under the stated conditional-dependence assumptions. In practice, systems often pass one best transcript and translation rather than sum over alternatives. That is cheaper but can discard uncertainty and propagate an early mistake with apparent confidence.

Speaker attribution, source separation, timing, and pronunciation are additional tasks, not details guaranteed by this three-box diagram. A name transcribed incorrectly can be translated and spoken perfectly incorrectly. A useful system preserves uncertainty around names, amounts, and other consequential content.

### What the cascade assumes

Automatic speech recognition (ASR) maps audio toward text. Machine translation (MT) maps text between languages. Text-to-speech (TTS) maps linguistic content and voice conditions toward audio. In the decomposition, translation depends on the selected transcript, and synthesis depends on translated text plus source audio. Summing over transcripts and translations propagates their uncertainty rather than committing immediately to one path.

For rebooking, translation may be unnecessary, but the same inference issue remains. If recognition assigns probabilities 0.55 and 0.45 to two booking codes, selecting the first and discarding the second conceals substantial uncertainty. Passing alternatives does not mean attempting transactions on both accounts. It means recognizing that a clarification or an authenticated lookup is needed before a consequential action.

The conditional assumptions are choices, not a complete description of speech. Translation may benefit from tone or surrounding dialogue absent from a plain transcript. Synthesis may need timing and speaker identity beyond the translated words. A hybrid representation can carry text plus timestamps, confidence on important spans, and permitted acoustic features. The appropriate interface is the one that preserves what the downstream task needs.

## 2. Audio tokens connect signal processing to language modeling [11:03](https://www.youtube.com/watch?v=vfF011ko89o&t=663s)

The speaker emphasizes context-dependent delivery and learned voice representations. The research extension is to encode audio into a sequence of discrete codec codes, then model those codes conditionally on text and an authorized voice reference.

**Definition: residual vector quantization.** Let an encoder produce vector $z$. Choose code $q_1$ from a learned codebook to approximate $z$, then choose $q_2$ to approximate residual $z-q_1$, and continue. After $K$ codebooks,

$$\hat z=\sum_{k=1}^{K}q_k,\qquad r_k=z-\sum_{j=1}^{k}q_j.$$

The decoder maps the quantized representation back to waveform. [EnCodec](https://arxiv.org/abs/2210.13438) provides a primary neural-audio-compression example. [VALL-E](https://arxiv.org/abs/2301.02111) demonstrates conditional language modeling over neural codec codes. These are research references, not disclosures of ElevenLabs' proprietary architecture.

**Worked bitrate example.** Suppose a hypothetical codec emits 50 frames per second, eight codebook indices per frame, and each codebook has 1,024 entries. Fixed-length coding uses

$$R=50\times8\times\log_2(1024)=4{,}000\ \text{bits/second}.$$

Uncompressed 24-kHz, 16-bit mono PCM uses 384,000 bits/second. The nominal ratio is 96 to one, excluding headers and other overhead. Compression quality depends on the signal and training objective; a low bitrate does not imply preservation of every acoustic detail.

### Quantization is a controlled approximation

An encoder maps a waveform segment to a vector $z$. A codebook is a finite set of representative vectors. The first quantizer chooses a representative close to $z$ under a specified distance; the second approximates what remains, and subsequent stages refine the residual. The index of each chosen vector can be transmitted instead of its full coordinates. The decoder must possess the corresponding codebooks and reconstruction model.

If the first approximation leaves scalar residual 0.3, and the next codebook offers residual representatives 0, 0.25, and 0.5, choosing 0.25 leaves residual 0.05. This toy example illustrates refinement, not an actual audio codec. A learned codec optimizes reconstruction under its chosen losses; preserving perceived voice quality does not imply exact preservation of every acoustic cue or digit's intelligibility.

Each codebook with 1,024 entries needs ten bits per fixed-length index because $2^{10}=1024$. Multiply frames per second, indices per frame, and bits per index to obtain bits per second. Entropy coding can change the actual rate when indices are nonuniform, and framing adds overhead. The [EnCodec](https://arxiv.org/abs/2210.13438) and [VALL-E](https://arxiv.org/abs/2301.02111) papers illustrate different roles for these codes: compression and conditional generation. A codec language model does not make all aspects of speech equivalent to ordinary text tokens.

## 3. Cascaded versus fused is a design space [22:04](https://www.youtube.com/watch?v=vfF011ko89o&t=1324s)

A text-only intermediate representation loses prosody, pauses, overlapping speech, and other information unless the system explicitly carries it forward. A fused system can process audio and generate audio more directly. Staniszewski nevertheless argues that a cascade can be useful when selecting a capable reasoning model, debugging tool calls, and satisfying enterprise requirements matter most.

**Information-theoretic extension.** Let $Y$ be a target property of interest, such as the spoken content or a prosodic feature, $A$ the observed audio, and $T$ a transcript computed only from $A$. Mutual information $I$ measures statistical dependence. Under the Markov condition $Y\to A\to T$, meaning the transcript adds no target information once audio is known, the data-processing inequality gives $I(Y;T)\leq I(Y;A)$. Compression cannot create information about that target that was absent from the input. This statement concerns information about a target, not an arbitrary downstream decision variable. It also does not show that a particular fused model uses all available information well.

The correct intermediate representation depends on the task. For calculating a bill, exact words and amounts may dominate. For turn taking, duration and overlap matter. For a user who explicitly requests slower delivery, a saved preference is more reliable than guessing from their accent. Emotion estimates should be treated as uncertain cues; vocal patterns do not uniquely reveal a person's internal state.

| Architecture | Practical advantage | Failure to inspect |
|---|---|---|
| ASR → reasoning → TTS | Inspectable intermediate text; component substitution | Lost acoustic context and propagated recognition error |
| Audio-native or fused | Richer direct acoustic path; potential latency savings | Harder localization of some failures; training and tool integration costs |
| Hybrid | Different routes for conversation and consequential actions | Routing mistakes and inconsistent state between routes |

These are tendencies, not guaranteed properties. A fused model can use structured tools; a cascade can be fast and expressive. Compare actual systems on matched tasks.

The data-processing result can be derived using the chain rule for mutual information. Under the Markov assumption, the transcript adds no information about $Y$ once audio $A$ is known, so $I(Y;A,T)=I(Y;A)$. Expanding in the other order gives $I(Y;A,T)=I(Y;T)+I(Y;A\mid T)$. Conditional mutual information is nonnegative, so the inequality follows. Equality holds when the transcript retains all information in the audio relevant to this target.

For exact word content in a clean utterance, a transcript may be sufficient for the next decision. For whether the speaker has finished a turn, timing and overlap can matter even when the recognized words are correct. The target $Y$ must be named before declaring the representation adequate. A larger acoustic model can have access to more information and still use it poorly; information availability is not a performance guarantee.

In the booking case, carry the recognized itinerary and amount as structured fields, preserve uncertainty on the reference code, and keep turn-taking signals available to the dialogue controller. These are compatible with either a cascade or a fused model. The decisive comparison asks whether the system preserves needed evidence, meets delay constraints, and respects the transaction state machine.

## 4. Speech fluency and action correctness require separate tests [25:01](https://www.youtube.com/watch?v=vfF011ko89o&t=1501s)

The recording names expressivity, reliability, and latency as distinct design axes. For agents, reliability needs a task definition. A beautiful apology is not a successful rebooking, and a spoken confirmation is not evidence that a reservation exists.

**Recognition metric.** Let $S$ count substitutions, $D$ deletions, $I$ insertions, and $N>0$ reference words under a word-sequence alignment. Word error rate is

$$\mathrm{WER}=\frac{S+D+I}{N},$$

with substitutions $S$, deletions $D$, insertions $I$, and reference word count $N$. It is useful for transcription, but it weights all words equally. One wrong digit in a confirmation code can matter more than several omitted articles. Also, WER can exceed one when insertions are numerous.

**Agent metric.** Measure verified task success, unauthorized-action rate, correct escalation, and constraint adherence alongside WER and listener ratings. Use diverse speakers and conditions, including background noise, interruptions, unfamiliar names, and incomplete sentences. [Whisper's research paper](https://arxiv.org/abs/2212.04356) is a primary entry point for large-scale speech recognition; its benchmark results do not replace domain evaluation.

A minimal transaction state machine is `unauthenticated → authenticated → proposal → confirmed → executed → verified`. The model can help interpret a request, but the harness should enforce allowed transitions. Retrying a timed-out booking requires an idempotency key or a status lookup, because absence of a response does not prove absence of a charge.

The rebooking proposal should bind passenger identity, original reservation, new itinerary, price, and any user constraint. Confirmation applies to that proposal, not to an arbitrarily changed price later. If availability changes before execution, regenerate the proposal and obtain whatever authorization the revised transaction requires. A model's conversational confidence cannot expand the confirmed scope.

An execution timeout creates an uncertain state. The booking may have committed even though the response was lost. A reconciliation query checks the authoritative reservation or transaction identifier. Only after that query can the assistant distinguish a failed attempt from a successful booking with a lost receipt. Saying “please try again” without this distinction can cause duplicate charges or reservations.

The word-error metric is intentionally simpler. An alignment counts the substitutions, deletions, and insertions needed to map a recognized sequence to a reference sequence. It does not assign higher cost to an incorrect price or account number. Add task-specific checks on critical fields and verified account outcomes. A system with lower average WER can still be worse at the few fields that determine transaction correctness.

## 5. Latency is an end-to-end budget [28:00](https://www.youtube.com/watch?v=vfF011ko89o&t=1680s)

The airline-booking example separates a smooth conversation from a correct transaction. Authentication, account lookup, availability checks, and payment can dominate response time even if speech generation is fast.

**Definition: time to first audible response.** A simplified sequential budget is

$$T_{\mathrm{first}}=T_{\mathrm{endpoint}}+T_{\mathrm{ASR}}+T_{\mathrm{reason}}+T_{\mathrm{tool}}+T_{\mathrm{TTS}}+T_{\mathrm{network}}.$$

Streaming overlaps some stages, so the true critical path must be measured from an event trace. Mean component times do not determine the 95th-percentile end-to-end latency, especially when outages or congestion correlate across stages.

**Worked example.** Endpoint detection takes 350 ms, final recognition 100 ms, initial reasoning 250 ms, TTS startup 150 ms, and networking 100 ms. With no tool call, the sequential total is 950 ms. A mandatory 1,200-ms database operation raises it to 2,150 ms. Halving TTS startup saves 75 ms in either case. The dominant opportunity is the endpoint, tool path, or overlap—not necessarily the model with the most visible voice.

Define the real-time factor of speech synthesis as $\mathrm{RTF}=T_{\mathrm{compute}}/T_{\mathrm{audio}}$. RTF below one means average production can keep up with playback on the measured hardware. It does not guarantee fast startup, stable chunk delivery, or acceptable tail latency.

### A latency budget is a dependency claim

Endpoint detection decides that the user has finished speaking; recognition finalizes the input; reasoning prepares a response or tool request; synthesis prepares audible speech. The sum assumes these stages wait for one another. Streaming can overlap partial recognition, reasoning, and speech, but an authenticated booking confirmation still depends on transaction evidence. A prompt acknowledgment can arrive early without falsely asserting completion.

```python
def first_audio_ms(endpoint, recognition, reasoning, tool, synthesis,
                   network):
    stages = (endpoint, recognition, reasoning, tool, synthesis, network)
    if any(time < 0 for time in stages):
        raise ValueError("Stage times must be nonnegative")
    return sum(stages)


ordinary = first_audio_ms(350, 100, 250, 0, 150, 100)
booking = first_audio_ms(350, 100, 250, 1200, 150, 100)
faster_tool = first_audio_ms(350, 100, 250, 600, 150, 100)
assert ordinary == 950 and booking == 2150
assert booking - faster_tool == 600
print(ordinary, booking, faster_tool)
```

Run `python labs/check_chapters.py 12`; it prints `950 2150 1550` in milliseconds. Inputs are nonnegative sequential stage times. The pure function returns their sum and has no audio or account effects. It does not model overlap or latency distributions. Treat its result as an explicit dependency scenario to compare against a real event trace.

Do not sum stage-level 95th percentiles and label the result the end-to-end 95th percentile. Quantiles depend on the joint distribution: slow stages may coincide or occur on different requests. Record per-request timing and calculate the end-to-end distribution directly. Also distinguish time to any audible response from time to a correct answer and time to a completed transaction.

## 6. Pricing, trust, and deployment work [38:01](https://www.youtube.com/watch?v=vfF011ko89o&t=2281s)

The business discussion emphasizes deployment expertise and value-based pricing. The suggested fraction of customer value is a heuristic, not a universal price law. Cost still sets a viability constraint, and value requires a measurable counterfactual.

**Worked economics.** Suppose an agent handles 10,000 monthly contacts, saves five minutes on 60% of them, and creates one minute of review per contact. Net time saved is $10{,}000(0.6\times5-1)=20{,}000$ minutes, or about 333 hours. Multiply by an appropriate marginal labor-value estimate, then subtract platform, integration, quality, and error costs. Gross automated minutes alone overstate the benefit.

In the safety discussion, Staniszewski argues against treating vocal resemblance as sufficient authentication. The general engineering principle is that a reproducible signal is poor proof of authority. Use an authenticated channel and explicit transaction controls. Consent to synthesize a voice, permission to perform an account action, and proof that content came from a particular generator are three separate questions.

Watermarking and provenance may help within their supported scope. They do not make absence of a detectable watermark proof that an audio sample is human. A detector's error rates depend on compression, recording conditions, transformations, and the generator population.

For the economics, define the counterfactual carefully. Five minutes saved relative to an inefficient old process is not necessarily five minutes saved relative to the best feasible alternative. Some saved staff time becomes usable capacity rather than reduced payroll expense. Both can have value, but their valuation differs. Track reopened contacts and human review in the same period so that automation cannot move costs outside the measurement window.

In the example, each contact saves an expected three gross minutes, then consumes one review minute, leaving two net. If review rises to four minutes, net savings become negative even though 60% of conversations are automated. Pricing from gross automation volume would then conceal a worsening customer workflow. The business comparison should include integration and error costs before making a value-based pricing claim.

## 7. Creative control and the local/cloud boundary [59:02](https://www.youtube.com/watch?v=vfF011ko89o&t=3542s)

The closing discussion frames AI as a tool inside an iterative creative process: a person supplies intent, evaluates delivery, and asks for controlled revisions. It also distinguishes local narration from the broader stack required for a connected, interactive assistant. Running one model on a device does not make every database, tool, or logging dependency local.

For a solo project, a bounded voice interface to your own research notebook is a useful experiment. Start with retrieval and playback; measure source accuracy, spoken mathematical notation, interruption handling, and startup latency. Add write actions only after read-only answers can be traced to evidence. The official [Sesame CSM repository](https://github.com/SesameAILabs/csm), mentioned in the lecture, offers an inspectable research artifact for studying conversational speech generation; check its requirements before choosing it for hardware you own.

Commercial revenue and hiring figures in the recording are not independently audited here. ARR is an annualized recurring-revenue rate, not necessarily recognized revenue over a completed year; the conversation sometimes moves between these terms. Product forecasts and statements about future on-device availability remain statements made at recording time.

For a local research-notebook assistant, define the actual boundary: recognition on device, retrieval from a local index, synthesis locally, and no remote tool calls. Moving only speech synthesis onto the device leaves the rest of the data path unchanged. Test interruptions while reading a formula, ambiguous source titles, and requests to modify a note. Local execution can improve control over data movement, but it does not make an incorrect interpretation correct.

**Limits.** The codec arithmetic omits coding overhead, the information bound concerns a specified target, and the latency sum assumes sequential stages. Voice quality and authentication are different properties. The rebooking system is successful only when the intended transaction is independently verified under the user's constraints.

## Exercises

1. A reference has 20 words, with two substitutions, one deletion, and one insertion. Compute WER. Explain why this says little about whether the account number is correct.
2. Recompute the codec bitrate with four codebooks rather than eight. Which quality conclusion cannot be drawn from the arithmetic alone?
3. In the latency example, how much does halving the database time improve total response time? Compare this with halving TTS startup.
4. Design a rebooking evaluation with five cases that sound conversationally successful but must fail verification.

<details><summary>Solutions and discussion</summary>

1. Add two substitutions, one deletion, and one insertion to obtain four edits. Divide by the twenty reference words to get 0.20. An account-number error and an omitted article can each contribute one edit while having radically different consequences. Therefore inspect critical fields and verified account outcomes separately. With enough insertions the numerator can exceed the reference length, so WER is not bounded by 100%.
2. Each frame now uses four ten-bit indices, giving $50(4)(10)=2000$ bits per second. Removing codebooks changes residual reconstruction, but the arithmetic does not determine perceived quality or intelligibility. Those require a specified signal population, codec, and listening or task evaluation. Header overhead can also make the actual bitrate differ from this payload calculation.
3. Database time falls from 1,200 to 600 ms, saving 600 and reducing the sequential total to 1,550 ms. Halving TTS startup saves only 75 ms. The first intervention saves eight times as much in this scenario. If the database call overlaps other work, the critical-path benefit must be recomputed rather than assuming the entire 600 ms appears in the end-to-end result.
4. Test a correct-sounding confirmation for the wrong passenger, a flight that became unavailable, a duplicate transaction after a lost response, a changed price without renewed authorization, and a tool failure reported as success. Each must fail the relevant verifier despite fluent speech. Require authoritative reservation state, a unique transaction identifier, and a match to the confirmed proposal. Keep an explicit uncertain state when evidence is missing instead of forcing success or failure by guess.

</details>

## Primary references and coverage

- [Défossez et al., High Fidelity Neural Audio Compression (2022)](https://arxiv.org/abs/2210.13438).
- [Wang et al., VALL-E (2023)](https://arxiv.org/abs/2301.02111).
- [Radford et al., Robust Speech Recognition via Large-Scale Weak Supervision (2022)](https://arxiv.org/abs/2212.04356).
- [Sesame, Conversational Speech Model: official repository](https://github.com/SesameAILabs/csm).

The chapter follows dubbing and initial scope, architecture tradeoffs, reliability and latency, deployment economics, trust, creative control, and local inference. International deployment anecdotes are compressed. Codec equations and all numerical examples are teaching extensions, not reverse engineering of ElevenLabs.
