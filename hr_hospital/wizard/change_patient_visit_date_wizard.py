from odoo import fields, models, exceptions, _


class ChangePatientVisitDateWizard(models.TransientModel):
    _name = 'change.patient.visit.date.wizard'
    _description = 'Change patient plan visit day'

    patient_id = fields.Many2one(comodel_name="hospital.patient")
    appointment_date = fields.Date(required=True)
    appointment_new_date = fields.Date(required=True)
    appointment_new_hour = fields.Integer(string='New appointment hour')
    doctor_id = fields.Many2one(comodel_name='hospital.doctor', required=True)

    def action_open_wizard(self):
        return {
            'name': _('Change patient plan visit day'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'change.patient.visit.date.wizard',
            'target': 'new',
        }

    def action_change_visit_date(self):
        self.ensure_one()
        visit = self.env['hospital.visit'].search([(
            'appointment_date', '=', self.appointment_date),
            ('is_plan', '=', True)])
        if not visit:
            raise exceptions.ValidationError(_('No planed visit for that '
                                               'day!'))
        visit[0].write({'appointment_date': self.appointment_new_date,
                        'appointment_hour': self.appointment_new_hour,
                        'doctor_id': self.doctor_id,
                        })
