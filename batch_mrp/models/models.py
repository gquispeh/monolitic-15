from csv import unregister_dialect
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


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
        ('1', 'Borrador'),
        ('2', 'En progreso'),
        ('3', 'Contando'),
        ('4', 'Fin del conteo'),
        ('5', 'Hecho'),
        ('6', 'Cancelado')
    ], default='1', string='Estado')

    lote_inicio = fields.Integer('Lote Inicio')
    lote_final = fields.Integer('Lote Final')

    def iniciar_conteo_tiempo(self):
        self.write({'state': '3'})
        pass

    def finalizar_conteo_tiempo(self):
        self.write({'state': '4'})
        pass

    # def compute_mrps(self):
    #    wo = self.env['mrp.workorder'].search(
    #        [(('production_id', 'in', self.mrp_ids.workorder_ids.ids))])
    #    _logger.info('*****WO IDS*****')
    #    _logger.info(self.mrp_ids.workorder_ids.ids)
    #    _logger.info('*****WO*****')
    #    _logger.info(wo.ids)
    #    return wo

        # for mo in self.mrp_ids:
        #    for wo in mo.workorder_ids:
        #        _logger.info('*****WO*****')


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
