# Packaging

## Build the wheel

```bash
make dist
```

The target builds a
[Python wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
as follows:

1. Removes stale build metadata and generated resources.
2. Copies top-level `docs/` to `dbrdemo/resources/docs/`.
3. Copies top-level `skills/` to `dbrdemo/resources/skills/`.
4. Builds `dist/*.whl`.

Generated resources are gitignored. Source documentation and skills remain in
their top-level directories.

Packaging both resources with the code creates one versioned artifact. Users
and agents can read matching documentation, and admins can install matching
Genie Code skills, without access to the source repository.

## Release the wheel

Assume the base version is `0.1.0`, the date is `2026.09.25`, and the current
commit is `abc123`.

```bash
# Development build
make release ENV=dev DAILY_BUILD_NUMBER=42
# dist/dbrdemo-0.1.0.dev0+2026.09.25.42.abc123-py3-none-any.whl

# Test build
make release ENV=test DAILY_BUILD_NUMBER=42
# dist/dbrdemo-0.1.0b0+2026.09.25.42.abc123-py3-none-any.whl

# Acceptance build
make release ENV=acc DAILY_BUILD_NUMBER=42
# dist/dbrdemo-0.1.0rc0+2026.09.25.42.abc123-py3-none-any.whl

# Production build
make release ENV=prod
# dist/dbrdemo-0.1.0-py3-none-any.whl
```

`update_package_version.py` reads the base version from `dbrdemo/version.py`,
adds the environment suffix, updates that file, and writes the result to
`.dist_version`. The date and commit are detected automatically.

`make dist` only builds the current version. `make release` updates the version
first and then runs `make dist`.

## Publish to a volume

Pass either a Unity Catalog volume name or path:

```bash
make release ENV=prod VOLUME=main.packages.python
# uploads to /Volumes/main/packages/python/dbrdemo-0.1.0-py3-none-any.whl

make release ENV=acc DAILY_BUILD_NUMBER=42 VOLUME=/Volumes/main/packages/python
```

The upload uses the Databricks Files API and the current Databricks
authentication. Production uploads never overwrite an existing wheel. If the
version already exists, increment the base version in `dbrdemo/version.py`
before releasing again. Non-production uploads may replace the same build.

Install the uploaded wheel in a Databricks notebook with:

```python
%pip install /Volumes/main/packages/python/dbrdemo-0.1.0-py3-none-any.whl
```

## Install the wheel

```bash
make install
```

This rebuilds and installs `dist/*.whl`. The installed package exposes:

- `dbrdemo-foobar`
- `dbrdemo-docs`
- `dbrdemo-install-skills`
- `dbrdemo-install-user-skill`
- `dbrdemo-install-workspace-skill`

Run `dbrdemo-docs` to display `user/foobar.md`, or pass another bundled path:

```bash
dbrdemo-docs admin/skills.md
```
