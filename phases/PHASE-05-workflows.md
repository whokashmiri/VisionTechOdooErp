# Phase 05 — HR Business Workflows

## Objective
Turn the employee directory into a small HR workflow application.

## Features
- Leave requests
- Leave approval and rejection
- Attendance check-in/check-out
- Employee onboarding request
- Approval history and notifications

## Learn
- Selection/state fields and state transitions
- `@api.depends`, `@api.onchange`, `@api.constrains`
- Date and datetime handling
- `models.TransientModel` and wizards
- Object buttons and server actions
- Scheduled actions (cron)
- Mail templates and activities
- Testing business rules

## Build incrementally
1. Add a leave request model.
2. Validate date ranges and calculate duration.
3. Implement draft, submitted, approved and rejected states.
4. Restrict who can approve requests.
5. Record who approved or rejected and when.
6. Add notifications or activities.
7. Add attendance records and basic duration calculations.
8. Add an onboarding or equipment request wizard if useful.

## Important design note
This phase is for learning custom workflow development. Compare the result with Odoo's standard Time Off and Attendances applications before deciding what should remain custom.

## Acceptance criteria
- Invalid leave date ranges are rejected.
- Only authorized users can approve or reject.
- State transitions follow the defined workflow.
- Approval history is retained.
- Attendance calculations handle missing or invalid check-out values safely.

## Suggested video searches
- [Odoo computed fields and constraints](https://www.youtube.com/results?search_query=Odoo+19+computed+fields+api.depends+api.constrains)
- [Odoo wizard TransientModel](https://www.youtube.com/results?search_query=Odoo+19+wizard+TransientModel+tutorial)
- [Odoo scheduled actions cron](https://www.youtube.com/results?search_query=Odoo+19+scheduled+actions+cron+tutorial)
- [Odoo email templates](https://www.youtube.com/results?search_query=Odoo+19+email+templates+tutorial)

## Deliverable
A working HR workflow with leave requests, approvals, basic attendance and notifications.
