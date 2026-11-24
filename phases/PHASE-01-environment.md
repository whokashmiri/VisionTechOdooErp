# Phase 01 — Environment and Tooling

## Objective
Prepare a repeatable local development environment for Odoo 19 Community.

## Learn
- Odoo Community versus Enterprise
- Odoo server, addons and configuration
- Python environments and dependencies
- PostgreSQL databases and users
- Docker and Docker Compose fundamentals
- Git repositories, commits and `.gitignore`

## Build
1. Install or configure Docker Desktop on Windows.
2. Create a project directory and Git repository.
3. Configure Odoo 19 Community and PostgreSQL services.
4. Create a persistent PostgreSQL volume.
5. Mount a local `custom_addons` directory into Odoo.
6. Create an Odoo configuration file.
7. Start the services and open the Odoo web interface.
8. Create a development database and enable developer mode.

## Expected structure
```text
business-management-erp/
├── custom_addons/
├── config/
│   └── odoo.conf
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Acceptance criteria
- Odoo starts successfully.
- PostgreSQL data survives container restarts.
- You can log in and create a development database.
- Odoo can see the custom addons directory.
- Configuration and secrets are not accidentally committed.

## Suggested video searches
- [Odoo 19 Docker installation](https://www.youtube.com/results?search_query=Odoo+19+Docker+installation+Community)
- [Odoo development environment setup](https://www.youtube.com/results?search_query=Odoo+19+development+environment+setup)
- [Docker Compose beginner course](https://www.youtube.com/results?search_query=Docker+Compose+beginner+full+course)

## Deliverable
A working local Odoo 19 development environment with PostgreSQL and a mounted custom addons directory.
