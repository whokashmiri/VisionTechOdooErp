
from odoo import api, fields, models
from odoo.exceptions import AccessError


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
        groups=(
            "vt_employee.group_vt_hr_user,"
            "base.group_system"
        ),
    )

    employee_ids = fields.One2many(
        comodel_name="vt.employee",
        inverse_name="department_id",
        string="Employees",
        groups=(
            "vt_employee.group_vt_hr_user,"
            "base.group_system"
        ),
    )

    employee_count = fields.Integer(
        string="Employee Count",
        compute="_compute_employee_count",
        groups=(
            "vt_employee.group_vt_hr_user,"
            "base.group_system"
        ),
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
                department.employee_ids.with_context(
                    active_test=True
                ).filtered("active")
            )

    def action_view_employees(self):
        self.ensure_one()
        self.check_access("read")
        if not (
            self.env.user.has_group(
                "vt_employee.group_vt_hr_user"
            )
            or self.env.user.has_group(
                "base.group_system"
            )
        ):
            raise AccessError(
                "You are not allowed to view department employees"
            )

        return {
            "type": "ir.actions.act_window",
            "name": f"Employees - {self.name}",
            "res_model": "vt.employee",
            "view_mode": "list,form",
            "views":[
                (False, "list"),
                (False, "form"),
            ],
            "domain":[
                ("department_id", "=", self.id),

            ],
            "context": {
                **self.env.context,
                "default_department_id": self.id,
            },
            "target":"current",
        }
