# Troubleshooting Guide

Common issues and solutions for the Ternary Operator Action.

<br/>

## Table of Contents
- [Common Issues](#common-issues)
- [Error Messages](#error-messages)
- [Debugging Tips](#debugging-tips)
- [Performance Issues](#performance-issues)
- [Getting Help](#getting-help)

---

## Common Issues

<br/>

### Issue 1: Condition Not Evaluating as Expected

**Symptoms:**
- Condition returns opposite of expected result
- Output doesn't match the actual state

**Common Causes:**

1. **Variable Not Set**
   ```yaml
   # ❌ Variable SERVICE not set in environment
   conditions: 'SERVICE == game'
   # Result: FALSE (even if you expect it to be true)
   ```
   
   **Solution:**
   ```yaml
   # ✅ Set variable first
   - name: Set Variable
     run: echo "SERVICE=game" >> $GITHUB_ENV
   
   - name: Evaluate
     uses: somaz94/ternary-operator@v1
     with:
       conditions: 'SERVICE == game'
   ```

2. **Case Sensitivity**
   ```yaml
   # ❌ SERVICE=game but checking for Game
   conditions: 'SERVICE == Game'
   # Result: FALSE
   ```
   
   **Solution:**
   ```yaml
   # ✅ Match exact case
   conditions: 'SERVICE == game'
   ```

3. **String vs Number Comparison**
   ```yaml
   # ❌ VERSION="1.5" (string) compared to number
   conditions: 'VERSION > 1.0'
   # Result: Depends on string representation
   ```
   
   **Solution:**
   ```yaml
   # ✅ Ensure numeric values aren't quoted in env
   - run: echo "VERSION=1.5" >> $GITHUB_ENV  # Not "VERSION=\"1.5\""
   ```

<br/>

---

### Issue 2: IN Operator Not Working

**Symptoms:**
- IN operator returns FALSE when value should match
- Unexpected parsing of comma-separated values

**Common Causes:**

1. **Whitespace in Values**
   ```yaml
   # ❌ Extra spaces around values
   conditions: 'SERVICE IN game, batch, api'
   # Might match " batch" instead of "batch"
   ```
   
   **Solution:**
   ```yaml
   # ✅ No spaces after commas (or they're auto-trimmed)
   conditions: 'SERVICE IN game,batch,api'
   ```

2. **Case Mismatch**
   ```yaml
   # ❌ SERVICE=Game but list has lowercase
   conditions: 'SERVICE IN game,batch'
   # Result: FALSE
   ```
   
   **Solution:**
   ```yaml
   # ✅ Match exact case
   conditions: 'SERVICE IN Game,Batch'
   # Or normalize in environment
   - run: echo "SERVICE=$(echo $SERVICE | tr '[:upper:]' '[:lower:]')" >> $GITHUB_ENV
   ```

3. **Confusion with AND/OR**
   ```yaml
   # ❌ Mixing IN with conditional operators incorrectly
   conditions: 'SERVICE IN game,batch && ENVIRONMENT == prod'
   # This checks: (SERVICE IN game,batch) AND (ENVIRONMENT == prod)
   ```
   
   **Solution: This is actually correct!** The IN operator groups the values:
   ```yaml
   # ✅ Properly structured
   conditions: 'SERVICE IN game,batch && ENVIRONMENT == prod'
   ```

<br/>

---

### Issue 3: Array Length Mismatch

**Symptoms:**
```
❌ Error: Number of conditions (3), true values (2), and false values (3) must match
```

**Cause:**
Different number of items in conditions, true_values, or false_values.

**Solution:**
```yaml
# ❌ Wrong
conditions: 'A == 1, B == 2, C == 3'  # 3 conditions
true_values: 'yes,ok'                  # 2 values
false_values: 'no,fail,never'         # 3 values

# ✅ Correct
conditions: 'A == 1, B == 2, C == 3'  # 3 conditions
true_values: 'yes,ok,good'            # 3 values
false_values: 'no,fail,never'         # 3 values
```

**Debugging Tip:**
Enable debug mode to see parsed conditions:
```yaml
debug_mode: true
# Output will show: "Parsed 3 conditions:"
```

<br/>

---

### Issue 4: Maximum Conditions Exceeded

**Symptoms:**
```
❌ Error: Maximum number of conditions (10) exceeded. Found 11 conditions
```

**Cause:**
More than 10 conditions in a single action call.

**Solutions:**

1. **Split into multiple calls:**
   ```yaml
   - name: First Batch
     id: batch1
     uses: somaz94/ternary-operator@v1
     with:
       conditions: # ... first 10 conditions
   
   - name: Second Batch
     id: batch2
     uses: somaz94/ternary-operator@v1
     with:
       conditions: # ... next conditions
   ```

2. **Combine conditions:**
   ```yaml
   # ❌ Before: 12 conditions
   SERVICE == game,
   SERVICE == batch,
   SERVICE == api,
   ...
   
   # ✅ After: 1 condition
   SERVICE IN game,batch,api,...
   ```

3. **Simplify logic:**
   ```yaml
   # ❌ Before: Multiple similar conditions
   ENV == dev || ENV == qa,
   ENV == stage || ENV == prod,
   ...
   
   # ✅ After: Grouped conditions
   ENV IN dev,qa,stage,prod
   ```

<br/>

---

### Issue 5: Variable Not Updating

**Symptoms:**
- Using updated variable but getting old value
- Variable changes not reflected in conditions

**Cause:**
Variable set in a previous step not available in current step's environment.

**Solution:**
```yaml
# ❌ Wrong order
- name: Evaluate
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE == game'

- name: Set Variable (too late!)
  run: echo "SERVICE=game" >> $GITHUB_ENV

# ✅ Correct order
- name: Set Variable
  run: echo "SERVICE=game" >> $GITHUB_ENV

- name: Evaluate
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE == game'
```

---

## Error Messages

<br/>

### "Missing required inputs"

**Full Error:**
```
❌ Error: Missing required inputs: CONDITIONS, TRUE_VALUES, FALSE_VALUES
```

**Cause:**
One or more required inputs not provided.

**Solution:**
```yaml
# ✅ Provide all required inputs
- uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE == game'     # Required
    true_values: 'deploy'             # Required
    false_values: 'skip'              # Required
```

<br/>

---

### "Number of conditions must match"

**Full Error:**
```
❌ Error: Number of conditions (2), true values (1), and false values (2) must match
```

**Cause:**
Mismatched array lengths.

**Solution:**
Count your comma-separated values:
```yaml
# Debug: Count conditions
conditions: 'A == 1, B == 2'      # Count: 2

# Debug: Count true_values
true_values: 'yes, ok'             # Count: 2

# Debug: Count false_values
false_values: 'no, fail'           # Count: 2
```

<br/>

---

### "Maximum number of conditions exceeded"

**Full Error:**
```
❌ Error: Maximum number of conditions (10) exceeded. Found 11 conditions
```

**Solution:**
See [Issue 4: Maximum Conditions Exceeded](#issue-4-maximum-conditions-exceeded)

---

## Debugging Tips

<br/>

### Enable Debug Mode

Always start by enabling debug mode:

```yaml
- uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE == game'
    true_values: 'deploy'
    false_values: 'skip'
    debug_mode: true  # ← Add this
```

**What You'll See:**
```
• Debug: Starting validation
• Debug: Raw conditions string: 'SERVICE == game'
• Debug: Parsed 1 conditions:
  1. SERVICE == game
• Debug: Variable SERVICE = game
• Debug: Processed condition: "game" == "game"
• Debug: Evaluating: "game" == "game"
✅ Success: Condition 1 is TRUE
```

<br/>

---

### Check Variable Values

Print environment variables before evaluation:

```yaml
- name: Debug Environment
  run: |
    echo "SERVICE=$SERVICE"
    echo "ENVIRONMENT=$ENVIRONMENT"
    echo "All env vars:"
    env | sort

- name: Evaluate
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE == game && ENVIRONMENT == prod'
    debug_mode: true
```

<br/>

---

### Test Locally

Before pushing to GitHub, test locally:

```bash
# Run comprehensive tests
python3 tests/test_local.py

# Run specific test
export SERVICE=game
export INPUT_CONDITIONS="SERVICE == game"
export INPUT_TRUE_VALUES="yes"
export INPUT_FALSE_VALUES="no"
export INPUT_DEBUG_MODE="true"
export GITHUB_OUTPUT="/tmp/output"
python3 entrypoint.py
```

See [Development Guide](development.md) for more details.

<br/>

---

### Validate Condition Syntax

Test your condition syntax:

```yaml
- name: Test Simple Condition
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE == game'      # Start simple
    true_values: 'yes'
    false_values: 'no'
    debug_mode: true

# Once working, add complexity:
# - name: Test Complex Condition
#   with:
#     conditions: 'SERVICE IN game,batch && ENV == prod'
```

<br/>

---

### Common Debugging Patterns

**Pattern 1: Check Each Condition Separately**
```yaml
# Instead of:
conditions: 'SERVICE == game && ENVIRONMENT == prod && BRANCH == main'

# Try:
conditions: >-
  SERVICE == game,
  ENVIRONMENT == prod,
  BRANCH == main
true_values: 'ok1,ok2,ok3'
false_values: 'fail1,fail2,fail3'

# Then check which one fails
```

**Pattern 2: Verify Variable Type**
```yaml
- name: Check Variable Type
  run: |
    echo "SERVICE value: '$SERVICE'"
    echo "SERVICE length: ${#SERVICE}"
    echo "Is numeric: $(if [[ $SERVICE =~ ^[0-9]+$ ]]; then echo yes; else echo no; fi)"
```

**Pattern 3: Test IN Operator Components**
```yaml
# Test individual components:
- name: Test Individual Values
  uses: somaz94/ternary-operator@v1
  with:
    conditions: >-
      SERVICE == game,
      SERVICE == batch,
      SERVICE == api
    true_values: 'g,b,a'
    false_values: 'ng,nb,na'

# If those work, combine with IN:
- name: Test IN Operator
  uses: somaz94/ternary-operator@v1
  with:
    conditions: 'SERVICE IN game,batch,api'
    true_values: 'yes'
    false_values: 'no'
```

---

## Performance Issues

<br/>

### Slow Execution

**Symptoms:**
- Action takes longer than expected

**Common Causes:**

1. **Too Many Conditions**
   - Each condition is evaluated sequentially
   - 10 conditions is the maximum, consider if you need all

2. **Complex Nested Logic**
   - `&&` and `||` create recursive evaluation
   - Simplify where possible

**Solutions:**
```yaml
# ❌ Slow
conditions: 'A == 1 && B == 2 && C == 3 && D == 4 && E == 5 || F == 6 || G == 7'

# ✅ Faster - split into simpler conditions
conditions: >-
  A == 1 && B == 2,
  C == 3 && D == 4,
  E == 5 || F == 6 || G == 7
```

---

## Getting Help

<br/>

### Before Asking for Help

1. ✅ Enable `debug_mode: true`
2. ✅ Check this troubleshooting guide
3. ✅ Test locally with `tests/test_local.py`
4. ✅ Review [Usage Examples](usage.md)
5. ✅ Check [Operators Reference](operators.md)

<br/>

### Where to Get Help

1. **GitHub Issues**
   - [Create an issue](https://github.com/somaz94/ternary-operator/issues)
   - Include debug output
   - Provide minimal reproduction example

2. **GitHub Discussions**
   - Ask questions
   - Share use cases
   - Get community help

<br/>

### Information to Include

When reporting issues, include:

```yaml
# Your workflow excerpt
- name: Problem Step
  uses: somaz94/ternary-operator@v1
  with:
    conditions: '...'  # What you're trying
    true_values: '...'
    false_values: '...'
    debug_mode: true   # Always enable for bug reports

# Environment context
# - What variables are set
# - What you expect vs what you get
# - Full debug output
```

---

## See Also

- [API Reference](api.md) - Input/output specifications
- [Operators Reference](operators.md) - Operator documentation
- [Usage Examples](usage.md) - Working examples
- [Development](development.md) - Local testing guide
