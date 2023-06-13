from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'doctor'

    name = fields.Char(string='Doctor name', required=True)
    description = fields.Text()
    is_active = fields.Boolean(string='Active', default=True)
