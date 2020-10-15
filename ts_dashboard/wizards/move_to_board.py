from odoo import api, fields, models, tools


class MovetoBoard(models.TransientModel):
    _name = 'move.to.board'
    _description = 'Sample Mail Wizard'

    board_id = fields.Many2one('ts.board.config', string='Board', required=True)

    @api.multi
    def move_to_board(self):
        self.ensure_one()
        if self.env.context.get('active_model', '') == 'ts.dashboard':
            dashboard_id = self.env['ts.dashboard'].browse(self.env.context.get('active_id', ''))
            if dashboard_id:
                dashboard_id.board_config_id = self.board_id
        return True
