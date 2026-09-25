# Rename this starter for your project

Clone, then do a find-replace. Everything below is intentionally simple string
substitution -- no cookiecutter, no templating engine.

## Strings to replace

| Replace | Where | Meaning |
| ------- | ----- | ------- |
| `dbrdemo` | package dir, imports, `pyproject.toml`, Makefile, and tests | Python package + project name |
| `dbrdemo-foobar` | `pyproject.toml` scripts, `dbrdemo/cli.py` | sample app CLI command |
| `dbrdemo-docs` | `pyproject.toml` scripts | bundled documentation CLI command |
| `dbrdemo-install-skills`, `dbrdemo-install-user-skills`, `dbrdemo-install-workspace-skills` | `pyproject.toml` scripts | skill install CLIs |
| `dbrdemo-` | `SKILL_DIR_PREFIX` in `dbrdemo/skills.py` and folders under `skills/` | skill folder prefix |
| author / email | `pyproject.toml` `[project].authors` | optional |

## Steps

1. Rename the package folder: `git mv dbrdemo yourpkg`.
2. Find-replace `dbrdemo` -> `yourpkg` across the repo.
3. Change `SKILL_DIR_PREFIX` in `yourpkg/skills.py` and rename the folders under
   `skills/` to match (`yourpkg-getting-started`, ...).
4. Update author/description in `pyproject.toml`.
5. `make dev && make flint && make test`.

## Notes

- Point `make dev` at the oldest DBR version your project supports; that
  Databricks Connect version also works with newer runtimes.
- To support another DBR version, add its requirements file, optional dependency,
  and Make target.
- Integration tests create an isolated Unity Catalog schema through the selected
  Databricks Connect compute and remove it after each test.
