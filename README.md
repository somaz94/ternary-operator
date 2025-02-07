# Ternary Operator

<!-- [![GitHub Super-Linter](https://github.com/somaz94/ternary-operator/actions/workflows/linter.yml/badge.svg)](https://github.com/somaz94/ternary-operator) -->
![CI](https://github.com/somaz94/ternary-operator/actions/workflows/ci.yml/badge.svg)
[![License](https://img.shields.io/github/license/somaz94/ternary-operator)](https://github.com/somaz94/container-action)
![Latest Tag](https://img.shields.io/github/v/tag/somaz94/ternary-operator)
![Top Language](https://img.shields.io/github/languages/top/somaz94/ternary-operator?color=green&logo=shell&logoColor=b)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Ternary%20Operator-blue?logo=github)](https://github.com/marketplace/actions/ternary-operator-action)

## Description

This GitHub Action evaluates a series of conditional expressions and sets output
variables based on the results. It's designed to facilitate dynamic workflows
that need to respond differently based on the conditions derived from the
environment or previous steps in a GitHub Actions workflow.

## Features

- 🔄 **Dynamic Evaluation**: Flexibly evaluate multiple conditions in a single step
- 🎯 **Conditional Logic**: Support for complex conditions with AND/OR operators
- 🔍 **Variable Substitution**: Automatically replaces environment variables in conditions
- 📤 **Multiple Outputs**: Support for up to 5 different condition evaluations
- 🚀 **Easy Integration**: Simple to integrate into existing workflows
- 📝 **Detailed Logging**: Clear debug output for troubleshooting
- ⚡ **Performance Optimized**: Fast evaluation of multiple conditions

## Inputs

| Input          | Description                                       | Required | Example |
| -------------- | ------------------------------------------------- | -------- | ------- |
| `conditions`   | Comma-separated conditions to evaluate            | Yes      | `SERVICE == game, ENVIRONMENT == dev` |
| `true_values`  | Values to return if conditions are true           | Yes      | `service-true,env-true` |
| `false_values` | Values to return if conditions are false          | Yes      | `service-false,env-false` |

## Outputs

| Output     | Description                                | Example Value |
| ---------- | ------------------------------------------ | ------------- |
| `output_1` | Result of evaluating the first condition   | `service-true` |
| `output_2` | Result of evaluating the second condition  | `env-false` |
| `output_3` | Result of evaluating the third condition   | `test-true` |
| `output_4` | Result of evaluating the fourth condition  | `env-true` |
| `output_5` | Result of evaluating the fifth condition   | `branch-false` |

## Example Use Cases

Add the following step to your GitHub Actions workflow to use this action:

```yaml
jobs:
  example_job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set Variable
        run: |
          # shellcheck disable=SC2086
          {
            echo "SERVICE=${{ github.event.inputs.service || 'game' }}"
            echo "ENVIRONMENT=${{ github.event.inputs.environment || 'qa' }}"
            echo "TEST=${{ github.event.inputs.test || 'prod' }}"
            echo "ENV=${{ github.event.inputs.env || 'xov' }}"
            echo "BRANCH=${{ github.event.inputs.branch || 'qa' }}"
          } >> $GITHUB_ENV # Grouping commands to address SC2129

      - name: Evaluate Conditions
        uses: somaz94/ternary-operator@v1
        id: ternary
        with:
          conditions:
            'SERVICE == game || SERVICE == batch, ENVIRONMENT == dev, TEST ==
            prod, ENV == xov, BRANCH == dev'
          true_values: 'service-true,environment-true,test-true,env-true,branch-true'
          false_values: 'service-false,environment-false,test-false,env-false,branch-false'

      - name: Print Output
        run: |
          echo "First condition result: ${{ steps.ternary.outputs.output_1 }}"
          echo "Second condition result: ${{ steps.ternary.outputs.output_2 }}"
          echo "Third condition result: ${{ steps.ternary.outputs.output_3 }}"
          echo "Fourth condition result: ${{ steps.ternary.outputs.output_4 }}"
          echo "Fifth condition result: ${{ steps.ternary.outputs.output_5 }}"
```

## Best Practices

1. **Condition Format**
   - Use clear, simple conditions
   - Properly quote string values
   - Use environment variables consistently

2. **Error Handling**
   - Always check output values
   - Provide meaningful true/false values
   - Use descriptive variable names

3. **Debugging**
   - Check action logs for evaluation details
   - Verify environment variable values
   - Test conditions independently

## Troubleshooting

### Common Issues

1. **Condition Not Evaluating as Expected**
   - Verify environment variables are set correctly
   - Check for proper spacing in conditions
   - Ensure proper quoting of string values

2. **Missing Outputs**
   - Verify the number of conditions matches true/false values
   - Check for syntax errors in conditions
   - Ensure all required inputs are provided

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.