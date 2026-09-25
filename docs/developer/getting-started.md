# Developer setup

## Connect to Databricks

1. Install version 2.17 or newer of the
   [Databricks VS Code extension](https://marketplace.visualstudio.com/items?itemName=databricks.databricks).
2. Authenticate and choose a clear profile name.
3. Select serverless or classic compute.

The extension writes the selected profile and compute to the gitignored
`.databricks/.databricks.env`.

## Prepare the repository

[`direnv`](https://direnv.net/) loads the extension-generated Databricks
environment and adds repo-local Unity Gateway tools to `PATH`.

```bash
make direnv    # install direnv and its shell hook
```

Open a new terminal, then run:

```bash
direnv allow   # approve .envrc
make dev       # create the Python 3.12 development environment
make flint     # format, lint, and type-check
```

## How the connection flows

1. The VS Code extension authenticates you and selects a workspace and compute.
2. The extension writes `.databricks/.databricks.env`.
3. Entering the repository triggers `.envrc`.
4. `.envrc` removes stale Databricks profile, token, and compute variables.
5. `dotenv_if_exists` exports the extension file as real environment variables.
6. Databricks Connect, the SDK, pytest, and Make targets inherit the same
   extension-selected connection.

Direnv scopes these changes to this repository. When you leave the directory,
it restores the parent shell environment.

## Variables loaded from the extension

The exact set depends on the selected compute. Common variables are:

- `DATABRICKS_AUTH_TYPE`: extension authentication method, normally
  `metadata-service`.
- `DATABRICKS_HOST`: selected workspace URL.
- `DATABRICKS_METADATA_SERVICE_URL`: local extension endpoint that supplies
  short-lived credentials.
- `DATABRICKS_SERVERLESS_COMPUTE_ID`: selected serverless compute.
- `DATABRICKS_CLUSTER_ID`: selected classic compute, when applicable.
- `DATABRICKS_WORKSPACE_ID`: selected workspace identifier.
- `DATABRICKS_BUNDLE_TARGET` and `DATABRICKS_PROJECT_ROOT`: local project
  context used by Databricks tooling.
- `SPARK_CONNECT_USER_AGENT` and `SPARK_CONNECT_PROGRESS_BAR_ENABLED`:
  Databricks Connect client settings.

Do not edit `.databricks/.databricks.env`; reconnect or select compute in the
extension instead. The file and its local metadata-service URL are gitignored.

## Refresh the environment

Run `direnv allow` after changing `.envrc`. When the extension rewrites its env
file, open a new terminal or run:

```bash
direnv reload
```

Make targets use `.venv` directly; activation is not required.

## Development commands

`make dev` currently selects Connect 17. Use `make dev16`, `make dev17`, or
`make dev18` when testing against a specific runtime generation; each target
recreates `.venv`.

```bash
make fmt       # fix lint issues and format code
make lint      # check formatting, lint, and types
make flint     # run fmt, then lint
make test      # build, install, and test the wheel
```

[Ruff](https://docs.astral.sh/ruff/) and
[Pyright](https://microsoft.github.io/pyright/) configuration live in
`pyproject.toml`. See [Testing](testing.md) for test details.

In a source checkout, open `dbrdemo-example.ipynb` to run the library from a
local VS Code notebook through Databricks Connect.

Windows users should use [WSL2](https://learn.microsoft.com/windows/wsl/install).
