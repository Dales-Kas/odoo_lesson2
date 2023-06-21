from odoo import fields, models, _


class SetPersonalDoctorMultiWizard(models.TransientModel):
    _name = 'set.personal.doctor.multi.wizard'
    _description = 'Wizard to set personal doctor to easy way'

    patient_ids = fields.Many2many("hospital.patient")
    doctor_id = fields.Many2one(
        'hospital.doctor',
        'New personal doctor')

    def action_open_wizard(self):
        return {
            'name': _('Set personal doctor Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'set.personal.doctor.multi.wizard',
            'target': 'new',
        }

    def action_set_doctor(self):
        self.ensure_one()
        for patient in self.patient_ids:
            patient.write({
                'personal_doctor_id': self.doctor_id.id
            })
