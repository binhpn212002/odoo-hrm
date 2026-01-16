import threading

from ebaysdk.utils import parse_yaml

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import datetime


class HrOvertimeSummary(models.Model):
    _name = "hr.overtime.summary"
    _description = "HR Overtime Summary"

    employee_id = fields.Many2one("hr.employee", string="Employee", required=True)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    total_overtime = fields.Float(string="Total Overtime", required=True)
    ot_type_id = fields.Many2one("hr.ot.type.vn", string="Overtime Type", required=True)

    # cron job to generate overtime summary 1 day once depend on  overtime approved
    def _cron_generate_overtime_summary(self):
        # start date and end date is day first of month and last day of month
        start_date = datetime.now().replace(day=1)
        end_date = datetime.now().replace(day=31)
        # group by employee_id and ot_type_id and sum duration
        cr = self.env.cr
        cr.execute(
            """
            SELECT employee_id, ot_type_id, SUM(duration) as duration
            FROM hr_overtime
            WHERE state = %s AND date >= %s AND date <= %s
            GROUP BY employee_id, ot_type_id
        """,
            ("approved", start_date.date(), end_date.date()),
        )
        overtime_groups = [
            {
                "employee_id": row[0] and (row[0], False),
                "ot_type_id": row[1] and (row[1], False),
                "duration": row[2],
            }
            for row in cr.fetchall()
        ]

        for overtime in overtime_groups:
            # check if overtime summary already =>update
            overtime_summary = self.env["hr.overtime.summary"].search(
                [
                    ("employee_id", "=", overtime["employee_id"][0]),
                    ("date_from", "=", start_date),
                    ("date_to", "=", end_date),
                    ("ot_type_id", "=", overtime["ot_type_id"][0]),
                ],
                limit=1,
            )
            if overtime_summary:
                overtime_summary.write(
                    {
                        "total_overtime": overtime["duration"],
                    }
                )
                continue
            # create overtime summary using SQL cursor
            cr.execute(
                """
                INSERT INTO hr_overtime_summary
                (employee_id, date_from, date_to, ot_type_id, total_overtime, create_uid, create_date, write_uid, write_date)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, NOW())
                """,
                (
                    overtime["employee_id"][0],
                    start_date,
                    end_date,
                    overtime["ot_type_id"][0],
                    overtime["duration"],
                    self.env.uid,
                    self.env.uid,
                ),
            )
