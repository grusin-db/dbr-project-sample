# Databricks VS Code Project Sample/Demo

Sample Databricks Project with unit tests and wheel file package.

Make sure you install [Databricks VS Code extension](https://marketplace.visualstudio.com/items?itemName=databricks.databricks) first, and connect to a cluster!

This project relies of [Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html) to establish connection with databricks clusters.

For purpose of this demo, this codebase assumes that you are running 14.3 LTS (latests as of now) Databricks Runtime. Python 3.10 or newer. Preferably make sure you VM matches setup of VM of [Databricks Runtime 14.3 LTS](https://docs.databricks.com/en/release-notes/runtime/14.3lts.html#system-environment)

## CLI Features (you should run them in order of listing for first time setup to setup everything):

- `make dev` - builds development environment on local machine
- `make fmt` - auto formats your code
- `make lint` - verifies if code follows programming guidelines, performs static type checking using `pyright`
- `make dist` - builds the wheel file, auto incrementing version
- `make test` - runs unit tests and display test coverage report in your browser
- `make install` - install the package and cli commands

## CLI Commands:

- `dbrdemo-foobar` - run with `--help` to see what advanced features it has!
  - for example `dbrdemo-foobar --foo test --bar 123` -- will establish spark session, and run some basic query

## Project Structure:

- `dbdemos` is the package folder, all it's contents will be put into wheel file when `make dist` is ran
- `tests` is the folder where unit tests are placed, there are 3 types of tests:
  - `pytest` simple tests just showing that pytest is working fine
  - `sdk` simple tests showing that SDK's `WorspaceClient` is working fine
  - `etl` simple tests checking some spark elt logic, it verifies that db connect is working as expected
  
Windows users might want to use WSL2 and setup VSCode to use WS2 image of your favorite linux distribution.

## Static Type checking:
Pyright is used to perform static type checking, in case codebase cannot be imediatelly fixed to pass all the checks, the files to ignore can be put into the `pyrightconfig.json`. Typical workflow for making existing codebase pass all tests involves putting all files in ignore list, and then one by one fixing the code and removing it from the ignore list to achive 100% type checking.


## Azure DevOps
This project provides a sample YML template `.pipelines/run-tests-pipeline-sample.yml` for an Azure DevOps pipeline that can be used to trigger the tests from an CICD interface.

This requires:

1. A Service Connection which is allowed access on the Databricks workspace (Contributor Role) where you want to run the tests.
```
variables:
- name: ConnectionName
  value: "Non-Prod Deployment SPN"
```
 2. A variable group containing the ClusterID & Databricks Host URL.
```
env:
	DATABRICKS_CLUSTER_ID: $(databricksCluster)
	DATABRICKS_HOST: $(databricksHost)
```
 We recommend using a variable group for management and referencing the variable names here, instead of hardcoding the cluster & host within the YML. 

### Functionality
The pipeline is kept minimalistic to allow for further customization.

It will fetch the required SPN credentials into a variable (which is required for Databricks-Connect), install the required package dependencies, run the test & publish the results.
