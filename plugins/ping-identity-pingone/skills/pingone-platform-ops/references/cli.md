---
title: "PingOne platform operations CLI mode"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["validation"]
services: []
audience: ["admin", "operator", "developer"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: false
last_updated: "2026-08-26"
slug: ""
---
# PingOne platform operations CLI mode

Use Ping CLI for authorized PingOne audit and Bill of Materials operations.

## Scope

**Covers:** CLI discovery and authenticated API calls for audit activities and environment BOM data.

**Does NOT cover:** DaVinci execution tracing.

## Prerequisites

Use an authenticated PingOne CLI profile with access to the target environment. Discover commands and flags with `-h` at every level; the installed CLI is the source of truth. Apply the investigation and guardrail rules from `playbooks/audit-investigation.md` and `catalogs/audit-guardrails.md`.

## Audit and BOM endpoints

`pingcli davinci` and `pingcli pingone` do not expose the execution and audit collections needed by this skill. Use authenticated API requests through `pingcli pingone api` for:

| Operation | API path |
|---|---|
| Audit activity search | `environments/<env-id>/activities` |
| Full audit activity | `environments/<env-id>/activities/<activity-id>` |
| Environment BOM | `environments/<env-id>/billOfMaterials` |

Execution and audit filters use the API's SCIM-style syntax. Resolve usernames or email addresses through the environment users collection before querying audit activity. Follow `_links.next` until absent when the requested investigation requires complete pagination.

## Safety

Treat CLI, HTTP, and authorization errors as evidence gaps, not product or flow failures. Never print credentials or tokens, and do not persist audit output, BOM output, or PII beyond the current session.
