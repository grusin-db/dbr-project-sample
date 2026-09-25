# Testing

## Setup

```bash
make direnv    # install direnv and its shell hook
direnv allow   # load the extension-selected workspace and compute
make dev       # create the Python 3.12 development environment
make test      # build, install, and test the wheel
```

Environment flow: VS Code extension → `.databricks/.databricks.env` → `direnv`
→ Make → pytest. Databricks Connect and the SDK therefore use the workspace and
compute selected in the extension. See [Developer setup](getting-started.md).

## What `make test` does

1. Build and install the wheel with its dependencies.
2. Run all files in `tests/`.
3. Write `.junittest.xml`, `coverage/html/`, and `coverage/xml/xml.xml`.

Important options:

- `-n8`: [pytest-xdist](https://pytest-xdist.readthedocs.io/) runs eight workers.
- `--exitfirst -vv`: stop on failure and show every test.
- `--cov=dbrdemo`: [pytest-cov](https://pytest-cov.readthedocs.io/) reports
  coverage without enforcing a threshold.

## Databricks test libraries

- [Databricks Labs pytester](https://github.com/databrickslabs/pytester)
  provides reusable pytest helpers such as `make_random`.
- [Databricks Labs Blueprint](https://github.com/databrickslabs/blueprint)
  provides the formatted logger enabled by `tests/conftest.py`.

## Test design

- Local tests cover docs, CLIs, and skill installation.
- Connected tests cover Spark, the SDK, Unity Catalog tables, volumes, and files.
- `temporary_schema` creates a random schema per test and always removes it.
- Random names keep parallel xdist workers isolated.

The test identity needs permission to create schemas, tables, and volumes in
the current catalog.

## Debug one test

```bash
.venv/bin/pytest -n0 -vv tests/foobar_test.py::test_write_foobar
```
