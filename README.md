# Ternary Operator Action

![CI](https://github.com/somaz94/ternary-operator/actions/workflows/ci.yml/badge.svg)
[![License](https://img.shields.io/github/license/somaz94/ternary-operator)](LICENSE)
![Latest Tag](https://img.shields.io/github/v/tag/somaz94/ternary-operator)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Ternary%20Operator-blue?logo=github)](https://github.com/marketplace/actions/ternary-operator-action)

A GitHub Action for evaluating conditional expressions and setting dynamic outputs based on the results. Perfect for creating flexible, condition-driven workflows.

<br/>

## Features

- **Multiple Conditions**: Evaluate up to 10 conditions in a single step
- **Rich Operators**: Support for comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`), logical (`&&`, `||`, `NOT`), special (`IN`), string (`CONTAINS`, `STARTS_WITH`, `ENDS_WITH`), regex (`MATCHES`), and validation (`EMPTY`, `NOT_EMPTY`) operators
- **Case Sensitivity Control**: Optional case-insensitive comparison mode
- **Default Values**: Fallback values when condition evaluation fails
- **JSON Result Output**: Combined JSON output for easy multi-condition access
- **Simple Syntax**: Clean, readable condition expressions
- **Debug Mode**: Detailed logging for troubleshooting
- **Zero Dependencies**: Lightweight Docker-based action
- **Fast Execution**: Efficient condition evaluation

<br/>

## Quick Start

```yaml
name: Conditional Deploy
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      
      # Set environment variables
      - name: Set Variables
        run: |
          echo "SERVICE=game" >> $GITHUB_ENV
          echo "ENVIRONMENT=prod" >> $GITHUB_ENV
      
      # Evaluate conditions
      - name: Check Deployment Rules
        id: check
        uses: somaz94/ternary-operator@v1
        with:
          conditions: 'SERVICE IN game,batch && ENVIRONMENT == prod'
          true_values: 'deploy-allowed'
          false_values: 'deploy-blocked'
      
      # Use the result
      - name: Deploy
        if: steps.check.outputs.output_1 == 'deploy-allowed'
        run: ./deploy.sh
```

<br/>

## Use Cases

- **Conditional Deployments**: Deploy based on service, environment, or branch
- **Dynamic Configuration**: Select configs based on multiple conditions
- **Feature Flags**: Enable/disable features conditionally
- **Multi-Environment CI/CD**: Different strategies per environment
- **Resource Scaling**: Adjust resources based on conditions

<br/>

## Documentation

<br/>

### Core Documentation
- **[API Reference](docs/api.md)** - Complete input/output specification
- **[Operators Guide](docs/operators.md)** - All supported operators with examples
- **[Usage Examples](docs/usage.md)** - Real-world patterns and scenarios
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[Development Guide](docs/development.md)** - Contributing and local testing

<br/>

### Operators at a Glance

| Category | Operators | Example |
|----------|-----------|---------|
| **Comparison** | `==` `!=` `<` `>` `<=` `>=` | `VERSION >= 1.5` |
| **Logical** | `&&` `\|\|` `NOT` | `SERVICE == game && ENV == prod` |
| **Special** | `IN` | `SERVICE IN game,batch,api` |
| **String** | `CONTAINS` `STARTS_WITH` `ENDS_WITH` | `BRANCH STARTS_WITH feature/` |
| **Regex** | `MATCHES` | `TAG MATCHES ^v[0-9]+\.[0-9]+$` |
| **Validation** | `EMPTY` `NOT_EMPTY` | `API_KEY NOT_EMPTY` |

[→ See detailed operator documentation](docs/operators.md)

<br/>

## Common Examples

<br/>

### Example 1: Simple Condition

```yaml
- uses: somaz94/ternary-operator@v1
  id: check
  with:
    conditions: 'ENVIRONMENT == prod'
    true_values: 'production-config'
    false_values: 'development-config'
```

<br/>

### Example 2: IN Operator (Simplified OR)

```yaml
- uses: somaz94/ternary-operator@v1
  id: check
  with:
    # Instead of: SERVICE == game || SERVICE == batch || SERVICE == api
    conditions: 'SERVICE IN game,batch,api'
    true_values: 'valid-service'
    false_values: 'invalid-service'
```

<br/>

### Example 3: Multiple Conditions

```yaml
- uses: somaz94/ternary-operator@v1
  id: checks
  with:
    conditions: >-
      SERVICE IN game,batch,api,
      ENVIRONMENT == prod,
      VERSION >= 1.5
    true_values: 'service-ok,prod-deploy,new-version'
    false_values: 'service-fail,no-deploy,old-version'

# Use outputs
- run: echo "Service: ${{ steps.checks.outputs.output_1 }}"
- run: echo "Environment: ${{ steps.checks.outputs.output_2 }}"
- run: echo "Version: ${{ steps.checks.outputs.output_3 }}"
```

<br/>

### Example 4: Complex Logic

```yaml
- uses: somaz94/ternary-operator@v1
  id: deploy
  with:
    conditions: 'SERVICE IN game,api && ENVIRONMENT == prod || BRANCH == hotfix'
    true_values: 'deploy'
    false_values: 'skip'
    debug_mode: true
```

[→ See more examples](docs/usage.md)

<br/>

## Local Testing

Test your changes before pushing to GitHub:

```bash
# Run unit tests with pytest (135 tests with coverage)
make test

# Run integration tests (42 test cases)
make test-local

# Run all tests
make test-all
```

Or without Makefile:

```bash
# Unit tests (pytest)
python3 -m pytest tests/ -v --ignore=tests/test_local.py

# Integration tests
python3 tests/test_local.py

# Bash tests
./tests/test_local.sh
```

#### Test Coverage:
- Unit tests: 135 tests (operators, parser, evaluator, colors)
- Integration tests: 42 test cases (end-to-end subprocess tests)
- Bash tests: 17 core tests

[→ See testing guide](docs/development.md#testing)

<br/>

## Inputs & Outputs

<br/>

### Inputs

| Input | Required | Description | Example |
|-------|----------|-------------|---------|
| `conditions` | Yes | Comma-separated conditions (max 10) | `SERVICE IN game,batch` |
| `true_values` | Yes | Values when conditions are true | `deploy,skip` |
| `false_values` | Yes | Values when conditions are false | `skip,deploy` |
| `default_values` | No | Fallback values on evaluation error | `fallback1,fallback2` |
| `case_sensitive` | No | Case-sensitive comparison (default: true) | `false` |
| `debug_mode` | No | Enable debug logging (default: false) | `true` |

<br/>

### Outputs

- `output_1` through `output_10` - Results of evaluated conditions
- `result` - JSON object containing all outputs (e.g. `{"output_1": "value1", "output_2": "value2"}`)

[→ See complete API reference](docs/api.md)

<br/>

## Tips & Best Practices

1. **Use IN operator** for multiple value checks:
   ```yaml
   # Good
   SERVICE IN game,batch,api
   
   # Avoid
   SERVICE == game || SERVICE == batch || SERVICE == api
   ```

2. **Keep conditions simple** for readability:
   ```yaml
   # Good - split into multiple conditions
   conditions: 'SERVICE == game, ENVIRONMENT == prod'
   
   # Harder to read
   conditions: 'SERVICE == game && ENV == prod && BRANCH == main && VERSION >= 1.0'
   ```

3. **Enable debug mode** when troubleshooting:
   ```yaml
   debug_mode: true  # Shows detailed evaluation process
   ```

4. **Test locally** before pushing:
   ```bash
   make test-all
   ```

[→ See more best practices](docs/usage.md)

<br/>

## Integration

Works great with:
- **[env-output-setter](https://github.com/somaz94/env-output-setter)** - Set environment variables and outputs
- **GitHub Environments** - Environment-specific deployments
- **Matrix Strategies** - Conditional logic per matrix combination

```yaml
# Example with env-output-setter
- name: Set Variables
  uses: somaz94/env-output-setter@v1
  with:
    env_key: 'SERVICE,ENVIRONMENT'
    env_value: 'game,prod'

- name: Evaluate
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE == game && ENVIRONMENT == prod'
```

[→ See integration examples](docs/usage.md#integration-examples)

<br/>

## Troubleshooting

#### Common Issues:

<details>
<summary>Condition not evaluating as expected?</summary>

1. Check variable is set: `echo "$VARIABLE" >> $GITHUB_ENV`
2. Enable debug mode: `debug_mode: true`
3. Check for case sensitivity: `game` ≠ `Game`
4. Verify operator syntax: [See operators guide](docs/operators.md)

</details>

<details>
<summary>Array length mismatch error?</summary>

Ensure same number of:
- Conditions
- True values
- False values

```yaml
# Correct - all have 2 items
conditions: 'A == 1, B == 2'
true_values: 'yes,ok'
false_values: 'no,fail'
```

</details>

<details>
<summary>Maximum conditions exceeded?</summary>

Split into multiple action calls or combine with IN operator:

```yaml
# Instead of 12 individual conditions
SERVICE == game, SERVICE == batch, ...

# Use IN operator
SERVICE IN game,batch,...
```

</details>

[→ See full troubleshooting guide](docs/troubleshooting.md)

<br/>

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test locally: `make test-all`
5. Commit: `git commit -am "feat: Add new feature"`
6. Push and create a Pull Request

[→ See development guide](docs/development.md)

<br/>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<br/>

## Support

- **Issues**: [GitHub Issues](https://github.com/somaz94/ternary-operator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/somaz94/ternary-operator/discussions)
- **Documentation**: [Full Documentation](docs/)

---

<div align="center">

**Made for better GitHub Actions workflows**

[Documentation](docs/) | [Examples](docs/usage.md) | [Contributing](docs/development.md)

</div>
