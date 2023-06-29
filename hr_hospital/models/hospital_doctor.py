from odoo import models, fields, api, exceptions, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'doctor of the hospital'
    _inherit = "hospital.person"

    name = fields.Char(required=True)
    description = fields.Text()
    specialty = fields.Char()
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one(
        comodel_name='hospital.doctor'
    )
    intern_ids = fields.One2many(
        comodel_name='hospital.doctor',
        inverse_name='mentor_id',
    )
    patient_ids = fields.One2many(
        comodel_name='hospital.patient',
        inverse_name='personal_doctor_id',
    )

    @api.constrains('mentor_id')
    def _check_mentor(self):
        for doctor in self:
            if not doctor.is_intern:
                return
            #     raise exceptions.ValidationError(
            #         _('Mentor can be selected only for the intern!'))
            if doctor.mentor_id and self.id == doctor.mentor_id:
                raise exceptions.ValidationError(
                    _("It's impossible to choose an intern"
                      "as a mentor doctor!"""))
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise exceptions.ValidationError(
                    _("It's impossible to choose an intern"
                      "as a mentor doctor!"""))

    def write(self, vals):
        if 'is_intern' in vals and not vals.get('is_intern'):
            vals['mentor_id'] = False
        return super(HospitalDoctor, self).write(vals)

    def action_open_report_wizard(self):
        return {
            'name': _('Patient\'s diseases'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'disease.report.wizard',
            'target': 'current',
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
                'default_doctor_id': self.id,
                'default_appointment_date': fields.Date.today(),
                'default_appointment_hour': 9,
            },
        }
