# Ping Identity Plugin

Agent skills for configuring, integrating, and operating Ping Identity platforms.

## What this plugin is for

- Orienting agents on which Ping platform applies to a given task
- Configuring and administering PingOne MT (multi-tenant cloud), PingOne ST (single-tenant), and on-premises Ping software
- Designing orchestration flows (DaVinci, PingOne ST journeys, PingAM trees)
- Integrating Ping into web, mobile, and SDK-based applications
- Using Ping Universal Services (Protect, Verify, IGA, Credentials, Authorize)
- Understanding Ping's Identity for AI and Verified Trust capabilities

## Skill role: context, not execution

MCP tools handle execution — they can create, update, and delete platform resources directly. These skills supply what the tools lack: platform architecture, correct configuration sequencing, key constraints, gotchas, and decision logic. Use skills to reason correctly about *what* to configure and *why*, then let MCP tools carry out the work.

## MCP tool-first execution

**If MCP tools are available for the target platform, always use them — do not instruct the user to make changes manually.**

Before responding to any configuration or administration request, scan your available tool list for tools that can perform the required operation against the target platform (PingOne ST, PingOne MT, etc.). If matching tools exist, use them to make the change directly.

**Execution order:**
1. Check available tools for operations matching the task (create, update, delete, list, get for the relevant resource type)
2. If found: use the tool, report what was done, show relevant IDs or output
3. If not found or the tool call fails: fall back to step-by-step console instructions

**Never ask the user to click through the admin console for an operation an MCP tool can perform.** A direct tool call is always preferred over written instructions.

## What this plugin is NOT for

- Generic identity concepts not specific to Ping products
- Non-Ping identity platforms (Okta, Auth0, Microsoft Entra, etc.)
- Application business logic unrelated to identity
- Infrastructure provisioning beyond what is required to deploy Ping software

## Standalone operation

This plugin is self-orienting. When installed without the full `agent-skills` repo, it carries its own:

- Platform and product scope (`platform-scope.md`)
- Skill map and routing (`plugin-map.md`, `routing-hints.md`)
- Reference index (`references/index.json`)

Load order for a plugin-only install:
1. `README.md` → orientation
2. `plugin-map.md` → skill selection
3. `platform-scope.md` → platform detection
4. `routing-hints.md` → routing fallback (replaces `/shared/taxonomies/routing-rules.md`)
5. Selected `skills/<skill>/SKILL.md`
6. `ping-quickstart`: load from `skills/ping-quickstart/references/` (flat — 1–2 files max)
7. Other skills: `skills/<skill>/references/curated/` → 1–3 curated anchors, then `references/generated/<branch>/` if needed

## Full repo

When the full `agent-skills` repo is present, defer to `/shared/taxonomies/` for canonical routing rules and platform definitions. The files in this plugin are a compact local subset — the full repo is authoritative.
