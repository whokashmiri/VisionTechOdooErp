from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vt_customer_segment = fields.Selection(
        selection=[
            ("individual", "Individual"),
            ("sme", "Small and Medium Enterprise"),
            ("enterprise", "Enterprise"),
            ("government", "Government"),
        ],
        string="Customer Segment",
        tracking=True,
        index=True,
        help="VisionTech business classification.",
    )