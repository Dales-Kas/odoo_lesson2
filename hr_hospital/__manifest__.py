{
    'name': "hr_hospital",
    'summary': "odoo lesson 2. My first module",
    'author': "dales",
    'website': "https://github.com/Dales-Kas",
    'category': 'Extra Tools',
    'version': '16.0.5.0.1',
    'license': "OPL-1",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_menus.xml',
        'data/hospital_disease_data.xml',
        'data/hospital_doctor_category_data.xml',
        'views/hospital_doctor_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_disease_views.xml',
        'views/hospital_analysis_views.xml',
        'views/hospital_diagnosis_views.xml',
        'views/hospital_visit_views.xml',
        'views/hospital_doctor_schedule_views.xml',
        'views/hospital_doctor_history_views.xml',
        'wizard/set_personal_doctor_multi_wizard_views.xml',
        'wizard/disease_report_wizard_views.xml',
        'wizard/create_doctor_schedule_wizard_views.xml',
        'wizard/change_patient_visit_date_wizard_views.xml',
        'wizard/create_quick_visit_wizard_views.xml',
        "report/doctor_reports_templates.xml",
        "report/doctor_report.xml",
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
