# Orchestration Design Principles

Product-neutral principles for designing, reviewing, and reasoning about authentication experiences. In these pages an **experience** is the end-to-end sequence of steps a person or machine actor goes through to reach an identity outcome — sign-in, registration, recovery, MFA, step-up, passwordless, and profile changes — including its branches, fallbacks, and what the user sees at each point. Ping platforms express an experience with different constructs: journeys/trees of nodes in Advanced Identity Cloud and PingAM, connector-based flows in PingOne DaVinci, and authentication policies in PingFederate. This page covers the what and why; exact nodes, connectors, scripts, and configuration are product documentation territory.

## Scope

**Covers:** Experience and orchestration design principles, lifecycle modeling, risk and fallback patterns, session behavior, messaging, supportability, and recurring reliability patterns that recur across Ping orchestration platforms.
**Does NOT cover:** Node, connector, or authentication-policy selection and configuration; platform security posture; promotion mechanics.

---

## Before designing: seven design inputs

Define these inputs before selecting nodes or implementation details:

1. Who is the user or actor?
2. What state are they in now?
3. What does success mean?
4. What should happen if risk increases?
5. What should happen if a dependency fails?
6. What changes in session or assurance posture after success or failure?
7. What will support need to reconstruct the experience later?

If any of these are undefined, the experience is not ready to build.

---

## Core design principles

### Start with the user and lifecycle state, not the node list

Define actor types first: customer, employee, admin, delegated admin, partner admin, or machine actor.

Define lifecycle states: invited, pending verification, active, suspended, disabled, locked, closed.

Define the attributes that matter: username, email, phone, tenant, locale, MFA state, recovery identifiers, consent state, role, group, entitlement state.

Keep these meanings consistent across login, registration, recovery, and step-up flows. If one app interprets the same user state differently from another, the experience will drift and support will become harder.

### Keep the experience explicit and explainable

An experience diagram should show the happy path, risk branches, fallback branches, degraded-mode behavior, and authentication outcomes.

Every branch should answer: what happened, what the user sees, what they can do next, and whether support or an admin is needed.

Avoid hidden behavior that only exists in scripts or policy conditions with no user-visible explanation.

### Match friction to risk

Use a small, understandable set of risk outcomes: allow, light check, step-up, limited fallback, or safe deny.

Do not challenge every user the same way. Do not under-protect privileged or high-impact actions because the main flow was optimized for speed.

The right question is not "can we add more authentication?" but "when is additional friction justified, for whom, and for which action?"

### Design for clear fallback behavior

The design should define what happens when:
- A risk engine is unavailable
- An email or SMS provider is delayed
- A factor is unavailable
- A link is expired or a token is stale
- An upstream identity provider is slow
- A required claim is missing

Avoid loops, blank screens, silent retries, and raw technical errors. If the preferred path is unavailable, the user should get either a safe alternate route or a clear explanation of why the flow cannot continue.

### Categorize failures, don't improvise them

Distinguish three error categories and give each its own treatment:

- **User error** — the user can correct it. Re-present the step with an inline message; never terminate the experience for a correctable mistake.
- **System error** — a dependency failed. Log it with a correlation reference, show a generic error with that reference, and keep the user's progress recoverable.
- **Security block** — the experience must not continue. Terminate with a clear, plain message and do not expose the underlying reason (for example, say only "account unavailable", never why).

Terminating on every error without user-visible feedback creates silent dead ends.

### Keep session behavior understandable

Decide explicitly what happens after: sign-in, password change, privilege elevation, MFA reset, device deregistration, logout, and entitlement changes.

Be explicit about idle timeout, max lifetime, renewal, forced re-authentication, and revocation behavior.

If a session posture changes, the experience should make that visible instead of forcing support to infer it from logs.

### Keep messaging safe, human-readable, localized, and accessible

User-facing text should explain the next step without exposing raw policy outcomes, protocol details, stack traces, or account existence.

This matters especially for login, recovery, step-up, and degraded-mode messaging. Accessibility and localization are not polish items — they are part of the experience definition.

### Design for change and operations

Important experiences should be observable, versioned, tested, and safe to roll forward or back.

Identity experiences are products, not one-time diagrams. They need release discipline, telemetry, support readiness, and rollback plans.

