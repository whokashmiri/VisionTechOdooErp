{
    "name": "VisionTech Attendance Management",
    "version": "19.0.1.0.0",
    "category": "Human Resources",
    "license": "LGPL-3",

    "depends": ["vt_employee"],

    "data": [
        "security/ir.model.access.csv",
        "security/attendance_rules.xml",
        "views/attendance_views.xml",
    ],

    "installable": True,
    "application": True,
}