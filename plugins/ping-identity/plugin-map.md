# Plugin Map — Ping Identity

Index of included skills, their purpose, and when to use each. Use this file to select the correct skill before loading any SKILL.md.

## Skills

### ping-quickstart
**Path:** `skills/ping-quickstart/`
**Use when:** The user does not know which Ping platform or product applies, or explicitly asks "where do I start?"
**Not for:** Any task where the platform is already known — go directly to the right skill.

### ping-foundation
**Path:** `skills/ping-foundation/`
**Use when:** The task is setup, configuration, or administration of a platform — tenant/environment creation, app registration, directory setup, authentication policy, branding.
**Not for:** Designing flows or journeys (→ ping-orchestration); invoking shared services (→ ping-universal-services); app/SDK code integration (→ ping-app-integration).

### ping-orchestration
**Path:** `skills/ping-orchestration/`
**Use when:** The task is designing or troubleshooting a DaVinci flow, PingOne ST journey, or PingAM authentication tree.

### ping-universal-services
**Path:** `skills/ping-universal-services/`
**Use when:** The task involves invoking a Ping Universal Service: PingOne Protect (risk scoring), PingOne Verify (identity verification/KYC), PingOne Credentials, IGA, Neo, or Authorize — across PingOne MT or PingOne ST. Also use for cross-platform shared service orchestration and service invocation patterns.

### ping-app-integration
**Path:** `skills/ping-app-integration/`
**Use when:** The task is integrating Ping into an application — Android SDK, iOS SDK, React SDK, DaVinci SDK, browser flows, or on-prem app-side configuration. Covers mobile and web SDK setup, OIDC/OAuth wiring, and integration troubleshooting.

### ping-identity-for-ai
**Path:** `skills/ping-identity-for-ai/`
**Use when:** The task involves securing AI agents with Ping Identity, implementing Verified Trust, building workforce helpdesk AI (password reset, account unlock), or applying identity security patterns to AI-driven applications and agentic workflows.

## Selection rule

1. Unknown platform or starting point → `ping-quickstart`
2. Setup / config / admin → `ping-foundation`
3. Flow / journey / orchestration design → `ping-orchestration`
4. Shared service invocation → `ping-universal-services`
5. App / SDK integration code → `ping-app-integration`
6. AI agent or trusted identity patterns → `ping-identity-for-ai`
