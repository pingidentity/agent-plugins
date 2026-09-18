# PingOne Advanced Services API

Use this handoff to select self-service administrative API documentation for a PingOne Advanced Services environment. It does not treat service-request work as a customer API or replace release-specific schemas and procedures.

## Intent routing
| API area | Request signals or operations | Deployment or version status | Continue with |
|---|---|---|---|
| Platform self-service | Manage administrators, use the platform administrative API, or create and update virtual hosts | Documentation and schemas are environment- and version-sensitive; verify the current P1AS environment | [Platform Admin API interactive documentation](https://docs.pingidentity.com/pingoneadvancedservices/latest/task_summary_table/p1as_platform_admin_api.html#interactive_api) |
| PingAccess self-service | Manage applications, authentication requirements, identity mappings, rules, or web sessions | Use the PingAccess surface exposed through the Advanced Services environment; verify the deployed release | [PingAccess API handoff](../pingaccess/api.md) |
| PingFederate self-service | Manage applications, authentication policies, or data sources | Use the PingFederate surface exposed through the Advanced Services environment; verify the deployed release | [PingFederate API handoff](../pingfederate/api.md) |
| PingDirectory self-service | Modify directory entries or other directory data | No dedicated PingDirectory API handoff is asserted for this Advanced Services self-service path; do not substitute a self-managed product API | Unavailable in this portfolio handoff; verify the current Advanced Services task summary |
| Service-request configuration | Request platform-managed operations, file-system changes, server configuration, certificates, SIEM, upgrades, testing, or other service-request items | Service-request work is handled through the applicable managed support process, not presented here as self-service REST | [Advanced Services task summary](https://docs.pingidentity.com/pingoneadvancedservices/2.2/task_summary_table/p1as_task_summary_table.html) |

## Source
- [Advanced Services task summary](https://docs.pingidentity.com/pingoneadvancedservices/2.2/task_summary_table/p1as_task_summary_table.html)
- [Platform Admin API interactive documentation](https://docs.pingidentity.com/pingoneadvancedservices/latest/task_summary_table/p1as_platform_admin_api.html#interactive_api)
