# Tenary Operator

[![GitHub Super-Linter](https://github.com/somaz94/ternary-operator/actions/workflows/linter.yml/badge.svg)](https://github.com/somaz94/ternary-operator)
![CI](https://github.com/somaz94/ternary-operator/actions/workflows/ci.yml/badge.svg)
[![License](https://img.shields.io/github/license/somaz94/ternary-operator)](https://github.com/somaz94/container-action)
![Latest Tag](https://img.shields.io/github/v/tag/somaz94/ternary-operator)
![Top Language](https://img.shields.io/github/languages/top/somaz94/ternary-operator?color=green&logo=terraform&logoColor=blue)

## Description

This GitHub Action evaluates a series of conditional expressions and sets output variables
based on the results. It's designed to facilitate dynamic workflows that need to respond
differently based on the conditions derived from the environment
or previous steps in a GitHub Actions workflow.

## Features

- **Dynamic Evaluation**: Flexibly evaluate conditions provided as inputs.
- **Customizable Outputs**: Outputs can be used later in the workflow for further steps.
- **Easy Integration**: Simple to integrate into existing workflows with minimal setup.

## Inputs

| Input            | Description                                                   | Required |
|------------------|---------------------------------------------------------------|----------|
| `conditions`     | Comma-separated conditions to evaluate.                       | Yes      |
| `true_values`    | Values to return if conditions evaluate to true.              | Yes      |
| `false_values`   | Values to return if conditions evaluate to false.             | Yes      |

## Outputs

| Output       | Description                                  |
|--------------|----------------------------------------------|
| `output_1`   | Result of evaluating the first condition.    |
| `output_2`   | Result of evaluating the second condition.   |
| `output_3`   | Result of evaluating the third condition.    |
| `output_4`   | Result of evaluating the fourth condition.   |
| `output_5`   | Result of evaluating the fifth condition.    |

## Usage

### Workflow Configuration

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
          conditions: 'SERVICE == game || SERVICE == batch, ENVIRONMENT == dev, TEST == prod, ENV == xov, BRANCH == dev'
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

## License

This project is licensed under the [MIT License](LICENSE) file for details.
