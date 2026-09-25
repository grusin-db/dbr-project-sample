# Foo/bar

`dbrdemo` creates a one-row Spark DataFrame and can append that row to a
Databricks table.

## Create a DataFrame

```python
from dbrdemo import create_foobar

df = create_foobar("hello", "world")
display(df)
```

The result has two string columns: `foo` and `bar`.

## Write to a table

```python
from dbrdemo import write_foobar

write_foobar("main.demo.foobar", "hello", "world")
```

The catalog and schema must exist. The table is created if needed; subsequent
calls append rows.

The CLI calls the same `write_foobar` function:

```bash
dbrdemo-foobar --table main.demo.foobar --foo hello --bar world
```
