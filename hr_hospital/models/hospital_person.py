from odoo import models, fields


class HospitalPerson(models.AbstractModel):
    _name = 'hospital.person'
    _description = 'Abstract person main model'

    name = fields.Char(required=True)
    phone = fields.Char()
    email = fields.Char()
    photo = fields.Binary()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ])
