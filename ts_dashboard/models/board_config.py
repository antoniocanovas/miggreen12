# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class BoardConfig(models.Model):
    _name = "ts.board.config"
    _description = "Dashboard"

    def _compute_items_count(self):
        for board in self:
            if board.is_default_dashboard:
                board.items_count = len(self.env['ts.dashboard'].search(['|',('active','=',False),('active','=',True),'|',('board_config_id','=',False),('board_config_id', '=', board.id)]))
            else:
                board.items_count = len(self.env['ts.dashboard'].search(['|',('active','=',False),('active','=',True),('board_config_id','=',board.id)]))

    name = fields.Char("Dashboard Name", required=True)
    active = fields.Boolean("Active", default=True)
    board_menu_name = fields.Char(string="Menu Name")
    parent_menu_id = fields.Many2one('ir.ui.menu', string="Show Under Menu", domain="[('parent_id','=',False)]")
    board_menu_id = fields.Many2one('ir.ui.menu')
    board_action_id = fields.Many2one('ir.actions.client')
    group_access_id = fields.Many2many('res.groups', string="Group Access")
    dashboard_ids = fields.One2many('ts.dashboard', 'board_config_id', string='Dashboard Items')
    items_count = fields.Integer(compute='_compute_items_count')
    is_default_dashboard = fields.Boolean("Default Dashboard", default=False)

    @api.model
    def create(self, vals):
        res = super(BoardConfig, self).create(vals)

        if 'parent_menu_id' in vals and 'board_menu_name' in vals:
            if not vals.get('board_action_id', False):
                action_id = {
                    'name': vals.get('board_menu_name') + " Board Action",
                    'res_model': 'ts.dashboard',
                    'params': {'board_id': res.id},
                    'tag': 'backend_ts_dashboard',
                }
                res.board_action_id = self.env['ir.actions.client'].sudo().create(action_id)
            else:
                res.board_action_id = vals.get('board_action_id')

            if not vals.get('board_menu_id', False):
                res.board_menu_id = self.env['ir.ui.menu'].sudo().create({
                    'name': vals.get('board_menu_name', ''),
                    'active': vals.get('active', True),
                    'parent_id': vals.get('parent_menu_id'),
                    'action': "ir.actions.client," + str(res.board_action_id.id),
                    'groups_id': vals.get('group_access_id', False),
                })
            else:
                res.board_menu_id = vals.get('board_menu_id')

        return res

    @api.multi
    def write(self, vals):
        res = super(BoardConfig, self).write(vals)
        for rec in self:
            if 'board_menu_name' in vals:
                rec.board_menu_id.sudo().name = vals.get('board_menu_name')
            if 'group_access_id' in vals:
                rec.board_menu_id.sudo().groups_id = vals.get('group_access_id')
            if 'active' in vals and rec.board_menu_id:
                rec.board_menu_id.sudo().active = vals.get('active')
            if 'parent_menu_id' in vals:
                rec.board_menu_id.write(
                    {'parent_id': vals.get('parent_menu_id')}
                )
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.is_default_dashboard:
                raise UserError("You can't delete Default Dashboard!!!")
            rec.board_action_id.sudo().unlink()
            rec.board_menu_id.sudo().unlink()
        return super(BoardConfig, self).unlink()

    def action_open_related_items(self):
        self.ensure_one()
        if self.is_default_dashboard:
            dashboards_ids = self.env['ts.dashboard'].search(['|',('active','=',False),('active','=',True),'|',('board_config_id', '=', False),('board_config_id', '=', self.id)])
            domain = ['|',['active','=',False],['active','=',True],["id", "in", dashboards_ids.ids]]
        else:
            dashboards_ids = self.env['ts.dashboard'].search(['|', ('active', '=', False), ('active', '=', True), ('board_config_id', '=', self.id)])
            domain = ['|',['active','=',False],['active','=',True],["id", "in", dashboards_ids.ids]]
        return {
            "type": "ir.actions.act_window",
            "res_model": "ts.dashboard",
            "views": [[self.env.ref('ts_dashboard.ts_dashboard_view_view_tree').id, "tree"],
                      [self.env.ref('ts_dashboard.ts_dashboard_view_form').id, "form"]],
            "domain": domain,
            "context": {"create": False},
            "name": _("Dashboard Items"),
        }
