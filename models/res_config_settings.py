from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def booking_chairs(self):
        """
        return active chairs for booking
        """
        return self.env['salon.chair'].search(
            [('active_booking_chairs', '=', True)])

    @api.model
    def holidays(self):
        """
        return holiday
        """
        return self.env['salon.holiday'].search([('holiday', '=', True)])

    salon_booking_chair_ids = fields.Many2many(
        'salon.chair', string="Booking Chairs", default=booking_chairs)
    salon_holiday_ids = fields.Many2many('salon.holiday', string="Holidays",
                                         default=holidays)

    def execute(self):
        """
        update boolean fields of holiday and chair
        """
        salon_chair_obj = self.env['salon.chair'].search([])
        book_chair = []
        for chairs in self.salon_booking_chair_ids:
            book_chair.append(chairs.id)
        for records in salon_chair_obj:
            if records.id in book_chair:
                records.active_booking_chairs = True
            else:
                records.active_booking_chairs = False
        salon_holiday_obj = self.env['salon.holiday'].search([])
        holiday = []
        for days in self.salon_holiday_ids:
            holiday.append(days.id)
        for records in salon_holiday_obj:
            if records.id in holiday:
                records.holiday = True
            else:
                records.holiday = False


class SalonWorkingHours(models.Model):
    _name = 'salon.working.hours'
    _description = 'Salon Working Hours'

    name = fields.Char(string="Name")
    from_time = fields.Float(string="Starting Time")
    to_time = fields.Float(string="Closing Time")


class SalonHoliday(models.Model):
    _name = 'salon.holiday'
    _description = 'Salon Holiday'

    name = fields.Char(string="Name")
    holiday = fields.Boolean(string="Holiday")