---
title: "End-to-End Validation — Test What You Just Built"
product_family: cross-platform
products: ["pingone", "pingone-aic", "davinci", "pingfederate"]
capabilities: ["quickstart", "validation"]
services: []
audience: ["admin", "developer", "architect"]
use_cases: ["workforce", "customer", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: ""
---

# End-to-End Validation — Test What You Just Built

Cross-cutting orientation for validating a Ping Identity configuration, journey, flow, or app integration end-to-end. Used after the build phase to prove the path works and to surface gaps that block completion.

## Scope

**Covers:** what to validate at each layer (platform / orchestration / app), tools available for each layer (MCP servers, CLIs, sample apps, hosted preview, browser testing), test-user creation patterns, repeatable reporting format, and what to do when something is read-only or sandbox-only.

**Does NOT cover:** building the configuration itself — see the relevant umbrella skill (`ping-foundation`, `ping-orchestration`, `ping-universal-services`, `ping-app-integration`). Production monitoring and observability beyond first-success validation.

---

## Validation matrix — what tools exist for each layer

| Layer | What to validate | Available tools | Falls back to |
|---|---|---|---|
| **Platform setup** (`ping-foundation`) | Tenant exists, env enabled services, app registered, redirect URIs match, sign-on policy attached | PingOne MCP server, AIC MCP server, REST API + Worker app, admin console smoke test | Manual console click-through |
| **Directory / users** | Test user exists, schema attributes populated, group/population membership correct | Same MCP servers; SCIM endpoint; AIC IDM REST API | Console user search; LDIF query (PingDS) |
| **Authentication policy / journey / flow** | Journey or flow runs end-to-end; expected branches reachable; session token issued | AIC journey preview ("Try Journey"); DaVinci "Try Flow"; PingFederate "Test Connection"; LightStep / DaVinci Analytics for trace | Browser-based end-user test in incognito |
| **Universal services in flow** | Protect risk score returned; Verify proofing transaction completes; Credentials issued | DaVinci flow trace; AIC `RiskAdvisorNode` debug output; Verify admin transaction history | Pull a transaction by ID via REST |
| **App integration / SDK** | Authorization code flow returns tokens; collectors render; tokens validate; refresh works | Sample app from each SDK repo; Postman / curl with PKCE; OIDC discovery endpoint reachability | OIDC.io online debugger; jwt.io for token introspection |
| **End-to-end UX** | A real user can complete the path on a real browser/device | Browser testing (Chrome DevTools, Safari Web Inspector); BrowserStack / Sauce Labs for cross-device | Manual user acceptance testing |

---

## What can be automated vs manual today

### Automatable (read-only via MCP / API)

- **PingOne MCP server** (where installed): list applications, sign-on policies, environments, populations, users
- **AIC tenant REST API** (with worker token): list realms, journeys, OAuth clients, identity store records
- **DaVinci Analytics API**: query flow execution traces, success/failure counts, branch percentages
- **PingFederate `pf-admin-api`**: query SP connections, adapters, policies
- **OIDC discovery endpoint**: probe `/.well-known/openid-configuration` to confirm AS reachability
- **Token endpoint**: scripted authorization code + PKCE to confirm tokens issue

### Automatable (write — requires admin write scope; use cautiously)

- Creating test users (only in dev/sandbox environments)
- Provisioning test OAuth clients with scoped redirect URIs
- Updating journey/flow versions (only in non-production environments)
- Triggering a Verify proofing transaction (only with sandbox document images, not live PII)

### Manual today (no automation surface)

- DaVinci "Try Flow" UX walk-through (no scripted equivalent)
- AIC "Try Journey" UX walk-through (browser-only)
- Branded hosted-page rendering verification (visual / DOM diff required)
- WebAuthn / passkey ceremonies (require human interaction with authenticator)
- Email and SMS deliverability (no synchronous test path)
- End-app UI rendering on real devices

---

## Test user creation patterns

| Pattern | Use when |
|---|---|
| **Dedicated test population / realm** | Multiple test scenarios; isolation from production users |
| **Per-test user with unique email** | Signup flows; need a fresh user per run |
| **Service account / worker app** | API testing; non-user-facing flows |
| **Admin "Sign in as" / impersonation** | Diagnosing a single user's broken flow (workforce only; never CIAM) |
| **Synthetic user with stubbed factor** | MFA testing without actual phone/email; configure dev-only authenticator |

**Safety rules:**
- Never create test users in production environments
- Use unique email patterns (e.g., `qa+<scenario>@example.com`) to avoid collisions
- Tag test users with a known attribute (`testUser: true`) so they can be cleaned up reliably
- For PII-touching flows (Verify), use the platform's sandbox document set — do not upload real PII

---

## Validation sequence — recommended order

For any new configuration, validate from the platform up:

1. **Platform reachable** — OIDC discovery endpoint resolves; admin console accepts your token
2. **App record correct** — client ID, redirect URIs, scopes match what the app sends
3. **Sign-on policy / journey active** — journey is activated (AIC); flow is deployed (DaVinci); policy is attached (PingFederate)
4. **Test user can authenticate** — happy path sign-in produces an ID token with expected claims
5. **Branches work** — invalid password, expired session, MFA challenge, risk-elevated path each reach the expected end state
6. **Recovery paths work** — password reset, account recovery, MFA recovery exit cleanly
7. **App integration produces tokens** — SDK/app receives tokens; tokens validate against the AS
8. **End-app behavior matches** — refreshed tokens work, logout clears session, deep-linked re-auth works
9. **Universal services succeed** — Protect signal received, Verify transaction completes, Credentials issued (if in scope)
10. **Visual/UX correctness** — branding renders, hosted pages match, custom domain serves with TLS

Stop at the first failure and isolate the layer. Do not test layer N+1 if layer N is broken — false positives compound.

---

## Reporting format — repeatable structure

When validation completes, summarize in this format. It surfaces both successes and gaps in a way that maps cleanly to next-action ownership.

```markdown
# Validation summary — <use case>

**Built:** <what was configured: e.g., AIC sign-up + sign-in + reset journeys for retail CIAM>
**Date:** <YYYY-MM-DD>
**Tester:** <name / agent>

## Worked
- [layer]: [what worked, with link to evidence — e.g., "AIC journey 'CustomerSignIn' end-to-end smoke pass; ID token issued with `email_verified: true` claim"]

## Failed
- [layer]: [what failed, with the exact error and one hypothesis] — *severity: blocker | high | medium | low*

## Ambiguous
- [layer]: [observed behavior that is unclear — needs clarification before it can be marked pass/fail]

## Blocked
- [layer]: [what could not be tested at all and why — missing tool, missing license, sandbox constraint]

## Gap report
- **Product gap:** [feature missing in the product itself — file as PR or ticket]
- **Asset gap:** [reference / docs / sample missing — file as content task]
- **Tooling gap:** [no MCP/CLI/script for this validation — file as DevEx task]
```

This format makes it easy to:
- Fast-fix asset/tooling gaps in the same sprint
- Escalate product gaps to the right product owner
- Re-run the same scenario after changes and track regression

---

## Read-only / sandbox / approval-required guardrails

Some validations require explicit care:

| Constraint | Rule |
|---|---|
| **Production environment** | Default read-only; do NOT create test users, change policies, or modify journeys without an explicit, documented change ticket |
| **PingOne Verify with real PII** | Use the sandbox document set in non-production; never test against your own real ID |
| **PingOne Credentials** | Sandbox credential issuance only; do not issue real verifiable credentials in test |
| **Email / SMS notifications** | Use a controlled test inbox / phone number; do not blast notifications during validation |
| **Worker app tokens** | Treat like production secrets; never commit to code or copy to logs |
| **Risk evaluation (Protect)** | Test with synthetic device signals only when supported; live signals from real devices may be subject to data-protection rules |

When a step requires human approval (e.g., release into a regulated environment), the agent should pause and surface the gate, not auto-execute.

---

## Cross-skill routing

| If the failure is in... | Route to |
|---|---|
| Tenant / app / policy / directory | `ping-foundation` |
| Journey / DaVinci flow logic | `ping-orchestration` |
| Protect / Verify / Credentials / IGA / Authorize | `ping-universal-services` |
| SDK / app code / token handling | `ping-app-integration` |
| AI agent identity / Verified Trust | `ping-identity-for-ai` |

If the failure straddles layers (typical), validate each layer independently using the sequence above before deciding which skill owns the fix.

---

## Common pitfalls

| Pitfall | Why it bites | Avoid by |
|---|---|---|
| Validating UX before platform | Most "UX bugs" are policy/redirect/scope misconfigurations | Run the platform-up sequence; do not skip layers |
| Using cached browser session | Hides journey misbehavior because the session is reused | Always test in incognito or a clean profile |
| Testing one happy path only | Branches are where production bugs live | Validate at least one failure branch and one risk-elevated branch per flow |
| Real PII in sandbox tests | Privacy violation; can leak through logs | Use platform sandbox data sets only |
| Asserting from logs alone | Logs lag, can be misleading, and may be sampled | Pair log assertions with token / API result assertions |
| "It works on my machine" | Browser, locale, OS, network differs; passkeys especially device-bound | Test on a clean test device or BrowserStack |

---

## Prerequisites

- Build phase complete: at least one happy path is configured and theoretically reachable
- Test user(s) provisioned in a non-production environment
- For SDK validation: a sample app from the relevant SDK repo or a curl/Postman script with PKCE
- For Universal Services validation: licenses or sandbox entitlements active in the test environment

## Common variants

| Variant | Note |
|---|---|
| First-time setup | Validate every layer; do not assume anything |
| Incremental change | Validate the changed layer + the layer above + the layer below |
| Pre-production cutover | Run the full sequence in staging environment that mirrors production config |
| Post-incident regression | Replay the failure scenario; assert it now passes; add to a regression suite |

## Related references

- `references/curated/getting-started-overview.md`
- `references/curated/common-starting-patterns.md`
- `plugins/ping-identity/skills/ping-app-integration/references/curated/integration-troubleshooting-basics.md`

## Source

- Strategy: `docs/ping-identity-agent-skill-strategy.md` §9 use case 9 — "Test this end to end"
- PingOne MCP server reference: https://docs.pingidentity.com/pingone-mcp/
- AIC REST API: https://docs.pingidentity.com/pingoneaic/api-reference/
- DaVinci Analytics: https://docs.pingidentity.com/davinci/davinci_analytics/davinci_analytics_overview.html
