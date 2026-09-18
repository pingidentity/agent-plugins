# Identity for AI

## Overview
Identity for AI is Ping Identity’s approach to securing, governing, and managing autonomous AI agents. It helps organizations understand agents and control their access.

For a high-level fulfillment sequence and critical configuration concepts for securing digital assistants, see the [securing digital assistants blueprint](blueprint.md).

## Core Concepts
- **Agent identity and governance** classify agents and distinguish managed agents from those outside the organization’s trust boundary, enabling appropriate oversight.
- **Agent types** include personal agents, digital assistants, and digital workers; the category determines ownership, authorization, monitoring, and approval needs.
- **Delegated access** lets an agent act for a human without impersonation, using scoped, audience-limited tokens that identify both the user and acting agent.
- **Token exchange and attribution** preserve delegation chains so services and telemetry can distinguish users from participating agents.
- **MCP and A2A security** protect agent access to tools and resources, and agent-to-agent collaboration, through authentication, authorization, and auditable requests.

## When to use
- Securing digital assistants or autonomous agents that access APIs, MCP servers, or business resources.
- Applying least privilege and traceable delegated access to agent actions.
- Establishing governance across multi-agent or AI-platform integrations.

## When not to use
- General model safety, content moderation, or AI behavior controls outside identity and access management.
- Product-specific configuration; use the relevant Ping product documentation for implementation detail.

For an implementation blueprint, see [Identity for AI: Securing Digital Assistants Blueprint](blueprint.md).

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/solution-guides/identity-for-ai/identity-for-ai-solutions.md)
