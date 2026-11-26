
from odoo import api, fields, models
from odoo.exceptions import AccessError


class OnboardingWizard(models.TransientModel):
    _name = "vt.onboarding.wizard"
    _description = "Create Employee Onboarding Request"

    name = fields.Char(
        string="Employee Name",
        required=True,
    )

    department_id = fields.Many2one(
        "vt.department",
        required=True,
    )

    joining_date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )

    equipment_required = fields.Boolean(
        default=True,
    )

    equipment_notes = fields.Text()

    @api.onchange("equipment_required")
    def _onchange_equipment_required(self):
        if not self.equipment_required:
            self.equipment_notes = False

    def action_create_request(self):
        self.ensure_one()
        self.check_access("read")

        if not (
            self.env.user.has_group(
                "vt_employee.group_vt_hr_manager"
            )
            or self.env.user.has_group(
                "base.group_system"
            )
        ):
            raise AccessError(
                "Only HR Managers can create onboarding requests."
            )

        request = self.env[
            "vt.onboarding.request"
        ].create({
            "name": self.name,
            "department_id": self.department_id.id,
            "joining_date": self.joining_date,
            "equipment_required": self.equipment_required,
            "equipment_notes": self.equipment_notes,
        })

        return {
            "type": "ir.actions.act_window",
            "name": "Onboarding Request",
            "res_model": "vt.onboarding.request",
            "res_id": request.id,
            "views": [(False, "form")],
            "target": "current",
        }
