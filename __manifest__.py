# -*- coding: utf-8 -*-
{
    'name': "salon_replica",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'base', 'base_setup', 'mail', 'website', 'contacts'],

    # always loaded
    'data': [
        'security/salon_management_groups.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/mail_template.xml',
        'data/salon_chair_data.xml',
        'data/salon_holiday_data.xml',
        'data/salon_order_data.xml',
        'data/salon_stages_data.xml',
        'data/salon_working_hours.xml',
        'views/views.xml',
        'views/chairs.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/booking_views.xml',
        'views/order_views.xml',
        'views/salon_menu.xml',
        'views/booking_templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'salon_replica/static/src/css/salon_dashboard.css',
            'salon_replica/static/src/xml/salon_dashboard.xml',
            'salon_replica/static/src/js/salon_dashboard.js',
            # 'salon_replica/static/src/js/salon_chair.js',
        ],
        'web.assets_frontend': [
            'salon_replica/static/src/css/salon_website.css',
            'salon_replica/static/src/js/website_salon_booking.js',
        ],
    },
}
