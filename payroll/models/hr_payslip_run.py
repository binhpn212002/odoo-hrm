# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError


class HrPayslipRun(models.Model):
    _name = "hr.payslip.run"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Payslip Batches"
    _order = "id desc"

    employee_ids = fields.Many2many(
        "hr.employee",
        "hr_employee_payslip_run_rel",
        "payslip_run_id",
        "employee_id",
        string="Employees",
        compute="_compute_employee_ids",
    )

    name = fields.Char(required=True, readonly=True, compute="_compute_name")
    slip_ids = fields.One2many(
        "hr.payslip",
        "payslip_run_id",
        string="Payslips",
        readonly=True,
    )
    state = fields.Selection(
        [("draft", "Draft"), ("close", "Close")],
        string="Status",
        index=True,
        readonly=True,
        copy=False,
        tracking=1,
        default="draft",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        copy=False,
        default=lambda self: self.env.company,
    )
    date_start = fields.Date(
        string="Date From",
        required=True,
        readonly=True,
        default=lambda self: fields.Date.today().replace(day=1),
    )
    date_end = fields.Date(
        string="Date To",
        required=True,
        readonly=True,
        default=lambda self: fields.Date.today().replace(day=1)
        + relativedelta(months=+1, day=1, days=-1),
    )
    credit_note = fields.Boolean(
        readonly=True,
        help="If its checked, indicates that all payslips generated from here "
        "are refund payslips.",
    )
    struct_id = fields.Many2one(
        "hr.payroll.structure",
        string="Structure",
        readonly=True,
        help="Defines the rules that have to be applied to this payslip batch, "
        "accordingly to the contract chosen. If you let empty the field "
        "contract, this field isn't mandatory anymore and thus the rules "
        "applied will be all the rules set on the structure of all contracts "
        "of the employee valid for the chosen period",
    )

    def draft_payslip_run(self):
        return self.write({"state": "draft"})

    def close_payslip_run(self):
        return self.write({"state": "close"})

    @api.depends("date_start", "date_end", "struct_id")
    def _compute_name(self):
        for run in self:
            month = run.date_start.month
            if run.struct_id:
                job_name = run.struct_id.job_id.name
                run.name = f"Bang luong cho {job_name} tu thang {month} "
            else:
                run.name = f"Bang luong tu thang {month} "

    @api.depends("struct_id")
    def _compute_employee_ids(self):
        for run in self:
            if run.struct_id:
                states = ["open", "draft"]
                contracts = self.env["hr.contract"].search(
                    [("struct_id.id", "=", run.struct_id.id), ("state", "in", states)]
                )
                employees = contracts.mapped("employee_id")
                run.employee_ids = employees
            else:
                run.employee_ids = False

    # Prepare payslip values for all selected employees
    def prepare_payslip_vals(self):
        for run in self:
            if run.employee_ids:
                for employee in run.employee_ids:
                    # check if payslip already exists
                    payslip = self.env["hr.payslip"].search(
                        [
                            ("employee_id", "=", employee.id),
                            ("date_from", "=", run.date_start),
                            ("date_to", "=", run.date_end),
                        ]
                    )
                    if payslip:
                        continue
                    payslip = self.env["hr.payslip"].create(
                        {
                            "name": f"Bang luong cho {employee.name} tu thang {run.date_start.month} den thang {run.date_end.month} ",
                            "employee_id": employee.id,
                            "date_from": run.date_start,
                            "date_to": run.date_end,
                            "credit_note": run.credit_note,
                            # "journal_id": run.journal_id.id,
                            "company_id": employee.company_id.id,
                            "struct_id": run.struct_id.id,
                            "contract_id": employee.contract_id.id,
                            "payslip_run_id": run.id,
                        }
                    )
