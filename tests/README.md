# Tests

Local testing suite for the Ternary Operator Action.

<br/>

## Quick Start (Makefile)

```bash
cd /path/to/ternary-operator
make test          # Run unit tests with pytest (73 tests with coverage)
make test-local    # Run Python integration tests (42 test cases)
make test-bash     # Run bash test suite (17 tests)
make test-all      # Run all tests
make coverage      # Coverage report
make clean         # Remove cache and build artifacts
make help          # Show all available commands
```

<br/>

## Test Files

| File | Type | Description |
|------|------|-------------|
| `conftest.py` | Unit | pytest fixtures (clean_env, github_output, default_env) |
| `test_evaluator.py` | Unit | TernaryOperator class tests (36 tests) |
| `test_operators.py` | Unit | IN, CONTAINS, EMPTY operator tests (22 tests) |
| `test_parser.py` | Unit | ConditionParser tests (13 tests) |
| `test_colors.py` | Unit | Color code tests (2 tests) |
| `test_local.py` | Integration | End-to-end subprocess tests (42 test cases) |
| `test_local.sh` | Integration | Bash test suite (17 core tests) |

<br/>

## Running Tests

```bash
# Unit tests with pytest (recommended)
python3 -m pytest tests/ -v --ignore=tests/test_local.py

# Integration tests
python3 tests/test_local.py

# Bash tests
bash tests/test_local.sh

# All tests via Makefile
make test-all
```

<br/>

## Test Categories

<br/>

### Comparison Operators
- `==`, `!=`, `<`, `>`, `<=`, `>=`
- Numeric comparison support (`COUNT > 5`, `VERSION <= 10`)

<br/>

### Logical Operators
- `&&` (AND) - both true, one false
- `||` (OR) - first true, second true, both false

<br/>

### Special Operators
- `IN` - match found, no match, multiple values, case sensitive
- `CONTAINS` - substring found, no match, case sensitive, exact match
- `NOT` - negate true/false, with IN, with AND
- `EMPTY` - empty string, not set, has value
- `NOT_EMPTY` - has value, empty string, not set

<br/>

### Combined Operators
- CONTAINS with AND
- NOT_EMPTY with OR
- NOT with CONTAINS
- IN with AND/OR
- Complex mixed expressions

<br/>

### Multiple Conditions
- All true (3 conditions)
- Mixed results (3 conditions)
- Maximum 10 conditions

<br/>

### Error Cases
- Exceed maximum conditions (11)
- Mismatched array lengths

<br/>

## Adding Custom Tests

### Python Tests

Edit `test_local.py` and add to the `create_test_suite()` function:

```python
tests.append(TestCase(
    name="My custom test",
    conditions="MY_VAR == expected_value",
    true_values="success",
    false_values="failure",
    expected_outputs={"output_1": "success"},
    env_vars={"MY_VAR": "expected_value"}
))
```

### Bash Tests

Edit `test_local.sh` and add a new test call:

```bash
run_test "My custom test" \
    "MY_VAR == expected_value" \
    "success" \
    "failure" \
    "success" \
    "export MY_VAR=expected_value"
```

<br/>

## Continuous Integration

The same conditions are tested in GitHub Actions CI:
- `.github/workflows/ci.yml` - Main CI workflow (local tests + Docker integration tests)
- `.github/workflows/use-action.yml` - Smoke test with released action
