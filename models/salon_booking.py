import json

from odoo import api, fields, models, _


class SalonBooking(models.Model):
    _name = 'salon.booking'
    _description = 'Salon Booking'

    name = fields.Char(string="Name")
    state = fields.Selection(
        string="State", default="draft",
        selection=[('draft', 'Draft'), ('approved', 'Approved'),
                   ('rejected', 'Rejected')])
    time = fields.Datetime(string="Date")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="E-Mail")
    service_ids = fields.Many2many('salon.service', string="Services")
    chair_id = fields.Many2one('salon.chair', string="Chair")
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company'].browse(1))
    language_id = fields.Many2one(
        'res.lang', 'Language',
        default=lambda self: self.env['res.lang'].browse(1))
    filtered_order_ids = fields.Many2many('salon.order', string="Salon Orders",
                                          compute="_compute_filtered_order_ids")

    def _compute_filtered_order_ids(self):
        """
        compute filtered_order_ids
        """

        date_only = fields.Date.context_today(self)
        date_start = date_only
        date_end = date_only
        salon_orders = self.env['salon.order'].search(
            [('chair_id', '=', self.chair_id.id),
             ('start_time', '>=', date_start), ('start_time', '<=', date_end)])
        self.filtered_order_ids = [(6, 0, [x.id for x in salon_orders])]

    def action_approve_booking(self):
        """
        approve booking for salon services
        """
        order_data = {
            'customer_name': self.name,
            'chair_id': self.chair_id.id,
            'start_time': self.time,
            'date': fields.Datetime.now(),
            'stage_id': 1,
            'booking_identifier': True,
        }
        order = self.env['salon.order'].create(order_data)
        for records in self.service_ids:
            service_data = {
                'service_id': records.id,
                'time_taken': records.time_taken,
                'price': records.price,
                'price_subtotal': records.price,
                'salon_order_id': order.id,
            }
            self.env['salon.order.line'].create(service_data)
        template = self.env.ref(
            'salon_replica.mail_template_salon_approved')
        self.env['mail.template'].browse(template.id).send_mail(self.id,
                                                                force_send=True)
        self.state = "approved"

    def action_reject_booking(self):
        """
        reject booking for salon services
        """
        template = self.env.ref(
            'salon_replica.mail_template_salon_rejected')
        self.env['mail.template'].browse(template.id).send_mail(self.id,
                                                                force_send=True)
        self.state = "rejected"

    @api.model
    def get_booking_count(self):
        salon_bookings = self.env['salon.booking'].search_count(
            [('state', '=', 'approved')])
        recent_works = self.env['salon.order'].search_count(
            [('stage_id', 'in', [3, 4])])
        salon_orders = self.env['salon.order'].search_count([])
        salon_clients = self.env['res.partner'].search_count(
            [('partner_salon', '=', True)])

        salon_chairs = self.env['salon.chair'].search([])
        values = {
            'bookings': salon_bookings,
            'sales': recent_works,
            'orders': salon_orders,
            'clients': salon_clients,
            'chairs': salon_chairs
        }
        # print(values)
        return values
