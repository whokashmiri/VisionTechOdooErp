from odoo import api, models
from odoo.exceptions import AccessError, UserError


def _require_report_group(env, groups):
    if not any(
        env.user.has_group(group)
        for group in groups
    ):
        raise AccessError(
            "You are not authorized to print this report."
        )


def _get_report_documents(env, model_name, docids):
    if not docids:
        raise UserError(
            "Select at least one record to print."
        )

    records = env[model_name].browse(docids)

    records.check_access("read")

    if len(records.exists()) != len(records):
        raise UserError(
            "One or more selected records no longer exist."
        )

    return {
        "doc_ids": records.ids,
        "doc_model": model_name,
        "docs": records,
    }


class EmployeeProfileReport(models.AbstractModel):
    _name = "report.vt_hr_reports.report_employee_profile"
    _description = "Employee Profile Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        _require_report_group(
            self.env,
            [
                "vt_employee.group_vt_employee",
                "base.group_system",
            ],
        )

        return _get_report_documents(
            self.env,
            "vt.employee",
            docids,
        )



class DepartmentEmployeesReport(models.AbstractModel):
    _name = "report.vt_hr_reports.report_department_employees"
    _description = "Department Employees Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        _require_report_group(
            self.env,
            [
                "vt_employee.group_vt_hr_user",
                "base.group_system",
            ],
        )

        values = _get_report_documents(
            self.env,
            "vt.department",
            docids,
        )

        department_employees = {}

        Employee = self.env["vt.employee"]

        for department in values["docs"]:
            employees = Employee.search(
                [
                    ("department_id", "=", department.id),
                    ("active", "=", True),
                ],
                order="employee_code asc",
            )

            department_employees[department.id] = employees

        values["department_employees"] = department_employees

        return values

class LeaveSummaryReport(models.AbstractModel):
    _name = "report.vt_hr_reports.report_leave_summary"
    _description = "Leave Request Summary Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        _require_report_group(
            self.env,
            [
                "vt_employee.group_vt_employee",
                "base.group_system",
            ],
        )

        return _get_report_documents(
            self.env,
            "vt.leave.request",
            docids,
        )