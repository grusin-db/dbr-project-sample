.EXPORT_ALL_VARIABLES:

DAILY_BUILD_NUMBER ?= 0
ENV ?= dev
VENV_DIR ?= .venv
VOLUME ?=

# Databricks Unity Gateway CLI (ug) + coding-agent installs.
# Targets: make direnv, make ug, make install_claudecode / install_codex / ...
include Makefile.ug.mk

.PHONY: dev dev15 dev16 dev17 dev18 prepare_resources _dev_install install uninstall \
	fmt lint flint dist release test clean \
	install_skills install_user_skills install_workspace_skills

# One Databricks Runtime at a time: the devN extras pin different
# databricks-connect versions.
prepare_resources:
	@rm -rf dbrdemo/resources/docs dbrdemo/resources/skills
	@mkdir -p dbrdemo/resources/docs dbrdemo/resources/skills
	@cp -R docs/. dbrdemo/resources/docs/
	@cp -R skills/. dbrdemo/resources/skills/

_dev_install: prepare_resources
	which uv || pip install --upgrade uv
	uv python pin 3.12
	uv venv --clear $(VENV_DIR)
	uv pip install '.[$(EXTRA)]'

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
	$(VENV_DIR)/bin/ruff check --fix dbrdemo tests update_package_version.py
	$(VENV_DIR)/bin/ruff format dbrdemo tests update_package_version.py

lint:
	$(VENV_DIR)/bin/ruff check dbrdemo tests update_package_version.py
	$(VENV_DIR)/bin/ruff format --check dbrdemo tests update_package_version.py
	$(VENV_DIR)/bin/pyright

flint: fmt lint

dist: prepare_resources
	@rm -rf dist build *.egg-info
	@uv build --wheel --quiet

release:
	$(VENV_DIR)/bin/python update_package_version.py --env "$(ENV)" --daily-build-no "$(DAILY_BUILD_NUMBER)"
	@$(MAKE) dist; status=$$?; \
		$(VENV_DIR)/bin/python update_package_version.py --restore; restore_status=$$?; \
		[ $$status -eq 0 ] || exit $$status; \
		exit $$restore_status
	@if [ -n "$(strip $(VOLUME))" ]; then \
		$(VENV_DIR)/bin/python -m dbrdemo.release --env "$(ENV)" --volume "$(VOLUME)"; \
	fi

test: install
	COVERAGE_FILE=.coverage $(VENV_DIR)/bin/pytest -n8 --exitfirst -vv --cov=dbrdemo --cov-report term-missing --cov-report html:coverage/html/ --cov-report xml:coverage/xml/xml.xml --junitxml=.junittest.xml tests/*
	- open coverage/html/index.html

# Skills: local agents (~/.agents/skills), current Databricks user, or workspace-wide.
install_skills: install
	$(VENV_DIR)/bin/dbrdemo-install-skills

install_user_skills: install
	$(VENV_DIR)/bin/dbrdemo-install-user-skills

install_workspace_skills: install
	$(VENV_DIR)/bin/dbrdemo-install-workspace-skills

clean: uninstall ug-clean
	rm -fr dist *.egg-info .pytest_cache build coverage .junittest*.xml coverage.xml .coverage*
	rm -rf __pycache__ dbrdemo/__pycache__ tests/__pycache__
	rm -rf dbrdemo/resources/docs dbrdemo/resources/skills
	python3 update_package_version.py --env prod
	rm -f .dist_version
	rm -rf $(VENV_DIR)
