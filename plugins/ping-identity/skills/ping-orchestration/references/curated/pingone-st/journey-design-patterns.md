---
title: "AIC and PingAM — Journey Design Reference"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect", "admin"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-19"
slug: "https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html"
---

# AIC and PingAM — Journey Design Reference

How to design, review, and reason about AIC and PingAM journeys in a way that is useful to architects, developers, support teams, and product teams. Applies to sign-in, MFA, registration, passwordless, recovery, profile management, delegated administration, and cross-channel identity flows.

## Scope

**Covers:** Journey design principles, lifecycle modeling, risk and fallback patterns, session behavior, messaging, supportability, and product-specific notes for AIC and PingAM.
**Does NOT cover:** Individual node configuration — see `nodes/`. DaVinci flow design — see `../pingone-mt/davinci-overview.md`. Platform setup — see `ping-foundation`.

---

## Before designing: seven questions to answer first

Before suggesting any node or implementation detail, an agent should be able to answer:

1. Who is the user or actor?
2. What state are they in now?
3. What does success mean?
4. What should happen if risk increases?
5. What should happen if a dependency fails?
6. What changes in session or assurance posture after success or failure?
7. What will support need to reconstruct the experience later?

If any of these are undefined, the journey is not ready to build.

---

## Core design principles

### Start with the user and lifecycle state, not the node list

Define actor types first: customer, employee, admin, delegated admin, partner admin, or machine actor.

Define lifecycle states: invited, pending verification, active, suspended, disabled, locked, closed.

Define the attributes that matter: username, email, phone, tenant, locale, MFA state, recovery identifiers, consent state, role, group, entitlement state.

Keep these meanings consistent across login, registration, recovery, and step-up flows. If one app interprets the same user state differently from another, the experience will drift and support will become harder.

### Keep the journey explicit and explainable

A journey diagram should show the happy path, risk branches, fallback branches, degraded-mode behavior, and user-facing outcomes.

Every branch should answer: what happened, what the user sees, what they can do next, and whether support or an admin is needed.

Avoid hidden behavior that only exists in scripts or policy conditions with no user-visible explanation.

### Match friction to risk

Use a small, understandable set of risk outcomes: allow, light check, step-up, limited fallback, or safe deny.

Do not challenge every user the same way. Do not under-protect privileged or high-impact actions because the main flow was optimized for speed.

The right question is not "can we add more authentication?" but "when is additional friction justified, for whom, and for which action?"

### Design for clear fallback behavior

Journeys should define what happens when:
- A risk engine is unavailable
- An email or SMS provider is delayed
- A factor is unavailable
- A link is expired or a token is stale
- An upstream IdP is slow
- A required claim is missing

Avoid loops, blank screens, silent retries, and raw technical errors. If the preferred path is unavailable, the user should get either a safe alternate route or a clear explanation of why the flow cannot continue.

### Keep session behavior understandable

Decide explicitly what happens after: sign-in, password change, privilege elevation, MFA reset, device deregistration, logout, and entitlement changes.

Be explicit about idle timeout, max lifetime, renewal, forced re-authentication, and revocation behavior.

If a session posture changes, the experience should make that visible instead of forcing support to infer it from logs.

### Keep messaging safe, human-readable, localized, and accessible

User-facing text should explain the next step without exposing raw policy outcomes, protocol details, stack traces, or account existence.

This matters especially for login, recovery, step-up, and degraded-mode messaging. Accessibility and localization are not polish items — they are part of the journey definition.

### Design for change and operations

Important journeys should be observable, versioned, tested, and safe to roll forward or back.

Identity journeys are products, not one-time diagrams. They need release discipline, telemetry, support readiness, and rollback plans.

---

## Good default journey shape

### Step 1 — Define persona, channel, trust level, and success criteria

- Is this SIAM, workforce, B2B, or delegated admin?
- Does the flow start in hosted UI, an SDK, a native app, a browser redirect, a webview, or an external IdP?
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

Include correlation IDs or equivalent reference codes where the user experience or support workflow needs them. Capture journey version, major branch decisions, failure categories, and abandonment points. Make sure support can reconstruct what the user saw.

### Step 7 — Version and release conservatively

Clone or version before major customization. Roll out high-impact identity changes in controlled stages. Know how to roll back without breaking users who are mid-journey.

---

## What "good" looks like by journey type

### Sign-in and MFA

A good sign-in journey is short for low-risk users, stronger for high-risk situations, and predictable across channels.

- Use contextual risk to decide when to add friction instead of applying the same challenge to every user and channel.
- Keep prompts and outcomes consistent across hosted, SDK, mobile, embedded, and custom UI.
- Prefer phishing-resistant and lower-friction approaches where appropriate (passkeys, passwordless).
- Define what happens when the preferred authenticator is unavailable.
- Define what happens when the user changes device, location, browser, privilege level, or assurance level.
- Make session upgrades, step-up prompts, and token posture changes visible in the UX.

**Common failure patterns:** too much friction for low-risk users; too little for privileged users; inconsistent MFA between mobile and web; no alternate factor when the preferred factor fails; unexplained step-up prompts.

