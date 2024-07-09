# Databricks VS Code Project Sample/Demo

Sample Databricks Project with unit tests and wheel file package.

Make sure you install [Databricks VS Code extension](https://marketplace.visualstudio.com/items?itemName=databricks.databricks) first, and connect to a cluster!

This project relies of [Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html) to estabilish connection with databricks clusters. For purspoe of this demo, this codebase assumes that you are running 14.3 LTS (latests as of now) databricks runtime.

CLI Features:

- `make dev` - builds development enviroment on local machine
- `make fmt` - auto formats your code
- `make lint` - verifies if code follows programming guidelines
- `make lint2` - runs `make lint` and also does static type code checking using `pyright`
- `make dist` - builds the wheel file, auto incrementing version
- `make test` - runs unit tests and display test coverage report in your browser
- `make install` - install the package and cli commands

CLI Commands:

- `dbrdemo-foobar` - run with `--help` to see what advanced features it has!

Project Structure:

- `dbdemos` is the package folder, all it's contents will be put into wheel file when `make dist` is ran
- `tests` is the folder where unit tests are placed, there are 3 types of tests:
  - `pytest` simple tests just showing that pytest is working fine
  - `sdk` simple tests showing that SDK's `WorspaceClient` is working fine
  - `etl` simple tests checking some spark elt logic, it verifies that db connect is working as expected
  
Windows users might want to use WSL2 and setup VSCode to use WS2 image of your favorite linux distribution.
