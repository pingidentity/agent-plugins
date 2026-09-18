<p align="center">
  <img src="assets/banner-build-with-ai.png" alt="A banner representing building with Ping using AI.">
</p>

# Ping Identity Agent Plugins

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ping Identity Agent Plugins give AI coding agents deep knowledge of the Ping Identity platform through purpose-built skills for platform foundations, flow and journey design, execution troubleshooting, and application integration. These skills help take the burden off you having to prompt-engineer Ping context. 

> [!NOTE]
> Plugins are being updated periodically. Check back here for updates!

**[Features](#features) | [Install](#install) | [Install Manually](#install-manually) | [MCP Servers](#mcp-servers) | [CLI Execution](#cli-execution) | [Plugins & Skills](#plugins--skills) | [Example Prompts](#example-prompts) | [Contributing](#contributing) | [Feedback](#feedback) | [Related Resources](#related-resources) | [License](#license)**

---

## Features

- **Ping Identity platform expertise**: Skills give AI agents the right context upfront so they can answer questions, design architectures, and write integrations without guessing.
- **Works with major AI coding agents**: Claude Code, Cursor, GitHub Copilot, Gemini CLI, and other agents that support skills or instruction files.
- **MCP-aware execution**: Certain skills use Ping's remote MCP server to perform actions. For example, the AIC journey design skill uses MCP tools to create and update PingOne Advanced Identity Cloud journeys when available; the DaVinci skills use PingOne MCP tools for live operations. Without MCP, the skills produce design and implementation artifacts without assuming a tool setup.
- **Multiple plugins covering various domains**: This repository provides plugins for human orientation, agents, as well as domain-specific ones.
- **Progressive context loading**: Skills load only what the agent needs for the task at hand, reducing token usage.

---

## Install

| Agent | Command |
|---|---|
| **Claude Code** | `/plugin marketplace add https://github.com/pingidentity/agent-plugins` |
| **Cursor** | Settings → Plugins → search and add `https://github.com/pingidentity/agent-plugins` |
| **GitHub Copilot** | Clone this repo, then add the relevant `SKILL.md` files to `.github/copilot-instructions.md` in your project |
| **Gemini CLI** | Add the relevant skill instructions to `GEMINI.md` in your project |
| **OpenCode / other** | `npx skills add pingidentity/agent-plugins` (via Skills CLI); see [skills.sh](https://skills.sh) for agent-specific setup |

> [!IMPORTANT]
> This marketplace distributes different plugin surfaces:
> - **`ping-identity-quickstart`**: human-facing front door for platform detection, orientation, and routing.
> - **`ping-identity`**: cross-portfolio plugin containing the ping-identity foundations skill with portfolio reference topics.
> - **`ping-orchestration-sdks`**: companion SDK plugin sourced from [`pingidentity/ping-sdk-agent-skills`](https://github.com/pingidentity/ping-sdk-agent-skills), with deep client-side integration skills when you need to embed PingOne AIC/PingAM journeys (trees) or PingOne DaVinci into your mobile and web apps.
> Product/solution specific plugins, such as **`ping-identity-pingone`** and **`ping-identity-pingone-aic`** — providing instructions scoped to individual products and use cases.

---

## Install Manually

You can also install using the Skills CLI:

```bash
npx skills add pingidentity/agent-plugins
```

For deep Android, iOS, React, and JavaScript client-side integration skills, also install the companion repository:

```bash
npx skills add pingidentity/ping-sdk-agent-skills
```

Or install a specific local plugin:

```bash
npx skills add pingidentity/agent-plugins/plugins/ping-identity-quickstart
npx skills add pingidentity/agent-plugins/plugins/ping-identity
npx skills add pingidentity/agent-plugins/plugins/ping-identity-pingone
npx skills add pingidentity/agent-plugins/plugins/ping-identity-pingone-aic
```

> [!TIP]
> The skills work better together. Install the quickstart and cross-portfolio plugins for orientation plus implementation guidance, add the companion SDK plugin when you are building mobile or web client integrations and add the domain-specific plugins for tailored domain guidance.

---

## MCP Servers

Ping provides two remote MCP servers; one for AIC and one for PingOne. For more information on loading the MCP servers alongside these skills, refer to [AIC](https://developer.pingidentity.com/build-with-ai/aic-remote-mcp-server/overview.html) and [PingOne](https://developer.pingidentity.com/build-with-ai/pingone-mcp-server/p1-overview.html) remote MCP servers.

When no MCP server is configured, the skills still provide flow designs, node sequencing, routing guidance, and app-side implementation artifacts. For precise product, API, SDK, or service details, the `ping-identity` skill directs the agent to current Ping developer or product documentation rather than assuming that a local CLI or console workflow is available.

## CLI Execution

Where available, certain skills in plugins reference the Ping CLI to perform execution. As with the MCP servers, when the Ping CLI is not configured, the skills provide the same benefit.

---

## Plugins & Skills

### `ping-identity-quickstart` (human-facing)

| Skill | What it does | Use when... |
|---|---|---|
| `ping-identity-quickstart` | Human front door — identifies the user's platform and goal, provides initial orientation, and hands off to the relevant skill | Platform is unknown; "where do I start"; evaluating or comparing Ping products; planning a migration |

### `ping-identity` (cross-portfolio, agent-facing)

| Skill | What it does | Use when... |
|---|---|---|
| `ping-identity` | Foundational portfolio layer — builds platform understanding across products, deployment models, solutions, integrations, and migration paths, then routes to authoritative docs or a downstream skill | You need product selection, cross-product architecture, solution orientation, migration planning, or journey/flow design principles |

### `ping-identity-pingone` (product-specific, agent-facing)

| Skill | What it does | Use when... |
|---|---|---|
| `davinci-flow-design` | Designs and builds PingOne DaVinci flows — registration, login, MFA enrollment and step-up, passkeys, subflow composition, error paths, and promotion | You are building or reviewing a DaVinci flow, or preparing flows for promotion between environments |
| `davinci-flow-engineering` | Traces and debugs live DaVinci flow executions using MCP evidence — actor/interaction/transaction correlation, subflow reconstruction, root cause and remediation | A flow execution failed or behaved unexpectedly and you need to find out why |
| `pingone-app-integration` | Implements app-side integration against a PingOne environment — SDK wiring for Android/iOS/JavaScript, OIDC/PKCE, CORS, Worker applications, push registration, and app-side troubleshooting | You are integrating an Android, iOS, JavaScript/React, or backend app with PingOne |

### `ping-identity-pingone-aic` (product-specific, agent-facing)

| Skill | What it does | Use when... |
|---|---|---|
| `aic-journey-design` | Designs and builds AIC journeys and PingAM authentication trees — node selection, wiring invariants, risk/MFA/passkey/recovery journeys — creating and updating journeys through AIC MCP tools when connected | You are building login, registration, recovery, MFA, step-up, passwordless, or social-login journeys in AIC or PingAM |
| `aic-app-integration` | Implements app-side integration against PingOne Advanced Identity Cloud (AIC) — Journey modules and journey client for Android/iOS/JavaScript, journey callbacks, OIDC/PKCE, tenant CORS, SAML, and app-side troubleshooting | You are integrating an Android, iOS, JavaScript/React, or backend app with AIC or PingAM |

### Companion plugin

- **`ping-orchestration-sdks`** — deep Android (Kotlin), iOS (Swift), and React/JavaScript SDK scaffolding and client-side integration guidance. It is sourced from [`pingidentity/ping-sdk-agent-skills`](https://github.com/pingidentity/ping-sdk-agent-skills), not stored under this repository's `plugins/` directory.

The quickstart skill routes orientation requests to the cross-portfolio plugin. Within `ping-identity`, use the foundations skill for advisory orientation; use the product plugins for app integration, flow/journey design, and troubleshooting. Product-specific details remain in current Ping documentation and downstream companion skills.

---

## Example Prompts

| # | Prompt | Plugin / Skill |
|---|---|---|
| 1 | "I'm new to Ping Identity and need to add login to my app. Where do I start?" | ping-identity-quickstart / ping-identity-quickstart |
| 2 | "What's the difference between PingOne, PingOne Advanced Identity Cloud, and PingFederate? Which should I use?" | ping-identity-quickstart / ping-identity-quickstart |
| 3 | "Design a solution that uses PingOne for CIAM and PingOne Protect for risk scoring." | ping-identity / ping-identity |
| 4 | "Register a new OIDC application and connect it to a login flow in my PingOne environment." | ping-identity-pingone / pingone-app-integration + ping-identity-pingone / davinci-flow-design |
| 5 | "Compare hosted-page branding options across PingOne Advanced Identity Cloud and PingOne." | ping-identity / ping-identity |
| 6 | "Help me build a passwordless login journey using FIDO2/passkeys in PingOne Advanced Identity Cloud." | ping-identity-pingone-aic / aic-journey-design |
| 7 | "What nodes do I need to build a progressive profiling flow?" | ping-identity-pingone-aic / aic-journey-design |
| 8 | "Set up a password policy with lockout for an AIC environment." | ping-identity / ping-identity |
| 9 | "Give my AI agent a client-credentials identity so it can call our internal APIs securely." | ping-identity / ping-identity |
| 10 | "List all the journeys in my AIC tenant and show me which ones have MFA enabled." | ping-identity-pingone-aic / aic-journey-design + MCP |
| 11 | "Create a new login journey in my AIC sandbox that collects username and password, then sends an email OTP." | ping-identity-pingone-aic / aic-journey-design + MCP |
| 12 | "Migrate our on-prem PingAM authentication trees into AIC and modernize the orchestration design." | ping-identity-pingone-aic / aic-journey-design |
| 13 | "Set up an Active Directory integration and determine which Ping service should own user synchronization." | ping-identity / ping-identity |

Prompts marked "+ MCP" work best with the relevant Ping MCP execution tools connected. Without them, the design skills return a design or implementation artifact rather than performing live tenant changes.

> [!TIP]
> Extend these prompts with the AIC and PingOne remote MCP servers or the Ping CLI to enable your agents to take action.

---

## Contributing

We welcome contributions! Add a skill, improve an existing skill, or fix a documentation issue by opening a pull request in this repository. Before submitting a change to skill or reference content, run the repository validator:

```bash
python3 scripts/validate_skills.py --root .
```

Refer to [AGENTS.md](AGENTS.md) for the repository layout, skill metadata requirements, reference-authoring rules, and validation guidance.

## Feedback

If you have feedback, questions, or want to request a new skill:

- [Open an issue](https://github.com/pingidentity/agent-plugins/issues/new) with the appropriate label (`enhancement`, `bug`, `question`, or `skill-request`)
- Vote on existing issues with thumbs up to help us prioritize

## Related Resources

- [Ping Developer Portal](https://developer.pingidentity.com/)
- [Ping Developer Blog](https://developer.pingidentity.com/blog/)
- [Ping Identity Documentation](https://docs.pingidentity.com/)
- [Build with AI](https://www.pingidentity.com/en/resources/developer/build-with-ai.html)
- [Agent Skills Standard](https://agentskills.io/)
- [Skills CLI](https://skills.sh)

---

## Disclaimer

> **This code is provided by Ping Identity Corporation ("Ping") on an "as is" basis, without
> warranty of any kind, to the fullest extent permitted by law.
> Ping Identity Corporation does not represent or warrant or make any guarantee regarding the use of
> this code or the accuracy, timeliness or completeness of any data or information relating to this
> code, and Ping Identity Corporation hereby disclaims all warranties whether express, or implied or
> statutory, including without limitation the implied warranties of merchantability, fitness for a
> particular purpose, and any warranty of non-infringement.
> Ping Identity Corporation shall not have any liability arising out of or related to any use,
> implementation or configuration of this code, including but not limited to use for any commercial
> purpose.
> Any action or suit relating to the use of the code may be brought only in the courts of a
> jurisdiction wherein Ping Identity Corporation resides or in which Ping Identity Corporation
> conducts its primary business, and under the laws of that jurisdiction excluding its conflict-of-law
> provisions.**

## License

This software may be modified and distributed under the terms of the MIT license. See the [LICENSE](./LICENSE) file for details

© Copyright 2026 Ping Identity Corporation. All rights reserved.
