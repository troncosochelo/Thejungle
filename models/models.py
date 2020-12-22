# -*- coding: utf-8 -*-
import time
import datetime

from odoo import models, fields, api
from datetime import datetime
from datetime import date
from datetime import datetime, date, time
from odoo.exceptions import ValidationError

class Plato(models.Model):
    _name = 'restaurante.plato'
    _rec_name ='nombre'

    nombre = fields.Char()
    precio = fields.Integer()

    detalle_plato_ids = fields.One2many('restaurante.detalle_plato', 'plato_id')
    detalle_ingrediente_ids = fields.One2many('restaurante.detalle_ingrediente', 'plato_id')



class Detalle_Plato(models.Model):
    _name = 'restaurante.detalle_plato'
    _rec_name = 'id'

    cantidad = fields.Integer()
    precio = fields.Integer(compute="_precio_platos") 
    hora = fields.Float(string='Time')
    estado = fields.Selection([ ('pendiente', 'Pendiente'),('entregado', 'Entregado')], default='pendiente')



    cocinero_id = fields.Many2one('restaurante.cocinero')
    pedido_id = fields.Many2one('restaurante.pedido')
    plato_id = fields.Many2one('restaurante.plato')

    @api.one
    @api.depends('plato_id', 'cantidad')
    def _precio_platos(self):
        for plato in self.plato_id:
            self.precio = plato.precio * self.cantidad

class Ingrediente(models.Model):
    _name = 'restaurante.ingrediente'
    _rec_name = 'nombre'

    nombre = fields.Char()
    costo = fields.Float()
    egreso = fields.Integer(compute="_egreso")
    ingreso = fields.Integer(compute="_ingreso")
    cantidad = fields.Integer(compute="_cal_cantidad")

    detalle_ingrediente_ids = fields.One2many('restaurante.detalle_ingrediente', 'ingrediente_id')
    detalle_factura_ingrediente_ids = fields.One2many('restaurante.detalle_factura_ingrediente', 'ingrediente_id')

    @api.one
    @api.depends('detalle_ingrediente_ids')
    def _egreso(self):
        for detalle_ingrediente in self.detalle_ingrediente_ids:
            self.egreso += detalle_ingrediente.cantidad

    @api.one
    @api.depends('detalle_factura_ingrediente_ids')
    def _ingreso(self):
        for detalle_factura_ingrediente in self.detalle_factura_ingrediente_ids:
            self.ingreso += detalle_factura_ingrediente.cantidad

    @api.one
    @api.depends('egreso', 'ingreso')
    def _cal_cantidad(self):
        self.cantidad = self.ingreso - self.egreso


class Detalle_Ingrediente(models.Model):
    _name = 'restaurante.detalle_ingrediente'


    cantidad = fields.Float()
    costo = fields.Float(compute="_costo_plato")
    stock = fields.Integer(compute="_stock")

    ingrediente_id = fields.Many2one('restaurante.ingrediente')
    plato_id = fields.Many2one('restaurante.plato')   

    @api.one
    @api.depends('ingrediente_id', 'cantidad')
    def _costo_plato(self):
        for ingrediente in self.ingrediente_id:
            self.costo = ingrediente.costo * self.cantidad

    @api.one
    @api.depends('ingrediente_id')
    def _stock(self):
        for ingrediente in self.ingrediente_id:
            self.stock = ingrediente.cantidad

    @api.constrains('cantidad')
    def _validar_stock(self):
        if self.stock < 0:
            raise ValidationError('No hay suficiente stock')

class Bebestible(models.Model):
    _name = 'restaurante.bebestible'
    _rec_name ='nombre'

    nombre = fields.Char()
    egreso = fields.Integer(compute="_egreso")
    ingreso = fields.Integer(compute="_ingreso")
    cantidad = fields.Integer(compute="_cal_cantidad")

    costo = fields.Float()
    precio = fields.Integer()

    detalle_bebestible_ids = fields.One2many('restaurante.detalle_bebestible', 'bebestible_id')
    detalle_factura_bebestible_ids = fields.One2many('restaurante.detalle_factura_bebestible', 'bebestible_id')

    @api.one
    @api.depends('detalle_bebestible_ids')
    def _egreso(self):
        for detalle_bebestible in self.detalle_bebestible_ids:
            self.egreso += detalle_bebestible.cantidad

    @api.one
    @api.depends('detalle_factura_bebestible_ids')
    def _ingreso(self):
        for detalle_factura_bebestible in self.detalle_factura_bebestible_ids:
            self.ingreso += detalle_factura_bebestible.cantidad

    @api.one
    @api.depends('egreso', 'ingreso')
    def _cal_cantidad(self):
        self.cantidad = self.ingreso - self.egreso


