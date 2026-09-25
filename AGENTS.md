# dbrdemo dev guide

Databricks starter/sample project. Tooling: `uv`, `ruff`, `pyright`, Unity Gateway CLI (`ug`), and Agent Skills.

## Quick setup

```bash
make direnv
# Open a new terminal.
direnv allow
make dev
```

The Databricks VS Code extension must be authenticated with compute selected.
See [developer setup](docs/developer/getting-started.md).

## Everyday commands

```bash
make fmt      # ruff auto-fix + format (quote style preserved)
make lint     # ruff check + ruff format --check + pyright
make flint    # fmt then lint
make test     # pytest + coverage (needs a Databricks connection)
make dist     # build the wheel
make release ENV=prod  # version and build a release wheel
```

## Code style (required)

- PEP 8, formatted by `ruff` (`make flint`). Line length 120. Quote style is
  `preserve` -- do not mass-convert quotes.
- Type-annotate every function signature, including every argument and return
  value. Import types normally when their package is a required dependency.
- Add a docstring to every module, public function, and fixture. Use Google
  style: an imperative one-line summary, then `Args:` and `Returns:` sections
  where they apply.
- Never add a `Raises:` docstring section.
- Preserve existing type annotations and docstring sections when editing.
- Keep imports lazy only when there is a real reason (avoid a connection on
  import, or an optional/cluster-only dependency); document that reason inline.

## Coding agents via Unity Gateway (`ug`)

```bash
make ug
make install_claudecode
ug claude
```

See [coding agents](docs/developer/coding-agents.md) for all supported agents.
Use `ug`, not the retired `ucode` command.

## Skills

Skills are `dbrdemo-*` folders under `skills/`; `make dist` bundles them.
See [skill installation](docs/admin/skills.md).

## Renaming for your own project

See [RENAME.md](RENAME.md).
