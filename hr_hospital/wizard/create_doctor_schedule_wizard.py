from datetime import timedelta

from odoo import fields, models, api, exceptions, _


class CreateDoctorScheduleWizard(models.TransientModel):
    _name = 'create.doctor.schedule.wizard'
    _description = 'Create doctor\'s schedule wizard'

    doctor_id = fields.Many2one('hospital.doctor')
    week_type = fields.Selection([
        ('even', 'even week'),
        ('odd', 'odd week')
    ],
        default='even')
    start_hour = fields.Integer()
    end_hour = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()

    @api.constrains('start_hour', 'end_hour')
    def _check_hours(self):
        for obj in self:
            if obj.start_hour > obj.end_hour:
                raise exceptions.ValidationError(_('End hour mast be greater '
                                                   'than start hour'))

    def action_open_wizard(self):
        return {
            'name': _('Create doctor\'s schedule wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'create.doctor.schedule.wizard',
            'target': 'new',
        }

    def action_create_schedule(self):
        self.ensure_one()

        # delete old records for that period:
        schedule_records = self.env['hospital.doctor.schedule'].search([
            ('doctor_id', '=', self.doctor_id.id),
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date)
        ])
        schedule_records.unlink()

        # Create new records:
        doctor_schedule_vals = []
        current_date = self.start_date
        days_increment = timedelta(days=1)
        while current_date <= self.end_date:
            is_even_week = current_date.isocalendar().week % 2 == 0
            if (is_even_week and self.week_type == 'even') \
                    or (is_even_week and self.week_type == 'odd'):
                hour = self.start_hour
                while hour <= self.end_hour:
                    doctor_schedule_vals.append({
                        'doctor_id': self.doctor_id.id,
                        'date': current_date,
                        'hour': hour
                    })
                    hour += 1
            current_date += days_increment
        self.env['hospital.doctor.schedule'].create(doctor_schedule_vals)
