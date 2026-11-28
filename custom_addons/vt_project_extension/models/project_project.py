
from odoo import api, fields, models
from odoo.exceptions import AccessError


class ProjectProject(models.Model):
    _inherit = "project.project"

    vt_budget_used_pct = fields.Float(
        string="Budget Used (%)",
        compute="_compute_vt_budget",
        groups="project.group_project_manager",
        digits=(16, 2),
    )

    vt_budget_status = fields.Selection(
        [
            ("not_set", "Not Allocated"),
            ("normal", "Within Budget"),
            ("warning", "Approaching Limit"),
            ("exceeded", "Budget Exceeded"),
        ],
        string="Time Budget Status",
        compute="_compute_vt_budget",
        groups="project.group_project_manager",
    )

    @api.depends(
        "allocated_hours",
        "effective_hours",
        "allow_timesheets",
    )
    def _compute_vt_budget(self):
        for project in self:
            project.vt_budget_used_pct = 0.0
            project.vt_budget_status = "not_set"

            if (
                not project.allow_timesheets
                or project.allocated_hours <= 0
            ):
                continue

            percentage = (
                project.effective_hours
                / project.allocated_hours
            ) * 100

            project.vt_budget_used_pct = percentage

            if percentage > 100:
                project.vt_budget_status = "exceeded"
            elif percentage >= 80:
                project.vt_budget_status = "warning"
            else:
                project.vt_budget_status = "normal"


    def action_vt_view_timesheets(self):
        self.ensure_one()
        self.check_access("read")
        if not self.env.user.has_group(
            "project.group_project_manager"
        ):
        raise AccessError(
            "Only project managers can use this report action."
        )

        Timesheet = self.env["account.analytic.line"]
        Timesheet.check_access("read")

        return {
            "type": "ir.actions.act_window",
            "name": "Project Timesheets",
            "res_model": "account.analytic.line",
            "views": [
                (False, "list"),
                (False, "form"),
            ],
            "domain": [
                ("project_id", "=", self.id),
            ],
            "context": {
                "default_project_id": self.id,
            },
            "target": "current",
        }