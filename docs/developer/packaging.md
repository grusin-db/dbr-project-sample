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
