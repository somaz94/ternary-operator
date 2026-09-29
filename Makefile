.PHONY: test test-unit test-local test-bash test-all coverage lint lint-fix format format-check ci check clean help

VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
PY_PATHS := src entrypoint.py tests

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

lint: $(VENV)/bin/activate ## Run Python linter (ruff)
	$(PYTHON) -m ruff check $(PY_PATHS)

lint-fix: $(VENV)/bin/activate ## Run Python linter with auto-fix
	$(PYTHON) -m ruff check --fix $(PY_PATHS)

format: $(VENV)/bin/activate ## Format Python code (ruff)
	$(PYTHON) -m ruff format $(PY_PATHS)

format-check: $(VENV)/bin/activate ## Check Python code formatting
	$(PYTHON) -m ruff format --check $(PY_PATHS)

ci: lint format-check test ## Run full CI pipeline (lint + format-check + test)

check: lint format-check ## Run code quality checks (lint + format-check)

clean: ## Remove venv, cache, and build artifacts
	rm -rf $(VENV) .pytest_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
