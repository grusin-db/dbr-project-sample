---
name: dbrdemo-getting-started
description: >-
  Use the dbrdemo library to create foo/bar DataFrames and append rows to a
  Databricks table. Use when a user asks how to call dbrdemo from Python or
  its CLI.
---

# Use dbrdemo

Create a one-row DataFrame:

```python
from dbrdemo import create_foobar

df = create_foobar("hello", "world")
display(df)
```

Append a row to an existing catalog and schema:

```python
from dbrdemo import write_foobar

write_foobar("catalog.schema.foobar", "hello", "world")
```

The equivalent CLI is:

```bash
dbrdemo-foobar --table catalog.schema.foobar --foo hello --bar world
```

Run `dbrdemo-docs user/foobar.md` for the complete API guide.
