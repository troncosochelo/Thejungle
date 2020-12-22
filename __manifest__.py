# -*- coding: utf-8 -*-
{
    'name': "restaurante",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/grupos.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/mesero.xml',
        'views/cliente.xml',
        'views/pedido.xml',
        'views/cocinero.xml',
        'views/plato.xml',
        'views/detalle_plato.xml',
        'views/bebestible.xml',
        'views/detalle_bebestible.xml',
        'views/ingrediente.xml',
        'views/detalle_ingrediente.xml',
        'views/horas_extraordinarias.xml',
        'views/nomina_sueldo.xml',
        'views/horas_extraordinarias_meseros.xml',
        'views/nomina_sueldo_meseros.xml',
        'views/factura_bebestible.xml',
        'views/detalle_factura_bebestible.xml',
        'views/factura_ingrediente.xml',
        'views/detalle_factura_ingrediente.xml',

        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
