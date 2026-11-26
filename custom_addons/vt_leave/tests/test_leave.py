
from datetime import date

from odoo import Command
from odoo.exceptions import (
    AccessError,
    UserError,
    ValidationError,
)
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestLeaveWorkflow(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        employee_group = cls.env.ref(
            "vt_employee.group_vt_employee"
        )

        manager_group = cls.env.ref(
            "vt_employee.group_vt_hr_manager"
        )

        Users = cls.env["res.users"]

        cls.employee_user = Users.create({
            "name": "Workflow Test Employee",
            "login": "workflow.employee.test",
            "group_ids": [
                Command.set([employee_group.id]),
            ],
        })

        cls.manager_user = Users.create({
            "name": "Workflow Test Manager",
            "login": "workflow.manager.test",
            "group_ids": [
                Command.set([manager_group.id]),
            ],
        })

        department = cls.env["vt.department"].create({
            "name": "Workflow Test Department",
            "code": "WORKFLOW-TEST",
        })

        cls.employee = cls.env["vt.employee"].create({
            "name": "Workflow Employee",
            "employee_code": "WORKFLOW-TEST-001",
            "department_id": department.id,
            "user_id": cls.employee_user.id,
        })

        cls.Leave = cls.env[
            "vt.leave.request"
        ].with_user(cls.employee_user)

    def _create_request(self, **extra):
        values = {
            "name": "Test Leave",
            "leave_type": "annual",
            "start_date": date(2026, 12, 1),
            "end_date": date(2026, 12, 5),
            "reason": "Automated test",
        }

        values.update(extra)

        return self.Leave.create(values)

    def test_duration(self):
        request = self._create_request()

        self.assertEqual(request.duration, 5)

    def test_invalid_dates(self):
        with self.assertRaises(ValidationError):
            with self.env.cr.savepoint():
                self._create_request(
                    end_date=date(2026, 11, 30),
                )

    def test_initial_state(self):
        request = self._create_request(
            state="approved",
        )

        self.assertEqual(request.state, "draft")

    def test_submit(self):
        request = self._create_request()

        request.action_submit()

        self.assertEqual(request.state, "submitted")
        self.assertEqual(
            request.submitted_by,
            self.employee_user,
        )

    def test_employee_cannot_approve(self):
        request = self._create_request()

        request.action_submit()

        with self.assertRaises(AccessError):
            request.action_approve()

    def test_direct_state_write_denied(self):
        request = self._create_request()

        with self.assertRaises(AccessError):
            request.write({
                "state": "approved",
            })

    def test_manager_can_approve(self):
        request = self._create_request()

        request.action_submit()

        request.with_user(
            self.manager_user
        ).action_approve()

        self.assertEqual(request.state, "approved")
        self.assertEqual(
            request.decision_by,
            self.manager_user,
        )
        self.assertTrue(request.decision_at)

    def test_manager_cannot_approve_draft(self):
        request = self._create_request()

        with self.assertRaises(UserError):
            request.with_user(
                self.manager_user
            ).action_approve()

    def test_rejected_request_is_final(self):
        request = self._create_request()

        request.action_submit()

        manager_request = request.with_user(
            self.manager_user
        )

        manager_request.action_reject()

        self.assertEqual(request.state, "rejected")

        with self.assertRaises(UserError):
            manager_request.action_approve()

    def test_submitted_request_cannot_be_deleted(self):
        request = self._create_request()

        request.action_submit()

        with self.assertRaises(AccessError):
            request.unlink()
