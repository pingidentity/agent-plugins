# PingDirectory API

PingDirectory provides a documented Directory REST API for HTTP access to directory data and operations. LDAP, SCIM, and SDK integrations remain separate product surfaces.

## Intent routing
| Request signal | Use when | Continue with |
|---|---|---|
| Directory REST | Access directory resources over HTTP | [Directory REST API](https://docs.pingidentity.com/pingdirectory/latest/pingdirectory_server_administration_guide/pd_ds_directory_rest_api.html) |
| LDAP or SCIM | Use LDAP operations or the SCIM servlet extension | [PingDirectory documentation](https://docs.pingidentity.com/pingdirectory/latest/pd_ds_intro_pindirectory_server.md) |

## Boundary
This handoff does not replace LDAP schema, access-control, replication, or Java SDK guidance. Verify the API behavior for the deployed version.

## Source
- [Directory REST API](https://docs.pingidentity.com/pingdirectory/11.1/pingdirectory_server_administration_guide/pd_ds_directory_rest_api.html)
- [PingDirectory official documentation](https://docs.pingidentity.com/pingdirectory/11.1/pd_ds_intro_pindirectory_server.md)
