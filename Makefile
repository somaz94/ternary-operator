.PHONY: test test-unit test-local test-bash test-all coverage clean help

VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

venv: $(VENV)/bin/activate ## Create virtualenv and install dev dependencies

$(VENV)/bin/activate: requirements-dev.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt
	touch $(VENV)/bin/activate
	@echo ""
	@echo "Virtualenv created. To activate:"
	@echo "  source $(VENV)/bin/activate"

test: $(VENV)/bin/activate ## Run unit tests with coverage
	$(PYTEST) tests/ -v --cov=src --cov-config=.coveragerc --cov-report=term-missing --ignore=tests/test_local.py

test-local: ## Run local integration tests
	python3 tests/test_local.py

test-bash: ## Run bash test suite
	bash tests/test_local.sh

test-all: test test-local ## Run all tests (unit + local)

coverage: $(VENV)/bin/activate ## Generate HTML coverage report
	$(PYTEST) tests/ --cov=src --cov-config=.coveragerc --cov-report=term-missing --cov-report=html --ignore=tests/test_local.py
	@echo "Open htmlcov/index.html in your browser"

clean: ## Remove venv, cache, and build artifacts
	rm -rf $(VENV) .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
