{
    "name": "VisionTech Employee Onboarding",
    "version": "19.0.1.0.0",
    "category": "Human Resources",
    "license": "LGPL-3",

    "depends": ["vt_employee"],

    "data": [
        "security/ir.model.access.csv",
        "views/onboarding_views.xml",
        "views/onboarding_wizard_views.xml",
    ],

    "installable": True,
    "application": True,
}