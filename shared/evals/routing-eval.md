---
name: ping-routing-eval
description: Evaluate a Ping Identity skill-routing system run. Use this whenever you need to test whether an agent chose the right skill, the right platform branch, the right retrieval tier, and gave a correct answer — all while staying token-efficient. Invoke this eval format for any benchmark prompt before shipping a skill update.
---

# Ping Identity — Skill Routing Eval

You are evaluating a skill-routing system for Ping Identity agent skills.

Your job is not just to answer the user's question. Your job is to evaluate the retrieval path and the answer at the same time.

---

## How to run an eval

For each benchmark prompt, complete all steps below in order. Do not skip steps.

---

## Step 1 — Choose the primary umbrella skill

Select one:
- `ping-quickstart`
- `ping-foundation`
- `ping-orchestration`
- `ping-universal-services`
- `ping-app-integration`
- `ping-identity-for-ai`

**Skill selection guide:**

| Signal in prompt | Likely skill |
|---|---|
| "Where do I start?", "Which product?", platform unknown | `ping-quickstart` |
| "Set up", "configure", "admin", "create environment", "add app", "install", "directory" | `ping-foundation` |
| "Build a flow", "journey", "DaVinci", "authentication tree", "scripted node", "registration flow" | `ping-orchestration` |
| "Protect", "Verify", "IGA", "Credentials", "Authorize", "risk score", "identity proofing" | `ping-universal-services` |
| "SDK", "mobile", "React", "iOS", "Android", "integrate my app", "hosted login page" | `ping-app-integration` |
| "AI agent identity", "Verified Trust", "MCP server auth", "identity for AI" | `ping-identity-for-ai` |

---

## Step 2 — Identify the skill route

State:
- **Primary umbrella skill** and why it wins
- **Secondary plausible skills**, if more than one could fit
- Why the primary should win over any secondary

---

## Step 3 — Choose the platform branch

Select one:
- `pingone-mt` — PingOne (multi-tenant cloud, apps.pingone.com)
- `pingone-st` — PingOne ST / AIC (single-tenant, PingAM/PingIDM/PingDS)
- `ping-software` — PingFederate, PingAccess, PingDirectory, PingAM standalone
- `cross-platform` — genuinely spans two or more families

Then select the **product or service branch** within the platform (e.g., DaVinci, PingFederate, PingOne Verify).

Note any secondary branch candidates if the prompt is ambiguous.

---

## Step 4 — Decide the minimum retrieval path

Choose the smallest tier that resolves the prompt:

| Tier | Use when |
|---|---|
| **Curated refs only** | The curated anchor(s) for the skill + platform fully answer the question |
| **Curated refs + bounded shortlist** | Curated anchors orient but do not cover the specific task; a generated shortlist provides the gap |
| **Docs fallback only if still necessary** | Neither curated nor shortlist is sufficient; a targeted external query is required |

**Retrieval discipline rules:**
- Load the smallest trusted context first
- Do not load more than 3 curated refs unless the task explicitly spans multiple domains
- Do not open a generated shortlist if a curated anchor already resolves the task
- Never load external docs if curated refs are sufficient
- Stop as soon as the answer is good enough

State:
- Retrieval tier used
- Curated refs you would load (by path)
- Shortlist refs you would load (by path), if any
- Whether external docs are needed: Yes / No
- Estimated retrieval token spend
- Estimated total token spend
- Why this is the minimum sufficient context

---

## Step 5 — Answer the benchmark prompt

Provide the actual answer as if you were the agent. Answer at the level of detail the prompt requires — do not over-explain, and do not under-answer.

---

## Step 6 — Score the run

Use this rubric. Score each dimension, then sum.

| Dimension | Max | Criteria |
|---|---|---|
| **Routing Correctness** | 30 | Correct umbrella skill selected; platform branch correct; secondary skills identified correctly |
| **Context Correctness** | 25 | Right curated files loaded; no irrelevant files loaded; shortlist used only when needed |
| **Answer Correctness** | 20 | Factually correct; matches platform; complete enough to act on |
| **Token Efficiency** | 15 | Minimum sufficient context; no over-retrieval; answer appropriately scoped |
| **Fallback Discipline** | 10 | No unnecessary external docs call; fallback used only when curated + shortlist are genuinely insufficient |

