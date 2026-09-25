# Foo/bar

`dbrdemo` creates a one-row
[Spark DataFrame](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html)
and can append that row to a
[Databricks table](https://docs.databricks.com/aws/en/tables/).

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
