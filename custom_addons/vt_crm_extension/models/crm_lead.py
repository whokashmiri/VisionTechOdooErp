
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    vt_service_type = fields.Selection(
        selection=[
            ("software", "Software Development"),
            ("consulting", "IT Consulting"),
            ("support", "Technical Support"),
            ("asset_management", "Asset Management"),
        ],
        string="Service Type",
        tracking=True,
        index=True,
    )

    vt_requirements = fields.Text(
        string="Business Requirements",
    )

    vt_qualified = fields.Boolean(
        string="Requirements Verified",
        default=False,
        tracking=True,
        copy=False,
    )

    vt_customer_segment = fields.Selection(
        related="partner_id.vt_customer_segment",
        string="Customer Segment",
        readonly=True,
    )

    @api.constrains(
        "vt_qualified",
        "vt_service_type",
        "vt_requirements",
        "partner_id",
    )
    def _check_vt_qualification(self):
        for lead in self:
            if not lead.vt_qualified:
                continue

            if not lead.partner_id:
                raise ValidationError(
                    "Select a customer before verifying requirements."
                )

            if not lead.vt_service_type:
                raise ValidationError(
                    "Select a service type before verifying requirements."
                )

            if not (lead.vt_requirements or "").strip():
                raise ValidationError(
                    "Describe the business requirements first."
                )
