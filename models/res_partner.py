# -*- coding: utf-8 -*-
from odoo import api, fields, models

CALL_CENTER_ROLE_ID = 8
CHAMPION_ROLE_ID = 9


class ResPartner(models.Model):
    _inherit = 'res.partner'

    hak_call_center_id = fields.Many2one(
        'res.users',
        string='Call Center Agent',
        domain=[('role_id', '=', CALL_CENTER_ROLE_ID), ('share', '=', False)],
        tracking=True,
        help='Call center agent responsible for this contact. '
             'Auto-filled from zone when zone is set.',
    )

    @api.onchange('zone_id')
    def _onchange_zone_id_set_team(self):
        """Auto-fill both CC agent and champion from zone."""
        for partner in self:
            if partner.zone_id:
                if partner.zone_id.call_center_id:
                    partner.hak_call_center_id = partner.zone_id.call_center_id
                if partner.zone_id.champion_id:
                    partner.user_id = partner.zone_id.champion_id

    @api.model_create_multi
    def create(self, vals_list):
        """On create, set salesperson from zone — not from creator."""
        for vals in vals_list:
            zone_id = vals.get('zone_id')
            if zone_id:
                zone = self.env['zone.zone'].browse(zone_id)
                if zone.champion_id:
                    vals['user_id'] = zone.champion_id.id
                if zone.call_center_id and 'hak_call_center_id' not in vals:
                    vals['hak_call_center_id'] = zone.call_center_id.id
            else:
                # No zone — don't auto-assign creator as salesperson
                if 'user_id' not in vals or vals.get('user_id') == self.env.uid:
                    vals.pop('user_id', None)
        return super().create(vals_list)

    def hak_backfill_call_center(self):
        """One-time backfill: set call_center_id from zone for all contacts."""
        partners = self.sudo().search([
            ('zone_id', '!=', False),
            ('zone_id.call_center_id', '!=', False),
            ('hak_call_center_id', '=', False),
        ])
        count = 0
        for partner in partners:
            partner.hak_call_center_id = partner.zone_id.call_center_id
            count += 1
        return count

    def hak_backfill_champion(self):
        """One-time backfill: set user_id (salesperson) from zone for all contacts."""
        partners = self.sudo().search([
            ('zone_id', '!=', False),
            ('zone_id.champion_id', '!=', False),
        ])
        count = 0
        for partner in partners:
            if partner.user_id != partner.zone_id.champion_id:
                partner.user_id = partner.zone_id.champion_id
                count += 1
        return count
