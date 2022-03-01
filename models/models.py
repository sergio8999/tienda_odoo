from odoo import models, fields, api
from dateutil.relativedelta import *
from datetime import date


class cliente(models.Model):
    _name = 'tienda.cliente'
    _description = 'model cliente'

    name = fields.Char('DNI',required=True)
    nombre = fields.Char(string='Nombre',required=True)
    apellido = fields.Char(string='Apellido',required=True)
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento',required=True)
    anios = fields.Integer("Años", compute="_get_anios")
    mayorEdad = fields.Char("Mayor de edad", compute="_get_mayor_edad")

    ordenador_ids = fields.One2many('tienda.ordenador', 'cliente_id', string='Ordenadores')
    factura_ids = fields.One2many('tienda.factura', 'cliente_id', string='Facturas')

    @api.depends('fecha_nacimiento')
    def _get_anios(self):
        for pers in self:
            hoy = date.today()
            pers.anios = relativedelta(hoy, pers.fecha_nacimiento).years

    @api.depends('anios')
    def _get_mayor_edad(self):
        for pers in self:
            if (pers.anios >= 18):
                pers.mayorEdad = "Si"
            else:
                pers.mayorEdad = "No"

class factura(models.Model):
    _name = 'tienda.factura'
    _description = 'model factura'

    name = fields.Char('cod',required=True)
    mes = fields.Char(string='Nombre mes',required=True)
    precioBase = fields.Float(string='Precio base', required=True, digits=(6, 2))
    iva = fields.Integer("IVA", required=True)
    total = fields.Float(string='Total', compute="_get_total")

    cliente_id = fields.Many2one('tienda.cliente', string='Cliente')

    @api.depends('precioBase',"iva")
    def _get_total(self):
        for precio in self:
            precio.total = precio.precioBase * ((100 + precio.iva)/100)


class ordenador(models.Model):
    _name = 'tienda.ordenador'
    _description = 'model cliente'

    name = fields.Char('Cod', required=True)
    descripcion = fields.Char(string='Nombre', required=True)
    precioFabrica = fields.Float(string='Precio fabrica', required=True, digits=(6, 2))
    precioVenta = fields.Float(string='Precio venta', digits=(6, 2), compute="_getVenta")
    beneficio = fields.Float(string='Beneficio', digits=(6, 2), compute= "_getBeneficio")

    pieza_ids = fields.One2many('tienda.pieza', 'ordenador_id', string='Piezas')
    cliente_id = fields.Many2one('tienda.cliente', string='Cliente')


    @api.depends('precioFabrica')
    def _getVenta(self):
        for precio in self:
            precio.precioVenta = precio.precioFabrica * 1.20

    @api.depends('precioVenta','precioFabrica')
    def _getBeneficio(self):
        for precio in self:
            precio.beneficio = precio.precioVenta - precio.precioFabrica

class pieza(models.Model):
    _name = 'tienda.pieza'
    _description = 'model cliente'

    name = fields.Char('Cod',required=True)
    nombre = fields.Char(string='Nombre',required=True)
    precio= fields.Float(string='Precio', required=True, digits=(6, 2))
    cantidad = fields.Integer(string='Cantidad', required=True)
    total = fields.Integer("Total", compute="_get_total")

    ordenador_id = fields.Many2one('tienda.ordenador', string='Ordenador')

    @api.depends('precio','cantidad')
    def _get_total(self):
        for pieza in self:
            pieza.total = pieza.precio * pieza.cantidad