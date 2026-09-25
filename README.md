# dbrdemo

A small reference for developing a Python library locally with
[Databricks Connect](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/python/)
and deploying it as a wheel on Databricks. The wheel includes matching
documentation and [Genie Code Agent Skills](https://docs.databricks.com/aws/en/genie-code/skills).

## Quick start

1. In the Databricks VS Code extension 2.17 or newer, authenticate and select
   serverless or classic compute.
2. Install the repository shell integration:

   ```bash
   make direnv
   ```

3. Open a new terminal, then prepare and check the project:

   ```bash
   direnv allow
   make dev
   make flint
   ```

See [Developer setup](docs/developer/getting-started.md) for connection details.
Windows users should use [WSL2](https://learn.microsoft.com/windows/wsl/install).

## Example

```python
from dbrdemo import write_foobar

write_foobar("catalog.schema.foobar", "hello", "world")
```

See the [foo/bar guide](docs/user/foobar.md) for the Python and CLI APIs.

## Documentation

- [User](docs/user/README.md): use the library, CLI, and example notebook
- [Admin](docs/admin/README.md): install skills and configure Azure DevOps
- [Developer](docs/developer/README.md): set up, test, package, and extend the project

Run `dbrdemo-docs` to read the same documentation from an installed wheel.

## Use this starter

Follow [RENAME.md](RENAME.md) to rename the package, commands, and Agent Skill.
