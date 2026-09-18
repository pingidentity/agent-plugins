# PingDS API

PingDS exposes LDAPv3 access and an HTTP-based HDAP interface that maps JSON resources to LDAP entries. Treat HDAP as an evolving interface and verify the deployed release.

## Intent routing
| Request signal | Use when | Continue with |
|---|---|---|
| HTTP or JSON access | Map HTTP operations to directory resources | [PingDS HTTP access (HDAP)](https://docs.pingidentity.com/pingds/rest-guide/preface.html) |
| LDAP access | Perform directory-native authentication, search, or updates | [PingDS official documentation](https://docs.pingidentity.com/pingds/latest/index.md) |

## Source
- [PingDS HTTP access](https://docs.pingidentity.com/pingds/rest-guide/preface.html)
- [PingDS official documentation](https://docs.pingidentity.com/pingds/latest/index.md)
