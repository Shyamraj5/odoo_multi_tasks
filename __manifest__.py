{
    'name': 'AIO',
    'version': '17.0.1.0',
    # 'summary': 'Automatically generate delivery orders and invoices on sale order confirmation',
    'author': 'shyamraj',
    'website': 'https://github.com/Shyamraj5',
    'category': 'Sales',
    'depends': ['sale','stock','base'],
    'data': [
             "views/sale_order.xml",
             "views/res_config.xml",
             "views/menu.xml"
             ],
    'installable': True,
    'auto_install': False,
}
