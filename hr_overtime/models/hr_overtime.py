# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class HrOvertime(models.Model):
    _name = 'hr.overtime'
    _inherit = 'mail.thread'
    _description = 'HR Overtime Management'
    _rec_name = 'employee_id'
    _order = 'id desc'

    name = fields.Char(compute='_compute_name')
    employee_id = fields.Many2one('hr.employee', string=(_("Empleado")))
    manager_id = fields.Many2one('hr.employee', string='Responsable', related="employee_id.parent_id")
    start_date = fields.Datetime(_('Fecha Desde'))
    stop_date = fields.Datetime(_('Fecha Hasta'))
    overtime_hours = fields.Float(_('Horas Extra'), compute="_compute_hours")
    units = fields.Float(_('Cantidad'))
    notes = fields.Text(string=(_('Notas')))
    state = fields.Selection([('draft', (_('Borrador'))), ('confirm', (_('Pendiente'))), ('refuse', (_('Rechazado'))),
                              ('validate', (_('Aprobado'))), ('cancel', (_('Cancelado')))], default='draft', copy=False)
    attendance_id = fields.Many2one('hr.attendance', string=(_('Registro de Asistencia')))
    overtime_type_id = fields.Many2one('hr.overtime.type', string='Tipo de Hora Extras')
    overtime_type_duration_type = fields.Selection(string='Tipo de Duracion', related='overtime_type_id.duration_type')
    contract_id = fields.Many2one(string="Contrato", related='employee_id.contract_id')

    @api.depends('start_date', 'stop_date')
    def _compute_hours(self):
        for record in self:
            if record.start_date and record.stop_date:
                delta = record.stop_date - record.start_date
                record.overtime_hours = delta.total_seconds() / 3600
            else:
                record.overtime_hours = 0.00

    @api.depends('employee_id', 'overtime_type_id')
    def _compute_name(self):
        for record in self:
            if record.employee_id and record.overtime_type_id and record.overtime_type_id:
                record.name = 'Horas extra para ' + record.employee_id.name + ' - Codigo: ' + record.overtime_type_id.payroll_code + ' (' + str(record.overtime_hours) + ')'
            else:
                record.name = 'Nuevo registro de horas extra...'

    @api.model
    def run_overtime_scheduler(self):
        """ Main Overtime Calculation Function """
        attend_signin_ids = self.env['hr.attendance'].search(
            [('overtime_created', '=', False)])
        for attendance in attend_signin_ids:
            if attendance.check_in and attendance.check_out:
                contracts = self.env['hr.contract'].search([('employee_id', '=', attendance.employee_id.id),
                                                            ('resource_calendar_id', '!=', False)])
                delta = attendance.check_out - attendance.check_in
                total_working_hours = delta.total_seconds() / 3600.0
                for contract in contracts:
                    normal_hours = contract.resource_calendar_id.hours_per_day
                    if total_working_hours > normal_hours:
                        overtime_hours = total_working_hours - normal_hours
                        vals = {
                            'employee_id': attendance.employee_id and attendance.employee_id.id or False,
                            'manager_id': attendance.employee_id and attendance.employee_id.parent_id and attendance.employee_id.parent_id.id or False,
                            'start_date': attendance.check_in,
                            'overtime_hours': round(overtime_hours, 2),
                            'attendance_id': attendance.id,
                            'overtime_type_code': False,
                        }
                        self.env['hr.overtime'].create(vals)
                        attendance.overtime_created = True

    def action_submit(self):
        return self.write({'state': 'confirm'})

    def action_cancel(self):
        return self.write({'state': 'cancel'})

    def action_approve(self):
        for record in self:
            if record.overtime_type_id:
                return self.write({'state': 'validate'})
            else:
                raise ValidationError(
                    _('ERROR: No puede validar horas extras sin haber definido antes su codigo.'))

    def action_refuse(self):
        return self.write({'state': 'refuse'})

    def action_view_attendance(self):
        attendances = self.mapped('attendance_id')
        action = self.env.ref('hr_attendance.hr_attendance_action').read()[0]
        if len(attendances) > 1:
            action['domain'] = [('id', 'in', attendances.ids)]
        elif len(attendances) == 1:
            action['views'] = [
                (self.env.ref('hr_attendance.hr_attendance_view_form').id, 'form')]
            action['res_id'] = self.attendance_id.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


class HrOvertimeType(models.Model):
    _name = 'hr.overtime.type'
    _description = 'HR Overtime Types'

    name = fields.Char(string='Nombre', required=True)
    payroll_code = fields.Char(string='Codigo de Payroll', required=True)
    duration_type = fields.Selection([
        ('hour', 'Horas'),
        ('unit', 'Unidades Fijas')
    ], string='Tipo de Unidad', default="hour", required=True)
    type = fields.Selection([
        ('fixed', 'Valor Fijo'),
        ('add_percentage', 'Porcentaje Adicional'),
    ], string='Tipo', default="add_percentage", required=True)
    fixed_amount = fields.Float(string='Valor Fijo')
    add_percentage_amount = fields.Float(string='Porcentaje')
    notes = fields.Text(string=(_('Notas')))

