# -*- coding: utf-8 -*-
{
    'name': 'HR Attendance Custom',
    'summary': 'Custom attendance features for HR module',
    'description': """
HR Attendance Custom
====================
- Mở rộng chức năng chấm công
- Bổ sung logic / báo cáo theo nhu cầu doanh nghiệp
- Tùy biến quy trình check-in / check-out
    """,

    'author': 'My Company',
    'website': 'https://www.yourcompany.com',

    'category': 'Human Resources',
    'version': '1.0.0',

    # Phụ thuộc bắt buộc
    'depends': [
        'hr',
        'hr_attendance',
    ],

    # Dữ liệu load khi cài module
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_setting.xml'
    ],

    # Dữ liệu demo
    'demo': [],

    # Các config bổ sung
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
