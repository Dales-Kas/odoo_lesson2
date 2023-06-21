from odoo import models, fields, api, exceptions, _


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
        comodel_name='hospital.diagnosis')
    description = fields.Text()
    is_finished = fields.Boolean()
    active = fields.Boolean(default=True)

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

    @api.constrains('date', 'doctor_id')
    @api.onchange('date', 'doctor_id')
    def _check_date_doctor(self):
        for visit in self:
            if visit.is_finished:
                raise exceptions.ValidationError(
                    _('Visit is finished!'))
    # def create(self, vals_list):
    #     visit = self.env['hospital.visit'].create({
    #         'date': fields.Date.today(),
    #     })
    #     visit.create_diagnosis()

    @api.model_create_multi
    def create(self, vals_list):
        # for values in vals_list:
        visit = super(HospitalVisit, self).create(vals_list)
        visit.create_diagnosis()
        return visit

    def create_diagnosis(self):
        diagnosis = self.env['hospital.diagnosis'].create({
            'visit_id': self.id,
            'date': self.date,
            'doctor_id': self.doctor_id.id,
            'patient_id': self.patient_id.id,
        })
        self.diagnosis_id = diagnosis.id
