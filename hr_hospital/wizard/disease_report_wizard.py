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
