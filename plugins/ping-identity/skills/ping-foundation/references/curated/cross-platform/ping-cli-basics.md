---
title: "Ping CLI — Configuration Automation Basics"
product_family: cross-platform
products: ["pingone", "pingfederate", "davinci", "pingone-authorize", "pingone-mfa", "pingone-protect", "pingone-verify", "pingone-credentials"]
capabilities: ["foundation"]
services: ["protect", "verify", "mfa", "credentials", "authorize"]
audience: ["admin", "developer", "operator"]
use_cases: ["workforce", "customer", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-24"
slug: "https://developer.pingidentity.com/pingcli/"
---

# Ping CLI — Configuration Automation Basics

Ping CLI (`pingcli`) is the unified open-source command-line tool for managing configuration across PingOne, PingFederate, DaVinci, and the Ping universal services.

## Scope

**Covers:** Why to use Ping CLI, install and first-run, configuration profile model, connecting Ping services, CRUD via per-product subcommands (1.x), CI/CD patterns.

**Does NOT cover:** `pingcli platform export` and `pingcli request` — these are 0.8 features not yet available in 1.x; see the [product compatibility matrix](https://developer.pingidentity.com/pingcli/latest/product-compatibility.html) for current 1.x feature availability. Interactive agent-driven config — use the PingOne MCP Server or DaVinci MCP Server. Long-term Terraform state management — see the PingOne and PingFederate Terraform providers. DaVinci flow design — see `ping-orchestration`. Per-service policy semantics — see `ping-universal-services`.

---

## Why Ping CLI

Ping CLI (`pingcli`) addresses the gap between the interactive admin console (good for humans, not scriptable) and raw REST API calls (scriptable, but require managing auth, base URLs, and retries manually). It provides:

- **Consistent CRUD interface** across PingOne, DaVinci, PingFederate, and the Ping universal services without raw `curl` calls
- **Profile-based authentication** so the same scripts run against dev, staging, and production using different credentials per environment
- **Automatic auth and base URL injection** — no per-command token management
- **CI/CD friendly** — non-interactive auth via env vars, `--output-format json`, detailed exit codes

For the current list of supported products and per-service CRUD availability, see the [product compatibility matrix](https://developer.pingidentity.com/pingcli/latest/product-compatibility.html).

> **Legacy note:** `pingctl` (earlier tool) is replaced by `pingcli`. Migrate by re-configuring profiles under the new tool.

---

## Install

| Platform | Method | Command |
|---|---|---|
| macOS | Homebrew (recommended) | `brew install pingidentity/tap/pingcli` |
| Linux | Package manager (apt/yum) or binary | See [Linux install guide](https://developer.pingidentity.com/pingcli/latest/install/linux.html) |
| Windows | Binary download | See [Windows install guide](https://developer.pingidentity.com/pingcli/latest/install/windows.html) |
| CI/CD | Docker image | `docker run pingidentity/pingcli:latest` |

Verify: `pingcli version`

---

## Configuration profiles

Profiles are named groups of settings stored in `$HOME/.pingcli/config.yaml`. Use one profile per target environment (dev, staging, prod).

| Operation | Command |
|---|---|
| Create a profile | `pingcli config profiles create --name dev` |
| Switch active profile | `pingcli config profiles use dev` |
| List profiles | `pingcli config profiles list` |
| View active profile | `pingcli config view-profile` |
| Delete a profile | `pingcli config profiles delete dev` |

---

## Connecting Ping services

Before using product subcommands, configure the service credentials in the active profile:

| Service | Prerequisites | Key config fields |
|---|---|---|
| PingOne | Worker application (client credentials) | `clientId`, `clientSecret`, `environmentId`, `region` |
| PingFederate | Admin API OAuth client | `baseURL`, `clientId`, `clientSecret` |
| DaVinci | Same Worker app as PingOne | Shares PingOne credentials |
| Universal services (MFA, Protect, Verify, Authorize, Credentials) | Same Worker app as PingOne | Share PingOne credentials via PingOne connector |

Use `pingcli init` for a guided first-run setup wizard. Configure manually with `pingcli config set`.

**Regions:** PingOne regions affect the base URL — ensure the profile uses the correct region string (`com`, `eu`, `asia`, `sg`, `ca`). A wrong region causes 404 on environment lookups.

---

## CRUD examples

Per-product subcommands follow consistent `list`, `get`, `create`, `update`/`replace`, `delete` patterns:

```bash
# PingOne — list environments
pingcli pingone environments list

# PingOne — create an application from a JSON config file
pingcli pingone applications create -f app.json

# DaVinci — list flows in an application
pingcli davinci flows list --application-id <id>

# PingOne MFA — replace a device policy
pingcli mfa device-policies replace -f policy.json
```

Universal-service connectors are accessible both at top level (`pingcli davinci ...`, `pingcli mfa ...`) and under the PingOne connector umbrella (`pingcli pingone davinci ...`). Both paths use the same PingOne Worker app credentials.

---

## CI/CD patterns

```bash
# Non-interactive auth (client credentials — no browser prompt)
export PINGCLI_PINGONE_CLIENT_ID=...
export PINGCLI_PINGONE_CLIENT_SECRET=...
export PINGCLI_PINGONE_ENVIRONMENT_ID=...
export PINGCLI_PINGONE_REGION=com

# JSON output for pipeline parsing
pingcli pingone applications list --output-format json

# Detailed exit codes for conditional pipeline steps
# Exit 0 = success; 1 = error; 2 = success with warnings
pingcli -D pingone environments list
```

**Profile-per-environment pattern:** Create one profile per environment (dev/staging/prod), each binding to a different Worker app. Scripts switch profiles to operate against the correct environment.

---

## Prerequisites

- PingOne: Worker application with the required admin roles; `clientId`, `clientSecret`, `environmentId`, and region.
- PingFederate: Admin API OAuth client; admin base URL (HTTPS, port 9999 by default).
- Network access from the CLI host to each product's admin API endpoint.

---

## Common variants

| Variant | Notes |
|---|---|
| Single tenant, one profile | Default setup; one profile, one Worker app |
| Multi-environment scripting | One profile per env; scripts switch profiles before running commands |
| Docker-only CI | Run `pingidentity/pingcli:latest` as a container step; pass credentials as env vars |
| Migrating from `pingctl` | Re-configure profiles under `pingcli`; `pingctl` commands are not compatible |

---

## Common gotchas

| Symptom | Cause | Fix |
|---|---|---|
| 404 on environment lookup | Wrong region in profile | Verify region string matches the PingOne tenant domain (e.g., `eu` for `pingone.eu`) |
| 403 on `applications create` | Worker app missing roles | Verify the Worker app has the required admin roles in the PingOne environment |
| `pingcli init` wizard skips a service | Service credentials not configured | Re-run `pingcli config set` for the missing service manually |

---

## Related references

- `references/curated/cross-platform/foundation-overview.md` — platform overview and admin model
- `references/curated/cross-platform/core-admin-patterns.md` — cross-product admin patterns
- `references/curated/pingone-mt/app-registration.md` — Worker app setup (prerequisite for PingOne auth)
- `references/curated/ping-software/pingfederate-basics.md` — PingFederate admin API context

---

## Source

- [Ping CLI overview and docs](https://developer.pingidentity.com/pingcli/)
- [Install guide](https://developer.pingidentity.com/pingcli/latest/pingcli_landing_page.html)
- [Product compatibility matrix](https://developer.pingidentity.com/pingcli/latest/product-compatibility.html)
- [Command reference](https://developer.pingidentity.com/pingcli/latest/command_reference/pingcli.html)
- [GitHub: pingidentity/pingcli](https://github.com/pingidentity/pingcli)
