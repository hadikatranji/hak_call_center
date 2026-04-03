# -*- coding: utf-8 -*-
# =============================================================================
# hak_call_center - zone_zone.py
# Author:  Hadi Katranji
# Created: 2026-03-24
#
# Extends zone.zone to add a Call Center agent field.
# Each zone gets one CC agent (Many2one). When a contact's zone changes,
# the CC agent auto-fills from this field (see res_partner.py).
#
# Future: upgrade to Many2many if multiple CC agents per zone are needed.
# =============================================================================
from odoo import api, fields, models

# Role ID for Call Center in res_role table
# Verified via: SELECT id, name FROM res_role WHERE id = 8;
CALL_CENTER_ROLE_ID = 8


class ZoneZone(models.Model):
    _inherit = 'zone.zone'

    # ------------------------------------------------------------------
    # HAK: Call Center agent assigned to this zone
    # Domain filters to users with role_id = 8 (Call Center) and
    # share = False (internal users only, not portal).
    # ------------------------------------------------------------------
    call_center_id = fields.Many2one(
        'res.users',
        string='Call Center Agent',
        domain=[('role_id', '=', CALL_CENTER_ROLE_ID), ('share', '=', False)],
        help='Call center agent responsible for this zone. '
             'Auto-fills on contacts when their zone is set.',
    )

    def write(self, vals):
        res = super().write(vals)
        if 'call_center_id' in vals:
            new_agent_id = vals['call_center_id']
            for zone in self:
                partners = self.env['res.partner'].sudo().search([
                    ('zone_id', '=', zone.id),
                    ('customer_rank', '>', 0),
                ])
                if partners:
                    partners.write({'hak_call_center_id': new_agent_id})
        return res
