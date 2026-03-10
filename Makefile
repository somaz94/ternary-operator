.PHONY: test test-local clean help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

test: test-local ## Run all tests (alias for test-local)

test-local: ## Run local integration tests
	python3 tests/test_local.py

test-bash: ## Run bash test suite
	bash tests/test_local.sh

clean: ## Remove cache and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
