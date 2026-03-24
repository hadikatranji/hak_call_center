# -*- coding: utf-8 -*-
# =============================================================================
# Module:  hak_call_center
# Author:  Hadi Katranji
# Created: 2026-03-24
# Purpose: Call Center agent assignment per zone and per contact.
#          Filters salesperson field to Champions only (role_id=9).
#          Designed for future extension: Grandstream integration,
#          CC activity automation, performance tracking.
# =============================================================================
{
    'name': 'Call Center Management',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summary': 'Assign call center agents per zone, filter salesperson to Champions',
    'author': 'Hadi Katranji',
    'depends': ['contacts', 'sale', 'das_zone_location', 'das_roles_module'],
    'data': [
        'views/zone_zone_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
