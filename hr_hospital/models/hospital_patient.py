from odoo import models, fields, api, _


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'patient of the hospital'
    _inherit = "hospital.person"

    name = fields.Char(required=True)
    description = fields.Text()
    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age')
    passport = fields.Char()
    contact_person_id = fields.Many2one(
        'hospital.contact.person')
    personal_doctor_id = fields.Many2one(
        'hospital.doctor')

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for patient in self:
            if patient.birth_date:
                delta = today - patient.birth_date
                patient.age = delta.days // 365
            else:
                patient.age = 0

    @api.constrains('personal_doctor_id')
    def create_personal_doctor_history(self):
        if self.personal_doctor_id:
            self.env['hospital.doctor.history'].create({
                'patient_id': self.id,
                'doctor_id': self.personal_doctor_id.id,
                'date': fields.Datetime.now(),
            })

    def action_open_wizard(self):
        return {
            'name': _('Set personal doctor Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'set.personal.doctor.multi.wizard',
            'target': 'new',
            'context': {
                'default_patient_ids': self.ids,
            },
        }