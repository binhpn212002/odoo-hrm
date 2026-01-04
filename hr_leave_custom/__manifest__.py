# -*- coding: utf-8 -*-
{
    'name': "hr_leave_custom",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_holidays'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_leave_type_views.xml',
        'views/res_config_setting.xml',
        'views/public_holidays_cron.xml',
        'views/hr_holiday_vn_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

