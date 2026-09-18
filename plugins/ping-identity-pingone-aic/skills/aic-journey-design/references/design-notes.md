# AIC Journey Design Notes

Design review lens for AIC journeys: what a journey description must state, the security lens to read journeys through, and the wiring invariants that recur across production journeys. For node-by-node detail, use the node-family references; for product-neutral design principles, use portfolio-level guidance.

## Scope

**Covers:** The AIC design checklist, AIC tenant-security lens, and cross-cutting journey wiring invariants.
**Does NOT cover:** Node configuration (see `nodes/`); product-neutral design principles; DaVinci flow design.

---

## Design checklist

**Describe journey intent, risk, fallback, session impact, state transitions, and user-visible behavior — not just nodes and plumbing.**

A journey description includes:
- Who the user is
- What state they begin in
- What success means
- What the main path is
- Where risk or policy branches appear
- What fallback exists if dependencies fail
- What changes in session, token, or assurance posture occur
- What the user sees at each important branch
- what telemetry or traceability is needed

A change assessment includes:
- Security impact
- User-experience impact
- supportability impact
- Rollout and rollback considerations
- Cross-channel implications

Implementation-specific designs require environment-specific inputs before defining exact nodes, scripts, policy settings, redirect patterns, or session settings.

High-level designs stay at the level of patterns, user-visible behavior, operational watch-outs, and journey structure.

**Prefer designs that are safe, explainable, supportable, and testable over designs that are merely technically possible.**

---

## AIC security lens

Read AIC journeys with a tenant-security and operational lens:

- AIC security guidance stresses HTTPS-only usage, trusted cookie-domain configuration, CORS controls, CSRF protections for `/am/json/` endpoints, and audit logging as part of secure tenant design.
- For account recovery, AIC guidance recommends step-up authentication, risk-based signals (PingOne Protect), stronger identity verification where needed, verified and unique recovery identifiers, and regular review of recovery processes.

When reasoning about AIC journeys, pay attention to:
- How hosted pages, cookies, and APIs interact across domains
- How tenant security controls affect experience design
- How recovery identifiers are verified and protected
- How risk signals affect sign-in and recovery consistency
- How auditability and support tracing are preserved
- How ESVs (Environment-Specific Variables) are used rather than hardcoded values in Scripted Decision node scripts for multi-environment portability

---

## Journey wiring invariants

These invariants recur across production AIC journeys. Violating them produces runtime failures or support problems that are hard to diagnose.

- **Terminal nodes:** Every journey must have at least one Success node; pair it with a Failure node for explicit failure termination. Do not leave outcomes unwired.
- **Anti-enumeration wiring:** In recovery and reset journeys, wire both the found and not-found outcomes to the same successor node (typically the same email-suspend node). Never route them to different user-facing messages — that leaks account existence.
- **PageNode children:** Interactive collectors must be declared as PageNode children — a PageNode without children renders an empty page. Outcomes come from the child decision node, not the PageNode itself.
- **SelectIdP outcomes are fixed:** Social login entry nodes emit exactly two outcomes (social authentication / local authentication) regardless of which providers are filtered; per-provider branching happens after authentication via a scripted decision node reading the provider alias.
- **Collector typing must match ceremony type:** An OATH-typed collector used in a WebAuthn flow (or any cross-type pairing) causes validation failures.
- **Script outcomes must be declared:** A scripted decision node that returns an outcome not listed in its configuration stalls the journey — declare every outcome the script can return and wire each one.
- **Protect result at both terminations:** A PingOne Protect result node must be called on both the success and the failure termination paths. Omitting it on one path degrades the risk model.
- **Inner journeys for composition:** Reusable logic (MFA, risk, profiling) belongs in inner journeys invoked from the main journey, each handling one concern. Parent journey data (username, auth level) flows in automatically; transient state does not persist across the boundary.
- **ESVs over hardcoded values:** Use environment-specific variables for anything environment-varying in scripts and node configs; inline secrets block promotion.

---

## Source

- [Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
- [AIC tenant security](https://docs.pingidentity.com/pingoneaic/tenants/tenant-security.html)
