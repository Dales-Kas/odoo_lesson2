from odoo import models, fields


class HospitalDoctorHistory(models.Model):
    _name = 'hospital.doctor.history'
    _description = 'History of personal doctor of patients'

    name = fields.Char()
    date = fields.Datetime(default=fields.Datetime.now)
    patient_id = fields.Many2one(comodel_name='hospital.patient')
    doctor_id = fields.Many2one(comodel_name='hospital.doctor')
