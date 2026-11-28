{
    "name": "VisionTech CRM Extension",
    "version": "19.0.1.0.0",
    "summary": "VisionTech customer and opportunity enhancements",
    "category": "Sales/CRM",
    "author": "VisionTech Solutions",
    "license": "LGPL-3",

    "depends": [
        "contacts",
        "crm",
    ],

    "data": [
        "views/res_partner_views.xml",
        "views/crm_lead_views.xml",
    ],

    "installable": True,
    "application": False,
    "auto_install": False,
}