### Registration and onboarding

A good registration journey aligns to the identity model and to downstream system expectations.

- Align form fields and validation with the identity model so registration does not drift from profile, recovery, and entitlement logic.
- Define which attributes are required, optional, conditionally required, or externally mastered.
- Decide where verification happens: email, phone, MFA setup, admin approval, or identity verification.
- Show users what is happening when provisioning or synchronization takes time.
- Test under realistic load including email verification, MFA setup, and cross-device handoffs.
- Include edge cases: duplicate emails, existing accounts, partially provisioned users, disabled identities, conflicting invites.

**Common failure patterns:** attributes that do not match downstream requirements; no clear status when provisioning lags; assuming single-device flows; weak handling of duplicate or partially created accounts.

### Recovery and self-service

Recovery is one of the highest-risk journey families and should be treated as such.

- Treat recovery as a high-risk journey. Add stronger verification, step-up authentication, or identity verification where justified.
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

- Treat profile updates, device changes, consent changes, role changes, and delegated admin actions as identity journeys.
- Make state changes visible and predictable.
- Define how session and access should change after profile, role, or device updates.
- In B2B and delegated admin journeys, make privilege scope obvious and separate from end-user views.
- Show admins what they can do, cannot do, and the current state of the tenant or user.

**Common failure patterns:** role changes that do not affect active sessions as expected; delegated admin actions with weak scope cues; missing auditability for high-impact actions.

---

## Common watch-outs

- Do not let different apps interpret the same user state, role, or attribute differently — that creates drift across login, recovery, delegated, and profile flows.
- Do not leak account existence or internal conditions through recovery, sign-in, step-up, or error messages.
- Do not assume web-only behavior. Cross-channel transitions, deep links, app switching, webviews, and native flows need explicit design and testing.
- Do not rely on undefined degraded behavior. Risk engine outages, directory lag, email/SMS delays, claim gaps, and IdP failures should have intentional fallback UX.
- Do not let session and privilege changes be invisible. Regenerate or invalidate sessions after sign-in, password change, privilege change, or device change, and make the effect clear.
- Do not customize OOTB flows without a rollback path or clone/version strategy.
- Do not ship journey changes without telemetry, version awareness, and support readiness.
- Do not treat accessibility, localization, or cross-device behavior as optional.

---

## Product-specific notes

### AIC

AIC guidance should be read with a tenant-security and operational lens.

- AIC security guidance stresses HTTPS-only usage, trusted cookie-domain configuration, CORS controls, CSRF protections for `/am/json/` endpoints, and audit logging as part of secure tenant design.
- For account recovery, AIC guidance recommends step-up authentication, risk-based signals (PingOne Protect), stronger identity verification where needed, verified and unique recovery identifiers, and regular review of recovery processes.

When reasoning about AIC journeys, pay attention to:
- How hosted pages, cookies, and APIs interact across domains
- How tenant security controls affect experience design
- How recovery identifiers are verified and protected
- How risk signals affect sign-in and recovery consistency
- How auditability and support tracing are preserved

### PingAM

PingAM guidance should be read with a realm, redirect, and session-governance lens.

- Reserve the root realm for administrative operations; use another realm (e.g., `alpha`) for journey work.
- Enable only the `goto`/redirect targets you actually trust after journey completion — PingAM denies them by default until the validation service is configured.
- Be intentional with session lifetime settings and client-side sessions, because session behavior is a core part of the security outcome.

When reasoning about PingAM journeys, pay attention to:
- Realm boundaries and administrative separation
- Redirect and return URL trust boundaries
- Session lifetime and idle timeout posture
- How the journey hands control back to the relying application
- How privilege and assurance changes affect active sessions

---

## Recommended agent behavior when using this reference

**Speak in terms of journey intent, risk, fallback, session impact, state transitions, and user-visible behavior — not just nodes and plumbing.**

When describing or proposing a journey, include:
- Who the user is
- What state they begin in
- What success means
- What the main path is
- Where risk or policy branches appear
- What fallback exists if dependencies fail
- What changes in session, token, or assurance posture occur
- What the user sees at each important branch
- What telemetry or traceability is needed

When recommending changes, call out:
- Security impact
- User-experience impact
- Supportability impact
- Rollout and rollback considerations
- Cross-channel implications

If the request is implementation-specific, follow up with environment-specific material before prescribing exact nodes, scripts, policy settings, redirect patterns, or session settings.

If the request is high level, stay at the level of design patterns, user-visible behavior, operational watch-outs, and journey structure.

**Prefer guidance that is safe, explainable, supportable, and testable over guidance that is merely technically possible.**

---

## Related references

- `nodes/basic-auth-nodes.md`
- `nodes/mfa-nodes.md`
- `nodes/risk-management-nodes.md`
- `nodes/identity-management-nodes.md`
- `nodes/utility-nodes.md`
- `nodes/federation-contextual-nodes.md`
- `scripted-decision-nodes.md`
- `inner-journeys.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
[Authentication node reference](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
