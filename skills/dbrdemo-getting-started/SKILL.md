---
name: dbrdemo-getting-started
description: >-
  Use the dbrdemo library to create foo/bar DataFrames and append rows to a
  Databricks table. Use when a user asks how to call dbrdemo from Python or
  its CLI.
---

# Use dbrdemo

Use this skill when Genie Code helps a user call `dbrdemo`. Compatible coding
agents can follow the same instructions.

## Create foo/bar data

```python
from dbrdemo import create_foobar

df = create_foobar("hello", "world")
display(df)
```

The result has one row and two string columns: `foo` and `bar`.

## Write to a table

```python
from dbrdemo import write_foobar

write_foobar("main.demo.foobar", "hello", "world")
```

This appends the row to the target table. The catalog and schema must exist.

The CLI calls the same `write_foobar` function:

```bash
dbrdemo-foobar --table main.demo.foobar --foo hello --bar world
```
