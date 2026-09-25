# Azure DevOps

The sample
[Azure DevOps Pipeline](https://learn.microsoft.com/azure/devops/pipelines/?view=azure-devops)
in `.pipelines/run-tests-pipeline-sample.yml` installs Python 3.12, restores
the development environment, runs quality checks, and executes tests.

## Required configuration

1. Create a secret-based Azure Resource Manager service connection backed by a
   Microsoft Entra service principal.
2. Add that service principal to the Databricks workspace and grant the
   permissions required by the tests.
3. Set the service connection name in the pipeline:

   ```yaml
   variables:
     - name: ConnectionName
       value: "Non-Prod Deployment SPN"
   ```

4. Create the `databricks-dev-params` variable group with `databricksHost`.

## Authentication flow

CI does not use `.databricks/.databricks.env` or `.envrc`.

1. `AzureCLI@2` authenticates through the service connection.
2. `addSpnToEnvironment` exposes the client ID, secret, and tenant ID.
3. The task stores them as `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, and
   `ARM_TENANT_ID` for later steps.
4. The test step adds `DATABRICKS_HOST` and sets
   `DATABRICKS_SERVERLESS_COMPUTE_ID=auto`.
5. [Databricks unified authentication](https://learn.microsoft.com/azure/databricks/dev-tools/auth/unified-auth)
   uses those variables for the SDK and Databricks Connect.

See [Microsoft Entra service principal authentication](https://learn.microsoft.com/azure/databricks/dev-tools/auth/azure-sp)
for the required Databricks workspace setup.

## Compute

Serverless is the default. The service principal needs serverless access and
the Unity Catalog permissions required by the tests.

To use classic compute instead, remove `DATABRICKS_SERVERLESS_COMPUTE_ID` and
set `DATABRICKS_CLUSTER_ID` to the cluster ID.
