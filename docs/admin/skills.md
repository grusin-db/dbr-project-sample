# Install Agent Skills

The wheel contains the `dbrdemo-*`
[Genie Code Agent Skills](https://docs.databricks.com/aws/en/genie-code/skills).
Install the wheel on Databricks, then run the Python examples below from a
notebook.

## Entire workspace (recommended)

Install skills for all Genie Code users in the workspace:

```python
from dbrdemo.skills import install_workspace_skills

install_workspace_skills()
```

Files are uploaded to `/Workspace/.assistant/skills`. This is the preferred
enterprise deployment and requires permission to write to that directory.

## Current user (testing only)

Use a user-scoped installation only for testing or troubleshooting:

```python
from dbrdemo.skills import install_user_skills

install_user_skills()
```

Files are uploaded to `/Users/<you>/.assistant/skills`.

User skills have lower priority than workspace skills. A user skill cannot
override a workspace skill with the same name. Test before workspace
deployment, or use a different skill name when a workspace version exists.

Both functions use the notebook user's Databricks identity. Existing
`dbrdemo-*` skill folders are replaced; unrelated skills are not changed.

## Refresh and verify

Skills are cached for the current browser session. After installation:

1. Refresh the Databricks browser page.
2. Start a new Genie Code session.
3. Ask: `What skills do you see?`

Genie Code should list `dbrdemo-getting-started` among other databricks skills.

Then test the skill with:

> Can you use dbrdemo to create a foobar DataFrame with hello world foobar zoobar and
> save it to a foobar table?
