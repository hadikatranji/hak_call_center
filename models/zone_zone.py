# -*- coding: utf-8 -*-
from odoo import api, fields, models

CALL_CENTER_ROLE_ID = 8
CHAMPION_ROLE_ID = 9


class ZoneZone(models.Model):
    _inherit = 'zone.zone'

    call_center_id = fields.Many2one(
        'res.users',
        string='Call Center Agent',
        domain=[('role_id', '=', CALL_CENTER_ROLE_ID), ('share', '=', False)],
        help='Call center agent responsible for this zone. '
             'Auto-fills on contacts when their zone is set.',
    )

    champion_id = fields.Many2one(
        'res.users',
        string='Champion (Salesperson)',
        domain=[('role_id', '=', CHAMPION_ROLE_ID), ('share', '=', False)],
        help='Champion (salesperson) responsible for this zone. '
             'Auto-fills on contacts when their zone is set.',
    )

    def write(self, vals):
        res = super().write(vals)
        for zone in self:
            partners = None
            if 'call_center_id' in vals or 'champion_id' in vals:
                partners = self.env['res.partner'].sudo().search([
                    ('zone_id', '=', zone.id),
                ])
            if partners:
                update = {}
                if 'call_center_id' in vals:
                    update['hak_call_center_id'] = vals['call_center_id']
                if 'champion_id' in vals:
                    update['user_id'] = vals['champion_id']
                if update:
                    partners.write(update)
        return res
