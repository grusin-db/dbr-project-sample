# Databricks Starter / Sample Project

A clone-and-go Databricks project with the good stuff wired up: `uv`, `ruff`,
`pyright`, per-runtime dependency sets, the Unity Gateway coding-agent CLI
(`ug`), and Agent Skills. Fork it, rename a few strings (see [RENAME.md](RENAME.md)),
and you have a well-structured project.

Uses [Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html)
for local execution against Databricks compute.

## First-time setup

1. Install version 2.17 or newer of the
   [Databricks VS Code extension](https://marketplace.visualstudio.com/items?itemName=databricks.databricks).
2. Authenticate through the extension. When prompted, choose a clear profile
   name for the workspace.
3. Select serverless or classic compute in the extension.
4. Build and verify the project:

```bash
direnv allow             # loads .databricks/.databricks.env automatically
make dev                 # uv venv + Python 3.12 + default DBR dependencies
make flint               # format + lint + type-check
make install_skills      # copy sample skills to ~/.agents/skills

# optional: coding agents through Unity Gateway
make ug
make install_cursorcli && ug cursor
```

The extension writes the selected profile and compute to the gitignored
`.databricks/.databricks.env`. The committed `.envrc` loads it automatically.

Choose a Databricks Runtime with `make dev15`, `dev16`, `dev17`, or `dev18`.
There is no lockfile -- pick **one** `make devN` at a time.

## Make targets

### Development

- `make dev` - build the default development environment
- `make dev15` / `dev16` / `dev17` / `dev18` - build for a specific DBR version
- `make fmt` - auto-format (ruff; quote style preserved)
- `make lint` - ruff check + `ruff format --check` + `pyright`
- `make flint` - `fmt` then `lint`
- `make test` - run unit tests with coverage

### Package

- `make dist` - build the wheel
- `make install` - install the package and its CLIs

### Agent Skills

- `make install_skills` - install locally
- `make install_user_skill` - install for the current Databricks user
- `make install_workspace_skill` - install for all workspace users

### Coding agents

- `make ug` - install the Unity Gateway CLI
- `make install_claudecode`, `make install_codex`, `make install_cursorcli`,
  `make install_gemini`, `make install_opencode`, `make install_copilot`, or
  `make install_pi` - install a coding agent for Unity Gateway

## CLI commands

- `dbrdemo-foobar` - sample app; e.g. `dbrdemo-foobar --foo test --bar 123`
- `dbrdemo-install-skills` / `dbrdemo-install-user-skill` / `dbrdemo-install-workspace-skill`

## Project structure

- `dbrdemo/` - the package (goes into the wheel on `make dist`)
  - `skills/dbrdemo-*/SKILL.md` - bundled Agent Skills
  - `skills.py` - minimal skill installer (`SKILL_DIR_PREFIX` is the rename knob)
- `tests/` - unit tests, three flavors:
  - `pytest` - plain pytest sanity checks
  - `sdk` - `WorkspaceClient` checks using the `ws` and `make_volume` fixtures
    from [databricks-labs-pytester](https://github.com/databrickslabs/pytester);
    `test_upload_file_to_volume` writes to a temporary UC volume that is cleaned up
  - `etl` - Spark ETL logic via Databricks Connect
- `Makefile.ug.mk` - portable Unity Gateway CLI + agent installs (copy into other repos)

Windows users: use WSL2.

## Coding agents (`ug`)

`ug` is the Unity Gateway CLI; it routes coding agents (Claude Code, Codex,
Gemini, OpenCode, Copilot, Pi, Cursor) through Databricks. It installs into
`.uvtools` (isolated from `.venv`). Launch with `ug claude`, `ug cursor`, etc.
The older `ucode` command is superseded by `ug`. See
[the ug docs](https://docs.databricks.com/aws/en/ai-gateway/coding-agent-ug-cli).

## Skills

Agent Skills give Genie Code and local coding agents project-specific
instructions that are not available from the source code alone. They are
optional for the application runtime, but keep agent answers consistent with
the project's workflow.

This project includes `dbrdemo-getting-started`. It teaches agents how to:

- configure Databricks authentication and compute
- select a DBR dependency set
- format, lint, test, and package the project
- install skills locally or in Databricks

Example Genie Code prompts:

- “How do I set up this project?”
- “Prepare this project for DBR 18.”
- “Format, lint, and type-check my changes.”
- “Build the wheel.”
- “Install this project’s skills for my Databricks user.”

Skills are stored as `dbrdemo-*` folders under `dbrdemo/skills/`. Replace the
sample guidance with your project-specific workflow after cloning.

| Target | Installs to |
|--------|-------------|
| `make install_skills` | `~/.agents/skills/` (local: Cursor, VS Code, Copilot CLI, ...) |
| `make install_user_skill` | Databricks `/Users/<you>/.assistant/skills` |
| `make install_workspace_skill` | Databricks `/Workspace/.assistant/skills` (all users) |

## Type checking

`pyright` runs in `make lint`. Configuration lives in `pyproject.toml` under
`[tool.pyright]`.

## Azure DevOps

`.pipelines/run-tests-pipeline-sample.yml` is a minimal pipeline that runs
`make dev` -> `make lint` -> `make test`. It requires:

1. A Service Connection with access to the Databricks workspace:
   ```yaml
   variables:
   - name: ConnectionName
     value: "Non-Prod Deployment SPN"
   ```
2. A variable group with the cluster ID and host:
   ```yaml
   env:
     DATABRICKS_CLUSTER_ID: $(databricksCluster)
     DATABRICKS_HOST: $(databricksHost)
   ```
