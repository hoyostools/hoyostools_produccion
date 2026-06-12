from odoo import models, fields, api
from odoo.exceptions import UserError

class StockTransferWizard(models.TransientModel):
    _name = 'stock.transfer.wizard'
    _description = 'Wizard de traslado'

    line_ids = fields.One2many('stock.transfer.wizard.line', 'wizard_id')

    picking_type_id = fields.Many2one(
        'stock.picking.type',
        string='Tipo de operación',
        required=True,
        domain="[('code','=','internal')]"
    )

    transfer_mode = fields.Selection([
        ('different', 'Ubicaciones diferentes'),
        ('same', 'Una misma ubicación')
    ], string='Modo de traslado', required=True, default='different')

    destination_location_id = fields.Many2one(
        'stock.location',
        string='Ubicación destino general'
    )

    state_option = fields.Selection([
        ('draft', 'Listo'),
        ('done', 'Hecho')
    ], string="Estado", required=True)

    user_id = fields.Many2one('res.users', string="Responsable")

    def action_create_transfer(self):

        self.ensure_one()

        if not self.line_ids:
            raise UserError("No hay líneas para trasladar.")

        created_pickings = self.env['stock.picking']

        for line in self.line_ids:

            # ==========================================
            # VALIDAR CANTIDAD
            # ==========================================

            if line.qty_to_move <= 0:
                continue

            if line.qty_to_move > line.available_qty:
                raise UserError(
                    f"Cantidad mayor a la disponible.\n\n"
                    f"Disponible: {line.available_qty}\n"
                    f"Solicitada: {line.qty_to_move}"
                )

            # ==========================================
            # DETERMINAR DESTINO
            # ==========================================

            if self.transfer_mode == 'same':

                if not self.destination_location_id:
                    raise UserError(
                        "Debe seleccionar una ubicación destino general."
                    )

                destination = self.destination_location_id

            else:

                if not line.location_dest_id:
                    raise UserError(
                        f"Debe indicar una ubicación destino para "
                        f"{line.product_id.display_name}"
                    )

                destination = line.location_dest_id

            # ==========================================
            # CREAR PICKING (1 POR PRODUCTO)
            # ==========================================

            picking = self.env['stock.picking'].create({
                'picking_type_id': self.picking_type_id.id,
                'location_id': line.location_id.id,
                'location_dest_id': destination.id,
                'user_id': self.user_id.id if self.user_id else False,
                'origin': 'Traslado Masivo',
            })

            # ==========================================
            # CREAR MOVE
            # ==========================================

            move = self.env['stock.move'].create({
                'name': line.product_id.display_name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.qty_to_move,
                'product_uom': line.product_id.uom_id.id,
                'location_id': line.location_id.id,
                'location_dest_id': destination.id,
                'picking_id': picking.id,
            })

            # ==========================================
            # CONFIRMAR
            # ==========================================

            picking.action_confirm()
            picking.action_assign()

            # ==========================================
            # VALIDAR SI ESTADO = HECHO
            # ==========================================

            if self.state_option == 'done':

                for move_line in move.move_line_ids:
                    move_line.quantity = line.qty_to_move

                picking.button_validate()

            created_pickings |= picking

        # ==========================================
        # ABRIR RESULTADO
        # ==========================================

        if not created_pickings:
            return {'type': 'ir.actions.act_window_close'}

        if len(created_pickings) == 1:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'view_mode': 'form',
                'res_id': created_pickings.id,
            }

        return {
            'type': 'ir.actions.act_window',
            'name': 'Traslados creados',
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created_pickings.ids)],
        }