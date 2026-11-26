
from odoo import api, fields, models
from odoo.exceptions import  ( AccessError, ValidationError , UserError )


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




    submitted_by = fields.Many2one(
        "res.users",
        readonly=True,
        copy=False,
    )

    submitted_at = fields.Datetime(
        readonly=True,
        copy=False,
    )

    decision_by = fields.Many2one(
        "res.users",
        string="Decision By",
        readonly=True,
        copy=False,
    )   

    decision_at = fields.Datetime(
        string="Decision At",
        readonly=True,
        copy=False,
    )

    notification_queued = fields.Boolean(
        default=False,
        readonly=True,
        copy=False,
        groups=(
            "vt_employee.group_vt_hr_manager,"
            "base.group_system"
        ),
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


    def _is_hr_manager(self):
        return (
            self.env.user.has_group(
                "vt_employee.group_vt_hr_manager"
            )
            or self.env.user.has_group(
                "base.group_system"
            )
        )

    def _lock_request(self):
        self.ensure_one()
        self.check_access("write")

        self.env.cr.execute(
            """
            SELECT id
            FROM vt_leave_request
            WHERE id = %s
            FOR UPDATE
            """,
            (self.id,),
        )

        self.invalidate_recordset()

    def action_submit(self):
        self.ensure_one()
        self._lock_request()

        if self.requester_id.id != self.env.uid:
            raise AccessError(
                "Only the requester can submit this request."
            )

        if self.state != "draft":
            raise UserError(
                "Only draft requests can be submitted."
            )

        super(LeaveRequest, self).write({
            "state": "submitted",
        })

    def action_approve(self):
        self.ensure_one()
        self._lock_request()

        if not self._is_hr_manager():
            raise AccessError(
                "Only an HR Manager can approve leave."
            )

        if self.state != "submitted":
            raise UserError(
                "Only submitted requests can be approved."
            )

        super(LeaveRequest, self).write({
            "state": "approved",
            "decision_by": self.env.uid,
            "decision_at": fields.Datetime.now(),
        })

    def action_reject(self):
        self.ensure_one()
        self._lock_request()

        if not self._is_hr_manager():
            raise AccessError(
                "Only an HR Manager can reject leave."
            )

        if self.state != "submitted":
            raise UserError(
                "Only submitted requests can be rejected."
            )

        super(LeaveRequest, self).write({
            "state": "rejected",
            "decision_by": self.env.uid,
            "decision_at": fields.Datetime.now(),
        })


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

    
    @api.model
    def default_get(self , fields_list):
        defaults = super().default_get(fields_list)

        employee = self._get_current_employee()

        if "employee_id" in fields_list:
            defaults["employee_id"] = employee.id or False
        
        if "requester_id" in fields_list:
            defaults["requester_id"] = self.id or False
        if "state" in fields_list:
            defaults["state"] = "draft"
        
        return


    @api.model_create_multi
    def create(self, vals_list):
        employee = self._get_current_employee()

        if not employee:
            raise ValidationError(
                "Your user must be linked to an active employee."
            )

        allowed_fields = {"name" ,"leave_type" ,"start_date" ,"end_date" , "reason"}

        prepared = {}

        for vals in vals_list:

            values = {
                key:value
                for key, value in vals.items()
                if key in allowed_fields
            }
            values.update({
                "employee_id": employee.id,
                "requester_id": self.env.uid,
                "state": "draft",
            })

            prepared.append(values)

        clean_context = {
            key: value
            for key, value in self.env.context_items()
            if not key.startswith("default_")
        }

        return super(LeaveRequest , self.with_context).create(prepared)

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


    @api.model
    def _cron_queue_decision_notifications(self):
        template = self.env.ref(
            "vt_leave.mail_template_leave_decision"
        )

        domain = [
            ("state", "in", ["approved", "rejected"]),
            ("decision_at", "!=", False),
            ("notification_queued", "=", False),
            ("requester_id.partner_id.email", "!=", False),
        ]

        requests = self.search(domain, limit=50)

        for request in requests:
            request._lock_request()

            if request.notification_queued:
                continue

            template.send_mail(
                request.id,
                force_send=False,
            )

            super(LeaveRequest, request).write({
                "notification_queued": True,
            })

        self.env["ir.cron"]._commit_progress(
            len(requests),
            remaining=self.search_count(domain),
        )