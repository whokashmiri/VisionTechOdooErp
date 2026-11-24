
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _name = "vt.employee"
    _description = "VisionTech Employee"
    _order = "name asc"
    _rec_name = "name"

    employee_code = fields.Char(
        string="Employee Code",
        required=True,
        copy=False,
        help="Unique employee identification code.",
    )

    name = fields.Char(
        string="Full Name",
        required=True,
    )

    email = fields.Char(
        string="Email",
    )

    phone = fields.Char(
        string="Phone Number",
    )

    joining_date = fields.Date(
        string="Joining Date",
        required=True,
        default=fields.Date.context_today,
    )

    status = fields.Selection(
        selection=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("resigned", "Resigned"),
        ],
        string="Employment Status",
        required=True,
        default="active",
    )

    department_id = fields.Many2one(
        comodel_name="vt.department",
        string="Department",
        required=True,
        ondelete="restrict",
        index=True,
    )

    manager_id = fields.Many2one(
        comodel_name="vt.employee",
        string="Reporting Manager",
        ondelete="set null",
        index=True,
    )

    subordinate_ids = fields.One2many(
        comodel_name="vt.employee",
        inverse_name="manager_id",
        string="Subordinates",
    )

    active = fields.Boolean(
        string="Active Record",
        default=True,
    )

    _unique_employee_code = models.Constraint(
        "UNIQUE(employee_code)",
        "The employee code must be unique.",
    )

    @api.constrains("joining_date")
    def _check_joining_date(self):
        for employee in self:
            if (
                employee.joining_date
                and employee.joining_date
                > fields.Date.context_today(employee)
            ):
                raise ValidationError(
                    "Joining date cannot be in the future."
                )

    @api.constrains("manager_id")
    def _check_manager(self):
        for employee in self:
            current_manager = employee.manager_id
            visited_ids = {employee.id}

            while current_manager:
                if current_manager.id in visited_ids:
                    raise ValidationError(
                        "Circular reporting relationships "
                        "are not allowed."
                    )

                visited_ids.add(current_manager.id)
                current_manager = current_manager.manager_id
