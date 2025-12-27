# -*- coding: utf-8 -*-
{
  'name': "Hrm  Core",

  'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

  'description': """
        Long description of module's purpose
    """,

  'author': "My Company",
  'website': "https://www.yourcompany.com",
  'sequence': -1,
  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
  # for the full list
  'category': 'Uncategorized',
  'version': '0.1',

  # any module necessary for this one to work correctly
  'depends': ['base', "mail", 'web'],

  # always loaded
  'data': [
    'security/real_estate_core_security.xml',
    'security/ir.model.access.csv',
    # 'security/security.xml',
    'data/res_company_demo.xml',
    'data/res_users_demo.xml',
    'data/res_partner_data.xml',
    'data/real_estate_team_demo.xml',
    'views/real_estate_team.xml',
    'views/real_estate_user.xml',
    'views/real_estate_core_menu.xml',
    'views/real_estate_company.xml',
    'views/real_estate_setting.xml',
    'views/templates.xml',
  ],
  'assets': {
    'web.assets_backend': [
      'hrm_core/static/src/**/*.js',
      'hrm_core/static/src/**/*.xml',
      'hrm_core/static/src/**/*.scss',
    ]
  },
  # only loaded in demonstration mode
  'demo': [
    'demo/demo.xml',
    # 'data/res_company_demo.xml',
    # 'data/res_users_demo.xml',
    # 'data/res_partner_data.xml',
    # 'data/real_estate_team_demo.xml',
  ],
  'auto_install': True,
}
