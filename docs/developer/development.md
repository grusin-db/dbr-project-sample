# Development

## Environment

Use `make dev` for normal development. It currently aliases `dev17`.
[Databricks Connect](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/python/)
must be equal to or older than the target runtime, so Connect 17 supports DBR
17, 18, and 19.

Change the alias in `Makefile` when the project's minimum runtime changes.
Versioned targets `dev15`, `dev16`, `dev17`, and `dev18` remain available for
compatibility testing. Each target recreates `.venv` and installs its
requirements directly with `uv`.

## Quality checks

```bash
make fmt       # fix lint issues and format code
make lint      # check formatting, lint, and types
make flint     # run fmt, then lint
```

[Ruff](https://docs.astral.sh/ruff/) and
[Pyright](https://microsoft.github.io/pyright/) configuration live in
`pyproject.toml`.

## Tests

Run `make test`. See [Testing](testing.md) for environment setup, parallel
execution, coverage, Databricks Labs pytester, and temporary resource cleanup.
