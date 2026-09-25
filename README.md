# Databricks Python Starter

Use this repository to start a Python library that runs locally through
Databricks Connect and as an installed wheel on Databricks.

It includes:

- Python 3.12 dependency management with `uv` and `uv.lock`
- Ruff formatting/linting and Pyright type checking
- Databricks SDK, Spark, and Unity Catalog test examples
- wheel-packaged documentation and Genie Code Agent Skills
- Unity Gateway support for compatible coding agents
- a sample Azure DevOps pipeline

## Quick start

1. Install version 2.17 or newer of the
   [Databricks VS Code extension](https://marketplace.visualstudio.com/items?itemName=databricks.databricks).
2. Authenticate with a clear profile name.
3. Select serverless or classic compute.
4. Prepare the repository:

   ```bash
   make direnv    # install direnv and its shell hook
   ```

5. Open a new terminal, then run:

   ```bash
   direnv allow   # load the extension-generated Databricks environment
   make dev       # create the locked Python 3.12 environment
   make flint     # format, lint, and type-check
   ```

See [Developer setup](docs/developer/getting-started.md) for details. Windows
users should use [WSL2](https://learn.microsoft.com/windows/wsl/install).

## Example library

Append a foo/bar row to a Databricks table:

```python
from dbrdemo import write_foobar

write_foobar("main.demo.foobar", "hello", "world")
```

The CLI calls the same function:

```bash
dbrdemo-foobar --table main.demo.foobar --foo hello --bar world
```

See the [foo/bar user guide](docs/user/foobar.md) for the DataFrame API and
table behavior.

## Documentation

- [User documentation](docs/user/README.md): library and CLI usage
- [Admin documentation](docs/admin/README.md): skill installation and Azure DevOps
- [Developer documentation](docs/developer/README.md): setup, testing, packaging, and coding agents

Documentation is included in the wheel. Display it from Python:

```python
from dbrdemo.documentation import read_doc

print(read_doc("README.md"))
```

## Build and install

```bash
make dist      # package code, docs, and skills in dist/*.whl
make install   # build and install the wheel
make test      # install the wheel and run the test suite
```

See [Packaging](docs/developer/packaging.md) for the wheel layout and installed
commands.

## Agent Skills

The bundled skill teaches Genie Code how to use the example library. The
preferred enterprise deployment installs it for the entire workspace:

```python
from dbrdemo.skills import install_workspace_skill

install_workspace_skill()
```

User-scoped installation is only for testing and troubleshooting; user skills
have lower priority than workspace skills. See
[Install Agent Skills](docs/admin/skills.md). Compatible local coding agents
can use `make install_skills`.

## Use this starter

Follow [RENAME.md](RENAME.md) to rename the package, CLI commands, and Agent
Skills for your project.
