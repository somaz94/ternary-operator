# Operators Reference

Complete guide to all operators supported by the Ternary Operator Action.

<br/>

## Table of Contents
- [Comparison Operators](#comparison-operators)
- [Logical Operators](#logical-operators)
- [Special Operators](#special-operators)
- [String Operators](#string-operators)
- [Validation Operators](#validation-operators)
- [Operator Precedence](#operator-precedence)
- [Advanced Usage](#advanced-usage)

---

## Comparison Operators

<br/>

Comparison operators evaluate relationships between two values.

<br/>

### Equal To (`==`)

Checks if two values are equal.

**Syntax:**
```yaml
VARIABLE == value
```

**Examples:**
```yaml
SERVICE == game          # Check if SERVICE is "game"
ENVIRONMENT == prod      # Check if ENVIRONMENT is "prod"
VERSION == 1.5           # Check if VERSION is "1.5"
COUNT == 10              # Numeric comparison
```

**Use Cases:**
- Checking exact service names
- Validating environment values
- Matching specific versions

<br/>

---

### Not Equal To (`!=`)

Checks if two values are NOT equal.

**Syntax:**
```yaml
VARIABLE != value
```

**Examples:**
```yaml
SERVICE != batch         # Check if SERVICE is NOT "batch"
ENVIRONMENT != prod      # Ensure not in production
BRANCH != main           # Check if not on main branch
```

**Use Cases:**
- Excluding specific values
- Safety checks (e.g., not in production)
- Negative matching

<br/>

---

### Greater Than (`>`)

Checks if left value is greater than right value (numeric comparison).

**Syntax:**
```yaml
VARIABLE > number
```

**Examples:**
```yaml
VERSION > 1.0            # Version higher than 1.0
COUNT > 5                # Count exceeds 5
REPLICAS > 3             # More than 3 replicas
```

**Use Cases:**
- Version checks
- Threshold validation
- Capacity checks

<br/>

---

### Less Than (`<`)

Checks if left value is less than right value (numeric comparison).

**Syntax:**
```yaml
VARIABLE < number
```

**Examples:**
```yaml
VERSION < 2.0            # Version below 2.0
COUNT < 10               # Count under limit
PRIORITY < 5             # Low priority
```

**Use Cases:**
- Maximum value checks
- Resource limits
- Priority filtering

<br/>

---

### Greater Than or Equal (`>=`)

Checks if left value is greater than or equal to right value.

**Syntax:**
```yaml
VARIABLE >= number
```

**Examples:**
```yaml
VERSION >= 1.5           # Version 1.5 or higher
REPLICAS >= 3            # At least 3 replicas
MEMORY >= 4096           # Minimum 4GB memory
```

**Use Cases:**
- Minimum requirements
- Inclusive thresholds
- Capability checks

<br/>

---

### Less Than or Equal (`<=`)

Checks if left value is less than or equal to right value.

**Syntax:**
```yaml
VARIABLE <= number
```

**Examples:**
```yaml
VERSION <= 2.0           # Version 2.0 or lower
REPLICAS <= 10           # Maximum 10 replicas
MEMORY <= 8192           # Up to 8GB memory
```

**Use Cases:**
- Maximum limits
- Capacity constraints
- Range validation

---

## Logical Operators

<br/>

Logical operators combine multiple conditions.

<br/>

### OR Operator (`||`)

Returns true if ANY condition is true.

**Syntax:**
```yaml
condition1 || condition2
```

**Examples:**
```yaml
SERVICE == game || SERVICE == batch
ENVIRONMENT == dev || ENVIRONMENT == qa
BRANCH == main || BRANCH == develop || BRANCH == release
```

**Truth Table:**

| Condition 1 | Condition 2 | Result |
|-------------|-------------|--------|
| True        | True        | True   |
| True        | False       | True   |
| False       | True        | True   |
| False       | False       | False  |

**Use Cases:**
- Multiple valid options
- Fallback scenarios
- Alternative paths

**Tip:** Consider using the `IN` operator for cleaner syntax when checking multiple values of the same variable.

<br/>

---

### AND Operator (`&&`)

Returns true if ALL conditions are true.

**Syntax:**
```yaml
condition1 && condition2
```

**Examples:**
```yaml
SERVICE == game && ENVIRONMENT == prod
BRANCH == main && VERSION >= 1.0
SERVICE IN game,batch && ENVIRONMENT != prod
```

**Truth Table:**

| Condition 1 | Condition 2 | Result |
|-------------|-------------|--------|
| True        | True        | True   |
| True        | False       | False  |
| False       | True        | False  |
| False       | False       | False  |

**Use Cases:**
- Combined requirements
- Multi-factor checks
- Strict validation

---

## Special Operators

<br/>

### IN Operator

Checks if a value exists in a list of values. This is a cleaner alternative to multiple OR conditions.

**Syntax:**
```yaml
VARIABLE IN value1,value2,value3
```

**Examples:**
```yaml
# Instead of this (using OR):
SERVICE == game || SERVICE == batch || SERVICE == api

# Use this (using IN):
SERVICE IN game,batch,api

# More examples:
ENVIRONMENT IN dev,qa,stage,prod
BRANCH IN main,develop,release,hotfix
REGION IN us-east,us-west,eu-west
STATUS IN pending,running,completed
```

**Features:**
- Cleaner syntax
- Easier to maintain
- Better readability
- Works with any number of values

**Use Cases:**
- Service name validation
- Environment checks
- Branch filtering
- Status matching
- Region selection

**Important Notes:**
- Values are case-sensitive: `game` != `Game`
- Whitespace after commas is automatically trimmed
- Each value is treated as a string
- No quotes needed around values

---

## String Operators

<br/>

### STARTS_WITH Operator

Checks if a string starts with a given prefix.

**Syntax:**
```yaml
VARIABLE STARTS_WITH prefix
```

**Examples:**
```yaml
# Branch name patterns
BRANCH STARTS_WITH feature/     # feature/new-login → true
BRANCH STARTS_WITH hotfix/      # feature/login → false

# File paths
FILE_PATH STARTS_WITH src/      # src/main.py → true
TAG STARTS_WITH v               # v1.2.3 → true
```

**Features:**
- Prefix matching
- Works with case_sensitive option
- Clean alternative to regex for simple prefix checks

**Use Cases:**
- Branch name filtering by prefix
- File path validation
- Tag format checking

**Example Workflow:**
```yaml
- name: Check Branch Prefix
  uses: somaz94/ternary-operator@v1
  id: branch
  with:
    conditions: 'BRANCH STARTS_WITH feature/'
    true_values: 'feature-branch'
    false_values: 'other-branch'
  env:
    BRANCH: ${{ github.ref_name }}
```

<br/>

---

### ENDS_WITH Operator

Checks if a string ends with a given suffix.

**Syntax:**
```yaml
VARIABLE ENDS_WITH suffix
```

**Examples:**
```yaml
# File extension checks
FILE ENDS_WITH .yml             # config.yml → true
FILE ENDS_WITH .py              # main.py → true

# Tag patterns
TAG ENDS_WITH -rc               # v1.0.0-rc → true
BRANCH ENDS_WITH /main          # release/main → true
```

**Features:**
- Suffix matching
- Works with case_sensitive option
- Clean alternative to regex for simple suffix checks

**Use Cases:**
- File extension filtering
- Tag format validation
- Branch name suffix checks

<br/>

---

### CONTAINS Operator

Checks if a string contains a substring (case-sensitive by default, respects `case_sensitive` option).

**Syntax:**
```yaml
VARIABLE CONTAINS substring
```

**Examples:**
```yaml
# Check branch name patterns
BRANCH_NAME CONTAINS feature     # feature/new-login → true
BRANCH_NAME CONTAINS hotfix      # fix/bug-123 → false

# Commit message checks
COMMIT_MESSAGE CONTAINS [skip ci]
COMMIT_MESSAGE CONTAINS urgent

# Path matching
FILE_PATH CONTAINS /src/          # src/components/App.js → true
TAG_NAME CONTAINS -rc             # v1.2.0-rc1 → true
```

**Features:**
- Case-sensitive matching
- Works with any string values
- Simple substring detection
- No regex complexity

**Use Cases:**
- Branch name pattern matching
- Commit message filtering
- Path-based conditionals
- Tag filtering
- Label checking

**Important:**
- Case-sensitive by default (respects `case_sensitive` option)
- Exact substring match required
- Left side is checked for containing right side

**Example Workflow:**
```yaml
- name: Check Branch Type
  id: branch
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'BRANCH_NAME CONTAINS feature'
    true_values: 'feature-branch'
    false_values: 'other-branch'
  env:
    BRANCH_NAME: ${{ github.ref_name }}

- name: Feature Branch Actions
  if: steps.branch.outputs.output_1 == 'feature-branch'
  run: echo "Running feature branch tests"
```

<br/>

---

### MATCHES Operator

Checks if a string matches a regular expression pattern.

**Syntax:**
```yaml
VARIABLE MATCHES regex_pattern
```

**Examples:**
```yaml
# Semver tag validation
TAG MATCHES ^v[0-9]+\.[0-9]+\.[0-9]+$     # v1.2.3 → true, latest → false

# Branch naming conventions
BRANCH MATCHES ^(feature|hotfix|release)/  # feature/login → true

# Commit message format
COMMIT_MSG MATCHES ^(feat|fix|docs):       # feat: add login → true

# Version range
VERSION MATCHES ^1\.[5-9]                  # 1.5 → true, 1.3 → false
```

**Features:**
- Full Python regex support (`re.search`)
- Partial matching (no need for `^...$` unless you want full match)
- Works with `case_sensitive` option (adds `re.IGNORECASE` flag)
- Invalid regex patterns return false with debug warning

**Use Cases:**
- Semver tag validation
- Branch naming convention enforcement
- Commit message format checking
- Complex pattern matching beyond CONTAINS

**Example Workflow:**
```yaml
- name: Validate Tag Format
  uses: somaz94/ternary-operator@v1
  id: tag
  with:
    conditions: 'TAG MATCHES ^v[0-9]+\.[0-9]+\.[0-9]+$'
    true_values: 'valid-semver'
    false_values: 'invalid-tag'
  env:
    TAG: ${{ github.ref_name }}

- name: Release
  if: steps.tag.outputs.output_1 == 'valid-semver'
  run: ./release.sh
```

<br/>

---

### NOT Operator

Negates (inverts) a condition result.

**Syntax:**
```yaml
NOT (condition)
```

**Examples:**
```yaml
# Basic negation
NOT (SERVICE == prod)            # True if NOT prod
NOT (ENVIRONMENT IN dev,qa)      # True if NOT dev or qa

# With IN operator
NOT (SERVICE IN batch,api)       # True if service is neither batch nor api

# With comparison
NOT (VERSION >= 2.0)             # True if version < 2.0
NOT (COUNT > 10)                 # True if count <= 10

# With logical operators
NOT (SERVICE == game && ENV == prod)    # False only when both are true
NOT (BRANCH == main || BRANCH == develop) # False when either is true
```

**Features:**
- Inverts any condition result
- Works with all operators
- Simplifies negative logic
- Cleaner than complex alternatives

**Use Cases:**
- Excluding specific values
- Negative validation
- Safety checks
- Inverse conditions
- Exception handling

**Truth Table:**

| Original | NOT Result |
|----------|------------|
| True     | False      |
| False    | True       |

**Tip:** Parentheses are optional but recommended for clarity.

**Example Workflow:**
```yaml
- name: Non-Production Check
  id: env_check
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'NOT (ENVIRONMENT == prod)'
    true_values: 'safe-to-deploy'
    false_values: 'requires-approval'
  env:
    ENVIRONMENT: ${{ inputs.environment }}

- name: Auto Deploy
  if: steps.env_check.outputs.output_1 == 'safe-to-deploy'
  run: ./deploy.sh
```

---

## Validation Operators

<br/>

### EMPTY Operator

Checks if a variable is empty or not set.

**Syntax:**
```yaml
VARIABLE EMPTY
```

**Examples:**
```yaml
# Check if optional variable is empty
OPTIONAL_VAR EMPTY               # True if empty or not set
API_KEY EMPTY                    # True if API key not provided
CUSTOM_CONFIG EMPTY              # True if no custom config

# Common patterns
DOCKER_TAG EMPTY                 # Use default tag
SLACK_WEBHOOK EMPTY              # Skip notification
CUSTOM_DOMAIN EMPTY              # Use default domain
```

**Conditions for EMPTY = true:**
- Variable is not set at all
- Variable is set to empty string `""`
- Variable contains only whitespace

**Features:**
- Checks for missing values
- Detects empty strings
- Ignores whitespace-only values
- Simple validation

**Use Cases:**
- Optional parameter validation
- Default value logic
- Configuration checks
- Feature flag detection
- Input validation

**Example Workflow:**
```yaml
- name: Check API Key
  id: api_check
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'API_KEY EMPTY'
    true_values: 'use-default'
    false_values: 'use-provided'
  env:
    API_KEY: ${{ secrets.API_KEY }}

- name: Use Default API
  if: steps.api_check.outputs.output_1 == 'use-default'
  run: echo "API_KEY=default-key" >> $GITHUB_ENV
```

<br/>

---

### NOT_EMPTY Operator

Checks if a variable has a value (opposite of EMPTY).

**Syntax:**
```yaml
VARIABLE NOT_EMPTY
```

**Examples:**
```yaml
# Check if required variable exists
REQUIRED_VAR NOT_EMPTY           # True if has value
DATABASE_URL NOT_EMPTY           # True if configured
API_TOKEN NOT_EMPTY              # True if token provided

# Validation patterns
DOCKER_TAG NOT_EMPTY             # Ensure tag is specified
ENVIRONMENT NOT_EMPTY            # Require environment
SERVICE_NAME NOT_EMPTY           # Validate service name
```

**Conditions for NOT_EMPTY = true:**
- Variable is set AND has a non-empty value
- Variable contains any non-whitespace characters

**Features:**
- Validates required values
- Ensures configuration exists
- Prevents empty inputs
- Simple presence check

**Use Cases:**
- Required parameter validation
- Configuration verification
- Input validation
- Prerequisite checks
- Safety validation

**Example Workflow:**
```yaml
- name: Validate Required Variables
  id: validate
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'DATABASE_URL NOT_EMPTY, API_KEY NOT_EMPTY'
    true_values: 'valid,valid'
    false_values: 'missing,missing'
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    API_KEY: ${{ secrets.API_KEY }}

- name: Deploy Application
  if: |
    steps.validate.outputs.output_1 == 'valid' &&
    steps.validate.outputs.output_2 == 'valid'
  run: ./deploy.sh
```

**Tip:** Use `NOT_EMPTY` to ensure required variables are set before proceeding with critical operations.

---

## Operator Precedence

<br/>

When multiple operators are used together, they are evaluated in this order:

1. **NOT operator** (highest priority - evaluated first)
2. **Comparison operators** (`==`, `!=`, `<`, `>`, `<=`, `>=`)
3. **String operators** (`STARTS_WITH`, `ENDS_WITH`, `MATCHES`, `CONTAINS`)
4. **Validation operators** (`EMPTY`, `NOT_EMPTY`)
5. **Special operators** (`IN`)
6. **AND operator** (`&&`)
7. **OR operator** (`||`)

**Example:**
```yaml
NOT (SERVICE == game) && ENVIRONMENT == prod || BRANCH == main
```

This is evaluated as:
```
((NOT (SERVICE == game)) && ENVIRONMENT == prod) || BRANCH == main
```

**Best Practice:** Use clear, simple conditions to avoid confusion. If you need complex logic, break it into multiple condition evaluations.

---

## Advanced Usage

<br/>

### Combining Operators

Mix different operators for complex conditions:

```yaml
# CONTAINS with logical operators
BRANCH_NAME CONTAINS feature && ENVIRONMENT == qa
COMMIT_MESSAGE CONTAINS hotfix || BRANCH_NAME CONTAINS urgent

# NOT with other operators
NOT (SERVICE IN batch,api) && ENVIRONMENT == prod
NOT (VERSION >= 2.0) || ENVIRONMENT == dev

# EMPTY/NOT_EMPTY validation
API_KEY NOT_EMPTY && ENVIRONMENT == prod
OPTIONAL_CONFIG EMPTY || USE_DEFAULT == true

# IN operator with AND
SERVICE IN game,batch && ENVIRONMENT == prod

# IN operator with OR
SERVICE == api || BRANCH IN main,develop

# Complex combinations
SERVICE IN game,batch && ENVIRONMENT != prod || BRANCH == hotfix
BRANCH_NAME CONTAINS feature && VERSION >= 1.0 && ENV NOT_EMPTY

# Numeric comparisons with logical operators
VERSION >= 1.0 && VERSION < 2.0
COUNT > 5 && ENVIRONMENT == prod
```

<br/>

### Multiple Conditions Example

```yaml
- name: Complex Evaluation
  uses: somaz94/ternary-operator@v1
  with:
    conditions: >-
      SERVICE IN game,batch,api,
      BRANCH_NAME CONTAINS feature && ENV NOT_EMPTY,
      NOT (ENVIRONMENT == prod) || VERSION >= 2.0
    true_values: 'service-ok,feature-ready,safe-deploy'
    false_values: 'service-fail,not-ready,blocked'
```

<br/>

### Practical Patterns

**Pattern 1: Service and Environment Check**
```yaml
SERVICE IN game,batch && ENVIRONMENT IN prod,stage
```
→ Deploy only specific services in specific environments

**Pattern 2: Branch Pattern Matching**
```yaml
BRANCH_NAME CONTAINS feature || BRANCH_NAME CONTAINS hotfix
```
→ Run tests for feature and hotfix branches

**Pattern 3: Required Configuration Validation**
```yaml
DATABASE_URL NOT_EMPTY && API_KEY NOT_EMPTY
```
→ Ensure all required configs are set

**Pattern 4: Version Range**
```yaml
VERSION >= 1.0 && VERSION < 2.0
```
→ Check if version is in 1.x range

**Pattern 5: Emergency Override**
```yaml
ENVIRONMENT != prod || BRANCH CONTAINS hotfix
```
→ Allow any environment except prod, unless it's a hotfix

**Pattern 6: Multi-Region Deployment**
```yaml
REGION IN us-east,us-west && SERVICE IN game,api
```
→ Deploy specific services to specific regions

**Pattern 7: Safe Production Deploy**
```yaml
NOT (TAG_NAME EMPTY) && ENVIRONMENT == prod && BRANCH == main
```
→ Require tag for production deployments from main

**Pattern 8: Development Feature Flags**
```yaml
FEATURE_FLAG NOT_EMPTY && NOT (ENVIRONMENT == prod)
```
→ Allow feature flags only in non-production

---

## Comparison with Bash/Shell

<br/>

| Feature | Bash | Ternary Operator Action |
|---------|------|------------------------|
| Equal | `==` or `=` | `==` |
| Not Equal | `!=` | `!=` |
| Greater Than | `-gt` | `>` |
| Less Than | `-lt` | `<` |
| Greater or Equal | `-ge` | `>=` |
| Less or Equal | `-le` | `<=` |
| AND | `&&` or `-a` | `&&` |
| OR | `\|\|` or `-o` | `\|\|` |
| IN operator | Not available | `IN` |
| Contains | `[[ $var == *"text"* ]]` | `CONTAINS` |
| Starts with | `[[ $var == "prefix"* ]]` | `STARTS_WITH` |
| Ends with | `[[ $var == *"suffix" ]]` | `ENDS_WITH` |
| Regex match | `[[ $var =~ regex ]]` | `MATCHES` |
| NOT operator | `!` | `NOT` |
| Empty check | `-z` | `EMPTY` |
| Not empty | `-n` | `NOT_EMPTY` |

---

## Tips and Best Practices

<br/>

1. **Use IN operator** when checking multiple values of the same variable
   ```yaml
   # Good
   SERVICE IN game,batch,api
   
   # Avoid
   SERVICE == game || SERVICE == batch || SERVICE == api
   ```

2. **Use CONTAINS** for pattern matching instead of complex equality checks
   ```yaml
   # Good
   BRANCH_NAME CONTAINS feature
   
   # Avoid
   BRANCH_NAME == feature/login || BRANCH_NAME == feature/api
   ```

3. **Use NOT_EMPTY** for required variable validation
   ```yaml
   # Good
   API_KEY NOT_EMPTY && DATABASE_URL NOT_EMPTY
   
   # More explicit than checking values
   ```

4. **Keep conditions simple** for better readability
   ```yaml
   # Good
   SERVICE == game && ENVIRONMENT == prod
   
   # Harder to read
   SERVICE == game && ENVIRONMENT == prod && BRANCH == main && VERSION >= 1.0
   ```

5. **Use numeric comparisons** for versions and counts
   ```yaml
   VERSION >= 1.5
   REPLICAS > 3
   MEMORY <= 8192
   ```

6. **Be explicit** with comparisons
   ```yaml
   # Good
   ENVIRONMENT == prod
   
   # Avoid implicit checks
   ENVIRONMENT
   ```

7. **Combine operators effectively**
   ```yaml
   # Validation + condition check
   CONFIG NOT_EMPTY && ENVIRONMENT IN prod,stage
   
   # Pattern + safety check
   BRANCH_NAME CONTAINS hotfix || NOT (ENVIRONMENT == prod)
   ```

8. **Test locally** before pushing (see [Development Guide](development.md))

---

## See Also

- [Usage Examples](usage.md) - Real-world usage patterns
- [API Reference](api.md) - Complete input/output documentation
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
