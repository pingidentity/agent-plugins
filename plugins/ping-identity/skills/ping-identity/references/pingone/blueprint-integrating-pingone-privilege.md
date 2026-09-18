# Researching a PingOne Privilege integration

## Scope

Use this as a focused research brief for **PingOne Privilege**, Ping Identity's cloud privileged-access-management product. Keep the product boundary explicit: this brief concerns privileged access to cloud infrastructure, Kubernetes, network infrastructure, databases, and applications, together with the documented access and workflow integration surfaces.

### Covers

- **Administrative/interface plane:** Privilege organization and administrator/user scope, deployment-model choice, target account or resource ownership, gateways or relays, service-account ownership, and workflow integration boundaries.
- **Runtime/access plane:** just-in-time privileged-access requests, supported access protocols, agent-based or agentless access, session visibility, and the application or workflow response to an access request.

### Does NOT cover

- Tenant mutations, commands, scripts, API payloads, secrets, policy values, agent installation, gateway installation, or executable access procedures.
- General PingOne authentication, authorization, SSO, or identity-lifecycle configuration. Use the relevant PingOne or product reference for those boundaries.
- A claim that a cloud account, Kubernetes cluster, network target, application, gateway, agent, or service account is ready merely because it is represented in an administrative view.

Treat this as orientation, not a configuration or operations runbook. Confirm the current Privilege documentation for the target release and deployment model.

## Research brief

Research two related planes:

- **Administrative/interface plane:** identify the Privilege organization, administrator and user populations, target resources, and chosen deployment model. Determine whether the design uses agent-based or agentless access, and whether it requires an AWS, Azure, or GCP account; an EKS, AKS, GKE, or other Kubernetes target; SSH, RDP, database, or application access; and a gateway, private gateway, or private relay. Establish who owns service accounts and any Jira, Microsoft Teams, ServiceNow, or Slack workflow integration. These are distinct dependencies even when they support one access request.
- **Runtime/access plane:** determine how the user reaches the target, what temporary access or approval context is available, which documented protocol or integration surface is used, and where session visibility or termination is handled. Separate Privilege's access decision and session controls from the target cloud provider, cluster, network, database, or application. The exact request, approval, credential, session, and audit behavior is release- and configuration-sensitive.

A documented integration lifecycle can be researched as: select the target and deployment model; establish the required account, network, protocol, application, or workflow relationship; request or obtain the authorized privileged-access context; access the target through the supported surface; and verify the resulting session and operational evidence. The precise authorization, approval, credential, and session contract must come from the current Privilege documentation rather than inference from product summaries.

## Resource index

### Privilege product and deployment boundary

- [PingOne Privilege documentation](https://docs.pingidentity.com/privilege/index.html)
- [Introduction](https://docs.pingidentity.com/privilege/getting-started/introduction.md)
- [Key concepts](https://docs.pingidentity.com/privilege/getting-started/key-concepts.md)
- [Choosing a deployment model](https://docs.pingidentity.com/privilege/getting-started/choosing-deployment-model.md)

### Access and target integrations

- [Certificate-based SSH](https://docs.pingidentity.com/privilege/configuration/access-protocols/ssh.md)
- [Remote desktop](https://docs.pingidentity.com/privilege/configuration/access-protocols/rdp.md)
- [Cloud accounts](https://docs.pingidentity.com/privilege/configuration/cloud-accounts/index.md)
- [Kubernetes access](https://docs.pingidentity.com/privilege/configuration/configuring-kubernetes-access/index.md)
- [Database access](https://docs.pingidentity.com/privilege/configuration/cloud-accounts/database-access.md)
- [Internal and SAML applications](https://docs.pingidentity.com/privilege/privileged-access-management/admin-tasks/access-management/internal-applications.md)
- [Network gateways](https://docs.pingidentity.com/privilege/configuration/network-infrastructure/configuring-private-gateways.md)
- [MCP gateway](https://docs.pingidentity.com/privilege/configuration/mcp-gateway.md)

### Workflow and administration surfaces

- [Jira integration](https://docs.pingidentity.com/privilege/integrations/jira.md)
- [Microsoft Teams integration](https://docs.pingidentity.com/privilege/integrations/microsoft-teams.md)
- [ServiceNow integration](https://docs.pingidentity.com/privilege/integrations/servicenow.md)
- [Slack integration](https://docs.pingidentity.com/privilege/integrations/slack.md)
- [Service accounts](https://docs.pingidentity.com/privilege/privileged-access-management/admin-tasks/directory/service-accounts.md)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product boundary | Is the request for PingOne Privilege PAM, or for general PingOne identity and access management? Which administrator, user, target, and population are in scope? | Stop and clarify when the target product or PAM boundary is ambiguous. |
| Deployment model | Is access agent-based or agentless? Which device, target, network, and operational constraints drive that choice? | Verify current supported model and release; do not treat one deployment path as universal. |
| Target topology | Which cloud account, Kubernetes cluster, network target, database, SSH/RDP endpoint, application, or MCP server is in scope? | Verify target-specific prerequisites, ownership, and network path in current documentation. |
| Access and session behavior | What access protocol or client surface is used? How are temporary access, approvals, session visibility, termination, and evidence represented? | Distinguish documented behavior from assumptions about credentials, TTLs, approvals, or audit fields. |
| Network and credentials | Are a gateway, private gateway, private relay, agent, or service account required? Where are secrets and trust relationships owned? | Verify target release, least privilege, secret handling, egress, and rotation requirements. |
| Workflow integrations | Is Jira, Teams, ServiceNow, Slack, or another documented integration part of the request? What system owns the request or notification state? | Confirm the current connector contract and failure/ownership boundaries. |
| Promotion and operations | What is recreated or verified across Privilege environments, targets, networks, and workflow systems? | Recheck bindings, agents, gateways, accounts, service accounts, secrets, monitoring, and drift. |

## Guardrails and report

Keep these distinctions visible:

- PingOne Privilege is a cloud PAM product; it is not a generic replacement for PingOne authentication, authorization, federation, or lifecycle services.
- Agent-based and agentless access are different deployment surfaces. Cloud-account onboarding, Kubernetes access, network gateways, application access, and workflow integrations are separate dependencies.
- A configured target, successful login, or visible session does not by itself prove that temporary authorization, least privilege, network controls, audit evidence, or termination behavior meets the intended policy.
- Product documentation is comparatively sparse for some Privilege integration details. Do not invent API, CLI, connector, approval, credential, session, or policy semantics when the current source does not document them.
- Resource, region, release, tenant, and integration limits are not established by this brief. Preserve unresolved questions and verify them in current official documentation.

Report: (1) the Privilege PAM and deployment-model boundary; (2) verified target, network, credential, and workflow readiness; (3) documented access and session behavior; (4) promotion, operations, and unresolved checks; (5) facts versus inference, tenant-specific observations, and release-sensitive claims; and (6) the appropriate handoff to the [PingOne Privilege reference](./README.md) or current official documentation. Do not turn the report into an installation or access runbook.
