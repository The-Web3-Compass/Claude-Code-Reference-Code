# support-api - Claude Code conventions

## Architecture

Three layers with distinct responsibilities:

- `app/routes/` - Flask route handlers. Validate input, call a service, return a response.
- `app/services/` - Business logic. All decision-making lives here.
- `app/models/` - Data structure only, no logic.

Routes call services. Services call models. Routes never query the database directly.
Models never contain business logic. When you see either boundary crossed, flag it.

## Python

- Type hints on all function signatures - parameters and return types both.
- Raise `AppError` from `app/errors.py` for application errors, not bare exceptions.

## Testing

Tests live in `tests/` mirroring the app structure. `app/routes/customers.py` is
tested in `tests/routes/test_customers.py`. Framework is pytest - no unittest patterns.

Before writing tests for any module, read the existing test file first. Don't suggest
scenarios already covered.

## Code review

Flag: database queries in route handlers, business logic in models, bare
`except Exception` blocks, missing type hints on exported functions.

Don't flag: variable naming preferences, docstring style, formatting that
black handles automatically.
