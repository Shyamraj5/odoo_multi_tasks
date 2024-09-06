{
    'name': 'AIO',
    'version': '17.0.1.0',
    # 'summary': 'Automatically generate delivery orders and invoices on sale order confirmation',
    'author': 'shyamraj',
    'website': 'https://github.com/Shyamraj5',
    'category': 'Sales',
    'depends': ['sale','stock','base'],
    'data': [
             "security/ir.model.access.csv",
             "views/sale_order.xml",
             "views/res_config.xml",
             'wizard/sale_report_wizard.xml',
             "wizard/sale_order_confirm_wizard.xml",
             "views/menu.xml"
             ],
    'installable': True,
    'auto_install': False,
}
