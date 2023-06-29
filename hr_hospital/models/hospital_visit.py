from datetime import timedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError


class HospitalVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'patient visit to the doctor'

    name = fields.Char()
    date = fields.Datetime(default=fields.Date.today)
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor')
    patient_id = fields.Many2one(
        comodel_name='hospital.patient')
    diagnosis_id = fields.Many2one(
        comodel_name='hospital.diagnosis',
        domain=[('visit_id', '=', id)]
    )
    description = fields.Text()
    is_finished = fields.Boolean()
    active = fields.Boolean(default=True)
    is_plan = fields.Boolean(string="Is Planned Appointment")
    appointment_date = fields.Date()
    appointment_hour = fields.Integer()
    appointment_start_date = fields.Datetime(
        compute='_compute_appointment_date'
    )
    appointment_end_date = fields.Datetime(
        compute='_compute_appointment_date'
    )

    def unlink(self):
        for visit in self:
            if visit.diagnosis_id:
                raise exceptions.ValidationError(_(
                    'You cannot delete a visit with a diagnosis.'))
        return super(HospitalVisit, self).unlink()

    def write(self, vals):
        if 'active' in vals and self.diagnosis_id:
            raise exceptions.ValidationError(_(
                'You cannot deactivate a visit with a diagnosis.'))
        return super(HospitalVisit, self).write(vals)

    def _compute_appointment_date(self):
        for visit in self:
            if visit.appointment_date:
                visit.appointment_start_date = \
                    fields.Datetime.to_datetime(visit.appointment_date) + \
                    timedelta(hours=float(visit.appointment_hour))
            else:
                visit.appointment_start_date = visit.date
            visit.appointment_end_date = \
                visit.appointment_start_date + timedelta(hours=float(1))

    @api.constrains('date', 'doctor_id')
    def _check_date_doctor(self):
        for visit in self:
            if visit.is_finished:
                raise ValidationError(_('Visit is finished!'))

    def create_diagnosis(self):
        diagnosis = self.env['hospital.diagnosis'].create({
            'visit_id': self.id,
            'date': self.date,
            'doctor_id': self.doctor_id.id,
            'patient_id': self.patient_id.id,
        })
        self.diagnosis_id = diagnosis.id

    @api.constrains('is_plan', 'appointment_date',
                    'appointment_hour', 'doctor_id')
    def _check_unique_plan_date(self):
        for visit in self:
            # check planned hour:
            if visit.is_plan and \
                    (visit.appointment_hour > 23
                     or visit.appointment_hour < 0):
                raise ValidationError(_('time must be between 0-23!'))
            # check planned date:
            if visit.is_plan and not visit.appointment_date:
                raise ValidationError(_('planed date must be filled!'))
            # check for duplicate planed visit:
            if visit.is_plan and visit.appointment_date and visit.doctor_id:
                count = self.search_count([
                    ('id', '!=', visit.id),
                    ('appointment_date', '=', visit.appointment_date),
                    ('doctor_id', '=', visit.doctor_id.id),
                    ('appointment_hour', '=', visit.appointment_hour),
                    ('is_plan', '=', True),
                ])
                if count > 0:
                    raise ValidationError(
                        _("The doctor has another appointment for that date!"))
            # check doctor's schedule:
            if visit.is_plan:
                count = self.env['hospital.doctor.schedule'].search_count([
                    ('date', '=', visit.appointment_date),
                    ('doctor_id', '=', visit.doctor_id.id),
                    ('hour', '=', visit.appointment_hour),
                ])
                if count == 0:
                    raise ValidationError(
                        _("the doctor is not working at that time!"))
