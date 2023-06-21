from odoo import models, fields


class HospitalContactPerson(models.Model):
    _name = 'hospital.contact.person'
    _description = 'Contact person of the patient'
    _inherit = "hospital.person"

    name = fields.Char(required=True)
    description = fields.Text()
