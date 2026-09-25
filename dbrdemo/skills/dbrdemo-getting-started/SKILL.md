---
name: dbrdemo-getting-started
description: >-
  Develop, test, package, and configure the dbrdemo project. Use when choosing
  a Databricks Runtime, running quality checks, building the wheel, or
  installing the bundled Agent Skills.
---

# dbrdemo-getting-started

Use this skill for development tasks in the dbrdemo repository.

## Setup

1. Install the Databricks VS Code extension 2.17 or newer.
2. Authenticate with a clear profile name.
3. Select serverless or classic compute.
4. Run `direnv allow`.
5. Run `make dev`.

## Commands

- `make dev15`, `dev16`, `dev17`, or `dev18`: select DBR dependencies.
- `make flint`: format, lint, and type-check.
- `make test`: run tests with coverage.
- `make dist`: build the wheel.
- `make install_skills`: install skills locally.
- `make install_user_skill`: install skills for the current Databricks user.
- `make install_workspace_skill`: install skills for all workspace users.

## Rename for your project

1. Change `SKILL_DIR_PREFIX` in `dbrdemo/skills.py`.
2. Rename this folder to `<your-prefix>-getting-started`.
3. Update the `name` in the frontmatter above.
4. Replace the dbrdemo-specific guidance with your project workflow.
