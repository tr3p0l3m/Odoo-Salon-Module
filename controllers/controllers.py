# -*- coding: utf-8 -*-
# from odoo import http


# class SalonReplica(http.Controller):
#     @http.route('/salon_replica/salon_replica', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salon_replica/salon_replica/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('salon_replica.listing', {
#             'root': '/salon_replica/salon_replica',
#             'objects': http.request.env['salon_replica.salon_replica'].search([]),
#         })

#     @http.route('/salon_replica/salon_replica/objects/<model("salon_replica.salon_replica"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salon_replica.object', {
#             'object': obj
#         })

import json
import pytz
from datetime import datetime, time

from odoo import fields, http
from odoo.http import request


class SalonBookingWeb(http.Controller):

    @http.route('/page/salon_details', csrf=False, type="http",
                methods=['POST', 'GET'], auth="public", website=True)
    def salon_details(self, **kwargs):
        name = kwargs['name']
        date = kwargs['date']
        time = kwargs['time']
        phone = kwargs['phone']
        email = kwargs['email']
        chair = kwargs['chair']
        j = 0
        service_list = []
        while j < (int(kwargs['number'])):
            item = "list_service[" + str(j) + "][i]"
            service_list.append(int(kwargs[item]))
            j += 1
        salon_service_obj = request.env['salon.service'].search([
            ('id', 'in', service_list)])
        dates_time = date + " " + time + ":00"
        date_and_time = dates_time
        salon_booking = request.env['salon.booking']
        booking_data = {
            'name': name,
            'phone': phone,
            'time': date_and_time,
            'email': email,
            'chair_id': chair,
            'service_ids': [(6, 0, [x.id for x in salon_service_obj])],
        }
        salon_booking.create(booking_data)
        return json.dumps({'result': True})

    @http.route('/page/salon_check_date', type='json', auth="public",
                website=True)
    def salon_check(self, **kwargs):
        day = int(kwargs.get('check_date')[3:5])
        month = int(kwargs.get('check_date')[0:2])
        year = int(kwargs.get('check_date')[6:10])
        date_start = datetime(year, month, day, 0, 0, 0)
        date_end = datetime(year, month, day, 23, 59, 59)
        order_obj = request.env['salon.order'].search(
            [('chair_id.active_booking_chairs', '=', True),
             ('stage_id', 'in', [1, 2, 3]), ('start_time', '>=', date_start),
             ('start_time', '<=', date_end)])
        order_details = {}
        for order in order_obj:
            data = {
                'number': order.id,
                'start_time_only': fields.Datetime.to_string(order.start_time)[11:16],
                'end_time_only': fields.Datetime.to_string(order.end_time)[11:16],
            }
            if order.chair_id.id not in order_details:
                order_details[order.chair_id.id] = {
                    'name': order.chair_id.name,
                    'orders': [data],
                }
            else:
                order_details[order.chair_id.id]['orders'].append(data)
        return order_details

    @http.route('/page/salon_replica/salon_booking_thank_you', type='http',
                auth="public", website=True)
    def thank_you(self, **post):
        return request.render('salon_replica.salon_booking_thank_you', {})

    @http.route('/page/salon_replica/salon_booking_form', type='http',
                auth="public", website=True)
    def chair_info(self, **post):
        salon_service_obj = request.env['salon.service'].search([])
        salon_working_hours_obj = request.env['salon.working.hours'].search([])
        salon_holiday_obj = request.env['salon.holiday'].search(
            [('holiday', '=', True)])
        date_check = datetime.today().date()
        date_start = date_check
        date_end = date_check
        chair_obj = request.env['salon.chair'].search(
            [('active_booking_chairs', '=', True)])
        order_obj = request.env['salon.order'].search(
            [('chair_id.active_booking_chairs', '=', True),
             ('stage_id', 'in', [1, 2, 3]), ('start_time', '>=', date_start),
             ('start_time', '<=', date_end)])
        return request.render(
            'salon_replica.salon_booking_form', {
                'chair_details': chair_obj,
                'order_details': order_obj,
                'salon_services': salon_service_obj,
                'date_search': date_check,
                'holiday': salon_holiday_obj,
                'working_time': salon_working_hours_obj,
            })


class SalonOrders(http.Controller):
    @http.route(['/salon/chairs'], type="json", auth="public")
    def elearning_snippet(self, products_per_slide=3):
        print('controller')
        chairs = []
        salon_chairs = request.env['salon.chair'].sudo().search([])
        number_of_orders = {}

        for i in salon_chairs:
            number_of_orders.update({i.id: len(request.env['salon.order'].search(
                [("chair_id", "=", i.id),
                 ("stage_id", "in", [2, 3])]))})
            # print(i.id)
            chairs.append(
                {'name': i.name, 'id': i.id, 'orders': number_of_orders[i.id]})
        print(number_of_orders, 'main')
        values = {
            's_chairs': chairs
        }
        print(values)

        response = http.Response(
            template='salon_replica.dashboard_salon_chairs', qcontext=values)
        print(response.render())
        return response.render()