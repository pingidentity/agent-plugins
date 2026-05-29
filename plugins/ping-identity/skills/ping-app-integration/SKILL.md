---
name: ping-app-integration
description: Implementation skill for integrating Ping Identity into web, mobile, and SDK experiences. Use this whenever a task involves Android, iOS, or React SDK integration; embedding journeys or DaVinci flows into an application; wiring OIDC / OAuth redirect flows into a web or mobile app; browser-based auth flows; orchestration SDK references; or on-prem app-side integration patterns where the primary task is implementation rather than platform administration. Also invoke with /ping-app-integration.
compatibility: Designed for Ping Identity app and SDK integration work. References product docs and SDK documentation.
metadata:
  publisher: Ping Identity
  version: "0.1.0-scaffold"
---

# ping-app-integration

> **Status:** Phase 0 scaffold per strategy doc § 4. Body authored in Phase 1. Routing logic stub only.

Implementation skill for integrating Ping Identity into web, mobile, and application SDK experiences.

## Invocation

Invoke explicitly with `/ping-app-integration` or by saying "use ping-app-integration to...".

## When to use this skill

- "Integrate Ping into my React app using the orchestration SDK"
- "Use the iOS SDK with AIC journeys"
- "Wire OIDC redirect into a mobile app"
- "Embed a journey in a webview"
- "Migrate from the ForgeRock SDK to the Ping SDK"
- "Add browser-based login to my web application"
- "Connect my Android app to a DaVinci flow"
- "App-side OIDC / OAuth configuration for PingFederate"

## When NOT to use this skill

- If the task is platform setup or app registration (not code): use `ping-foundation`.
- If the task is designing the flow or journey itself: use `ping-orchestration`.
- If the user is just orienting: use `ping-quickstart`.

## Multi-skill use cases

A complete app integration typically spans:

| Layer | Skill |
|---|---|
| Platform setup + app registration | `ping-foundation` |
| Journey or flow design | `ping-orchestration` |
| SDK / app-side implementation | `ping-app-integration` (this skill) |

## Routing — Step 1: What are you trying to do?

| Task | Branch |
|---|---|
| Android SDK integration (Journey or DaVinci) | Mobile → Android branch |
| iOS SDK integration (Journey or DaVinci) | Mobile → iOS branch |
| React / JavaScript web integration | Web → React branch |
| Generic OIDC web app integration | Web → OIDC branch |
| Browser-based redirect / hosted login | Web → browser-flows branch |
| On-prem app integration (PingFederate, PingAccess) | On-prem integration branch |

## Step 2: Platform branch

| Platform | Curated reference |
|---|---|
| PingOne ST (AIC) | `references/curated/mobile-integration-basics.md` (Phase 1) |
| PingOne MT | `references/curated/web-integration-basics.md` (Phase 1) |
| Ping Software Suite | `references/curated/app-integration-overview.md` (Phase 1) |

## Retrieval escalation

Per strategy doc § 0:

1. Curated anchors (`references/curated/`) — load 1–3 max. Stop if sufficient.
2. Generated shortlist (`references/generated/<surface>/top-N.json`) — Phase 2.
3. Docs MCP fallback — see `references/runtime/docs-mcp-routing.md`. Only if curated + shortlist insufficient.