---

## Good default experience shape

### Step 1 — Define persona, channel, trust level, and success criteria

- Is this CIAM, workforce, B2B, or delegated admin?
- Does the flow start in a hosted UI, an SDK, a native app, a browser redirect, a webview, or an external identity provider?
- What outcome should the user achieve, in business terms?

### Step 2 — Model the happy path first

Start with the shortest correct flow for the intended user. Confirm which systems are read from, which are written to, and what timing assumptions exist. Keep early branching to a minimum until the intended baseline experience is clear.

### Step 3 — Add risk and policy branches

- What causes extra friction?
- What causes a hard block versus limited fallback?
- Where do privileged flows differ from normal ones?

### Step 4 — Add fallback and degraded-mode behavior

- What happens if signals, factors, providers, or claims are unavailable?
- Include retry guidance, alternate channels, assisted options, and stop conditions.
- Explicitly prevent redirect loops and repeated returns to unusable screens.

### Step 5 — Add safe messaging and state transitions

Use non-technical, localized, accessible messaging. Make recovery, consent, timeout, step-up, and error states understandable. Preserve anti-enumeration requirements wherever account existence or user status could leak.

### Step 6 — Add telemetry and supportability

Include correlation IDs or equivalent reference codes where the user experience or support workflow needs them. Capture experience version, major branch decisions, failure categories, and abandonment points. Make sure support can reconstruct what the user saw.

### Step 7 — Version and release conservatively

Clone or version before major customization. Roll out high-impact identity changes in controlled stages. Know how to roll back without breaking users who are partway through an experience.

---

## What "good" looks like by experience type

### Sign-in and MFA

A good sign-in experience is short for low-risk users, stronger for high-risk situations, and predictable across channels.

- Use contextual risk to decide when to add friction instead of applying the same challenge to every user and channel.
- Keep prompts and outcomes consistent across hosted, SDK, mobile, embedded, and custom UI.
- Prefer phishing-resistant and lower-friction approaches where appropriate (passkeys, passwordless).
- Define what happens when the preferred authenticator is unavailable.
- Define what happens when the user changes device, location, browser, privilege level, or assurance level.
- Make session upgrades, step-up prompts, and token posture changes visible in the UX.

**Common failure patterns:** too much friction for low-risk users; too little for privileged users; inconsistent MFA between mobile and web; no alternate factor when the preferred factor fails; unexplained step-up prompts.

### Registration and onboarding

A good registration experience aligns to the identity model and to downstream system expectations.

- Align form fields and validation with the identity model so registration does not drift from profile, recovery, and entitlement logic.
- Define which attributes are required, optional, conditionally required, or externally mastered.
- Decide where verification happens: email, phone, MFA setup, admin approval, or identity verification.
- Show users what is happening when provisioning or synchronization takes time.
- Include edge cases: duplicate emails, existing accounts, partially provisioned users, disabled identities, conflicting invites.

**Common failure patterns:** attributes that do not match downstream requirements; no clear status when provisioning lags; assuming single-device flows; weak handling of duplicate or partially created accounts.

### Recovery and self-service

Recovery is one of the highest-risk experience families and should be treated as such.

- Treat recovery as a high-risk experience. Add stronger verification, step-up authentication, or identity verification where justified.
- Use non-revealing messages ("If an account exists, we've sent instructions") paired with rate limits, lockouts, and clear next steps.
- Recovery artifacts (links, codes, tokens) should be short-lived, one-time use, and invalidated after use or suspected compromise.
- Define distinct handling for: password reset, username reminder, MFA reset, device recovery, email/phone change, and assisted recovery.
- Define what happens when limits trigger, when abuse is suspected, and when assisted recovery is required.

**Common failure patterns:** reusable or long-lived recovery artifacts; messages with no next step; strong MFA in sign-in but weak verification in recovery; delivery-channel failures with no alternate route.

### Passwordless and step-up evolution

The long-term direction should be lower friction with stronger assurance.

- Reduce dependence on passwords where possible.
- Prefer strong authenticators over memorized secrets when the use case supports it.
- Use step-up based on risk and action sensitivity rather than applying it everywhere by default.
- Roll out passwordless changes incrementally — only some users may be ready.
- Make sure fallback and recovery are mature before aggressively reducing password-based options.

