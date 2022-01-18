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

    def iniciar_conteo_tiempo(self):
        pass

    def finalizar_conteo_tiempo(self):
        pass

    @api.onchange('mrp_ids')
    def compute_mrps(self):
        # lines = self.env['stock.move.line.details'].search(
        #    [('line_id', '=', self.line_id.id)]).ids
        #lines = []
        #self.write({'subtask_ids': [(6, 0, lines)]})
        #(6, 0, mo.workorder_ids.ids)
        workorder_ids = [_logger.info(mo)
                         for mo in self.mrp_ids]

        _logger.info('**********')
        _logger.info(workorder_ids)


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
