
from odoo import api, fields, models
from odoo.exceptions import (
    AccessError,
    ValidationError,
)


class OnboardingRequest(models.Model):
    _name = "vt.onboarding.request"
    _description = "VisionTech Onboarding Request"
    _order = "create_date desc"

    name = fields.Char(
        string="New Employee Name",
        required=True,
    )

    department_id = fields.Many2one(
        "vt.department",
        required=True,
        ondelete="restrict",
    )

    joining_date = fields.Date(
        required=True,
    )

    equipment_required = fields.Boolean(
        default=True,
    )

    equipment_notes = fields.Text()

    requested_by = fields.Many2one(
        "res.users",
        readonly=True,
        required=True,
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["requested_by"] = self.env.uid

        return super().create(vals_list)

    def write(self, vals):
        if "requested_by" in vals:
            raise AccessError(
                "The requester cannot be changed."
            )

        return super().write(vals)

    @api.constrains(
        "equipment_required",
        "equipment_notes",
    )
    def _check_equipment_notes(self):
        for request in self:
            if (
                request.equipment_required
                and not (
                    request.equipment_notes or ""
                ).strip()
            ):
                raise ValidationError(
                    "Describe the required equipment."
                )
