# Routing Hints — Ping Identity Plugin

Lightweight routing rules for plugin-only installs. Replaces `/shared/taxonomies/routing-rules.md` when the full repo is absent.

## Step 1 — Select the skill

| User intent | Skill |
|---|---|
| "Where do I start?", "Which product?", "Help me choose" | `ping-quickstart` |
| "Set up", "configure", "admin", "create environment/tenant", "add app", "manage directory", "install" | `ping-foundation` |
| "Build a flow", "DaVinci", "journey", "auth tree", "orchestrate" | `ping-orchestration` |
| "AI agent identity", "Verified Trust", "identity for AI" | `ping-identity-for-ai` |
| "Use Protect", "Verify", "IGA", "Credentials", "Authorize", "Neo" | `ping-universal-services` |
| "Integrate my app", "SDK", "mobile", "React", "iOS", "Android", "web login" | `ping-app-integration` |

## Step 2 — Detect the platform

Match the MOST SPECIFIC signal first:

| Signal | Platform tag |
|---|---|
| "PingOne Advanced Identity Cloud", "AIC", "PingAM", "IDM", "ForgeRock", "Identity Management", "identity cloud", "forgeblocks" | `pingone-st` |
| "PingOne" (bare, without "Advanced Identity Cloud"), "apps.pingone.com", "PingOne environment", "PingOne admin console", "PingOne DaVinci", "auth.pingone.com" | `pingone-mt` |
| "PingFederate", "PingAccess", "PingDirectory", "PingAM", "PingIDM", "PingDirectory", "PingAuthorize", "PingDS", PingGateway", "software", "on-prem", "self-managed" | `ping-software` |
| Service question spanning PingOne (multi-tenant cloud) and AIC | `cross-platform` |
| Unknown | Ask: "Are you in PingOne, PingOne Advanced Identity Cloud (AIC), or on-premises software?" |

## Step 3 — Select reference tier

1. `skills/<skill>/references/curated/` — load 1–3 anchor docs

## Cross-skill escalation

| Task spans... | Also reference |
|---|---|
| Flow or journey design | `ping-orchestration` SKILL.md |
| Shared service (Protect, Verify, IGA) | `ping-universal-services` SKILL.md |
| App/SDK code | `ping-app-integration` SKILL.md |
| Platform orientation | `ping-quickstart` SKILL.md |

## Principle

Use the smallest context first. Only widen retrieval when the current tier cannot complete the task.
