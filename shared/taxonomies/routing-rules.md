# Routing Rules

Decision logic for agents and SKILL.md files. Apply these rules in order to reach the correct skill and reference tier.

## Step 1 — Identify the user's job

| User says... | Route to |
|---|---|
| "Where do I start?", "Which product do I need?", "Help me choose" | ping-quickstart |
| "Set up", "configure", "admin", "create tenant", "add app", "manage directory" | ping-foundation |
| "Build a flow", "design a journey", "DaVinci", "auth tree", "orchestrate" | ping-orchestration |
| "AI agent identity", "trust agent", "Verified Trust", "identity for AI" | ping-identity-for-ai |
| "Use Protect", "add Verify", "configure IGA", "enable Credentials", "Authorize" | ping-universal-services |
| "Integrate my app", "add SDK", "mobile auth", "web app login", "React SDK" | ping-app-integration |

## Step 2 — Identify the platform family

After routing to a skill, apply platform detection:

1. PingOne admin console / PingOne APIs → `pingone-mt`
2. PingOne ST tenant admin / AM / IDM / DS → `pingone-st`
3. On-prem deployment / server software → `ping-software`
4. Cross-platform or service-layer question → `cross-platform`

## Step 3 — Select reference tier

Apply in order; stop at the first tier that satisfies the task:

1. **Curated anchors** (`references/curated/`) — canonical, task-completing docs. Load 1–3 max.
2. **Generated shortlist** (`references/generated/<branch>/`) — ranked top-N candidate list. Pull only matching titles/summaries.
3. **Docs MCP retrieval** (`references/runtime/<platform>/docs-mcp-routing.md`) — surgical query: exact product + task + feature. Retrieve specific sections, not full pages.

## Step 4 — Stop condition

Stop retrieving context as soon as the task can be completed. Do not pre-load all tiers.

## Cross-skill escalation

If task spans skills, complete primary routing first, then reference the secondary skill explicitly rather than loading its full context.
