from odoo import models, fields


class HospitalAnalysis(models.Model):
    _name = 'hospital.analysis'
    _description = "patient's analysis"

    name = fields.Char()
    date = fields.Date(
        required=True,
        default=fields.date.today())
    doctor_id = fields.Many2one(
        'hospital.doctor',
        required=True)
    patient_id = fields.Many2one(
        'hospital.patient',
        required=True)
    type = fields.Char()
    comment = fields.Char()
