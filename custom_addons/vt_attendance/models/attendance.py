
from odoo import api, fields, models
from odoo.exceptions import (
    AccessError,
    UserError,
    ValidationError,
)


class Attendance(models.Model):
    _name = "vt.attendance"
    _description = "VisionTech Attendance"
    _order = "check_in desc"
    _rec_name = "employee_id"

    employee_id = fields.Many2one(
        "vt.employee",
        required=True,
        ondelete="restrict",
        readonly=True,
        index=True,
    )

    owner_id = fields.Many2one(
        "res.users",
        required=True,
        readonly=True,
        index=True,
        ondelete="restrict",
    )

    check_in = fields.Datetime(
        required=True,
        default=fields.Datetime.now,
        readonly=True,
    )

    check_out = fields.Datetime(
        readonly=True,
    )

    worked_hours = fields.Float(
        compute="_compute_worked_hours",
        store=True,
    )

    state = fields.Selection(
        [
            ("open", "Checked In"),
            ("closed", "Checked Out"),
        ],
        compute="_compute_state",
        store=True,
    )

    open_slot = fields.Integer(
        default=1,
        copy=False,
        readonly=True,
    )

    _unique_open = models.Constraint(
        "UNIQUE(employee_id, open_slot)",
        "This employee already has an open attendance.",
    )

    _valid_checkout = models.Constraint(
        "CHECK(check_out IS NULL OR check_out >= check_in)",
        "Check-out cannot be before check-in.",
    )

    @api.model
    def _current_employee(self):
        return self.env["vt.employee"].sudo().search(
            [
                ("user_id", "=", self.env.uid),
                ("active", "=", True),
                ("status", "=", "active"),
            ],
            limit=1,
        )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)

        if "employee_id" in fields_list:
            values["employee_id"] = (
                self._current_employee().id or False
            )

        if "owner_id" in fields_list:
            values["owner_id"] = self.env.uid

        if "check_out" in fields_list:
            values["check_out"] = False

        if "check_in" in fields_list:
            values["check_in"] = fields.Datetime.now()

        return values

    @api.model_create_multi
    def create(self, vals_list):
        employee = self._current_employee()

        if not employee:
            raise ValidationError(
                "Your account must be linked "
                "to an active employee."
            )

        context = {
            key: value
            for key, value in self.env.context.items()
            if not key.startswith("default_")
        }

        prepared = [
            {
                "employee_id": employee.id,
                "owner_id": self.env.uid,
                "check_in": fields.Datetime.now(),
                "check_out": False,
                "open_slot": 1,
            }
            for vals in vals_list
        ]

        return super(
            Attendance,
            self.with_context(context),
        ).create(prepared)

    def write(self, vals):
        raise AccessError(
            "Attendance records cannot be edited directly. "
            "Use the attendance actions."
        )

    @api.depends("check_in", "check_out")
    def _compute_worked_hours(self):
        for attendance in self:
            attendance.worked_hours = 0.0

            if (
                attendance.check_in
                and attendance.check_out
                and attendance.check_out >= attendance.check_in
            ):
                delta = (
                    attendance.check_out
                    - attendance.check_in
                )

                attendance.worked_hours = (
                    delta.total_seconds() / 3600
                )

    @api.depends("check_out")
    def _compute_state(self):
        for attendance in self:
            attendance.state = (
                "closed"
                if attendance.check_out
                else "open"
            )

    @api.constrains("check_in", "check_out")
    def _check_attendance_dates(self):
        for attendance in self:
            if (
                attendance.check_out
                and attendance.check_out < attendance.check_in
            ):
                raise ValidationError(
                    "Check-out cannot be before check-in."
                )

    def action_check_out(self):
        self.ensure_one()
        self.check_access("write")

        is_manager = (
            self.env.user.has_group(
                "vt_employee.group_vt_hr_manager"
            )
            or self.env.user.has_group(
                "base.group_system"
            )
        )

        if (
            self.owner_id.id != self.env.uid
            and not is_manager
        ):
            raise AccessError(
                "You cannot check out another employee."
            )

        self.env.cr.execute(
            """
            SELECT id
            FROM vt_attendance
            WHERE id = %s
            FOR UPDATE
            """,
            (self.id,),
        )

        self.invalidate_recordset()

        if self.check_out:
            raise UserError(
                "This attendance is already closed."
            )

        super(Attendance, self).write({
            "check_out": fields.Datetime.now(),
            "open_slot": self.id + 1,
        })
