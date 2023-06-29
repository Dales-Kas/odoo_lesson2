from odoo import fields, models, _


class CreateQuickVisitWizard(models.TransientModel):
    _name = 'create.quick.visit.wizard'
    _description = 'Quick create patient plan visit to the doctor'

    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        required=True
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        required=True
    )
    appointment_date = fields.Date(required=True)
    appointment_hour = fields.Integer()

    def action_open_wizard(self):
        return {
            'name': _('Quick create patient plan visit'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'create.quick.visit.wizard',
            'target': 'new',
        }

    def action_create_visit(self):
        self.ensure_one()
        visit = self.env['hospital.visit'].create({
            'doctor_id': self.doctor_id.id,
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'appointment_hour': self.appointment_hour,
            'is_plan': True
        })

        if not visit:
            return

        disease_name = f"{self.patient_id} / {self.appointment_date}"

        self.env['hospital.diagnosis'].create({
            'name': disease_name,
            'visit_id': visit.id,
            'doctor_id': self.doctor_id.id,
            'patient_id': self.patient_id.id,
        })
