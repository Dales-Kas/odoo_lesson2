from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor.category'
    _description = 'doctor\'s category'

    name = fields.Char(required=True)
