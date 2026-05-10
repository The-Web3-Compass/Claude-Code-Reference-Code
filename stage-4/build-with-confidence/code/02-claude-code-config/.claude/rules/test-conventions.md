---
paths:
  - "tests/**/*.py"
---

# Test conventions

pytest only. No unittest.TestCase, no self.assert* methods.

Before writing new tests, read the existing test file for that module first. Don't
suggest scenarios already covered.

When testing routes, mock at the service boundary. Don't mock the database directly.
