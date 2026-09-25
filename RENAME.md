# Rename this starter for your project

Clone, then do a find-replace. Everything below is intentionally simple string
substitution -- no cookiecutter, no templating engine.

## Strings to replace

| Replace | Where | Meaning |
|---------|-------|---------|
| `dbrdemo` | package dir `dbrdemo/`, imports, `pyproject.toml` `name`, `update_package_version.py`, Makefile lint paths | Python package + project name |
| `dbrdemo-foobar` | `pyproject.toml` scripts, `dbrdemo/cli.py` | sample app CLI command |
| `dbrdemo-install-skills`, `dbrdemo-install-user-skill`, `dbrdemo-install-workspace-skill` | `pyproject.toml` scripts | skill install CLIs |
| `dbrdemo-` | `SKILL_DIR_PREFIX` in `dbrdemo/skills.py` **and** the skill folder names under `dbrdemo/skills/` | skill folder prefix (the one knob) |
| author / email | `pyproject.toml` `[project].authors` | optional |

## Steps

1. Rename the package folder: `git mv dbrdemo yourpkg`.
2. Find-replace `dbrdemo` -> `yourpkg` across the repo.
3. Change `SKILL_DIR_PREFIX` in `yourpkg/skills.py` and rename the folders under
   `yourpkg/skills/` to match (`yourpkg-getting-started`, ...).
4. Update author/description in `pyproject.toml`.
5. `make dev && make flint && make test`.

## Notes

- No lockfile: pick one `make devN` (DBR 15-18) at a time.
- There is no `make dev19` yet -- `databricks-connect` 19.x is not on PyPI. Add
  `requirements/dev19.txt` + a `dev19` extra + `make dev19` once it ships.
- `tests/sdk_test.py` uses the `ws` and `make_volume` fixtures from
  databricks-labs-pytester. `make_volume` needs Unity Catalog access (and a
  warehouse for schema creation) in the connected workspace; the volume is
  auto-cleaned after the test.
