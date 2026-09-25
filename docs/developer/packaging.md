# Packaging

## Build the wheel

```bash
make dist
```

The target prepares resources and builds a
[Python wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
as follows:

1. Removes stale build metadata and generated resources.
2. Copies top-level `docs/` to `dbrdemo/resources/docs/`.
3. Copies top-level `skills/` to `dbrdemo/resources/skills/`.
4. Builds `dist/*.whl`.

Generated resources are gitignored. Source documentation and skills remain in
their top-level directories. `make dev` runs the same resource preparation
before installing the development package.

Packaging both resources with the code creates one versioned artifact. Users
and agents can read matching documentation, and admins can install matching
Genie Code skills, without access to the source repository.

## Release the wheel

Assume the base version is `0.2.0`, the date is `2026.09.25`, and the current
commit is `abc123`. Wheel filenames normalize the date to `2026.9.25`.

```bash
# Development build
make release ENV=dev DAILY_BUILD_NUMBER=42
# dist/dbrdemo-0.2.0.dev0+2026.9.25.42.abc123-py3-none-any.whl

# Test build
make release ENV=test DAILY_BUILD_NUMBER=42
# dist/dbrdemo-0.2.0b0+2026.9.25.42.abc123-py3-none-any.whl

# Acceptance build
make release ENV=acc DAILY_BUILD_NUMBER=42
# dist/dbrdemo-0.2.0rc0+2026.9.25.42.abc123-py3-none-any.whl

# Production build
make release ENV=prod
# dist/dbrdemo-0.2.0-py3-none-any.whl
```

`update_package_version.py` reads the base version from `dbrdemo/version.py`,
adds the environment suffix, temporarily updates that module, and writes the
release version to `.dist_version`. `make release` builds the wheel, then
restores `dbrdemo/version.py` to its base version. The date and commit are
detected automatically.

`make dist` only builds the current version. `make release` updates the version
first and then runs `make dist`. `make clean` restores the base production
version and removes `.dist_version`, `.venv`, `.uvtools`, and build artifacts.

## Publish to a volume

Pass either a Unity Catalog volume name or path:

```bash
make release ENV=prod VOLUME=main.packages.python
# uploads to /Volumes/main/packages/python/dbrdemo-0.2.0-py3-none-any.whl

make release ENV=acc DAILY_BUILD_NUMBER=42 VOLUME=/Volumes/main/packages/python
```

The upload uses the Databricks Files API and the current Databricks
authentication. Only `dev` uploads may overwrite a published package. `test`,
`acc`, and `prod` packages are immutable after upload. Use a new build number
or base version for the next release.

Install the uploaded wheel in a Databricks notebook with:

```python
%pip install -q /Volumes/main/packages/python/dbrdemo-0.2.0-py3-none-any.whl
dbutils.library.restartPython()
```

## Install the wheel

```bash
make install
```

This rebuilds and installs `dist/*.whl`. The installed package exposes:

- `dbrdemo-foobar`
- `dbrdemo-docs`
- `dbrdemo-install-skills`
- `dbrdemo-install-user-skills`
- `dbrdemo-install-workspace-skills`

Run `dbrdemo-docs` to display the documentation index, or pass a bundled path:

```bash
dbrdemo-docs admin/skills.md
```
