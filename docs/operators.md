# Operators Reference

Complete guide to all operators supported by the Ternary Operator Action.

<br/>

## Table of Contents
- [Comparison Operators](#comparison-operators)
- [Logical Operators](#logical-operators)
- [Special Operators](#special-operators)
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

**💡 Tip:** Consider using the `IN` operator for cleaner syntax when checking multiple values of the same variable.

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
- ✅ Cleaner syntax
- ✅ Easier to maintain
- ✅ Better readability
- ✅ Works with any number of values

**Use Cases:**
- Service name validation
- Environment checks
- Branch filtering
- Status matching
- Region selection

**⚠️ Important Notes:**
- Values are case-sensitive: `game` != `Game`
- Whitespace after commas is automatically trimmed
- Each value is treated as a string
- No quotes needed around values

---

## Operator Precedence

<br/>

When multiple operators are used together, they are evaluated in this order:

1. **Comparison operators** (`==`, `!=`, `<`, `>`, `<=`, `>=`, `IN`)
2. **AND operator** (`&&`)
3. **OR operator** (`||`)

**Example:**
```yaml
SERVICE == game && ENVIRONMENT == prod || BRANCH == main
```

This is evaluated as:
```
(SERVICE == game && ENVIRONMENT == prod) || BRANCH == main
```

**💡 Best Practice:** Use clear, simple conditions to avoid confusion. If you need complex logic, break it into multiple condition evaluations.

---

## Advanced Usage

<br/>

### Combining Operators

Mix different operators for complex conditions:

```yaml
# IN operator with AND
SERVICE IN game,batch && ENVIRONMENT == prod

# IN operator with OR
SERVICE == api || BRANCH IN main,develop

# Complex combinations
SERVICE IN game,batch && ENVIRONMENT != prod || BRANCH == hotfix

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
      ENVIRONMENT == prod && BRANCH == main,
      VERSION >= 1.5 || ENVIRONMENT IN dev,qa
    true_values: 'service-ok,production-deploy,version-ok'
    false_values: 'service-fail,no-deploy,version-fail'
```

<br/>

### Practical Patterns

**Pattern 1: Service and Environment Check**
```yaml
SERVICE IN game,batch && ENVIRONMENT IN prod,stage
```
→ Deploy only specific services in specific environments

**Pattern 2: Version Range**
```yaml
VERSION >= 1.0 && VERSION < 2.0
```
→ Check if version is in 1.x range

**Pattern 3: Emergency Override**
```yaml
ENVIRONMENT != prod || BRANCH == hotfix
```
→ Allow any environment except prod, unless it's a hotfix

**Pattern 4: Multi-Region Deployment**
```yaml
REGION IN us-east,us-west && SERVICE IN game,api
```
→ Deploy specific services to specific regions

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

2. **Keep conditions simple** for better readability
   ```yaml
   # Good
   SERVICE == game && ENVIRONMENT == prod
   
   # Harder to read
   SERVICE == game && ENVIRONMENT == prod && BRANCH == main && VERSION >= 1.0
   ```

3. **Use numeric comparisons** for versions and counts
   ```yaml
   VERSION >= 1.5
   REPLICAS > 3
   MEMORY <= 8192
   ```

4. **Be explicit** with comparisons
   ```yaml
   # Good
   ENVIRONMENT == prod
   
   # Avoid implicit checks
   ENVIRONMENT
   ```

5. **Test locally** before pushing (see [Development Guide](development.md))

---

## See Also

- [Usage Examples](usage.md) - Real-world usage patterns
- [API Reference](api.md) - Complete input/output documentation
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
