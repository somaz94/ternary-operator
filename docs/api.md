# API Reference

Complete reference for all inputs and outputs of the Ternary Operator Action.

<br/>

## Table of Contents
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Limits and Constraints](#limits-and-constraints)
- [Environment Variables](#environment-variables)

---

## Inputs

<br/>

### `conditions`

**Required:** Yes  
**Type:** String  
**Format:** Comma-separated conditions

List of conditional expressions to evaluate. Each condition is evaluated independently and produces a corresponding output.

#### Example:
```yaml
conditions: >-
  SERVICE IN game,batch,api,
  ENVIRONMENT == dev,
  TEST == prod
```

#### Constraints:
- Maximum 10 conditions
- Each condition must be a valid expression
- Conditions are separated by commas
- Whitespace is automatically trimmed

#### Supported Formats:
```yaml
# Single line
conditions: 'SERVICE == game, ENVIRONMENT == prod'

# Multi-line with >-
conditions: >-
  SERVICE IN game,batch,
  ENVIRONMENT == dev

# Multi-line with |
conditions: |
  SERVICE == game,
  ENVIRONMENT == prod
```

---

### `true_values`

**Required:** Yes  
**Type:** String  
**Format:** Comma-separated values

Values to return when corresponding conditions evaluate to TRUE.

#### Example:
```yaml
true_values: 'service-true,environment-true,test-true'
```

#### Constraints:
- Must have same number of values as conditions
- Each value corresponds to a condition by position
- Values can be any string

#### Best Practices:
```yaml
# Descriptive values
true_values: 'deploy-production,use-config-a,enable-feature'

# Boolean-like values
true_values: 'true,yes,1'

# Action identifiers
true_values: 'deploy,build,test'
```

---

### `false_values`

**Required:** Yes  
**Type:** String  
**Format:** Comma-separated values

Values to return when corresponding conditions evaluate to FALSE.

#### Example:
```yaml
false_values: 'service-false,environment-false,test-false'
```

#### Constraints:
- Must have same number of values as conditions
- Each value corresponds to a condition by position
- Values can be any string

#### Best Practices:
```yaml
# Descriptive values
false_values: 'skip-deploy,use-config-b,disable-feature'

# Boolean-like values
false_values: 'false,no,0'

# Action identifiers
false_values: 'skip,skip,skip'
```

---

### `debug_mode`

**Required:** No  
**Type:** Boolean  
**Default:** `false`

Enable detailed debug logging for troubleshooting.

#### Example:
```yaml
debug_mode: true
```

#### When Enabled:
- Shows variable substitution details
- Displays condition evaluation steps
- Reports warnings for undefined variables
- Shows intermediate processing results

#### Debug Output Example:
```
• Debug: Starting validation
• Debug: Raw conditions string: 'SERVICE IN game,batch,api'
• Debug: Parsed 3 conditions:
  1. SERVICE IN game,batch,api
• Debug: Variable SERVICE = game
• Debug: Checking if SERVICE='game' IN [game, batch, api]
• Debug: IN operator result: True
✅ Success: Condition 1 is TRUE
```

#### Use Cases:
- Development and testing
- Troubleshooting condition evaluation
- Verifying environment variable values
- Understanding processing flow

---

## Outputs

The action generates outputs named `output_1` through `output_10`, corresponding to each evaluated condition.

<br/>

### Output Format

**Name Pattern:** `output_N` where N is 1-10  
**Type:** String  
**Value:** Either the corresponding `true_value` or `false_value`

<br/>

### Output Reference Table

| Output | Corresponds To | Value Source |
|--------|----------------|--------------|
| `output_1` | 1st condition | `true_values[0]` or `false_values[0]` |
| `output_2` | 2nd condition | `true_values[1]` or `false_values[1]` |
| `output_3` | 3rd condition | `true_values[2]` or `false_values[2]` |
| `output_4` | 4th condition | `true_values[3]` or `false_values[3]` |
| `output_5` | 5th condition | `true_values[4]` or `false_values[4]` |
| `output_6` | 6th condition | `true_values[5]` or `false_values[5]` |
| `output_7` | 7th condition | `true_values[6]` or `false_values[6]` |
| `output_8` | 8th condition | `true_values[7]` or `false_values[7]` |
| `output_9` | 9th condition | `true_values[8]` or `false_values[8]` |
| `output_10` | 10th condition | `true_values[9]` or `false_values[9]` |

<br/>

### Using Outputs

#### In Workflow Steps:
```yaml
- name: Evaluate
  uses: somaz94/ternary-operator@v1
  id: check
  with:
    conditions: 'SERVICE == game'
    true_values: 'deploy'
    false_values: 'skip'

- name: Use Output
  run: echo "Result: ${{ steps.check.outputs.output_1 }}"

- name: Conditional Step
  if: steps.check.outputs.output_1 == 'deploy'
  run: ./deploy.sh
```

<br/>

#### In Job Outputs:
```yaml
jobs:
  evaluate:
    runs-on: ubuntu-latest
    outputs:
      deploy_action: ${{ steps.check.outputs.output_1 }}
      config_type: ${{ steps.check.outputs.output_2 }}
    steps:
      - name: Check
        id: check
        uses: somaz94/ternary-operator@v1
        with:
          conditions: 'SERVICE == game, ENVIRONMENT == prod'
          true_values: 'deploy,prod-config'
          false_values: 'skip,dev-config'
  
  deploy:
    needs: evaluate
    if: needs.evaluate.outputs.deploy_action == 'deploy'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```

---

## Limits and Constraints

<br/>

### Maximum Conditions

**Limit:** 10 conditions per action call  
**Rationale:** Keeps outputs manageable and promotes clarity

#### Enforcement:
```
❌ Error: Maximum number of conditions (10) exceeded. Found 11 conditions
```

#### Workaround:
If you need more than 10 conditions, split them into multiple action calls:

```yaml
- name: First Batch
  uses: somaz94/ternary-operator@v1
  id: batch1
  with:
    conditions: # conditions 1-10

- name: Second Batch
  uses: somaz94/ternary-operator@v1
  id: batch2
  with:
    conditions: # conditions 11-20
```

<br/>

### Array Length Matching

All three arrays must have the same length:
- `conditions` count
- `true_values` count
- `false_values` count

#### Error Example:
```yaml
# ❌ This will fail
conditions: 'A == 1, B == 2'      # 2 conditions
true_values: 'yes'                 # 1 value
false_values: 'no,never'          # 2 values

# Error: Number of conditions (2), true values (1), and false values (2) must match
```

#### Correct:
```yaml
# ✅ This works
conditions: 'A == 1, B == 2'      # 2 conditions
true_values: 'yes,ok'             # 2 values
false_values: 'no,fail'           # 2 values
```

<br/>

### Variable Name Requirements

Environment variables used in conditions must:
- Start with an uppercase letter
- Contain only uppercase letters, numbers, and underscores
- Be set before the action runs

#### Valid:
```yaml
SERVICE       # ✅
ENVIRONMENT   # ✅
MY_VAR        # ✅
API_V2        # ✅
COUNT         # ✅
```

#### Invalid:
```yaml
service       # ❌ lowercase
my-var        # ❌ contains hyphen
2ND_VAR       # ❌ starts with number
```

---

## Environment Variables

The action reads environment variables set in the workflow.

<br/>

### Setting Environment Variables

#### Method 1: Workflow-level
```yaml
env:
  SERVICE: game
  ENVIRONMENT: prod

jobs:
  test:
    steps:
      - uses: somaz94/ternary-operator@v1
        with:
          conditions: 'SERVICE == game'
```

#### Method 2: Job-level
```yaml
jobs:
  test:
    env:
      SERVICE: game
      ENVIRONMENT: prod
    steps:
      - uses: somaz94/ternary-operator@v1
```

#### Method 3: Step-level
```yaml
steps:
  - name: Set Variable
    run: echo "SERVICE=game" >> $GITHUB_ENV
  
  - uses: somaz94/ternary-operator@v1
    env:
      ENVIRONMENT: prod
    with:
      conditions: 'SERVICE == game && ENVIRONMENT == prod'
```

#### Method 4: Using env-output-setter (Recommended)
```yaml
- name: Set Variables
  uses: somaz94/env-output-setter@v1
  with:
    env_key: 'SERVICE,ENVIRONMENT'
    env_value: 'game,prod'

- uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE == game'
```

<br/>

### Variable Substitution

The action automatically substitutes environment variables in conditions:

```yaml
# Before substitution
conditions: 'SERVICE == game && ENVIRONMENT == prod'

# After substitution (if SERVICE=game, ENVIRONMENT=qa)
conditions: '"game" == "game" && "qa" == "prod"'
```

<br/>

### Undefined Variables

If a variable is not set:
- The condition evaluates to FALSE
- A warning is shown in debug mode

```yaml
# SERVICE is not set
conditions: 'SERVICE == game'

# Debug output:
• Debug: Warning: Variable SERVICE is not set or empty
• Debug: Condition 1 is FALSE
```

---

## Complete Example

```yaml
name: Complete API Demo
on: [workflow_dispatch]

jobs:
  demo:
    runs-on: ubuntu-latest
    outputs:
      result1: ${{ steps.evaluate.outputs.output_1 }}
      result2: ${{ steps.evaluate.outputs.output_2 }}
      result3: ${{ steps.evaluate.outputs.output_3 }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set Environment Variables
        uses: somaz94/env-output-setter@v1
        with:
          env_key: 'SERVICE,ENVIRONMENT,VERSION'
          env_value: 'game,prod,1.5.0'
          output_key: 'SERVICE,ENVIRONMENT,VERSION'
          output_value: 'game,prod,1.5.0'
      
      - name: Evaluate Conditions
        id: evaluate
        uses: somaz94/ternary-operator@v1
        with:
          # Input 1: conditions (required)
          conditions: >-
            SERVICE IN game,batch,api,
            ENVIRONMENT == prod,
            VERSION >= 1.5
          
          # Input 2: true_values (required)
          true_values: >-
            valid-service,
            production-deploy,
            new-version
          
          # Input 3: false_values (required)
          false_values: >-
            invalid-service,
            non-prod-deploy,
            old-version
          
          # Input 4: debug_mode (optional)
          debug_mode: true
      
      # Output 1: output_1
      - name: Check Service
        run: echo "Service validation: ${{ steps.evaluate.outputs.output_1 }}"
      
      # Output 2: output_2
      - name: Check Environment
        run: echo "Environment check: ${{ steps.evaluate.outputs.output_2 }}"
      
      # Output 3: output_3
      - name: Check Version
        run: echo "Version check: ${{ steps.evaluate.outputs.output_3 }}"
      
      # Using outputs in conditionals
      - name: Deploy
        if: |
          steps.evaluate.outputs.output_1 == 'valid-service' &&
          steps.evaluate.outputs.output_2 == 'production-deploy' &&
          steps.evaluate.outputs.output_3 == 'new-version'
        run: echo "All checks passed, deploying..."
```

---

## See Also

- [Operators Reference](operators.md) - Detailed operator documentation
- [Usage Examples](usage.md) - Practical usage patterns
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
