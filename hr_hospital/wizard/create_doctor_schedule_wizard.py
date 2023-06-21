from odoo import fields, models, _


class CreateDoctorScheduleWizard(models.TransientModel):
    _name = 'create.doctor.schedule.wizard'
    _description = 'Create doctor\'s schedule wizard'

    doctor_id = fields.Many2one('hospital.doctor')

    def action_open_wizard(self):
        return {
            'name': _('Create doctor\'s schedule wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'create.doctor.schedule.wizard',
            'target': 'new',
        }
