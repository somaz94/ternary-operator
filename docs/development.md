# Development Guide

Guide for contributors and developers working on the Ternary Operator Action.

<br/>

## Table of Contents
- [Local Development Setup](#local-development-setup)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Release Process](#release-process)

---

## Local Development Setup

<br/>

### Prerequisites

- **Python 3.10+** (Python 3.14+ recommended)
- **Docker** (for building container image)
- **Git**

<br/>

### Clone the Repository

```bash
git clone https://github.com/somaz94/ternary-operator.git
cd ternary-operator
```

<br/>

### Environment Setup

For development, install dev dependencies:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Verify Python version
python3 --version
```

---

## Testing

<br/>

### Using Makefile (Recommended)

```bash
# Run unit tests with coverage (pytest, 73 tests)
make test

# Run integration tests (subprocess, 42 tests)
make test-local

# Run bash tests (17 tests)
make test-bash

# Run all tests
make test-all

# Coverage report
make coverage
```

<br/>

### Unit Tests (pytest)

```bash
# Run with coverage
python3 -m pytest tests/ -v \
  --cov=src \
  --cov-config=.coveragerc \
  --cov-report=term-missing \
  --ignore=tests/test_local.py
```

**Test files:**
- `tests/test_evaluator.py` - 36 tests (main evaluator class)
- `tests/test_operators.py` - 22 tests (IN, CONTAINS, EMPTY operators)
- `tests/test_parser.py` - 13 tests (condition parser)
- `tests/test_colors.py` - 2 tests (color codes)

<br/>

### Integration Tests

```bash
# Python test suite (42 end-to-end test cases)
python3 tests/test_local.py

# Bash test suite (17 core tests)
./tests/test_local.sh
```

<br/>

### Running from Any Directory

Both test scripts automatically detect the project root:

```bash
# From project root
python3 tests/test_local.py

# From tests directory
cd tests
python3 test_local.py

# From anywhere (if you add to PATH)
/path/to/ternary-operator/tests/test_local.py
```

<br/>

### Manual Testing

Test specific scenarios:

```bash
# Set up test environment
export SERVICE=game
export ENVIRONMENT=qa
export INPUT_CONDITIONS="SERVICE IN game,batch,api"
export INPUT_TRUE_VALUES="service-pass"
export INPUT_FALSE_VALUES="service-fail"
export INPUT_DEBUG_MODE="true"
export GITHUB_OUTPUT="/tmp/test_output"

# Run entrypoint
python3 entrypoint.py

# Check output
cat /tmp/test_output
```

<br/>

### Testing with Docker

Build and test the Docker image:

```bash
# Build image
docker build -t ternary-operator:test .

# Run container test
docker run --rm \
  -e SERVICE=game \
  -e INPUT_CONDITIONS="SERVICE == game" \
  -e INPUT_TRUE_VALUES="yes" \
  -e INPUT_FALSE_VALUES="no" \
  -e INPUT_DEBUG_MODE="true" \
  -e GITHUB_OUTPUT="/tmp/output" \
  ternary-operator:test
```

---

## Project Structure

<br/>

```
ternary-operator/
├── README.md                 # Main documentation (overview + quickstart)
├── LICENSE                   # MIT License
├── CLAUDE.md                 # Project conventions and guidelines
├── CODEOWNERS                # Repository code owners
├── CONTRIBUTORS.md           # Contributors list (auto-generated)
├── Makefile                  # Development commands
├── action.yml                # GitHub Action metadata
├── Dockerfile                # Container definition
├── entrypoint.py             # Main entry point
├── requirements-dev.txt      # Dev dependencies (pytest, pytest-cov)
├── .coveragerc               # Coverage configuration
├── cliff.toml                # git-cliff changelog configuration
│
├── src/                      # Source modules (modular architecture)
│   ├── __init__.py           # Package initialization
│   ├── colors.py             # Terminal output formatting
│   ├── operators.py          # Operator evaluation logic
│   ├── parser.py             # Condition parsing logic
│   └── evaluator.py          # Main orchestration class
│
├── docs/                     # Detailed documentation
│   ├── README.md             # Documentation index
│   ├── api.md                # Input/output reference
│   ├── operators.md          # Operator documentation
│   ├── usage.md              # Usage examples
│   ├── troubleshooting.md    # Problem solving guide
│   └── development.md        # This file
│
├── tests/                    # Test suite
│   ├── README.md             # Test documentation
│   ├── conftest.py           # pytest fixtures
│   ├── test_evaluator.py     # Unit tests - evaluator (36 tests)
│   ├── test_operators.py     # Unit tests - operators (22 tests)
│   ├── test_parser.py        # Unit tests - parser (13 tests)
│   ├── test_colors.py        # Unit tests - colors (2 tests)
│   ├── test_local.py         # Integration tests (42 test cases)
│   └── test_local.sh         # Bash integration tests (17 tests)
│
├── .github/
│   ├── release.yml           # PR label-based release notes
│   └── workflows/
│       ├── ci.yml            # CI/CD workflow
│       ├── release.yml       # Release creation workflow
│       ├── use-action.yml    # Smoke test workflow
│       ├── changelog-generator.yml
│       ├── contributors.yml
│       ├── gitlab-mirror.yml
│       └── issue-greeting.yml
│
└── backup/                   # Archived old files
```

<br/>

### Key Files

<br/>

#### `entrypoint.py`

Main entry point (now simplified to 19 lines):

```python
#!/usr/bin/env python3
from src.evaluator import TernaryOperator

def main() -> int:
    operator = TernaryOperator()
    return operator.run()
```

**Key Change:**
- Simplified to a thin wrapper that imports from `src/` modules
- All logic moved to modular structure

<br/>

#### `src/` Module Structure

**`src/evaluator.py`** - Main orchestration class:

```python
class TernaryOperator:
    - validate_inputs()          # Input validation
    - evaluate_conditions()      # Main evaluation loop
    - evaluate_condition()       # Single condition evaluation
    - _parse_comparison()        # Safe comparison parsing
    - _is_numeric()              # Numeric value detection
```

**`src/operators.py`** - Operator evaluation logic (176 lines):

```python
class OperatorEvaluator:         # Base evaluator
class InOperatorEvaluator:       # IN operator handler
class ContainsOperatorEvaluator: # CONTAINS operator handler
class EmptyOperatorEvaluator:    # EMPTY/NOT_EMPTY handler
```

**`src/parser.py`** - Condition parsing (129 lines):

```python
class ConditionParser:
    - parse()                    # Static method for parsing conditions
                                 # Handles IN operator commas, parentheses
```

**`src/colors.py`** - Terminal output formatting (15 lines):

```python
class Colors:
    # ANSI color codes for terminal output
```

**Key Features:**
- Modular architecture (separation of concerns)
- Condition parsing with IN operator support
- Variable substitution (environment variables)
- Operator support (==, !=, <, >, <=, >=, &&, ||, IN, CONTAINS, NOT, EMPTY, NOT_EMPTY)
- Numeric comparison support
- Debug output

<br/>

#### `action.yml`

GitHub Action definition:

```yaml
inputs:              # Action inputs
  conditions:        # Conditions to evaluate
  true_values:       # Values when true
  false_values:      # Values when false
  debug_mode:        # Enable debug output

outputs:             # Action outputs
  output_1..10:      # Result outputs

runs:                # Docker container config
  using: docker
  image: Dockerfile
```

<br/>

#### `Dockerfile`

Container definition:

```dockerfile
FROM python:3.14-slim         # Base image
COPY entrypoint.py /usr/src/  # Copy entry point
COPY src/ /usr/src/src/       # Copy source modules
ENTRYPOINT ["python", "/usr/src/entrypoint.py"]
```

---

## Contributing

<br/>

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Make your changes**
4. **Test locally**
   ```bash
   make test-all
   ```

5. **Commit your changes**
   ```bash
   git commit -am "Add new feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

7. **Create a Pull Request**

<br/>

### Coding Guidelines

<br/>

#### Python Style

Follow PEP 8 style guide:

```python
# Good
def evaluate_condition(self, condition: str) -> bool:
    """Evaluate a single condition."""
    pass

# Use type hints
def process_value(value: str) -> int:
    return int(value)

# Clear variable names
condition_result = self.evaluate_condition(cond)

# Docstrings for public methods
def public_method(self):
    """
    Brief description.
    
    Args:
        param: Description
    
    Returns:
        Description
    """
    pass
```

<br/>

#### Testing Requirements

All changes must include tests:

```bash
# Unit tests (pytest) - add to tests/test_evaluator.py, test_operators.py, etc.
# Integration tests - add to tests/test_local.py
make test-all
```

<br/>

#### Documentation

Update relevant documentation:

- `README.md` - If adding major features
- `docs/operators.md` - If adding/changing operators
- `docs/usage.md` - Add usage examples
- `docs/api.md` - If changing inputs/outputs

<br/>

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "feat: Add support for regex in IN operator"
git commit -m "fix: Handle empty string values in conditions"
git commit -m "docs: Update troubleshooting guide"
git commit -m "test: Add numeric comparison test cases"

# Avoid
git commit -m "Update code"
git commit -m "Fix bug"
git commit -m "Changes"
```

**Commit Type Prefixes:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

---

## Release Process

<br/>

### Version Numbers

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** (`1.x.x`) - Breaking changes
- **MINOR** (`x.1.x`) - New features (backward compatible)
- **PATCH** (`x.x.1`) - Bug fixes

<br/>

### Creating a Release

1. **Update version in code** (if applicable)

2. **Update CHANGELOG.md**
   ```markdown
   ## [1.2.0] - 2025-01-15
   
   ### Added
   - IN operator for simplified OR conditions
   - Numeric comparison support
   
   ### Fixed
   - Variable substitution for uppercase+number combinations
   
   ### Changed
   - Improved debug output formatting
   ```

3. **Commit changes**
   ```bash
   git commit -am "chore: Prepare v1.2.0 release"
   ```

4. **Create and push tag**
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

5. **Create GitHub Release**
   - Go to GitHub Releases
   - Click "Draft a new release"
   - Select tag `v1.2.0`
   - Title: `v1.2.0 - Feature Name`
   - Description: Copy from CHANGELOG.md
   - Publish release

6. **Update major version tag** (optional)
   ```bash
   # Update v1 tag to point to latest v1.x.x
   git tag -fa v1 -m "Update v1 to v1.2.0"
   git push origin v1 --force
   ```

<br/>

### Testing Before Release

1. **Run full test suite**
   ```bash
   make test-all
   ```

2. **Test in real workflow**
   - Create test workflow in `.github/workflows/test-release.yml`
   - Test with different scenarios
   - Verify all outputs

3. **Build and test Docker image**
   ```bash
   docker build -t ternary-operator:test .
   # Run various tests with container
   ```

---

## Development Workflow

<br/>

### Typical Development Cycle

```bash
# 1. Create branch
git checkout -b feature/new-operator

# 2. Make changes
vim entrypoint.py

# 3. Test locally
make test-all

# 4. Add tests if needed
vim tests/test_evaluator.py

# 5. Test again
make test-all

# 6. Update documentation
vim docs/operators.md

# 7. Commit
git add .
git commit -m "feat: Add new operator support"

# 8. Push and create PR
git push origin feature/new-operator
```

<br/>

### Debugging

<br/>

#### Debug entrypoint.py

```python
# Add debug prints
print(f"DEBUG: condition = {condition}")
print(f"DEBUG: processed = {processed}")

# Or use Python debugger
import pdb; pdb.set_trace()
```

<br/>

#### Test specific condition

```bash
# Create test script
cat > test_debug.sh << 'EOF'
export SERVICE=game
export INPUT_CONDITIONS="SERVICE IN game,batch"
export INPUT_TRUE_VALUES="yes"
export INPUT_FALSE_VALUES="no"
export INPUT_DEBUG_MODE="true"
export GITHUB_OUTPUT="/tmp/output"
python3 entrypoint.py
EOF

chmod +x test_debug.sh
./test_debug.sh
```

---

## Adding New Features

<br/>

### Example: Adding a New Operator

1. **Update `evaluate_condition()` method**
   ```python
   def evaluate_condition(self, condition: str) -> bool:
       # Add new operator check
       if ' CONTAINS ' in condition.upper():
           return self._evaluate_contains_operator(condition)
       # ... rest of code
   ```

2. **Implement operator method**
   ```python
   def _evaluate_contains_operator(self, condition: str) -> bool:
       """Evaluate CONTAINS operator."""
       # Implementation
       pass
   ```

3. **Add tests**
   ```python
   tests.append(TestCase(
       name="CONTAINS operator",
       conditions="MESSAGE CONTAINS error",
       true_values="has-error",
       false_values="no-error",
       expected_outputs={"output_1": "has-error"},
       env_vars={"MESSAGE": "This is an error message"}
   ))
   ```

4. **Update documentation**
   - Add to `docs/operators.md`
   - Add examples to `docs/usage.md`
   - Update README.md features list

5. **Test thoroughly**
   ```bash
   python3 tests/test_local.py
   ```

---

## Continuous Integration

<br/>

### GitHub Actions Workflows

<br/>

#### `ci.yml`

Runs on every push and PR:
- Tests all operators
- Tests error cases
- Validates outputs

<br/>

#### `use-action.yml`

Demonstrates usage:
- Real-world examples
- Output verification
- Integration testing

<br/>

### Running CI Locally

```bash
# Simulate CI environment
act push

# Or specific workflow
act -W .github/workflows/ci.yml
```

---

## Resources

<br/>

### Internal Documentation
- [API Reference](api.md)
- [Operators Reference](operators.md)
- [Usage Examples](usage.md)
- [Troubleshooting](troubleshooting.md)

<br/>

### External Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Python Documentation](https://docs.python.org/)

<br/>

### Tools
- [act](https://github.com/nektos/act) - Run GitHub Actions locally
- [actionlint](https://github.com/rhysd/actionlint) - Lint GitHub Actions workflows

---

## Questions?

<br/>

- **Issues:** [GitHub Issues](https://github.com/somaz94/ternary-operator/issues)
- **Discussions:** [GitHub Discussions](https://github.com/somaz94/ternary-operator/discussions)
- **Email:** Create an issue for private concerns

Thank you for contributing!
