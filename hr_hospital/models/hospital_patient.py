from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'patient'

    name = fields.Char(string="Patient name", required=True)
    description = fields.Text()
