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
make dev       # create the locked Python 3.12 environment
make flint     # format, lint, and type-check
```

Make targets use `.venv` directly; activation is not required.

Windows users should use [WSL2](https://learn.microsoft.com/windows/wsl/install).
