---
title: "PingOne MT — Administrator Roles and Access Management"
product_family: pingone-mt
products: ["pingone"]
capabilities: ["foundation"]
services: []
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingone/administrators/p1_admin_roles.html"
---

# PingOne MT — Administrator Roles and Access Management

Configuring administrator roles, scoping access to environments and populations, and onboarding new administrators in PingOne MT.

## Scope

**Covers:** Built-in and custom administrator roles, role scoping (org / environment / population), three methods for adding administrators (individual, group, invitation), admin email verification, and the Administrators environment best practice.

**Does NOT cover:** End-user identity management — see `references/curated/pingone-mt/directory-and-populations.md`; application roles (PingOne Authorize authorization) — distinct from admin roles; PingOne ST admin configuration.

---

## Built-in administrator roles

PingOne uses a flat role model — there is no super-admin role with global permissions. Every role grants a specific set of permissions scoped to a level.

| Role | Key permissions |
|---|---|
| Organization Admin | Create/edit/delete environments; manage organization settings |
| Environment Admin | Manage environments, populations, password policies; invite roles |
| Identity Data Admin | Create/edit users; reset passwords; manage user attributes |
| Client Application Developer | Create/edit/delete applications; reset client secrets |
| Identity Data Read Only | Read-only subset of Identity Data Admin |
| Configuration Read Only | Read-only subset of Environment Admin |

Additional SSO roles delegate access to connected products (PingOne AIC, PingFederate) — scoped to the connected product's admin surface only.

**No role hierarchy:** You cannot assign a role that you do not hold. An Organization Admin cannot grant more permissions than their own grant level.

**Privileged permissions:** Some permissions grant access to sensitive data or destructive operations (delete environment, view personal user data). Assign these sparingly and review before delegating.

---

## Custom roles

Custom roles delegate a restricted subset of permissions for a specific resource set.

| Property | Detail |
|---|---|
| Scope | Environment-specific — must be recreated in each environment where needed |
| Who can create | Organization Admin, Custom Roles Admin, or a custom role with equivalent Custom Roles Admin permissions |
| Assignment levels | Organization, environment, or population |
| Permission set | Subset of built-in permissions; cannot exceed the creating admin's own permissions |

Custom roles are the right tool when a business unit needs admin access to its own population without visibility into others.

---

## Role scoping levels

A role assignment always combines: **role** + **assignee** (user or group) + **scope** (where permissions apply).

| Level | Covers | Typical use |
|---|---|---|
| Organization | All environments in the org | Org Admin overseeing the entire tenant |
| Environment | One or more named environments | Environment Admin scoped to Dev + Staging only |
| Population | One population within an environment | Identity Data Admin scoped to the "Customers-EMEA" population only |

Scoping to a population means the admin cannot see or manage users in other populations in the same environment.

---

## Administrators environment

PingOne automatically creates an **Administrators environment** when the organization is provisioned.

| Rule | Detail |
|---|---|
| Best practice | Create all administrator identities in the Administrators environment; do not co-locate admins with end users |
| Why | Prevents privilege escalation; simplifies access audit |
| Cross-environment admin access | A user in the Administrators environment can be granted Environment Admin or Identity Data Admin for any other environment — the identity stays in the Administrators environment |
| Getting Started Guide toggle | Settings > Environment Properties > Getting Started Guides — show or hide the admin wizard on the Environments page |

Older organizations may have co-located admin and end-user identities. If restructuring, plan a user migration before splitting environments.

---

## Adding administrators — three methods

### Method 1: Assign roles to an individual user

**Admin surface:** Directory > Users > (user) > Roles tab > Grant Roles

| Step | What to configure |
|---|---|
| Select or create the user | Directory > Users |
| Grant the role | Roles tab → role name + scope (environment or population) |
| Share the Console Login URL | Settings > Environment Properties → Console Login URL |
| Trigger email verification | User profile → Verify action sends the verification email |

**Email verification is required** before an administrator can access the console.

### Method 2: Grant roles to a group

Groups allow role assignment to scale across many users at once.

**Admin surface:** Directory > Groups > (group) > Roles tab > Grant Roles

| Step | What to configure |
|---|---|
| Create or select a group | Directory > Groups |
| Add users to the group | Add/Remove Users on the group record |
| Assign the role | Roles tab → role name + scope (environment or population) |

All current and future members of the group inherit the role automatically.

**Prerequisite:** Performing admin must have Identity Data Admin role (or equivalent) to create or edit groups.

### Method 3: Invite an administrator to register

Use when the target user does not yet have a PingOne account.

**Admin surface:** Directory > Users > Invite Admin

| Field | Value guidance |
|---|---|
| Name + email | Required; invitation is sent to this address |
| Population | Scopes the invitation to a specific population |
| Invitation expiry | Maximum 24 hours from time of issue |
| Role assignment | Set during the invite flow; takes effect on registration completion |

After the invitation is sent, it appears in the Users list with an active/revoke toggle. The invitee receives an email with a registration link, pastes the invite code, sets a password, and verifies email.

**Prerequisites:** PingOne must be the identity provider; administrator security must be enabled with PingOne or a hybrid authentication source.

---

## Console Login URL

Each environment has a unique **Console Login URL** distinct from the main `console.pingone.com` entry point. Provide this URL to new administrators alongside their username so they access the correct environment directly.

**Location:** Settings > Environment Properties > URLs

---

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Admin cannot access console after role assignment | Login succeeds but no environments or settings visible | Verify email on the user's Profile tab; confirm role scope includes the target environment |
| Invitation code rejected | "Invalid code" error during registration | Invitation may have expired (max 24h); resend the invitation; old code is invalidated |
| Cannot assign a role you don't hold | Role assignment blocked or role not visible in dropdown | Contact an Org Admin to escalate; you cannot delegate above your own grant level |
| Group role not inherited by new member | New group member lacks expected admin access | Check the group's Roles tab; re-save the assignment if it shows correctly but isn't propagating |
| Admin and end users co-located | Hard to audit; privilege escalation risk | Move admin identities to the Administrators environment |
| Custom role missing in another environment | Expected custom role not available | Custom roles are environment-scoped; recreate in each environment |
| Admin invited but PingOne not configured as IdP | Invite flow blocked | Confirm PingOne is the identity provider and administrator security is enabled in environment settings |

---

## Prerequisites

- PingOne organization with Organization Admin or Environment Admin role
- For invitations: PingOne configured as the identity provider; administrator security enabled
- For group-based role assignment: Identity Data Admin role in the target environment

---

## Common variants

| Variant | Pattern |
|---|---|
| Org-wide operations team | Assign Organization Admin; scope covers entire org |
| Per-environment team lead | Environment Admin scoped to Dev + Staging; no Production access |
| Per-population HR data steward | Identity Data Admin scoped to the HR population; cannot see other populations |
| Automated admin via Worker app | Create a Worker application; assign it Organization Admin or Environment Admin; use client credentials tokens for API-driven configuration |

---

## Related references

- `references/curated/pingone-mt/tenant-and-environment-setup.md` — environment creation and initial configuration
- `references/curated/pingone-mt/directory-and-populations.md` — population, group, and user management
- `references/curated/pingone-mt/app-registration.md` — application management and developer role

---

## Source

- https://docs.pingidentity.com/pingone/administrators/p1_admin_roles.html
- https://docs.pingidentity.com/pingone/administrators/p1_managing_administrators.html
- https://docs.pingidentity.com/pingone/administrators/p1_adding_administrators.html
- https://docs.pingidentity.com/pingone/administrators/p1_invite_admin.html
- https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_getting_started.html
