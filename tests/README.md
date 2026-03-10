# Tests

Local testing suite for the Ternary Operator Action.

<br/>

## Quick Start (Makefile)

```bash
cd /path/to/ternary-operator
make test          # Run all tests (alias for test-local)
make test-local    # Run Python integration tests
make test-bash     # Run bash test suite
make clean         # Remove cache and build artifacts
make help          # Show all available commands
```

<br/>

## Test Files

| File | Description |
|------|-------------|
| `test_local.py` | Python integration test suite (42 test cases, subprocess-based) |
| `test_local.sh` | Bash test suite (17 core tests, lightweight) |

<br/>

## Running Tests

```bash
# Python tests (recommended)
python3 tests/test_local.py

# Bash tests
bash tests/test_local.sh

# Or using Makefile
make test
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
