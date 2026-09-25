.EXPORT_ALL_VARIABLES:

VENV_DIR ?= .venv

# Databricks Unity Gateway CLI (ug) + coding-agent installs.
# Targets: make direnv, make ug, make install_claudecode / install_codex / ...
include Makefile.ug.mk

.PHONY: dev dev15 dev16 dev17 dev18 _dev_install install uninstall \
	fmt lint flint dist test clean \
	install_skills install_user_skill install_workspace_skill

# One Databricks Runtime at a time: the devN extras pin different
# databricks-connect versions and are declared as conflicts in pyproject.toml.
_dev_install:
	which uv || pip install --upgrade uv
	uv python pin 3.12
	uv sync --locked --extra $(EXTRA)

dev: dev17
dev15: ; $(MAKE) _dev_install EXTRA=dev15
dev16: ; $(MAKE) _dev_install EXTRA=dev16
dev17: ; $(MAKE) _dev_install EXTRA=dev17
dev18: ; $(MAKE) _dev_install EXTRA=dev18

install: dist
	@uv pip install --quiet --reinstall dist/*.whl

uninstall:
	yes | uv pip uninstall dbrdemo || true

fmt:
	$(VENV_DIR)/bin/ruff check --fix dbrdemo tests
	$(VENV_DIR)/bin/ruff format dbrdemo tests

lint:
	$(VENV_DIR)/bin/ruff check dbrdemo tests
	$(VENV_DIR)/bin/ruff format --check dbrdemo tests
	$(VENV_DIR)/bin/pyright dbrdemo

flint: fmt lint

dist:
	@rm -rf dist build *.egg-info dbrdemo/resources/docs dbrdemo/resources/skills
	@mkdir -p dbrdemo/resources/docs dbrdemo/resources/skills
	@cp -R docs/. dbrdemo/resources/docs/
	@cp -R skills/. dbrdemo/resources/skills/
	@uv build --wheel --quiet

test: install
	COVERAGE_FILE=.coverage $(VENV_DIR)/bin/pytest -n8 --exitfirst -vv --cov=dbrdemo --cov-report html:coverage/html/ --cov-report xml:coverage/xml/xml.xml --junitxml=.junittest.xml tests/*
	- open coverage/html/index.html

# Skills: local agents (~/.agents/skills), current Databricks user, or workspace-wide.
install_skills: install
	$(VENV_DIR)/bin/dbrdemo-install-skills

install_user_skill: install
	$(VENV_DIR)/bin/dbrdemo-install-user-skill

install_workspace_skill: install
	$(VENV_DIR)/bin/dbrdemo-install-workspace-skill

clean: uninstall ug-clean
	rm -fr dist *.egg-info .pytest_cache build coverage .junittest*.xml coverage.xml .coverage* **/__pycache__
	rm -rf dbrdemo/resources/docs dbrdemo/resources/skills
