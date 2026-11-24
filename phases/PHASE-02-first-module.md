# Phase 02 — First Custom Module — Employee and Department Models

## Objective
Create the first installable custom Odoo module and implement the initial backend data models.

## Business requirement
VisionTech Solutions needs a basic employee directory. Employees belong to departments. Each department can have a manager.

## Learn
- Python classes and inheritance in Odoo
- Addon/module structure
- `__manifest__.py` and `__init__.py`
- `models.Model`
- Field types: Char, Text, Boolean, Integer, Float, Date, Selection
- Required fields, defaults and help text
- Odoo ORM basics: `create`, `search`, `browse`, `write`, `unlink`
- Basic recordsets and `self.env`

## Build
1. Create `vt_employee`.
2. Add a valid module manifest and initialize Python packages.
3. Create a Department model.
4. Create an Employee model.
5. Add employee code, name, email, phone, joining date and status.
6. Add department and manager relationships.
7. Add basic validation and sensible defaults.
8. Install the module and verify that the models are registered.

## Suggested conceptual models
- `vt.department`
- `vt.employee`

Do not manually create SQL tables. Odoo ORM creates and manages the model tables.

## Acceptance criteria
- The module appears in the Apps list and installs without errors.
- Employee and Department models are registered.
- Fields have the correct types and required/default behavior.
- Relationships point to the correct models.
- You can create and update records through a temporary shell/test or later through views.

## Suggested video searches
- [Odoo 19 custom module from scratch](https://www.youtube.com/results?search_query=Odoo+19+create+custom+module+from+scratch)
- [Odoo ORM models and fields](https://www.youtube.com/results?search_query=Odoo+19+ORM+models+fields+tutorial)
- [Odoo Many2one One2many Many2many](https://www.youtube.com/results?search_query=Odoo+19+Many2one+One2many+Many2many+tutorial)

## Deliverable
An installable `vt_employee` module containing Employee and Department backend models.
