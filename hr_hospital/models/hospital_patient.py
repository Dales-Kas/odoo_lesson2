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
        comodel_name='hospital.contact.person')
    personal_doctor_id = fields.Many2one(
        comodel_name='hospital.doctor')
    doctor_history_ids = fields.One2many(
        comodel_name='hospital.doctor.history',
        inverse_name='patient_id')
    disease_history_ids = fields.One2many(
        comodel_name='hospital.diagnosis',
        inverse_name='patient_id')
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')],
        default='low')

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for patient in self:
            if patient.birth_date:
                delta = today - patient.birth_date
                patient.age = delta.days // 365
            else:
                patient.age = 0

    def write(self, vals):
        res = super(HospitalPatient, self).write(vals)
        if 'personal_doctor_id' in vals:
            for patient in self:
                if self.personal_doctor_id:
                    self.env['hospital.doctor.history'].create({
                        'patient_id': patient.id,
                        'doctor_id': patient.personal_doctor_id.id,
                        'date': fields.Datetime.now(),
                    })
        return res

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

    def action_open_visit(self):
        self.ensure_one()
        return {
            'name': _('Patient visits'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.visit',
            'target': 'current',
            'domain': [('patient_id', '=', self.id)],
        }

    def action_open_analysis(self):
        self.ensure_one()
        return {
            'name': _('Patient analyses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.analysis',
            'target': 'current',
            'domain': [('patient_id', '=', self.id)],
        }

    def action_open_diagnosis(self):
        self.ensure_one()
        return {
            'name': _('Patient diagnoses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.diagnosis',
            'target': 'current',
            'domain': [('patient_id', '=', self.id)],
        }

    def action_create_visit(self):
        self.ensure_one()
        return {
            'name': _('Quick visit create'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'create.quick.visit.wizard',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.personal_doctor_id.id,
                'default_appointment_date': fields.Date.today(),
                'default_appointment_hour': 9,
            },
        }
