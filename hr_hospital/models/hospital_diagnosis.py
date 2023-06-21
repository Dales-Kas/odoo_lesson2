from odoo import models, fields, api, exceptions, _


class HospitalDiagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = "doctor's diagnosis of patient"

    name = fields.Char()
    date = fields.Date(
        required=True,
        default=fields.date.today())
    doctor_id = fields.Many2one(
        'hospital.doctor',
        required=True)
    patient_id = fields.Many2one(
        'hospital.patient',
        required=True)
    disease_id = fields.Many2one('hospital.disease')
    appointment = fields.Text()
    doctor_comment = fields.Text(string="Mentor doctor's comment")
    visit_id = fields.Many2one(
        'hospital.visit',
        readonly=True)

    @api.constrains('doctor_comment')
    def _check_doctor_comment(self):
        for disease in self:
            if disease.doctor_id \
                    and disease.doctor_id.is_intern \
                    and disease.doctor_comment == "":
                raise exceptions.UserError(
                    _("Please, write doctor's conclusion"))
