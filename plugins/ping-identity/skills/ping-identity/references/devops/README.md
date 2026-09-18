# Ping Identity Container & Kubernetes Deployment (Ping DevOps & ForgeOps)

## Overview
This skill covers containerized deployment frameworks for Ping Identity solutions. It combines Ping Identity DevOps (focused on traditional Ping products via Docker, Compose, and Kubernetes) and ForgeOps (focused on Ping Advanced Identity Software deployed natively on Kubernetes).

## Product Scope & Distinctions

* **Ping DevOps:** Covers PingFederate, PingAccess, PingAuthorize, and PingDirectory.
* **ForgeOps:** Covers PingAM, PingIDM, and PingDS (Ping Advanced Identity Software).

## Core Concepts

* **Container Packaging:** Pre-packaged Docker images document ports, tags, and environment variables to streamline runtime selection across Compose, Helm, and Kubernetes.
* **Configuration Baselines & Customization:** Server profiles (Ping DevOps) along with Helm charts and Kustomize resources (ForgeOps) externalize configuration from images to enable reusable baselines and customizable environments.
* **Environment Externalization:** Variable substitution decouples deployment-specific settings from underlying profile baselines and manifests.
* **Lifecycle & Automation:** Lifecycle hooks (shell scripts) and orchestration utilities handle startup behavior, operational automation, upgrades, and platform maintenance.
* **Production Preparation:** ForgeOps supplies guidance for security hardening, monitoring, alerting, data protection, recovery, sizing, and performance validation on Kubernetes.

## When to Use

* Standardizing and containerizing Ping product environments across local dev, staging, and production.
* Rapidly launching local development or demo environments using Docker Compose (Ping DevOps).
* Building, testing, and planning Kubernetes-based deployments for Ping Advanced Identity Software or enterprise orchestration patterns.

## When Not to Use

* Detailed product-specific setup: Use individual product documentation for feature-level configuration rather than container deployment guides.
* Out-of-the-box production runs: Reference architectures and default deployments (especially ForgeOps) require validation, customization, and security tailoring before production exposure.
* Kubernetes deployments without prerequisites: Avoid running ForgeOps in production without strong Kubernetes and cloud-native architecture expertise.

## Source

* [Product Index](https://docs.pingidentity.com/product-index.html)
* [Ping DevOps Official Documentation](https://developer.pingidentity.com/devops/overview.md)
* [ForgeOps Official Documentation](https://docs.pingidentity.com/forgeops/latest/index.md)