**Scoring guidance:**
- Deduct 15–30 points from Routing Correctness for wrong umbrella skill on an easy case
- Deduct 10–20 points from Answer Correctness for a major factual error
- Deduct all 10 Fallback Discipline points for an unnecessary external docs call
- Deduct 10–15 points from Token Efficiency if retrieval exceeds 150% of minimum needed

---

## Step 7 — Hard gate pass/fail

A run **FAILS** if any of the following is true:
- Wrong umbrella skill on an easy case (unambiguous prompt)
- Major factual error in the answer
- Unnecessary external docs call on an easy case
- Token spend above 150% of the estimated minimum
- Final score below 80/100

---

## Output format

Use this exact format for every eval run:

```
# Skill Routing Eval

## Benchmark Prompt
[paste the benchmark prompt here]

## Route Decision
- Primary umbrella skill:
- Secondary plausible skills:
- Platform branch:
- Product or service branch:
- Secondary branch candidates:
- Confidence: High / Medium / Low

## Retrieval Plan
- Retrieval tier used:
- Curated refs to load:
- Shortlist refs to load:
- Docs fallback needed: Yes / No
- Estimated retrieval token spend:
- Estimated total token spend:
- Why this is the minimum sufficient context:

## Answer
[Provide the actual answer to the benchmark prompt]

## Scorecard
- Routing Correctness: X/30
- Context Correctness: X/25
- Answer Correctness: X/20
- Token Efficiency: X/15
- Fallback Discipline: X/10
- Final Score: X/100

## Pass/Fail
- Result: PASS or FAIL
- Hard fail reason, if any:

## Short Rationale
- What you routed correctly:
- What context you intentionally did not load:
- Whether fallback was disciplined:
- Biggest risk in this run:
```

---

## Benchmark prompt library

Use these prompts to validate skill routing. Add new prompts as new skills and references are built. Each prompt should be a realistic, substantive user message — not a generic one-liner.

### Easy cases (should route confidently)

**E-01 — Foundation, PingOne ST**
> I need to register a new OIDC application in my AIC tenant so my React app can use it for login. What do I need to configure?

**E-02 — Orchestration, PingOne ST**
> I want to build a registration journey in PingOne ST that collects the user's email, sends a verification OTP, and creates a managed object on success. What nodes do I need and in what order?

**E-03 — Quickstart**
> My company is evaluating Ping Identity. We're not sure whether to go with PingOne or the on-premises software. What questions should we be asking?

**E-04 — Foundation, Ping Software**
> We're installing PingFederate on-prem and need to configure an SP connection for SAML SSO to Salesforce. Where do I start?

**E-05 — Orchestration, PingOne MT**
> I need to build a DaVinci flow that does username/password login, checks risk, and does an MFA step-up if risk is medium or high.

### Medium cases (some ambiguity)

**M-01 — Foundation + Orchestration boundary**
> I want to add an MFA policy to my PingOne MT environment. Is that a policy configuration or do I need to build a flow?

**M-02 — Orchestration + Universal Services boundary**
> I'm building an AIC journey and want to add PingOne Verify for identity proofing during registration. What does that involve?

**M-03 — App Integration**
> We have a PingOne ST tenant set up and a journey ready. Now I need to integrate the hosted login page into our iOS app using the Ping SDK.

### Hard cases (multi-skill or cross-platform)

**H-01 — Full stack**
> We're building a CIAM solution on PingOne ST: tenant provisioned, apps registered, now we need a registration journey with email OTP, identity verification via PingOne Verify, and then the iOS SDK integration. What's the sequence of skills and what does each one own?

**H-02 — Cross-platform ambiguity**
> We're running PingFederate on-prem and want to add PingOne MFA as a step-up. How do these two products connect?

---

## Guidance for writing new benchmark prompts

From Anthropic's skill-creator guidance: "Query quality matters — create realistic, substantive prompts with context (file names, column values, backstory), not generic requests."

A good benchmark prompt:
- Reads like a real user message, not a test question
- Has enough context to make routing unambiguous (easy cases) or intentionally ambiguous (medium/hard cases)
- Has one clearly correct primary skill on easy cases
- Tests a specific curated reference or routing decision you want to validate
- Is not solvable from general LLM knowledge alone — it requires the skill's curated context to answer well

A poor benchmark prompt is a one-liner like "How do I set up PingOne?" — too vague to test routing precision.
