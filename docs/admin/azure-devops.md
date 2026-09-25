# Azure DevOps

`.pipelines/run-tests-pipeline-sample.yml` installs Python 3.12, restores the
locked development environment, runs quality checks, and executes the tests.

## Required configuration

1. Create an Azure service connection that can authenticate to Databricks.
2. Set its name in the pipeline:

   ```yaml
   variables:
     - name: ConnectionName
       value: "Non-Prod Deployment SPN"
   ```

3. Create the `databricks-dev-params` variable group with:
   - `databricksHost`
   - `databricksCluster`

The pipeline maps the service principal credentials and Databricks settings to
the environment expected by the SDK, Databricks Connect, and pytest.
