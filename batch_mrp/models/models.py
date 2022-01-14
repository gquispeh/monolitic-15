from csv import unregister_dialect
from odoo import api, fields, models


class MrpProductionDetails(models.Model):
    _inherit = 'mrp.production'
    details_ids = fields.One2many(
        'stock.move.line.details', 'mrp_id', string='Movimiento de Componentes')


class MrpProductionBatch(models.Model):
    _name = 'mrp.production.batch'

    name = fields.Char(string='Nombre')
    mrp_ids = fields.Many2many(
        'mrp.production', string='Ordenes de Fabricación')
    lot_ids = fields.Many2many(
        'stock.production.lot', string='Lotes')
    move_raw_ids = fields.Many2many(
        'stock.move.line.details', string='Movimiento de Componentes')

    workorder_ids = fields.Many2many(
        'mrp.workorder', string='Orden de Trabajo')

    state = fields.Selection([
        ('1', 'draft'),
        ('2', 'in_progress'),
        ('3', 'done'),
        ('4', 'cancel')
    ], string='Estado')


class StockMoveLineDetails(models.Model):
    _name = "stock.move.line.details"

    user_id = fields.Many2one('res.users', string='Responsable')
    company_id = fields.Many2one('res.company', string='Compañia')
    name = fields.Char('Name')
    mrp_id = fields.Many2one('mrp.production', string='MO')
    equipo_lot_id = fields.Many2one('stock.production.lot', string='Lote')
    product_id = fields.Many2one('product.template', string='Producto')
    cantidad = fields.Integer(string='Cantidad')
    serie_componente = fields.Char(string='Serie Componente')
