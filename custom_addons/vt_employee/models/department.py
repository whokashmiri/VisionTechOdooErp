
from odoo import api, fields, models


class Department(models.Model):
    _name = "vt.department"
    _description = "VisionTech Department"
    _order = "name asc"
    _rec_name = "name"

    name = fields.Char(
        string="Department Name",
        required=True,
        help="The official name of the department.",
    )

    code = fields.Char(
        string="Department Code",
        required=True,
        copy=False,
    )

    description = fields.Text(
        string="Description",
    )

    manager_id = fields.Many2one(
        comodel_name="vt.employee",
        string="Department Manager",
        ondelete="set null",
    )

    employee_ids = fields.One2many(
        comodel_name="vt.employee",
        inverse_name="department_id",
        string="Employees",
    )

    employee_count = fields.Integer(
        string="Employee Count",
        compute="_compute_employee_count",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    _unique_code = models.Constraint(
        "UNIQUE(code)",
        "The department code must be unique.",
    )

    @api.depends("employee_ids", "employee_ids.active")
    def _compute_employee_count(self):
        for department in self:
            department.employee_count = len(
                department.employee_ids
            )
