from csv import unregister_dialect
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class MrpProductionDetails(models.Model):
    _inherit = 'mrp.production'
    details_ids = fields.One2many(
        'stock.move.line.details', 'mrp_id', string='Movimiento de Componentes')
    batch_id = fields.Many2one('mrp.production.batch', string='Batch Group')

    def move_raw_line_details(self):
        for mol in self.move_raw_ids:
            for mold in mol.move_line_ids:
                i = 1
                while i <= int(mold.product_qty):
                    lines = self.env['stock.move.line.details'].create({
                        'user_id': self.user_id.id,
                        'company_id': self.company_id.id,
                        'name': mold.display_name,
                        'mrp_id': mold.production_id.id,
                        'equipo_lot_id': self.lot_producing_id.id,
                        'product_id': mold.product_id.id,
                        'cantidad': '1'
                        # 'serie_componente':
                    })
                    i = i+1

    def action_view_batch(self):
        backorder_ids = self.procurement_group_id.mrp_production_ids
        if self.batch_id:
            return {
                'name': 'List Batch',
                'view_mode': 'form',
                'res_model': 'mrp.production.batch',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.batch_id.id,
                'domain': [('id', '=', self.batch_id.id)],
            }
        else:
            form_view = self.env.ref(
                'batch_mrp.mrp_production_batch_view_form')
            b_lotes_list = []
            b_workorder_list = []
            b_move_raw_ids = []
            for b_lotes_line in backorder_ids:
                b_lotes_list.append(b_lotes_line.lot_producing_id.id)
                for wo in b_lotes_line.workorder_ids:
                    b_workorder_list.append(wo.id)
                for modl in b_lotes_line.details_ids:
                    b_move_raw_ids.append(modl.id)

            # USAR backorder_ids.split(", ") para agregar el nombre automaticamente
            # _logger.info(
            #    "************ {}".format(backorder_ids[0].name.split("-")[0]))
            context = {
                'default_name': "#Batch {}".format(backorder_ids[0].name.split("-")[0]),
                'default_mrp_ids': backorder_ids.ids,
                'default_lot_ids': b_lotes_list,
                'default_workorder_ids': b_workorder_list,
                'default_move_raw_ids': b_move_raw_ids
            }

            return {
                'name': 'MO Batch',
                'view_mode': 'form',
                'res_model': 'mrp.production.batch',
                'view_id': form_view.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': context
            }


class MrpProductionBatch(models.Model):
    _name = 'mrp.production.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre')
    mrp_ids = fields.One2many(
        'mrp.production', 'batch_id', string='Ordenes de Fabricación')
    lot_ids = fields.Many2many(
        'stock.production.lot', string='Lotes')
    move_raw_ids = fields.Many2many(
        'stock.move.line.details', string='Movimiento de Componentes', readonly=False, compute="_listar_componentes", store=True)
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

    # FUNCION PARA ACTUALIZAR LOS COMPONENTES
    # @api.depends('mrp_ids')
    # def _depends_mrp_ids(self):
    #    b_move_raw_ids = []
    #    for rec in self:
    #        for mo in self.mrp_ids:
    #            for modl in mo.details_ids:
    #                b_move_raw_ids.append(modl.id)
    #        rec.move_raw_ids = b_move_raw_ids

    def imputar_tiempos(self):

        context = {
            'default_name': 'Wizard',
            'default_workorder_ids': self.workorder_ids.ids
        }
        return {
            'name': 'Imputar Tiempos',
            'view_mode': 'form',
            'res_model': 'wizard.batch.workorder',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
        }


# MODELO WIZARD PARA ORDENES DE TRABAJO
class WizardBatchWorkorders(models.TransientModel):
    _name = 'wizard.batch.workorder'

    name = fields.Char('name')
    proceso = fields.Selection([
        ('todo', 'Todo'),
        ('montaje', 'Montaje'),
        ('ensamblaje', 'Ensamblaje'),
        ('verificacion', 'Verificación')
    ], string='Proceso', default="todo")
    workorder_ids = fields.Many2many(
        'mrp.workorder', string='Orden de Trabajo')

    @api.onchange('proces')
    def _onchange_proces(self):
        pass


# MODELO DEL LINEAS DE COMPONENTES
class StockMoveLineDetails(models.Model):
    _name = "stock.move.line.details"

    user_id = fields.Many2one('res.users', string='Responsable')
    company_id = fields.Many2one('res.company', string='Compañia')
    name = fields.Char('Name')
    mrp_id = fields.Many2one('mrp.production', string='MO')
    equipo_lot_id = fields.Many2one('stock.production.lot', string='Lote')
    product_id = fields.Many2one('product.product', string='Producto')
    cantidad = fields.Integer(string='Cantidad')
    serie_componente = fields.Char(string='Serie Componente')


class MrpWorkordersType(models.Model):
    _inherit = "mrp.workorder"
    proceso = fields.Selection([
        ('montaje', 'Montaje'),
        ('ensamblaje', 'Ensamblaje'),
        ('verificacion', 'Verificación')
    ], string='Proceso')
