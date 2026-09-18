# PingAM API

Use the PingAM REST and protocol documentation to identify the API area for a self-managed deployment. Verify the exact PingAM release, deployment URL, realm, endpoint, and authorization context before generating requests.

## Intent routing
| API area | Request signals / operations | Deployment or version status | Continue with |
|---|---|---|---|
| REST API discovery and runtime authentication | Discover REST resources, authenticate with sessions or SSO tokens, or inspect release-specific endpoints | Release-specific; verify the installed release | [REST API guide](https://docs.pingidentity.com/pingam/latest/REST-guide/preface.html) and [authentication and SSO](https://docs.pingidentity.com/pingam/latest/am-authentication/preface.html) |
| OAuth 2.0 and OpenID Connect | Configure OAuth clients, tokens, scopes, or OIDC provider behavior | Release-specific; protocol endpoints are not administrative REST APIs | [OAuth 2.0](https://docs.pingidentity.com/pingam/latest/am-oauth2/preface.html) and [OpenID Connect 1.0](https://docs.pingidentity.com/pingam/latest/am-oidc1/preface.html) |
| Authorization and policy | Configure authorization applications, policies, resource types, or policy decisions | Release-specific | [Authorization](https://docs.pingidentity.com/pingam/latest/am-authorization/preface.html) |
| Federation | Configure or troubleshoot SAML federation behavior and endpoints | Release-specific; verify protocol and deployment configuration | [SAML 2.0](https://docs.pingidentity.com/pingam/latest/am-saml2/preface.html) |
| Realm and server administration | Manage realm, server, or deployment configuration and operations | Release-specific; use administrative REST only where the installed release documents it | [Setup and configuration](https://docs.pingidentity.com/pingam/latest/setup/preface.html) |

## Source
- [PingAM official documentation](https://docs.pingidentity.com/pingam/latest/index.md)