**Common failure patterns:** assuming all populations are ready for the same passwordless posture; removing fallback too early; excessive step-up fatigue; changing friction without explaining why.

### Profile, entitlement, and delegated flows

These flows are often treated as secondary, but they are where state drift becomes visible.

- Treat profile updates, device changes, consent changes, role changes, and delegated admin actions as identity experiences.
- Make state changes visible and predictable.
- Define how session and access should change after profile, role, or device updates.
- In B2B and delegated admin experiences, make privilege scope obvious and separate from end-user views.

**Common failure patterns:** role changes that do not affect active sessions as expected; delegated admin actions with weak scope cues; missing auditability for high-impact actions.

---

## Recurring reliability patterns

These patterns appear in nearly every production experience. At design level: know that they exist, require them in reviews, and let the platform documentation define the mechanics.

- **Anti-enumeration:** Recovery and reset flows must never confirm or deny whether an account exists. Both the found and not-found paths present the same user-facing behavior; only rate limiting and telemetry differ.
- **Risk results reported at every outcome:** Risk-evaluation integrations lose accuracy if the risk engine only hears about the successful path. The evaluation result must be reported back at both the success and failure terminations of an experience.
- **Notifications are best-effort:** Delivery failure of an informational notification (for example, a confirmation email) should not block the experience. Delivery-gating notifications (for example, a verification link the user must act on) are a different class and must have a failure path.
- **Partial-state cleanup:** When account creation fails partway through, the partially created record must be removed or explicitly reconciled before the user can retry — orphaned partial accounts cause downstream drift.
- **Retry caps with lockout:** Repetitive-entry points (OTP, recovery codes) get an explicit retry cap, and exceeding it leads to a defined lockout or lockout-escalation behavior — never an unbounded loop.
- **Fail safe on ambiguous outcomes:** When an authorization or policy decision returns an indeterminate or errored result, the experience fails closed (denies) rather than allowing.
- **Trusted-device fast paths:** Step-up can be skipped for known, healthy devices; the trust decision itself must be explicit and auditable, not implicit in node ordering.

---

## Common watch-outs

- Do not let different apps interpret the same user state, role, or attribute differently — that creates drift across login, recovery, delegated, and profile flows.
- Do not leak account existence or internal conditions through recovery, sign-in, step-up, or error messages.
- Do not assume web-only behavior. Cross-channel transitions, deep links, app switching, webviews, and native flows need explicit design and testing.
- Do not rely on undefined degraded behavior. Risk engine outages, directory lag, email/SMS delays, claim gaps, and identity provider failures should have intentional fallback UX.
- Do not let session and privilege changes be invisible. Regenerate or invalidate sessions after sign-in, password change, privilege change, or device change, and make the effect clear.
- Do not customize out-of-the-box flows without a rollback path or clone/version strategy.
- Do not ship experience changes without telemetry, version awareness, and support readiness.
- Do not treat accessibility, localization, or cross-device behavior as optional.

---

## Design checklist

**Describe experience intent, risk, fallback, session impact, state transitions, and user-visible behavior — not just nodes and plumbing.**

An experience description includes:
- Who the user is, what state they begin in, and what success means
- The main path, and where risk or policy branches appear
- What fallback exists if dependencies fail
- What changes in session, token, or assurance posture occur
- What the user sees at each important branch
- What telemetry or traceability is needed

A change assessment includes security impact, user-experience impact, supportability impact, rollout and rollback considerations, and cross-channel implications.

Implementation-specific designs require environment-specific inputs before defining exact nodes, scripts, policy settings, redirect patterns, or session settings.

High-level designs stay at the level of patterns, user-visible behavior, operational watch-outs, and experience structure.

**Prefer designs that are safe, explainable, supportable, and testable over designs that are merely technically possible.**

---

## Source

- [Advanced Identity Cloud journeys documentation](https://docs.pingidentity.com/pingoneaic/home.md)
- [PingAM authentication node reference](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
- [PingOne DaVinci documentation](https://docs.pingidentity.com/davinci/davinci_introduction.md)
- [PingFederate authentication policies](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_authentication_policies.html)
