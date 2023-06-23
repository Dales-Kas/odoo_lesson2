from odoo import fields, models, _


class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Patient\'s diseases report'

    disease_id = fields.Many2one('hospital.disease')
    qty = fields.Integer()

    def action_open_wizard(self):
        return {
            'name': _('Patient\'s diseases'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'disease.report.wizard',
            'target': 'current',
        }

    def create_report(self):
        report_data = []
        all_disease = self.env['hospital.disease'].search()
        for disease in all_disease:
            qty = self.env['hospital.diagnosis'].search_count([
                ('disease_id', 'child_of', disease.id)
            ])
            report_data.append({
                'disease_id': disease.id,
                'qty': qty,
            })
            disease.disease_count = self.env['hospital.diagnosis'].\
                search_count([('disease_id', 'child_of', disease.id)])
