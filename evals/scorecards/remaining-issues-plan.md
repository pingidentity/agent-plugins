# Remaining Eval Issues — Plan and Input Needed

Last eval run: 2026-06-04. Current scores after all implemented fixes:

| Model | Skills passing |
|---|---|
| Sonnet 4.6 | 5 / 6 |
| Opus 4.7 | 4 / 6 |
| Haiku 4.5 | 4 / 6 |
| gpt-5.5 | 3 / 6 |
| gpt-5.4-nano | 3 / 6 |
| gpt-5.4-mini | 1 / 6 |

Issues are grouped by type: **eval prompt bugs** (wrong expected skill/behaviour),
**genuine ambiguity** (needs your call), and **tier limitations** (model capability ceilings).

---

## Group A — Eval prompt bugs (no human input needed, safe to fix now)

These are cases where the model is correct and the test is wrong.

### A1 — `ping-app-integration` N-05 (affects: Sonnet, gpt-5.x)

**Prompt:** *"How do I invoke the PingOne Verify service to verify a user's identity document
from my backend?"*
**Expected:** `ping-universal-services`
**Models route to:** `ping-app-integration`

**Why the test is wrong:** "invoke the PingOne Verify service... from my backend" describes
calling the Verify REST API from server-side code — that is an application integration
task (`ping-app-integration`), not service configuration. `ping-universal-services` covers
*configuring* Verify policies and handling outcomes; calling the API from code is app
integration. The models are correct.

**Suggested fix:** Change expected skill to `ping-app-integration`, or rewrite the prompt to
unambiguously describe service configuration: *"Configure a PingOne Verify policy with
document + liveness checks and set the approved/review thresholds."*

**⚠️ Your input needed:** Do you agree with this interpretation? Is calling the Verify API
from a backend app an `ping-app-integration` task or a `ping-universal-services` task in
your mental model?

---

### A2 — `ping-foundation` T-58 (affects: Sonnet, Opus)

**Prompt:** *"Set up SSO for our workforce so employees can sign in to all our apps with one
account."*
**Expected:** `ping-foundation`
**Models return:** empty (no skill routed)

**Why it's likely a prompt quality issue:** This prompt has no platform signal and is a
high-level orientation request — "set up SSO for our workforce" without naming PingOne,
PingFederate, or AIC is exactly the kind of prompt `ping-quickstart` should catch first.
Models are declining to route because the prompt doesn't clearly belong to foundation
without platform context.

