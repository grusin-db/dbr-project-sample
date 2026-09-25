# Development

## Environment

Use `make dev` for normal development. It currently aliases `dev17`.
[Databricks Connect](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/python/)
must be equal to or older than the target runtime, so Connect 17 supports DBR
17, 18, and 19.

Change the alias in `Makefile` when the project's minimum runtime changes.
Versioned targets `dev15`, `dev16`, `dev17`, and `dev18` remain available for
compatibility testing.
[`uv.lock`](https://docs.astral.sh/uv/concepts/projects/layout/#the-lockfile)
keeps all environments reproducible.

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

```bash
make test
```

Tests use Databricks Connect and
[`databricks-labs-pytester`](https://github.com/databrickslabs/pytester). The
examples cover:

- package documentation and local skill installation
- Databricks SDK access
- file upload through a temporary Unity Catalog volume
- writing and reading foo/bar rows through a temporary table

Pytester removes temporary workspace resources after each test.
