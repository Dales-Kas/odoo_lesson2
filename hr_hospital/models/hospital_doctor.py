from odoo import models, fields, api, exceptions, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'doctor of the hospital'
    _inherit = "hospital.person"

    name = fields.Char(required=True)
    description = fields.Text()
    specialty = fields.Char()
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one(comodel_name='hospital.doctor')

    @api.constrains('mentor_id')
    def _check_mentor(self):
        for doctor in self:
            if not doctor.is_intern:
                raise exceptions.ValidationError(
                    _('Mentor can be selected only for the intern!'))
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise exceptions.ValidationError(
                    _("""It's impossible to choose an intern
as a mentor doctor!"""))

    @api.onchange('is_intern')
    @api.constrains('is_intern')
    def _onchange_is_intern(self):
        for doctor in self:
            if not doctor.is_intern:
                doctor.mentor_id = ''

    def action_open_report_wizard(self):
        return {
            'name': _('Patient\'s diseases'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'disease.report.wizard',
            'target': 'current',
        }
