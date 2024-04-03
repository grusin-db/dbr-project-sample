.EXPORT_ALL_VARIABLES:

ENV_NAME ?= local
DAILY_BUILD_NUMBER ?= 0

dev:
	python -m venv .venv
	. .venv/bin/activate
	pip install --upgrade pip
	pip install '.[dev]'

install: dist
	pip install .

uninstall:
	pip uninstall -y dbrdemo

fmt:
	yapf -pri dbrdemo tests
	autoflake -ri dbrdemo tests
	isort dbrdemo tests

lint:
	pycodestyle dbrdemo
	autoflake --check-diff --quiet --recursive dbrdemo

test: local
	COVERAGE_FILE=.coverage pytest -n8 --exitfirst -vv --cov=dbrdemo --cov-report html:coverage/html/ --cov-report xml:coverage/xml/xml.xml --junitxml=.junittest.xml tests/*
	- open coverage/html/index.html

dist:
	python update_package_version.py --env $(ENV_NAME) --daily-build-no $(DAILY_BUILD_NUMBER)
	python setup.py bdist_wheel sdist

clean: uninstall
	rm -fr dist *.egg-info .pytest_cache build coverage .junittest*.xml coverage.xml .coverage* sphinx_docs/_build **/__pycache__
	python update_package_version.py --env prod


