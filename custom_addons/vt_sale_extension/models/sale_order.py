
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    vt_project_reference = fields.Char(
        string="Project Reference",
        copy=False,
        tracking=True,
        index=True,
        help="Customer-facing reference for the project.",
    )

    vt_service_type = fields.Selection(
        [
            ("software", "Software Development"),
            ("consulting", "IT Consulting"),
            ("support", "Technical Support"),
            ("asset_management", "Asset Management"),
        ],
        string="Service Type",
        tracking=True,
    )

    @api.onchange("opportunity_id")
    def _onchange_vt_opportunity(self):
        if self.opportunity_id:
            self.vt_service_type = (
                self.opportunity_id.vt_service_type
            )
