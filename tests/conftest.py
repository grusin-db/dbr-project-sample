"""Configure shared Databricks test fixtures."""

import pytest
from databricks.sdk import WorkspaceClient


@pytest.fixture
def ws() -> WorkspaceClient:
    """Create a workspace client from the configured Databricks profile.

    Returns:
        An authenticated workspace client.
    """
    return WorkspaceClient()
