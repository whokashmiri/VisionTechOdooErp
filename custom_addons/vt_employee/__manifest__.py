
{
    "name": "VisionTech Employee Management",
    "version": "19.0.3.0.0",
    "summary": "Manage employees and departments",
    "description": """
        Employee and department management
        for VisionTech Solutions.
    """,
    "author": "VisionTech Solutions",
    "category": "Human Resources",
    "license": "LGPL-3",

    "depends": [
        "base",
        "web",
    ],

    "data": [
        "security/employee_groups.xml",
        "security/ir.model.access.csv",
        "views/employee_views.xml",
        "views/department_views.xml",
        "views/employee_view_inherit.xml",
        "views/employee_menus.xml",
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}
