from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalDoctorSchedule(models.Model):
    _name = 'hospital.doctor.schedule'
    _description = 'Doctor Schedule'

    doctor_id = fields.Many2one(
        'hospital.doctor',
        required=True)
    date = fields.Date(required=True)
    hour = fields.Integer()

    @api.constrains('doctor_id', 'date', 'time')
    def _check_unique_schedule(self):
        for record in self:
            if record.hour > 23 or record.hour < 0:
                raise ValidationError(_('time must be between 0-23!'))
            existing_schedule = self.search([
                ('doctor_id', '=', record.doctor_id.id),
                ('date', '=', record.date),
                ('hour', '=', record.hour),
                ('id', '!=', record.id)
            ])
            if existing_schedule:
                raise ValidationError(
                    _('Schedule already exists'
                      'for this doctor at the given hour.'))