**Suggested fix:** Either add a platform signal to the prompt (*"Set up SSO for our
workforce on PingOne MT so employees can sign in to all our apps with one account"*), or
move it to `ping-quickstart` as a trigger prompt.

**⚠️ Your input needed:** Is this a foundation trigger (assume platform implied by
"workforce SSO") or a quickstart trigger (needs platform clarification first)?

---

### A3 — `ping-orchestration` T-57 (affects: Sonnet intermittently)

**Prompt:** *"Our users need to approve high-value transactions via an email confirmation
step — how do I add that to the flow?"*
**Expected:** `ping-orchestration`
**Sonnet routes to:** empty

**Why it's intermittent:** This prompt was passing in earlier runs and is failing on some
Sonnet runs. The phrase "to the flow" is a clear orchestration signal. Likely a model
variance issue at this temperature rather than a description problem.

**Suggested fix:** Strengthen the trigger by making the platform explicit: *"In our AIC
journey, our users need to approve high-value transactions via an email confirmation step —
which nodes do I use?"* This removes any ambiguity about whether this is a flow design or
a service configuration task.

**No human input needed** — safe to rewrite.

---

### A4 — `ping-orchestration` T-52 (affects: Haiku, Opus intermittently)

**Prompt:** *"Add passkey / FIDO2 passwordless authentication to our customer journey, with
magic link fallback."*
**Expected:** `ping-orchestration`
**Some models route to:** empty or quickstart

**Why:** "customer journey" + "passkey" + "FIDO2" + "magic link" should be a strong
orchestration signal. Intermittent failures suggest model variance. The `ping-quickstart`
changes we made recently may be pulling orientation-flavoured "customer journey" language.

**Suggested fix:** Add "in PingOne ST" or "in DaVinci" to anchor it to a specific
orchestration platform: *"Add passkey / FIDO2 passwordless to our PingOne ST customer
journey, with magic link fallback."*

**No human input needed** — safe to add platform context.

---

## Group B — Genuine ambiguity (your call needed)

These are cases where the prompt is legitimately unclear and reasonable people disagree
on the right answer. The current expected behaviour may need to change.

### B1 — `ping-app-integration` A-03 (affects: Sonnet, Opus, GPT)

**Prompt:** *"How do I integrate Ping with my backend?"*
**Expected behaviour:** clarify (ask about stack/use case)
**Models do:** route directly to `ping-app-integration` or `ping-foundation`

**The ambiguity:** "my backend" is a genuinely contested term:
- Backend resource server validating JWTs → `ping-app-integration`
- Backend registering an OAuth client in PingOne → `ping-foundation`
- Backend calling PingOne APIs as a Worker app → `ping-foundation`
- Backend microservice doing M2M client_credentials → `ping-app-integration`

A model routing to `ping-app-integration` directly is not wrong — it's the most common
interpretation. The test asserting that clarification is required may be too strict.

**⚠️ Your input needed — three options:**
- **Option A:** Drop A-03 from ambiguous prompts. Accept that routing directly to
  `ping-app-integration` is a valid answer; the skill will ask for more detail once loaded.
- **Option B:** Replace with a sharper ambiguous case where clarification is unambiguously
  needed, e.g. *"Set up my backend"* (even less context).
- **Option C:** Keep as-is and accept this as a known gap that all models (including Claude)
  only partially satisfy.

---

### B2 — `ping-orchestration` A-03 (affects: GPT models, intermittently Sonnet)

**Prompt:** *"Where do I configure MFA in Ping?"*
**Expected behaviour:** clarify (ask platform / flow vs policy distinction)
**Models do:** route to `ping-orchestration` or `ping-foundation` directly

**The ambiguity:** This is a cross-skill question. "Where do I configure MFA" could mean:
- MFA node in a journey/flow → `ping-orchestration`
- MFA policy (Device Authentication Policy) → `ping-universal-services`
- Sign-on policy with MFA step → `ping-foundation`

The model routing directly to orchestration is answering the most common interpretation.
Clarification is genuinely helpful but the prompt doesn't force it.

**⚠️ Your input needed — two options:**
- **Option A:** Rewrite the prompt to be more explicitly undecidable: *"Do I configure
  MFA in the sign-on policy, the DaVinci flow, or the MFA service settings?"* — forces
  a platform/context question.
- **Option B:** Accept that routing to orchestration is a valid first response and remove
  this from the ambiguous set. The orchestration skill body already handles the routing
  split internally.

---

### B3 — `ping-identity-for-ai` A-01 (affects: Opus, some GPT tiers)

**Prompt:** *"I need to authenticate an agent."*
**Expected behaviour:** clarify (ask if it's an AI agent or a conventional service/process)
**Opus does:** routes to `ping-orchestration` or `ping-app-integration`

**The ambiguity:** "an agent" in Ping context can mean:
- An AI agent / LLM → `ping-identity-for-ai`
- A Ping Gateway agent, PingFederate agent, or integration agent → `ping-foundation`
- A user-agent (browser/app) → `ping-app-integration`

The test is correct that clarification is needed. Opus isn't asking — it's guessing.

**Suggested fix (description-level):** The `ping-identity-for-ai` description already has
the clarification guard: *"If the request says 'automated process', 'scheduled job', or
'service account' WITHOUT mentioning AI, LLM, or agent — ask a clarifying question before
routing here."* The word "agent" alone should also trigger this guard.

**Proposed description addition:** Extend the guard explicitly: *"The word 'agent' alone
is ambiguous — it could mean an AI agent, a Ping integration agent, or a browser user-agent.
If the prompt says only 'agent' without AI/LLM/agentic context, ask a clarifying question."*

**⚠️ Your input needed:** Do you agree that "agent" alone should force a clarifying
question, or should it default-route to `ping-identity-for-ai` (i.e. assume AI context)?
If you have a strong convention in your documentation that "agent" = AI agent, routing
directly may be correct.

---

### B4 — `ping-identity-for-ai` A-03 (affects: GPT models)

**Prompt:** *"How do I add trust to my application so that downstream services can rely on
the claims it presents?"*
**Expected behaviour:** clarify (is this Verified Trust / AI or standard OIDC?)
**GPT does:** routes to `ping-identity-for-ai` or `ping-foundation`

**The ambiguity:** A standard OIDC app asserting claims to downstream services is
`ping-foundation`. An AI app presenting verifiable credentials is `ping-identity-for-ai`.
The prompt doesn't distinguish them. GPT routing directly is defensible.

**⚠️ Your input needed — two options:**
- **Option A:** Rewrite the prompt to force the AI-vs-standard split: *"My application
  is an AI agent that needs downstream services to trust the claims it presents — how do
  I use Verified Trust for this?"* Removes ambiguity, becomes a clear trigger.
- **Option B:** Accept that the current prompt is too close to standard OIDC to reliably
  distinguish without clarification, and accept partial pass rates on this prompt.

---

### B5 — `ping-universal-services` A-03 (affects: GPT models)

**Prompt:** *"A user says they can't verify their identity when they try to log in — is this
a Verify issue or an MFA issue?"*
**Expected behaviour:** clarify
**GPT does:** answers directly (explains the Verify vs MFA distinction)

**Why this may be a test bug:** The user is *explicitly asking* "is this Verify or MFA?" —
that IS a clarification request. A model that answers *"that depends on whether they see
a document capture screen (Verify) or an OTP prompt (MFA)"* is being more helpful than
asking another clarifying question. The expected behaviour (clarify) may be wrong here.

**Suggested fix:** Change the expected behaviour from `clarify` to `route`, accepting
`ping-universal-services` as the answer. Or rewrite the prompt to be a genuine ambiguous
case: *"Some users can't complete identity verification during login — I'm not sure if it's
a Verify or MFA configuration issue."*

**⚠️ Your input needed:** Is an agent that answers this question (explains the Verify/MFA
distinction) providing good behaviour, or do you want it to ask for more information first?

---

## Group C — Tier limitations (no fix available without fine-tuning)

These failures are consistent with the model's capability ceiling. Description changes
cause regressions in larger/more capable tiers when targeted at these.

### C1 — Haiku 4.5 `ping-orchestration` trigger (T-53, T-55, T-57)

Haiku routes complex multi-step orchestration prompts to empty or to `ping-quickstart`.
The prompts all have strong platform context (AIC, DaVinci, passkeys). Haiku simply has
less capacity to hold the full skill routing context and the task description simultaneously.

**Recommended action:** Accept as a Haiku tier limitation. Document in README as known.
No description change is likely to help without regressing Sonnet/Opus.

### C2 — Haiku 4.5 `ping-universal-services` trigger (T-10, T-12)

*T-10:* "I'm not sure which Ping shared service I need..." — Haiku returns empty.
*T-12:* "Call the PingOne Protect risk evaluation API from a PingFederate custom adapter"
→ routes to `ping-app-integration`.

T-12 is actually a reasonable Haiku response — "custom adapter" + "integrate" is strong
app-integration language. T-10 is a genuine miss (the prompt asks which service, which
is a universal-services disambiguation task).

**Recommended action:** T-12 may be a prompt quality issue — the routing tie-breaker in
the OpenAI adapter handles this correctly for GPT but Claude doesn't have the same
instruction. Adding it to the Claude adapter's system prompt is a low-risk option.
**⚠️ Your input needed for T-12:** Same ownership question as A1 — is "call the Protect
API from a PingFederate adapter" app integration or universal-services?

### C3 — GPT-5.4-mini persistent ambiguous failures

`gpt-5.4-mini` remains at 1/6 despite the adapter instructions. The model is at the bottom
of the GPT-5.x capability range and doesn't consistently follow the clarification rule even
when stated explicitly. Further tuning is unlikely to yield significant lift.

**Recommended action:** Accept as a model capability floor. The adapter instructions are
already in place; `gpt-5.4-mini` is not a recommended deployment target.

---

## Summary — Input needed from you

| Item | Question |
|---|---|
| A1 — N-05 Verify from backend | Is calling the Verify API from app code `ping-app-integration` or `ping-universal-services`? |
| A2 — T-58 workforce SSO | Foundation trigger (assume platform implied) or quickstart trigger (needs clarification)? |
| B1 — A-03 "integrate with my backend" | Drop from ambiguous (accept direct route), replace, or keep as known gap? |
| B2 — A-03 "where do I configure MFA" | Rewrite to force undecidable framing, or accept orchestration as valid first route? |
| B3 — A-01 "authenticate an agent" | Should "agent" alone force clarification, or default-route to `ping-identity-for-ai`? |
| B4 — A-03 "add trust to my application" | Rewrite as explicit AI agent / Verified Trust prompt, or accept partial pass? |
| B5 — A-03 "is this Verify or MFA?" | Change expected to `route` (model answering is correct behaviour), or rewrite prompt? |
| C2 — T-12 Protect API from PingFederate adapter | App integration or universal-services? |

---

## Items safe to implement without further input

| Item | Action |
|---|---|
| A3 — T-57 transaction approval prompt | Add "in AIC" or "in our journey" to anchor it |
| A4 — T-52 passkey journey prompt | Add "in PingOne ST" to remove platform ambiguity |
| B3 — A-01 description guard (if you agree) | Add "agent alone is ambiguous" to `ping-identity-for-ai` description |
