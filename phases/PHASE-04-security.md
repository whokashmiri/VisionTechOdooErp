# Phase 04 — Security and Access Control

## Objective
Protect employee information and provide different capabilities to different users.

## Learn
- Odoo security groups
- `ir.model.access.csv`
- Access control lists (read, write, create, unlink)
- Record rules and domains
- Field-level groups
- The meaning and risks of `sudo()`
- Multi-company security concepts

## Build
1. Define appropriate HR user and HR manager groups.
2. Add access control entries for Employee and Department.
3. Define record rules for the intended visibility rules.
4. Restrict sensitive fields such as salary to authorized users.
5. Assign test users to different groups.
6. Test allowed and denied operations.

## Initial role expectations
- HR Manager: manage employee and department records.
- HR User: access permitted employee information.
- Regular Employee: only access information explicitly allowed by the policy.
- Administrator: full technical administration.

These rules are a learning baseline; real HR access policies must be reviewed carefully.

## Acceptance criteria
- Users without permission cannot perform restricted operations.
- Record rules limit visibility as intended.
- Sensitive salary data is not exposed to unauthorized users.
- Security is tested with separate user accounts, not only the administrator.

## Suggested video searches
- [Odoo 19 access rights and record rules](https://www.youtube.com/results?search_query=Odoo+19+access+rights+record+rules)
- [Odoo security groups and ir.model.access.csv](https://www.youtube.com/results?search_query=Odoo+security+groups+ir.model.access.csv+tutorial)

## Deliverable
A tested role-based security model for the employee module.
