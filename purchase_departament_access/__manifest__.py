{
    "name": "Purchase Department Access",
    "version": "17.0.1.0.0",
    "category": "Purchases",
    "summary": "Restrict purchase order visibility by department",
    "depends": ["purchase", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "security/purchase_department_rules.xml",
    ],
    "installable": True,
    "application": False,
}
