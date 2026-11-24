# Phase 07 — Extend Standard Odoo Applications

## Objective
Integrate the custom ERP with Odoo's existing business applications instead of duplicating standard features.

## Applications to explore
- Contacts and CRM
- Project and Timesheets
- Inventory
- Sales
- Purchase (optional, useful for procurement workflows)

## Learn
- How to inspect standard Odoo models
- `_inherit` and extension patterns
- View inheritance and XPath
- Module dependencies
- External identifiers (XML IDs)
- Domains and context
- Safe customization without editing Odoo core
- Upgrade and compatibility considerations

## Build
1. Install the relevant standard applications.
2. Map business requirements to existing Odoo features.
3. Extend CRM with company-specific fields or workflow logic.
4. Extend Project with relevant reporting or assignment behavior.
5. Extend Inventory with a low-stock alert or approval requirement.
6. Extend Sales with a company-specific field or document behavior.
7. Document which functionality is standard and which is custom.

## Acceptance criteria
- Standard applications continue to work.
- Customizations are isolated in custom addons.
- Dependencies are declared correctly.
- Existing views are extended safely.
- No unnecessary duplicate models or workflows are created.

## Suggested video searches
- [Odoo model inheritance](https://www.youtube.com/results?search_query=Odoo+19+model+inheritance+_inherit+tutorial)
- [Odoo view inheritance XPath](https://www.youtube.com/results?search_query=Odoo+19+view+inheritance+XPath)
- [Odoo CRM customization](https://www.youtube.com/results?search_query=Odoo+19+CRM+customization+developer)
- [Odoo Inventory customization](https://www.youtube.com/results?search_query=Odoo+19+inventory+customization+developer)

## Deliverable
A set of custom extensions integrated with standard Odoo CRM, Project, Inventory and Sales applications.
