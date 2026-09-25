# dbrdemo dev guide

Databricks starter/sample project. Tooling: `uv`, `ruff`, `pyright`, Unity Gateway CLI (`ug`), and Agent Skills.

## Quick setup

```bash
# Install the Databricks VS Code extension 2.17+, authenticate with a clear
# profile name, then select serverless or classic compute in the extension.
direnv allow # loads .databricks/.databricks.env automatically

make dev                 # uv + Python 3.12 + DBR 17 environment
```

Use `make dev` (currently `dev17`). Connect must be equal to or older than the
runtime, so Connect 17 supports DBR 17-19.

## Everyday commands

```bash
make fmt      # ruff auto-fix + format (quote style preserved)
make lint     # ruff check + ruff format --check + pyright
make flint    # fmt then lint
make test     # pytest + coverage (needs a Databricks connection)
make dist     # build the wheel
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

Genie Code uses the bundled Agent Skills directly in Databricks. For compatible
external coding agents, `ug` routes Claude Code, Codex, Gemini, OpenCode,
Copilot, Pi, and Cursor through Databricks Unity Gateway. It is installed into
`.uvtools` (isolated from `.venv`).
Docs: https://docs.databricks.com/aws/en/ai-gateway/coding-agent-ug-cli

```bash
make ug                  # install the ug CLI (runs `make direnv` first)
direnv allow             # once, so .uvtools/bin is on PATH

# Install an agent CLI, then launch it through ug:
make install_claudecode  && ug claude
make install_codex       && ug codex
make install_cursorcli   && ug cursor
# also: install_gemini, install_opencode, install_copilot, install_pi
```

Do not use the old `ucode` command; `ug` replaces it.

## Skills

Skills are `dbrdemo-*` folders under `skills/`. `make dist` copies them into
the wheel.

- `make install_workspace_skill`: preferred enterprise installation for all
  Genie Code users.
- `make install_user_skill`: testing/troubleshooting only. User skills have
  lower priority and cannot override same-name workspace skills.
- `make install_skills`: compatible local coding agents.

Each target removes existing `dbrdemo-*` skill folders in the target first, then
copies the bundled ones. Other folders are left untouched.

## Renaming for your own project

See [RENAME.md](RENAME.md).
