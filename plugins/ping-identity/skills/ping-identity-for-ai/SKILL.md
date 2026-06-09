---
name: ping-identity-for-ai
description: "Use this skill whenever the task involves an AI agent, LLM, or agentic workflow interacting with Ping Identity. Triggers: giving an AI agent or LLM a verified machine identity; securing agent-to-API access with client credentials or short-lived tokens; Verified Trust signals or verifiable credentials for AI apps; Identity for AI 5-pillar architecture (Agent Identity, Agent Security, Agent Gateway, Agent Detection, Verified Trust); PingGateway as an MCP gateway for AI agents; CIBA human-in-the-loop approvals for high-risk agent actions; bot detection and AI agent detection with PingOne Protect; delegated tokens for helpdesk AI or workforce AI assistants; 'how do I give my AI agent an identity', 'secure my MCP server', 'token rotation for an autonomous agent'. If the request says 'automated process', 'scheduled job', or 'service account' WITHOUT mentioning AI, LLM, or agent — ask a clarifying question before routing here. If the prompt says only 'agent' or 'authenticate an agent' with no AI/LLM/agentic context — ask a clarifying question, as 'agent' is ambiguous (could mean AI agent, Ping integration agent, or browser user-agent). Also invoke with /ping-identity-for-ai."
compatibility: Designed for AI identity and agent security work on Ping Identity platforms. References product docs and Ping Labs content.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-identity-for-ai

AI-era identity patterns: Identity for AI, Verified Trust, agent identity, agent security, and AI application authentication.

## Invocation

Invoke explicitly with `/ping-identity-for-ai` or by saying "use ping-identity-for-ai to...".

## When to use this skill

- "Give my AI agent a verified identity for API access"
- "Use Verified Trust signals in my MCP server"
- "Secure agent-to-agent authentication using Ping"
- "Workforce helpdesk AI — how do I authenticate users for my AI assistant?"
- "Identity for AI architecture with Ping"
- "AI app authentication patterns on PingOne"
- "Agent security and authorization for agentic workflows"
- "Short-lived tokens or token rotation for an autonomous agent"
- "Delegated token for an AI assistant acting on behalf of an employee"
- "Revoke a compromised AI agent's access immediately"

## When NOT to use this skill

- General platform setup or tenant administration: use `ping-foundation`.
- Building a journey or DaVinci flow for human authentication (not AI-specific): use `ping-orchestration`.
- App SDK integration without AI context: use `ping-app-integration`.
- User is orienting or selecting a platform: use `ping-quickstart`.
- Using Ping Protect, PingOne Verify, or PingOne Authorize as standalone services without AI agent context: use `ping-universal-services`.
- "Automated process", "batch job", "scheduled task", or "service account" **without any AI / LLM / agent context** — ask a clarifying question to determine whether this involves an AI agent or a conventional machine process before routing here.

## Multi-skill use cases

A complete AI identity solution typically spans multiple skills:

| Layer | Skill |
|---|---|
| Platform setup and app registration | `ping-foundation` |
| Auth flow / journey / DaVinci design | `ping-orchestration` |
| AI identity patterns and Verified Trust | `ping-identity-for-ai` (this skill) |
| App / SDK integration | `ping-app-integration` |

**Example sequence:**

1. `ping-foundation` — register the AI agent application and configure the environment.
2. `ping-identity-for-ai` — design the token scoping and delegation model (this skill).
3. `ping-orchestration` — build the step-up MFA flow using DaVinci or Journey.
4. `ping-app-integration` — integrate the OIDC client in the AI application.

Complete agent token scoping, Verified Trust signal design, and delegation model here, then hand off to `ping-orchestration` for step-up MFA flows and `ping-app-integration` for SDK/OIDC client wiring.

## Routing — Step 1: What are you trying to do?

| Task | Curated anchor |
|---|---|
| Overview / strategy for Identity for AI (5-pillar) | `references/curated/identity-for-ai-overview.md` |
| Register an AI agent as a managed identity | `references/curated/agent-security-patterns.md` |
| Machine-to-machine auth, token scoping, rotation, revocation | `references/curated/agent-security-patterns.md` |
| CIBA human-in-the-loop approvals for high-risk agent actions | `references/curated/agent-security-patterns.md` |
| Bot / agentic AI detection in flows (Protect) | `references/curated/agent-security-patterns.md` |
| Protect / secure an MCP server (PingGateway) | `references/curated/agent-gateway-mcp.md` |
| Apply Verified Trust signals or verifiable credentials | `references/curated/verified-trust-overview.md` |
| Workforce helpdesk AI — delegation + step-up pattern | `references/curated/workforce-helpdesk-ai.md` |
| AI application end-user authentication (delegated) | `references/curated/workforce-helpdesk-ai.md` |

## Step 2: Load curated anchors (1–3 max)

Load the anchors identified in Step 1. Stop if the curated anchor is sufficient. Do not load all four anchors unless the user's task explicitly spans all sub-areas.

## MCP execution

See `references/runtime/mcp-preflight.md` for MCP config and Cursor preflight steps.

## Retrieval escalation

1. Curated anchors (`references/curated/`) — load 1–3 max. Stop if sufficient.
