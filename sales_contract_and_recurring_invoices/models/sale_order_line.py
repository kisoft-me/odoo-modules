from odoo import fields, models,api


class SaleOrderLine(models.Model):
    """ Add contract reference in sale order line """
    _inherit = 'sale.order.line'


    contract_id = fields.Many2one(
        'subscription.contracts',
        string='Contracts',
        help='For adding Contracts in sale order line')

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if line.contract_id:
                line.contract_id.write({
                    'sale_order_line_ids': [(4, line.id)]
                })
        return lines

    def write(self, vals):
        res = super().write(vals)
        for line in self:
            if line.contract_id:
                line.contract_id.write({
                    'sale_order_line_ids': [(4, line.id)]
                })
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contract_id = fields.Many2one(
        'subscription.contracts',
        string='Subscription Contract',
        ondelete='set null'
    )

    contract_count = fields.Integer(
        compute='_compute_contract_count'
    )

    def _compute_contract_count(self):
        for order in self:
            order.contract_count = self.env['subscription.contracts'].search_count([
                ('sale_order_line_ids.order_id', '=', order.id)
            ])

    def action_view_contract(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'subscription.contracts',
            'view_mode': 'form',
            'res_id': self.contract_id.id,
        }

