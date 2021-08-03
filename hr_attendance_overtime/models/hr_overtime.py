# Copyright (C) 2021 Nimarosa (Nicolas Rodriguez) (<nicolasrsande@gmail.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class HrOvertime(models.Model):
    _name = 'hr.overtime'
    _description = 'HR Overtime Management'
    _rec_name = 'employee_id'
    _order = 'id desc'

    employee_id = fields.Many2one('hr.employee', string=(_("Empleado")))
    manager_id = fields.Many2one('hr.employee', string=(_('Oficial HR')))
    start_date = fields.Datetime(_('Fecha'))
    overtime_hours = fields.Float(_('Horas Extra'))
    notes = fields.Text(string=(_('Notas')))
    state = fields.Selection([('draft', (_('Borrador'))), ('confirm', (_('Esperando Aprobacion'))), ('refuse', (_('Rechazado'))),
                              ('validate', (_('Aprovado'))), ('cancel', (_('Cancelado')))], default='draft', copy=False)
    attendance_id = fields.Many2one('hr.attendance', string=(_('Registro de Asistencia')))
    overtime_type_id = fields.Many2one('hr.overtime.type', string='Tipo de Hora Extras')

    @api.model
    def run_overtime(self):
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

    @api.model
    def run_overtime_scheduler(self):
        """ Scheduler Function """
        self.run_overtime()

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
    _name = 'hr.attendance.overtime.type'
    _description = 'HR Overtime Types'

    description = fields.Char(string='Descripcion')
    payroll_code = fields.Char(string='Codigo de Payroll')
    name = fields.Char(compute='_compute_name', string='')

    @api.depends('payroll_code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = '( ' + record.payroll_code + ' ) ' + record.description
