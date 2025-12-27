# -*- coding: utf-8 -*-
{
  'name': "hrm_theme",
  'summary': "Short (1 phrase/line) summary of the module's purpose",
  'description': """
Long description of module's purpose
    """,
  'author': "My Company",
  'website': "https://www.yourcompany.com",
  'category': 'Uncategorized',
  'version': '0.1',
  'depends': ['base', 'web', 'mail'],
  'data': [
    'security/ir.model.access.csv',
    'views/templates.xml',
    'views/reset_password.xml',
    'views/login_layout.xml',
    'views/login.xml',
    'views/signup.xml',
    'views/hrm_theme.xml',
    'views/res_user.xml',
    'demo/hrm_theme.xml'
  ],
  # only loaded in demonstration mode
  'demo': [
  ],
  'assets': {
    'web.assets_backend': [
      'hrm_theme/static/src/form/*.scss',
      'hrm_theme/static/src/views/list/*.js',
      'hrm_theme/static/src/views/list/*.xml',
      'hrm_theme/static/src/views/list/*.scss',
      'hrm_theme/static/src/views/list/**/*.xml',
      'hrm_theme/static/src/views/list/**/*.js',
      'hrm_theme/static/src/views/list/**/*.scss',
      'hrm_theme/static/src/search/*.js',
      'hrm_theme/static/src/search/*.xml',
      'hrm_theme/static/src/search/*.scss',
      'hrm_theme/static/src/search/**/*.xml',
      'hrm_theme/static/src/search/**/*.js',
      'hrm_theme/static/src/search/**/*.scss',
      'hrm_theme/static/src/constant/constant.js',
      'hrm_theme/static/src/**/*.js',
      'hrm_theme/static/src/**/*.xml',
      'hrm_theme/static/src/**/*.scss',
      'hrm_theme/static/src/pages/**/*.js',
      'hrm_theme/static/src/pages/**/*.xml',
      'hrm_theme/static/src/pages/**/*.scss'
    ],
  },
}
