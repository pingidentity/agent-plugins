# Ping Government Identity Cloud (FedRAMP)

## Overview
Ping Government Identity Cloud is a managed SaaS service for government organizations and customers with strict security and compliance needs. Hosted on AWS GovCloud, it provides isolated resources for identity and access management.

## Core Concepts
- **Compliance posture:** FedRAMP High and DoD Impact Level 5 provisional authorizations support government security requirements.
- **Managed environments:** Production and non-production environments separate live service from development, testing, and pre-release validation.
- **Identity services:** Federation supports shared access; PingDirectory repositories store identity data; provisioning automates account lifecycle changes.
- **Connectivity and operations:** An isolated VPC connects AWS GovCloud or on-premises sources; secure containers, monitoring, and log forwarding support resilience and visibility.

## When to use
- Government agencies, suppliers, or partners handling sensitive information and needing managed identity infrastructure.
- Teams connecting existing directories or applications while retaining control of product configuration.

## When not to use
- Not for multicloud deployments or direct access to normal AWS features; choose a service designed for that model.
- Do not use Production, Dev, or Test for load testing; Stage requires documented approval.
- Marketplace kits, nodes, and connectors are not guaranteed compatible with PGIC images; use supported Ping integrations.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pgic/index.md)
