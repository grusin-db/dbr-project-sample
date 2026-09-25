# dbrdemo

Reference implementation for a Python library that runs locally through
[Databricks Connect](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/python/)
and as an installed [Python wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
on Databricks.

It includes:

- [Python 3.12](https://docs.python.org/3.12/) environments and dependency
  installation with [`uv`](https://docs.astral.sh/uv/)
- [Ruff](https://docs.astral.sh/ruff/) formatting/linting and
  [Pyright](https://microsoft.github.io/pyright/) type checking
- Test examples for the
  [Databricks SDK for Python](https://databricks-sdk-py.readthedocs.io/en/latest/),
  [Databricks Connect](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/python/),
  and [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/);
  Databricks Connect supplies the PySpark client transitively
- [wheel-packaged documentation](docs/README.md) and
  [Genie Code Agent Skills](https://docs.databricks.com/aws/en/genie-code/skills)
- [Unity Gateway](https://docs.databricks.com/aws/en/ai-gateway/coding-agent-quickstart)
  support for [compatible coding agents](https://docs.databricks.com/aws/en/ai-gateway/coding-agent-supported-agents)
- a sample [Azure DevOps Pipeline](https://learn.microsoft.com/azure/devops/pipelines/?view=azure-devops)

## Quick start

1. Install version 2.17 or newer of the
   [Databricks VS Code extension](https://marketplace.visualstudio.com/items?itemName=databricks.databricks).
2. Authenticate with a clear profile name.
3. Select [serverless](https://docs.databricks.com/aws/en/compute/serverless/)
   or [classic compute](https://docs.databricks.com/aws/en/compute/configure).
4. Prepare the repository with [`direnv`](https://direnv.net/):

   ```bash
   make direnv    # install direnv and its shell hook
   ```

5. Open a new terminal, then run:

   ```bash
   direnv allow   # load the extension-generated Databricks environment
   make dev       # create the Python 3.12 development environment
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

See the [foo/bar user guide](docs/user/foobar.md) for the
[DataFrame API](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html)
and table behavior. The
[local VS Code notebook guide](docs/user/local-notebook.md) explains how to run
[`dbrdemo-example.ipynb`](dbrdemo-example.ipynb) through Databricks Connect.

## Documentation

- [User documentation](docs/user/README.md): library and CLI usage
- [Admin documentation](docs/admin/README.md): skill installation and Azure DevOps
- [Developer documentation](docs/developer/README.md): setup, testing, packaging, and coding agents

Docs and skills ship in the wheel, so users and agents get guidance matching
the installed code.

Display bundled documentation from Python:

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

## Ideas for production projects

Keep this reference small, then add controls your project needs:

- Commit [`uv.lock`](https://docs.astral.sh/uv/concepts/projects/layout/#the-lockfile)
  when deployments require fully reproducible dependency resolution.
- Add [Radon](https://radon.readthedocs.io/) or
  [Xenon](https://xenon.readthedocs.io/) complexity limits.
- Run formatting and checks automatically with
  [pre-commit](https://pre-commit.com/).
- Scan dependencies with [pip-audit](https://github.com/pypa/pip-audit) and
  Python code with [Bandit](https://bandit.readthedocs.io/).
- Automate dependency updates with
  [Dependabot](https://docs.github.com/code-security/dependabot) or
  [Renovate](https://docs.renovatebot.com/).
- Enforce a minimum test coverage percentage in CI.
- Publish versioned wheels to an internal artifact repository or Unity Catalog
  volume.

## Use this starter

Follow [RENAME.md](RENAME.md) to rename the package, CLI commands, and Agent
Skills for your project.
