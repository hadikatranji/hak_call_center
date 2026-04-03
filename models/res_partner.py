# -*- coding: utf-8 -*-
# =============================================================================
# hak_call_center - res_partner.py
# Author:  Hadi Katranji
# Created: 2026-03-24
#
# Extends res.partner to:
# 1. Add call_center_id field (CC agent per contact)
# 2. Auto-fill call_center_id from zone mapping when zone changes
#    (only if call_center_id is not already set)
# 3. Provide a backfill method to populate existing contacts
#
# Note: The salesperson domain filter (Champions only) is handled in
# the XML view via domain attribute, not in Python. This avoids
# breaking other modules that rely on user_id without domain.
# =============================================================================
from odoo import api, fields, models

# Role IDs from res_role table (OK Distribution)
# Verified via: SELECT id, name::text FROM res_role ORDER BY id;
CALL_CENTER_ROLE_ID = 8
CHAMPION_ROLE_ID = 9


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # ------------------------------------------------------------------
    # HAK: Call Center agent assigned to this contact
    # Domain filters to users with role_id = 8 (Call Center).
    # Auto-populated from zone.call_center_id on zone change.
    # ------------------------------------------------------------------
    hak_call_center_id = fields.Many2one(
        'res.users',
        string='Call Center Agent',
        domain=[('role_id', '=', CALL_CENTER_ROLE_ID), ('share', '=', False)],
        tracking=True,
        help='Call center agent responsible for this contact. '
             'Auto-filled from zone when zone is set (if empty).',
    )

    # ------------------------------------------------------------------
    # HAK: Auto-fill CC agent when zone changes
    # Always sets CC agent from zone — zone is the authoritative source.
    # ------------------------------------------------------------------
    @api.onchange('zone_id')
    def _onchange_zone_id_set_call_center(self):
        for partner in self:
            if partner.zone_id and partner.zone_id.call_center_id:
                partner.hak_call_center_id = partner.zone_id.call_center_id

    # ------------------------------------------------------------------
    # HAK: Backfill existing contacts
    # Run once after install to populate call_center_id on all contacts
    # that have a zone with a CC agent assigned.
    # Usage: Settings > Technical > Server Actions, or via shell:
    #   self.env['res.partner'].hak_backfill_call_center()
    # ------------------------------------------------------------------
    def hak_backfill_call_center(self):
        """One-time backfill: set call_center_id from zone for all contacts
        that have a zone assigned but no CC agent yet."""
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
