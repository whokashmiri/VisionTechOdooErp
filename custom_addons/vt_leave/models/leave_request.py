
from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError


class LeaveRequest(models.Model):
    _name = "vt.leave.request"
    _description = "VisionTech Leave Request"
    _order = "create_date desc"
    _rec_name = "name"

    name = fields.Char(
        string="Request Title",
        required=True,
        default="Leave Request",
    )

    employee_id = fields.Many2one(
        "vt.employee",
        string="Employee",
        required=True,
        ondelete="restrict",
        index=True,
        readonly=True,
    )

    requester_id = fields.Many2one(
        "res.users",
        string="Requested By",
        required=True,
        readonly=True,
        copy=False,
        index=True,
        ondelete="restrict",
    )

    leave_type = fields.Selection(
        [
            ("annual", "Annual Leave"),
            ("sick", "Sick Leave"),
            ("emergency", "Emergency Leave"),
            ("unpaid", "Unpaid Leave"),
        ],
        required=True,
        default="annual",
    )

    start_date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )

    end_date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )

    duration = fields.Integer(
        string="Duration (Days)",
        compute="_compute_duration",
        store=True,
    )

    reason = fields.Text(required=True)

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        required=True,
        default="draft",
        readonly=True,
        copy=False,
        index=True,
    )

    @api.model
    def _get_current_employee(self):
        return self.env["vt.employee"].sudo().search(
            [
                ("user_id", "=", self.env.uid),
                ("active", "=", True),
                ("status", "=", "active"),
            ],
            limit=1,
        )

    @api.model_create_multi
    def create(self, vals_list):
        employee = self._get_current_employee()

        if not employee:
            raise ValidationError(
                "Your user must be linked to an active employee."
            )

        for vals in vals_list:
            vals.update({
                "employee_id": employee.id,
                "requester_id": self.env.uid,
                "state": "draft",
            })

        return super().create(vals_list)

    def write(self, vals):
        editable = {
            "name",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
        }

        self.check_access("write")

        if set(vals) - editable:
            raise AccessError(
                "Protected workflow fields cannot be edited directly."
            )

        for request in self:
            if request.state != "draft":
                raise ValidationError(
                    "Only draft requests can be edited."
                )

            if request.requester_id.id != self.env.uid:
                raise AccessError(
                    "Only the requester can edit a draft."
                )

        return super().write(vals)

    def unlink(self):
        self.check_access("unlink")

        for request in self:
            if (
                request.state != "draft"
                or request.requester_id.id != self.env.uid
            ):
                raise AccessError(
                    "Only your own draft requests can be deleted."
                )

        return super().unlink()

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for request in self:
            request.duration = 0

            if (
                request.start_date
                and request.end_date
                and request.end_date >= request.start_date
            ):
                request.duration = (
                    request.end_date - request.start_date
                ).days + 1

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for request in self:
            if request.end_date < request.start_date:
                raise ValidationError(
                    "End date cannot be before start date."
                )

    @api.onchange("start_date")
    def _onchange_start_date(self):
        if self.start_date and (
            not self.end_date
            or self.end_date < self.start_date
        ):
            self.end_date = self.start_date
