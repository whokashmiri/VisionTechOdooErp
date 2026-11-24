# Phase 08 — Controllers and External API Integrations

## Objective
Connect Odoo to external applications and expose selected business operations safely.

## Learn
- Odoo HTTP controllers and routes
- Request and response handling
- JSON payload validation
- Authentication and authorization
- REST API design
- Webhooks
- Error handling and logging
- Idempotency and retry considerations
- External API credentials and secret management
- JSON-RPC/XML-RPC concepts and version-specific API availability

## Build
1. Create a small custom controller.
2. Expose a read-only endpoint for permitted employee or project data.
3. Add authentication and authorization appropriate to the endpoint.
4. Validate incoming JSON data.
5. Create a webhook receiver for a simulated external event.
6. Add structured error responses and logging.
7. Test endpoints using Postman or an equivalent API client.
8. Document request and response examples.

## Security requirements
- Never expose private employee or salary data publicly.
- Do not hardcode API keys or passwords.
- Validate every incoming value.
- Apply permissions at the business-record level.
- Avoid using `sudo()` as a shortcut around authorization.

## Acceptance criteria
- Endpoints return documented responses.
- Unauthorized requests are rejected.
- Invalid payloads produce useful errors.
- Duplicate webhook deliveries do not create duplicate business actions where idempotency is required.
- Secrets are kept outside source control.

## Suggested video searches
- [Odoo 19 controllers tutorial](https://www.youtube.com/results?search_query=Odoo+19+controllers+HTTP+routes+tutorial)
- [Odoo REST API integration](https://www.youtube.com/results?search_query=Odoo+19+REST+API+integration)
- [Odoo webhook integration](https://www.youtube.com/results?search_query=Odoo+webhook+integration+Python)

## Deliverable
A documented and tested API integration module.
