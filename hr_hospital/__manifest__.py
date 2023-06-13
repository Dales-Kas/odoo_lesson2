{
    'name': "hr_hospital",
    'summary': "odoo lesson 2. My first module",
    'author': "dales",
    'website': "https://www.yourcompany.com",
    'category': 'Extra Tools',
    'version': '16.0.1.0.0',
    'license': "OPL-1",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_menus.xml',
        'data/hospital_disease_data.xml',
        'views/hospital_doctor_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_disease_views.xml',
        'views/hospital_visit_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'data/hospital_doctor_demo.xml',
        'data/hospital_patient_demo.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False
}