# Local Testing Suite

This directory contains local testing scripts for the Ternary Operator Action.

## Test Files

### `test_local.py` (Recommended)
Comprehensive Python test suite with 25+ test cases.

**Features:**
- Tests all operators (comparison, logical, IN, mixed)
- Numeric comparison support
- Color-coded output
- Detailed failure messages
- Edge case and error testing

**Usage:**
```bash
# From root directory
python3 tests/test_local.py

# From tests directory
cd tests && python3 test_local.py
```

### `test_local.sh`
Lightweight bash test script with 17 core test cases.

**Features:**
- Fast execution
- Simple pass/fail output
- Easy to customize

**Usage:**
```bash
# From root directory
./tests/test_local.sh

# From tests directory
cd tests && ./test_local.sh

# Make executable if needed
chmod +x tests/test_local.sh
```

## Test Coverage

Both scripts test:
- ✅ **Comparison operators**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- ✅ **Logical operators**: `&&`, `||`
- ✅ **IN operator**: `VAR IN val1,val2,val3`
- ✅ **Mixed operators**: `SERVICE IN game,batch && ENV == qa`
- ✅ **Multiple conditions**: Up to 10 conditions
- ✅ **Numeric comparisons**: `COUNT > 5`, `VERSION <= 10`
- ✅ **Error cases**: Max conditions limit, mismatched arrays

## Running Tests Before Push

Always run tests before pushing changes to GitHub:

```bash
# Quick check with Python (recommended)
python3 tests/test_local.py

# Or with bash
./tests/test_local.sh
```

If all tests pass (✅ All tests passed!), you're ready to commit and push! 🚀

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

## Continuous Integration

The same conditions are tested in GitHub Actions CI:
- `.github/workflows/ci.yml` - Main CI workflow
- `.github/workflows/use-action.yml` - Action usage examples

Local tests help catch issues before they reach CI! 🛡️
