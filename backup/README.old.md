# Ternary Operator

<!-- [![GitHub Super-Linter](https://github.com/somaz94/ternary-operator/actions/workflows/linter.yml/badge.svg)](https://github.com/somaz94/ternary-operator) -->
![CI](https://github.com/somaz94/ternary-operator/actions/workflows/ci.yml/badge.svg)
[![License](https://img.shields.io/github/license/somaz94/ternary-operator)](https://github.com/somaz94/container-action)
![Latest Tag](https://img.shields.io/github/v/tag/somaz94/ternary-operator)
![Top Language](https://img.shields.io/github/languages/top/somaz94/ternary-operator?color=green&logo=shell&logoColor=b)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Ternary%20Operator-blue?logo=github)](https://github.com/marketplace/actions/ternary-operator-action)

<br/>

## Description

This GitHub Action evaluates a series of conditional expressions and sets output
variables based on the results. It's designed to facilitate dynamic workflows
that need to respond differently based on the conditions derived from the
environment or previous steps in a GitHub Actions workflow.

<br/>

## Features

- **Dynamic Evaluation**: Flexibly evaluate multiple conditions in a single step
- **Conditional Logic**: Support for complex conditions with AND/OR/IN operators
- **Variable Substitution**: Automatically replaces environment variables in conditions
- **Multiple Outputs**: Support for up to 10 different condition evaluations
- **Easy Integration**: Simple to integrate with env-output-setter
- **Detailed Logging**: Clear debug output for troubleshooting
- **Performance Optimized**: Fast evaluation of multiple conditions
- **IN Operator**: Simplify multiple OR conditions with IN operator

<br/>

## Inputs

| Input          | Description                                       | Required | Default | Example |
| -------------- | ------------------------------------------------- | -------- | ------- | ------- |
| `conditions`   | Comma-separated conditions to evaluate (max 10)    | Yes      | -       | `SERVICE IN game,batch, ENVIRONMENT == dev` |
| `true_values`  | Values to return if conditions are true           | Yes      | -       | `service-true,env-true` |
| `false_values` | Values to return if conditions are false          | Yes      | -       | `service-false,env-false` |
| `debug_mode`   | Enable detailed debug logging                     | No       | false   | `true` |

<br/>

## Outputs

| Output      | Description                                | Example Value |
| ----------- | ------------------------------------------ | ------------- |
| `output_1`  | Result of evaluating the first condition   | `service-true` |
| `output_2`  | Result of evaluating the second condition  | `env-false` |
| `output_3`  | Result of evaluating the third condition   | `test-true` |
| `output_4`  | Result of evaluating the fourth condition  | `env-true` |
| `output_5`  | Result of evaluating the fifth condition   | `branch-false` |
| `output_6`  | Result of evaluating the sixth condition   | `service-true-2` |
| `output_7`  | Result of evaluating the seventh condition | `env-false-2` |
| `output_8`  | Result of evaluating the eighth condition  | `test-true-2` |
| `output_9`  | Result of evaluating the ninth condition   | `env-true-2` |
| `output_10` | Result of evaluating the tenth condition   | `branch-false-2` |

<br/>

## Supported Operators

The action supports various operators for flexible condition evaluation:

<br/>

### Comparison Operators
- `==` - Equal to
- `!=` - Not equal to
- `<` - Less than
- `>` - Greater than
- `<=` - Less than or equal to
- `>=` - Greater than or equal to

<br/>

### Logical Operators
- `||` - OR (logical or)
- `&&` - AND (logical and)

<br/>

### Special Operators
- `IN` - Check if value is in a list

#### Examples:
```yaml
# Comparison
SERVICE == game
VERSION >= 1.5
ENVIRONMENT != prod

# Logical operators
SERVICE == game || SERVICE == batch
ENVIRONMENT == dev && BRANCH == main

# IN operator (simplified OR)
SERVICE IN game,batch,api,worker
ENVIRONMENT IN dev,qa,stage,prod
BRANCH IN main,develop,release
```

<br/>

## Usage

<br/>

### Basic Workflow Example

```yaml
name: Conditional Workflow
on:
  workflow_dispatch:
    inputs:
      service:
        description: 'Service name'
        required: true
        default: 'game'
        type: choice
        options:
          - game
          - batch
      environment:
        description: 'Environment'
        required: true
        default: 'qa'
        type: environment

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set Variables
        id: set_vars
        uses: somaz94/env-output-setter@v1
        with:
          env_key: 'SERVICE,ENVIRONMENT,TEST,ENV,BRANCH'
          env_value: "${{ github.event.inputs.service || 'game' }},${{ github.event.inputs.environment || 'qa' }},${{ github.event.inputs.test || 'prod' }},${{ github.event.inputs.env || 'xov' }},${{ github.event.inputs.branch || 'qa' }}"
          output_key: 'SERVICE,ENVIRONMENT,TEST,ENV,BRANCH'
          output_value: "${{ github.event.inputs.service || 'game' }},${{ github.event.inputs.environment || 'qa' }},${{ github.event.inputs.test || 'prod' }},${{ github.event.inputs.env || 'xov' }},${{ github.event.inputs.branch || 'qa' }}"

      - name: Evaluate Conditions
        uses: somaz94/ternary-operator@v1
        id: ternary
        with:
          conditions: >-
            SERVICE IN game,batch,api,
            ENVIRONMENT == dev,
            TEST == prod,
            ENV IN xov,dev,qa,
            BRANCH == dev,
            SERVICE == game,
            ENVIRONMENT == qa,
            TEST == stage,
            ENV == dev,
            BRANCH IN main,develop
          true_values: >-
            service-true,environment-true,test-true,env-true,branch-true,
            service-true-2,environment-true-2,test-true-2,env-true-2,branch-true-2
          false_values: >-
            service-false,environment-false,test-false,env-false,branch-false,
            service-false-2,environment-false-2,test-false-2,env-false-2,branch-false-2

      - name: Use Results
        run: |
          echo "First condition result: ${{ steps.ternary.outputs.output_1 }}"
          echo "Second condition result: ${{ steps.ternary.outputs.output_2 }}"
          echo "Third condition result: ${{ steps.ternary.outputs.output_3 }}"
          echo "Fourth condition result: ${{ steps.ternary.outputs.output_4 }}"
          echo "Fifth condition result: ${{ steps.ternary.outputs.output_5 }}"
          echo "Sixth condition result: ${{ steps.ternary.outputs.output_6 }}"
          echo "Seventh condition result: ${{ steps.ternary.outputs.output_7 }}"
          echo "Eighth condition result: ${{ steps.ternary.outputs.output_8 }}"
          echo "Ninth condition result: ${{ steps.ternary.outputs.output_9 }}"
          echo "Tenth condition result: ${{ steps.ternary.outputs.output_10 }}"
```

<br/>

### Advanced Example

```yaml
name: Advanced Conditional Workflow
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set Multiple Variables
        id: set_vars
        uses: somaz94/env-output-setter@v1
        with:
          env_key: 'SERVICE,ENVIRONMENT,TEST,ENV,BRANCH'
          env_value: "${{ github.event.inputs.service || 'game' }},${{ github.event.inputs.environment || 'qa' }},${{ github.event.inputs.test || 'prod' }},${{ github.event.inputs.env || 'xov' }},${{ github.event.inputs.branch || 'qa' }}"
          output_key: 'SERVICE,ENVIRONMENT,TEST,ENV,BRANCH'
          output_value: "${{ github.event.inputs.service || 'game' }},${{ github.event.inputs.environment || 'qa' }},${{ github.event.inputs.test || 'prod' }},${{ github.event.inputs.env || 'xov' }},${{ github.event.inputs.branch || 'qa' }}"

      - name: Evaluate Multiple Conditions
        uses: somaz94/ternary-operator@v1
        id: ternary
        with:
          conditions: >-
            SERVICE IN game,batch,api,
            ENVIRONMENT == dev,
            TEST == prod,
            ENV IN xov,dev,qa,
            BRANCH == dev,
            SERVICE == game,
            ENVIRONMENT == qa,
            TEST == stage,
            ENV == dev,
            BRANCH IN main,develop
          true_values: >-
            service-true,environment-true,test-true,env-true,branch-true,
            service-true-2,environment-true-2,test-true-2,env-true-2,branch-true-2
          false_values: >-
            service-false,environment-false,test-false,env-false,branch-false,
            service-false-2,environment-false-2,test-false-2,env-false-2,branch-false-2
```

<br/>

## Best Practices

1. **Variable Setting**
   - Use env-output-setter for consistent variable management
   - Group related variables together
   - Provide default values for all variables

2. **Condition Format**
   - Use clear, simple conditions
   - Use IN operator for multiple value checks instead of repeated OR
   - Properly quote string values
   - Use environment variables consistently

3. **Operator Selection**
   - Use `==` for single value comparison
   - Use `IN` for checking against multiple values
   - Use `||` only when combining different conditions
   - Example: `SERVICE IN game,batch` instead of `SERVICE == game || SERVICE == batch`

4. **Error Handling**
   - Always check output values
   - Provide meaningful true/false values
   - Use descriptive variable names

<br/>

## Debug Mode

The action supports detailed debug logging that can be enabled by setting `debug_mode: true`. When enabled, it provides:

- Detailed condition evaluation process
- Variable substitution information
- Warning messages for undefined variables
- Step-by-step execution flow

Example with debug mode:

```yaml
- name: Evaluate Conditions with Debug
  uses: somaz94/ternary-operator@v1
  id: ternary
  with:
    conditions: 'SERVICE IN game,batch,api'
    true_values: 'service-true'
    false_values: 'service-false'
    debug_mode: true
```

#### Debug Output Example:
```
• Debug: Variable SERVICE = game
• Debug: Checking if SERVICE='game' IN [game, batch, api]
• Debug: IN operator result: True
✅ Success: Condition 1 is TRUE
```

<br/>

## Local Testing

Before pushing your changes to GitHub, you can test the action locally using the provided test scripts in the `tests/` directory.

### Using Python Test Script (Recommended)

The Python test script provides comprehensive testing with detailed output:

```bash
# Run all tests
python3 tests/test_local.py

# Or run from tests directory
cd tests && python3 test_local.py

# Test results show:
# - Individual test results with pass/fail status
# - Expected vs actual output comparison
# - Test summary with total, passed, and failed counts
```

**Features:**
- 25+ comprehensive test cases
- Tests all operators (comparison, logical, IN, mixed)
- Tests edge cases and error conditions
- Color-coded output for easy reading
- Detailed failure messages

### Using Bash Test Script

For a lighter-weight option, use the bash script:

```bash
# Run all tests
./tests/test_local.sh

# Or run from tests directory
cd tests && ./test_local.sh

# Or make it executable first
chmod +x tests/test_local.sh
./tests/test_local.sh
```

**Features:**
- Fast execution
- Simple pass/fail output
- Tests core functionality
- Easy to customize

### Test Coverage

Both scripts test:
- ✅ Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- ✅ Logical operators: `&&`, `||`
- ✅ IN operator: `VAR IN val1,val2,val3`
- ✅ Mixed operators: `SERVICE IN game,batch && ENV == qa`
- ✅ Multiple conditions (up to 10)
- ✅ Numeric comparisons
- ✅ Error cases (max conditions, mismatched arrays)

### Example Test Output

```bash
$ python3 tests/test_local.py

🧪 Local Test Suite for Ternary Operator Action

==================================================
📋 Comparison Operators
==================================================

Testing: Equal operator (==)
✅ PASS: Equal operator (==)

Testing: Not equal operator (!=)
✅ PASS: Not equal operator (!=)

...

==================================================
📊 Test Summary
==================================================
Total Tests: 25
Passed: 25
Failed: 0

✅ All tests passed!
```

### Adding Custom Tests

You can easily add your own tests to `tests/test_local.py`:

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

<br/>

## Troubleshooting

<br/>

### Common Issues

1. **Variable Not Set Correctly**
   - Verify env-output-setter configuration
   - Check variable names and values
   - Ensure proper escaping of special characters

2. **Condition Not Evaluating as Expected**
   - Verify environment variables are set correctly
   - Check for proper spacing in conditions
   - Ensure proper quoting of string values

3. **Missing Outputs**
   - Verify the number of conditions matches true/false values
   - Check for syntax errors in conditions
   - Ensure all required inputs are provided

4. **Debug Mode Usage**
   - Enable debug_mode for detailed logging
   - Check variable substitution in conditions
   - Monitor the evaluation process
   - Verify environment variable values

<br/>

## License

This project is licensed under the [MIT License](LICENSE).

<br/>

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.