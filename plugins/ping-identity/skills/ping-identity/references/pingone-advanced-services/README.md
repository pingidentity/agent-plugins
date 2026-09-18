# PingOne Advanced Services

## Overview
PingOne Advanced Services is a managed cloud identity platform providing each organization isolated environments and a dedicated cloud network. Ping Identity operates the infrastructure while customers configure identity services for secure sign-on across hybrid systems.

## Core Concepts
- **Managed infrastructure:** Ping Identity operates cloud resources, networking, scaling, recovery, and backups, reducing customer infrastructure-management work.
- **Environment model:** Production and optional development, test, and staging environments support development, acceptance, validation, and performance work.
- **Dedicated networking:** An isolated AWS VPC connects the service with on-premises systems, AWS resources, and other clouds.
- **Hybrid integration:** Open standards, legacy integrations, on-premises data and authentication sources, and identity-provider or service-provider roles support enterprise architectures.
- **Shared operations:** Ping Identity monitors infrastructure and deployments; customers monitor applications and configurations, with service requests for work outside self-service.
- **Configuration task types:** The [Advanced Services task summary](https://docs.pingidentity.com/pingoneadvancedservices/latest/task_summary_table/p1as_task_summary_table.html) separates customer-managed **self-service** configuration from **service requests** handled through the applicable Ping support process.

## When to use
- Choose it when dedicated isolation, customization, or complex hybrid and legacy integrations matter.
- Use it when managed infrastructure is needed alongside customer administration.

## When not to use
- It is not the best fit when standardized multitenant SaaS and centralized administration are priorities; see PingOne Cloud Platform.
- Do not use development or test environments for performance or load testing; use staging instead.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingoneadvancedservices/latest/index.md)
