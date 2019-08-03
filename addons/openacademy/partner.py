from odoo import models, fields, api

class Partner(models.Model):

    _inherit = 'res.partner'

    instructor = fields.Boolean(string="Instructor")
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)

