
{
    "name": "VisionTech HR Reports",
    "version": "19.0.1.0.0",
    "summary": "Employee and HR PDF reports",
    "category": "Human Resources",
    "author": "VisionTech Solutions",
    "license": "LGPL-3",

    "depends": [
        "vt_employee",
        "vt_leave",
        "web",
    ],

    "data": [
        "reports/paperformat.xml",
        "reports/report_styles.xml",
        "reports/employee_report.xml",
        "reports/department_report.xml",
        "reports/leave_report.xml",
        "reports/report_actions.xml",
        "views/employee_report_views.xml",
    ],

    "installable": True,
    "application": False,
    "auto_install": False,
}
