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

- 🔄 **Dynamic Evaluation**: Flexibly evaluate multiple conditions in a single step
- 🎯 **Conditional Logic**: Support for complex conditions with AND/OR operators
- 🔍 **Variable Substitution**: Automatically replaces environment variables in conditions
- 📤 **Multiple Outputs**: Support for up to 10 different condition evaluations
- 🚀 **Easy Integration**: Simple to integrate with env-output-setter
- 📝 **Detailed Logging**: Clear debug output for troubleshooting
- ⚡ **Performance Optimized**: Fast evaluation of multiple conditions

<br/>

## Inputs

| Input          | Description                                       | Required | Default | Example |
| -------------- | ------------------------------------------------- | -------- | ------- | ------- |
| `conditions`   | Comma-separated conditions to evaluate (max 10)    | Yes      | -       | `SERVICE == game, ENVIRONMENT == dev` |
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
            SERVICE == game || SERVICE == batch,
            ENVIRONMENT == dev,
            TEST == prod,
            ENV == xov,
            BRANCH == dev,
            SERVICE == game,
            ENVIRONMENT == qa,
            TEST == stage,
            ENV == dev,
            BRANCH == main
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
            SERVICE == game || SERVICE == batch,
            ENVIRONMENT == dev,
            TEST == prod,
            ENV == xov,
            BRANCH == dev,
            SERVICE == game,
            ENVIRONMENT == qa,
            TEST == stage,
            ENV == dev,
            BRANCH == main
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
   - Properly quote string values
   - Use environment variables consistently

3. **Error Handling**
   - Always check output values
   - Provide meaningful true/false values
   - Use descriptive variable names

<br/>

## Debug Mode

The action supports detailed debug logging that can be enabled by setting `debug_mode: true`. When enabled, it provides:

- 🔍 Detailed condition evaluation process
- 📝 Variable substitution information
- ⚠️ Warning messages for undefined variables
- 🔄 Step-by-step execution flow

Example with debug mode:

```yaml
- name: Evaluate Conditions with Debug
  uses: somaz94/ternary-operator@v1
  id: ternary
  with:
    conditions: 'SERVICE == game'
    true_values: 'service-true'
    false_values: 'service-false'
    debug_mode: true
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