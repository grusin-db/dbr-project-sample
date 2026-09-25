# Local VS Code notebook

Use [`dbrdemo-example.ipynb`](../../dbrdemo-example.ipynb) to call the library
from a local Jupyter kernel through Databricks Connect.

## Prerequisites

1. Install version 2.17 or newer of the
   [Databricks VS Code extension](https://marketplace.visualstudio.com/items?itemName=databricks.databricks).
2. Authenticate in the extension and select serverless or classic compute.
3. Run:

   ```bash
   direnv allow
   make dev
   ```

4. Open `dbrdemo-example.ipynb`.
5. Select `.venv/bin/python` as the notebook kernel.

## What the notebook demonstrates

1. Optionally enable formatted logging with `install_logger()`.
2. Import `spark` and `dbutils` from `dbrdemo`.
3. Use Spark SQL to show the current user and catalog.
4. List accessible secret scopes with `dbutils.secrets.listScopes()`.
5. Create a foo/bar DataFrame.
6. Append the row to a table and read it back.

The notebook uses standard Python and PySpark output methods, so it does not
depend on Databricks notebook globals such as `display()`.
