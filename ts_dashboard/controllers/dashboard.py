# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class TSDashboard(http.Controller):

    @http.route('/ts_dashboard/get_dashboard_data', type="json", auth='user')
    def fetch_dashboard_data(self, board_id=False):
        dashboard_obj = request.env['ts.dashboard'].sudo()
        board_obj = request.env['ts.board.config'].sudo()
        if board_id and not board_obj.browse(board_id).is_default_dashboard:
            dashboard_ids = board_obj.browse(board_id).dashboard_ids
        else:
            default_board_id = request.env['ts.board.config'].sudo().search([('is_default_dashboard','=',True)])
            dashboard_ids = dashboard_obj.search(['|',('board_config_id','=',False),('board_config_id','=',default_board_id.id)])
        dashboard_data = dashboard_obj.get_dashboard_data(dashboard_ids)
        return_dashboard_data = {
            'refresh_interval': request.env['ir.config_parameter'].sudo().get_param('refresh_interval'),
            'dashboards': dashboard_data}
        return return_dashboard_data
