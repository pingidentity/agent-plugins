# Capability Map

Maps user intents to the owning umbrella skill. Used by SKILL.md routing logic and agents to determine the correct skill before loading references.

## Capability Buckets

| Capability | Owning Skill | Description |
|---|---|---|
| Orientation / "Where do I start?" | ping-quickstart | Product detection, platform selection, initial direction |
| Setup / Admin / Configuration | ping-foundation | Tenant setup, apps, directories, policies, branding, on-prem admin |
| Flows / Journeys / Orchestration | ping-orchestration | DaVinci flows, AIC journeys, PingAM auth trees |
| AI identity / Agent trust | ping-identity-for-ai | Identity for AI, Verified Trust, agent security patterns |
| Shared strategic services | ping-universal-services | Protect, Verify, Credentials, SSO, IGA, Neo, Authorize |
| App / SDK / mobile integration | ping-app-integration | Web, mobile, SDK, browser flows, on-prem app integration |

## Boundary Rules

- **ping-foundation vs ping-app-integration**: foundation = admin and platform configuration; app-integration = code-level integration, SDK usage, app-side flows
- **ping-foundation vs ping-universal-services**: foundation = core tenant/environment setup; universal-services = cross-platform shared services invoked after setup
- **ping-orchestration vs ping-app-integration**: orchestration = designing and configuring flows/journeys; app-integration = implementing the app-side client that calls into those flows
- **ping-universal-services vs ping-foundation**: universal services are consumed capabilities, not configuration destinations

## Escalation Path

If a task spans more than one capability bucket, route to the first relevant skill and let its SKILL.md cross-reference the others.