class Detalle_Bebestible(models.Model):
    _name = 'restaurante.detalle_bebestible'

    cantidad = fields.Integer()
    precio = fields.Integer(compute="_precio_bebestible") 
    utilidad_por_bebestible = fields.Float(compute="_utilidad_bebestible")
    estado = fields.Selection([ ('pendiente', 'Pendiente'),('entregado', 'Entregado')], default='pendiente')
    stock = fields.Integer(compute="_stock")

    bebestible_id = fields.Many2one('restaurante.bebestible')
    pedido_id = fields.Many2one('restaurante.pedido')

    @api.one
    @api.depends('bebestible_id', 'cantidad')
    def _precio_bebestible(self):
        for bebestible in self.bebestible_id:
            self.precio = bebestible.precio * self.cantidad

    
    @api.one
    @api.depends('bebestible_id')
    def _utilidad_bebestible(self):
        for bebestible in self.bebestible_id:
            costo_total = bebestible.costo * self.cantidad
            self.utilidad_por_bebestible = self.precio - costo_total

    @api.one
    @api.depends('bebestible_id')
    def _stock(self):
        for bebestible in self.bebestible_id:
            self.stock = bebestible.cantidad

    @api.constrains('cantidad')
    def _validar_stock(self):
        if self.stock < 0:
            raise ValidationError('No hay suficiente stock')

class Factura_Bebestible(models.Model):
    _name = 'restaurante.factura_bebestible'

    nombre_proveedor = fields.Char()
    fecha = fields.Date()
    total = fields.Float(compute="_calcular_total")

    detalle_factura_bebestible_ids = fields.One2many('restaurante.detalle_factura_bebestible', 'factura_bebestible_id')

    @api.one
    @api.depends('detalle_factura_bebestible_ids')
    def _calcular_total(self):
        for detalle_factura_bebestible in self.detalle_factura_bebestible_ids:
            self.total += detalle_factura_bebestible.precio
    

class Detalle_Factura_Bebestible(models.Model):
    _name = 'restaurante.detalle_factura_bebestible'

    cantidad = fields.Integer()
    precio = fields.Float(compute="_calcular_precio")   

    factura_bebestible_id = fields.Many2one('restaurante.factura_bebestible')
    bebestible_id = fields.Many2one('restaurante.bebestible')

    @api.one
    @api.depends('bebestible_id')
    def _calcular_precio(self):
        for bebestible in self.bebestible_id:
            self.precio = self.cantidad * bebestible.costo

class Factura_Ingrediente(models.Model):
    _name = 'restaurante.factura_ingrediente'

    nombre_proveedor = fields.Char()
    fecha = fields.Date()
    total = fields.Float(compute="_calcular_total")

    detalle_factura_ingrediente_ids = fields.One2many('restaurante.detalle_factura_ingrediente', 'factura_ingrediente_id')

    @api.one
    @api.depends('detalle_factura_ingrediente_ids')
    def _calcular_total(self):
        for detalle_factura_ingrediente in self.detalle_factura_ingrediente_ids:
            self.total += detalle_factura_ingrediente.precio
    

class Detalle_Factura_Ingrediente(models.Model):
    _name = 'restaurante.detalle_factura_ingrediente'

    cantidad = fields.Integer()
    precio = fields.Float(compute="_calcular_precio")   

    factura_ingrediente_id = fields.Many2one('restaurante.factura_ingrediente')
    ingrediente_id = fields.Many2one('restaurante.ingrediente')

    @api.one
    @api.depends('ingrediente_id')
    def _calcular_precio(self):
        for ingrediente in self.ingrediente_id:
            self.precio = self.cantidad * ingrediente.costo

 

    