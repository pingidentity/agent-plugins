# Ping Identity Advanced Identity Cloud Plugin

Agent-focused guidance for PingOne Advanced Identity Cloud (AIC) — designing and building AIC journeys and PingAM authentication trees, and connecting applications to AIC through app-side integration.

## What this plugin is for

- Designing login, registration, recovery, MFA, step-up, passwordless, and social login journeys
- Selecting and wiring AIC journey nodes with production-validated composition invariants
- Creating and updating journeys directly through AIC MCP tools when connected
- Preparing journeys, scripts, and themes for promotion between environments
- Implementing app-side integration against AIC — Journey modules, journey client, OIDC/PKCE, tenant CORS, troubleshooting

## Requirements

Journey creation uses the PingOne Advanced Identity Cloud MCP server when connected. Without MCP tools, the skill produces journey design artifacts. The plugin does not install tools or modify the agent harness.

## Skills

| Skill | Path | Use when |
|---|---|---|
| `aic-journey-design` | `skills/aic-journey-design/` | Designing or building AIC journeys or PingAM trees |
| `aic-app-integration` | `skills/aic-app-integration/` | Integrating an Android, iOS, JavaScript/React, or backend app with AIC or PingAM |
