from odoo import models, fields, api, _, exceptions


class HospitalDisease(models.Model):
    _name = 'hospital.disease'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'
    _description = 'disease of peoples'

    name = fields.Char(required=True)
    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True,
        store=True)
    description = fields.Text()
    parent_id = fields.Many2one(
        comodel_name='hospital.disease',
        string='Parent disease',
        index=True,
        ondelete='cascade')
    parent_path = fields.Char(
        index=True,
        unaccent=False)
    child_id = fields.One2many(
        comodel_name='hospital.disease',
        inverse_name='parent_id',
        string='Child diseases')
    disease_count = fields.Integer(
        string='# Diseases',
        compute='_compute_disease_count',
        help="The number of diseases under this \
        disease (Does not consider the children categories)")

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for obj in self:
            if obj.parent_id:
                obj.complete_name = '%s / %s' % (obj.parent_id.complete_name,
                                                 obj.name)
            else:
                obj.complete_name = obj.name

    def _compute_disease_count(self):
        for disease in self:
            disease.disease_count = self.env['hospital.diagnosis'].\
                search_count([('disease_id', 'child_of', disease.id)])

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise exceptions.ValidationError(_('You cannot create \
recursive diseases.'))
