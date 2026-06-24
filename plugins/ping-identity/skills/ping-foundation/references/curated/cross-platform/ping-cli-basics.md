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
last_updated: "2026-06-22"
slug: "https://developer.pingidentity.com/pingcli/"
---

# Ping CLI — Configuration Automation Basics

Scriptable, deterministic configuration management across PingOne, PingFederate, DaVinci, and the Ping universal services using the `pingcli` command-line tool.

## Scope

**Covers:** Install and first-run, configuration profile model, connecting Ping services, CRUD via per-product subcommands, `pingcli platform export` for Configuration-as-Code / Terraform HCL, `pingcli request` for unmodeled endpoints, CI/CD patterns, and the migration from the legacy `pingctl` tool.

**Does NOT cover:** Interactive agent-driven config — use the PingOne MCP Server or DaVinci MCP Server for that. Long-term Terraform state management — see the PingOne and PingFederate Terraform providers at `developer.pingidentity.com/terraform/`. DaVinci flow design — see `ping-orchestration`. PingFederate console or federation configuration — see `references/curated/ping-software/pingfederate-basics.md`. Per-service policy semantics (Protect risk, Verify KYC) — see `ping-universal-services`.

---

## What Ping CLI is

Ping CLI (`pingcli`) is the unified open-source CLI for managing configuration across PingOne, PingFederate, DaVinci, and the Ping universal services. It provides:

- A consistent CRUD interface for admin operations without raw `curl` calls
- Multi-product Configuration-as-Code export (`pingcli platform export`) for Terraform integration
- Profile-based authentication so the same scripts run against dev, staging, and production
- Raw admin API access with managed auth for endpoints that don't yet have first-class commands

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

| Operation | Command (1.0) |
|---|---|
| Create a profile | `pingcli config profiles create --name dev` |
| Switch active profile | `pingcli config profiles use dev` |
| List profiles | `pingcli config profiles list` |
| View active profile | `pingcli config view-profile` |
| Delete a profile | `pingcli config profiles delete dev` |

> **Version note:** Ping CLI 0.8 used different subcommand names (`add-profile`, `set-active-profile`). If commands fail, verify your installed version with `pingcli version` and cross-check the [0.8 command reference](https://developer.pingidentity.com/pingcli/0.8/command_reference/pingcli_config.html) if needed.

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

# PingFederate — raw admin API call (GET /oauth/clients)
pingcli pingfederate api GET /oauth/clients
```

Universal-service connectors are accessible both at top level (`pingcli davinci ...`, `pingcli mfa ...`) and under the PingOne connector umbrella (`pingcli pingone davinci ...`). Both paths use the same PingOne Worker app credentials.

---

## `pingcli platform export`

Exports multi-product configuration as Configuration-as-Code packages, optionally as Terraform HCL `import {}` blocks.

```bash
# Export all connected products
pingcli platform export

# Export only PingOne services
pingcli platform export --service-group pingone

# Export as Terraform HCL (requires pingcli-plugin-terraformer)
pingcli platform export --format HCL
```

**Export availability per product:** Not all products produce HCL today. `pingone-platform`, `pingone-sso`, `pingone-mfa`, `pingone-protect`, `pingone-authorize`, and `pingfederate` are supported; `pingone-davinci`, `pingone-credentials`, and `pingone-verify` are listed but export support is partial. Always check the [product compatibility page](https://developer.pingidentity.com/pingcli/latest/product-compatibility.html) for the current status.

**Terraformer plugin:** `pingcli-plugin-terraformer` (installed via `pingcli plugin add`) produces opinionated, ready-to-store HCL with post-processing suited for GitOps promotion pipelines.

---

## Custom API requests

For endpoints without a first-class subcommand, use the raw request interfaces. The CLI injects auth, base URL, and retry handling automatically.

```bash
# Generic request (all products)
pingcli request GET /pingone/environments/<envId>/applications

# Product-specific wrappers (1.0)
pingcli pingone api GET /environments/<envId>/applications
pingcli pingfederate api GET /oauth/clients
```

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
pingcli -D platform export
# Exit 0 = success; 1 = error; 2 = success with warnings
```

**Profile-per-environment promotion pattern:** Create one profile per environment (dev/staging/prod), each binding to a different Worker app. A promotion script switches profiles and runs the export or create commands.

---

## Prerequisites

- PingOne: Worker application with the required admin roles; `clientId`, `clientSecret`, `environmentId`, and region.
- PingFederate: Admin API OAuth client; admin base URL (HTTPS, port 9999 by default).
- Network access from the CLI host to each product's admin API endpoint.
- For Terraform HCL export: `pingcli-plugin-terraformer` installed via `pingcli plugin add`.

---

## Common variants

| Variant | Notes |
|---|---|
| Single tenant, one profile | Default setup; one profile, one Worker app |
| Multi-environment promotion | One profile per env; promotion script switches profiles before export/create |
| Docker-only CI | Run `pingidentity/pingcli:latest` as a container step; pass credentials as env vars |
| Terraform GitOps | `pingcli platform export --format HCL` + Terraformer plugin + Terraform plan/apply in PR pipeline |
| Migrating from `pingctl` | Re-configure profiles under `pingcli`; `pingctl` commands are not compatible |

---

## Common gotchas

| Symptom | Cause | Fix |
|---|---|---|
| 404 on environment lookup | Wrong region in profile | Verify region string matches the PingOne tenant domain (e.g., `eu` for `pingone.eu`) |
| 403 on `applications create` | Worker app missing roles | Verify the Worker app has the required admin roles in the PingOne environment |
| 0.8 profile commands fail on 1.0 | Command names changed between versions | Run `pingcli version`; update scripts to use 1.0 command names (`profiles create`, not `add-profile`) |
| `platform export` returns empty package for a service | Service not yet supported for export | Check the product compatibility matrix; use `pingcli request` as fallback |
| `pingcli init` wizard skips a service | Service credentials not configured | Re-run `pingcli config set` for the missing service manually |

---

## Related references

- `references/curated/cross-platform/foundation-overview.md` — platform overview and admin model
- `references/curated/cross-platform/core-admin-patterns.md` — cross-product admin patterns
- `references/curated/pingone-mt/app-registration.md` — Worker app setup (prerequisite for PingOne auth)
- `references/curated/ping-software/pingfederate-basics.md` — PingFederate admin API context

---

## Source

- [Ping CLI overview](https://developer.pingidentity.com/pingcli/)
- [Install guide](https://developer.pingidentity.com/pingcli/latest/pingcli_landing_page.html)
- [Product compatibility matrix](https://developer.pingidentity.com/pingcli/latest/product-compatibility.html)
- [Command reference](https://developer.pingidentity.com/pingcli/latest/command_reference/pingcli.html)
- [Exporting platform configuration](https://developer.pingidentity.com/pingcli/general/exporting-platform-configuration.html)
- [Configuration promotion overview](https://developer.pingidentity.com/config-automation-promotion/configuration_promotion_landing_page.html)
- [GitHub: pingidentity/pingcli](https://github.com/pingidentity/pingcli)
