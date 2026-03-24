# -*- coding: utf-8 -*-
# =============================================================================
# hak_call_center - sale_order.py
# Author:  Hadi Katranji
# Created: 2026-03-24
#
# Adds a related Call Center Agent field on sale.order,
# pulled from the customer's (partner_id) hak_call_center_id.
# Read-only — set on the contact, displayed here for reference.
# =============================================================================
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ------------------------------------------------------------------
    # HAK: CC agent from the customer contact (read-only, for reference)
    # ------------------------------------------------------------------
    hak_call_center_id = fields.Many2one(
        'res.users',
        string='Call Center Agent',
        related='partner_id.hak_call_center_id',
        store=True,
        readonly=True,
    )
