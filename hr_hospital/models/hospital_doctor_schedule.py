from datetime import timedelta

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
    start_date = fields.Datetime(
        compute='_compute_date'
    )
    end_date = fields.Datetime(
        compute='_compute_appointment_date'
    )

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

    def _compute_date(self):
        for schedule in self:
            if schedule.date:
                schedule.start_date = \
                    fields.Datetime.to_datetime(schedule.date) + \
                    timedelta(hours=float(schedule.hour))
            else:
                schedule.start_date = schedule.date
            schedule.end_date = \
                schedule.start_date + timedelta(hours=float(1))
