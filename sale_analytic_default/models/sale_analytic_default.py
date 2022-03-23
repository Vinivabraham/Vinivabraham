from odoo import models, api, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        default_analytic_account = self.env['account.analytic.default'].search(
            [('partner_id', '=', self.partner_id.id)], limit=1)
        if default_analytic_account:
            for rec in self:
                rec.analytic_account_id = default_analytic_account.analytic_id
        res = super(SaleOrder, self).action_confirm()
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        for line in self:
            default_analytic_account = self.env['account.analytic.default'].search([('product_id', '=', line.product_id.id), ('partner_id', '=', self.order_id.partner_id.id)])
            if default_analytic_account:
                line.analytic_tag_ids = default_analytic_account.analytic_tag_ids
        res = super(SaleOrderLine, self).product_id_change()
        return res