---
name: analyse-module
description: Analyse a Python module and return a structured summary.
context: fork
allowed-tools: Read, Grep, Glob
argument-hint: "path to the module (e.g. app/services/order_service.py)"
---

Analyse the module at $ARGUMENTS.

Return a structured summary covering:

1. Purpose - what this module does in plain terms
2. Public interface - functions and classes other modules actually use
3. Dependencies - what it imports (standard library, third-party, and internal)
4. Dependents - what imports this module
5. Patterns - conventions the module uses
6. Issues - coupling, missing error handling, anything conflicting with CLAUDE.md

Keep it concise.
