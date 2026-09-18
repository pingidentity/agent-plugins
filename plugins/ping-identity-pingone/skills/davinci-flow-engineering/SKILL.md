---
name: davinci-flow-engineering
description: "Use when tracing, debugging, or explaining a PingOne DaVinci flow execution failure."
compatibility: "Designed for PingOne DaVinci execution troubleshooting. Live investigation requires authorized PingOne MCP access or Ping CLI 1.4.0 or later."
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# DaVinci Flow Engineering

Route each request to the reference that owns its use case. This skill currently covers troubleshooting.

## Decision Trees

| Trigger | Reference |
|---|---|
| Tracing, debugging, or explaining a PingOne DaVinci flow execution failure by username, email, interaction ID, transaction ID, flow, or time window. Correlates subflows and produces an evidence-based timeline, root cause, confidence rating, and remediation. | `references/troubleshooting.md` |
