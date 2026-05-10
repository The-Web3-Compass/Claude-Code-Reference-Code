---
paths:
  - "app/routes/**/*.py"
---

# Route handler conventions

Route handlers do exactly three things: validate input, call a service, return a response.
No business logic. No database queries.

Errors from services arrive as AppError. Catch those in the handler and return the
appropriate HTTP response. Don't catch other exceptions.
