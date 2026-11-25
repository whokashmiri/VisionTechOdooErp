=========Understanding Node vs Odoo==========
Concept Node.js / Express Odoo
Programming language JavaScript / TypeScript Python
Web framework Express Odoo framework
Database MongoDB / PostgreSQL PostgreSQL
Data models Mongoose / Prisma Odoo ORM
HTTP endpoints Express routes Odoo controllers
Authentication Custom JWT or sessions Built-in authentication
Authorization Custom middleware ACLs and record rules
Frontend React XML and OWL
Business features Built manually Existing or custom modules
Scheduled tasks Cron packages ir.cron

odoo.conf ? - file is the primary configuration file used to control the behavior of the
odoo server (like env , application.properties)

api - Decorator (decorator modifies or registers the behavior of a Python function.) that control model method behavior
fields - field definitions
models - model class and framework functionality

recordset - instance of a model class
write() - updates records in a record set
unlink() - Deletes records

Build UI? using XML (Extensible Markup Language) and odoo renders them using its web client

\*\* operator unpacks the existing Python dictionary.

Object buttton - Executes Py Method , implement business logic, construct dynamic domains, return diff actions, Good for workflows
Action button - Executes Existing action, usually opens predefined functionality , references a particular action, good for navigation

sequence - shows UI (menuitem) in order

Access Control List (CRUD operations) - create = create() ; read = search(), read(); update = write() ; delete = unlink()
odoo use the ir.model.access model to store these permissions
