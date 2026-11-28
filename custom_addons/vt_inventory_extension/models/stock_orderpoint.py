
from odoo import api, fields, models
from odoo.tools import float_compare


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    vt_stock_status = fields.Selection(
        [
            ("unknown", "Not Configured"),
            ("normal", "Stock Sufficient"),
            ("low", "Low Stock"),
            ("negative", "Negative Forecast"),
        ],
        string="Stock Alert",
        compute="_compute_vt_stock_alert",
        groups="stock.group_stock_user",
    )

    vt_shortage_qty = fields.Float(
        string="Minimum Stock Shortage",
        compute="_compute_vt_stock_alert",
        digits="Product Unit",
        groups="stock.group_stock_user",
    )

    @api.depends(
        "qty_forecast",
        "product_min_qty",
        "product_id",
        "location_id",
        "product_uom.rounding",
    )
    def _compute_vt_stock_alert(self):
        for rule in self:
            rule.vt_stock_status = "unknown"
            rule.vt_shortage_qty = 0.0

            if (
                not rule.product_id
                or not rule.location_id
                or not rule.product_uom
            ):
                continue

            forecast = rule.qty_forecast
            minimum = rule.product_min_qty
            rounding = rule.product_uom.rounding

            comparison = float_compare(
                forecast,
                minimum,
                precision_rounding=rounding,
            )

            if float_compare(
                forecast,
                0.0,
                precision_rounding=rounding,
            ) < 0:
                rule.vt_stock_status = "negative"

            elif comparison < 0:
                rule.vt_stock_status = "low"

            else:
                rule.vt_stock_status = "normal"

            if comparison < 0:
                rule.vt_shortage_qty = max(
                    minimum - forecast,
                    0.0,
                )
