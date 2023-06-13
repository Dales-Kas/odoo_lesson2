from odoo import models, fields


class HospitalVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'patient visit'

    name = fields.Char()
    date = fields.Date(string="Visit day", default=fields.Date.today())
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    disease_ids = fields.Many2many('hospital.disease', string='Diseases')
    description = fields.Text()
