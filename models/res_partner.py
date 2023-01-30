from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    partner_salon = fields.Boolean(string="Is a Salon Partner",default=True)