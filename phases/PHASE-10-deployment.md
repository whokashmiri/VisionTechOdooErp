# Phase 10 — Testing, Deployment and Production Readiness

## Objective
Prepare the ERP for a repeatable deployment and maintainable operation.

## Learn
- Odoo testing patterns and test tags
- Python unit tests and integration tests
- API testing
- Logging and debugging
- PostgreSQL backups and restores
- Docker Compose production considerations
- Linux server administration
- Nginx reverse proxy
- HTTPS and SSL certificates
- Odoo workers and resource configuration
- File storage and attachments
- Upgrade and rollback planning
- Monitoring and performance basics

## Build
1. Add tests for critical models and business workflows.
2. Test access rights and record rules using different users.
3. Test API success and failure cases.
4. Create a production-oriented Docker Compose configuration.
5. Configure a persistent database and filestore.
6. Configure Nginx as a reverse proxy.
7. Configure HTTPS using a trusted certificate process.
8. Create and test backup/restore procedures.
9. Document deployment and recovery steps.
10. Run a final acceptance test of the complete application.

## Production cautions
- Do not expose PostgreSQL directly to the public internet.
- Use strong unique credentials and secure secret storage.
- Configure HTTPS.
- Restrict administrative access.
- Test backups by restoring them.
- Review Odoo's production deployment guidance before going live.
- Do not use real personal or employee data in a learning environment.

## Acceptance criteria
- Automated tests pass.
- Critical user journeys work from start to finish.
- Access control has been tested.
- The application can be deployed from documented steps.
- Database and filestore backups can be restored.
- Secrets are not stored in Git.
- Known limitations and operational procedures are documented.

## Suggested video searches
- [Odoo testing tutorial](https://www.youtube.com/results?search_query=Odoo+19+testing+unit+tests+tutorial)
- [Odoo Docker production deployment](https://www.youtube.com/results?search_query=Odoo+19+Docker+production+deployment)
- [Odoo Nginx HTTPS deployment](https://www.youtube.com/results?search_query=Odoo+Nginx+HTTPS+production+deployment)
- [PostgreSQL backup and restore](https://www.youtube.com/results?search_query=PostgreSQL+backup+restore+pg_dump+tutorial)

## Deliverable
A tested, documented Odoo ERP deployment with backup and recovery instructions.
