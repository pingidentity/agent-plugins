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

1. PingOne Advanced Identity Cloud (AIC) / AIC tenant / AM / IDM / DS → `pingone-st`
2. PingOne (bare, without "Advanced Identity Cloud") / PingOne admin console / PingOne APIs → `pingone-mt`
3. On-prem deployment / server software → `ping-software`
4. Cross-platform or service-layer question → `cross-platform`

## Step 3 — Select reference tier

1. **Curated anchors** (`references/curated/`) — canonical, task-completing docs. Load 1–3 max.

## Step 4 — Stop condition

Stop retrieving context as soon as the task can be completed. Do not pre-load every anchor.

## Cross-skill escalation

If task spans skills, complete primary routing first, then reference the secondary skill explicitly rather than loading its full context.
