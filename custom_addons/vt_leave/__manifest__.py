{
    "name": "VisionTech Leave Management",
    "version": "19.0.1.0.0",
    "summary": "Employee leave requests and approvals",
    "category": "Human Resources",
    "author": "VisionTech Solutions",
    "license": "LGPL-3",

    "depends": [
        "vt_employee",
        "mail",
    ],

    "data": [
        "security/ir.model.access.csv",
        "security/leave_rules.xml",
        "views/leave_views.xml",
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}