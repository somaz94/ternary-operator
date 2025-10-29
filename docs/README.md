# Documentation Index

Complete documentation for the Ternary Operator Action.

<br/>

## Documentation Structure

<br/>

### Getting Started
1. **[Main README](../README.md)** - Overview, quick start, and basic usage

<br/>

### Core Documentation
2. **[API Reference](api.md)** - Complete input/output specification
   - Inputs (`conditions`, `true_values`, `false_values`, `debug_mode`)
   - Outputs (`output_1` through `output_10`)
   - Limits and constraints
   - Environment variables

3. **[Operators Guide](operators.md)** - All supported operators
   - Comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`)
   - Logical operators (`&&`, `||`)
   - IN operator (special)
   - Operator precedence
   - Advanced usage patterns

4. **[Usage Examples](usage.md)** - Real-world patterns and scenarios
   - Quick start examples
   - Basic patterns
   - Advanced patterns
   - Real-world scenarios
   - Integration examples

<br/>

### Support & Development

5. **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
   - Common problems
   - Error messages
   - Debugging tips
   - Performance issues
   - Getting help

6. **[Development Guide](development.md)** - Contributing and local testing
   - Local development setup
   - Testing (Python & Bash suites)
   - Project structure
   - Contributing guidelines
   - Release process

---

## Quick Navigation

<br/>

### By Use Case

**I want to...**

- **Learn the basics** → [Main README](../README.md)
- **See examples** → [Usage Examples](usage.md)
- **Understand operators** → [Operators Guide](operators.md)
- **Check inputs/outputs** → [API Reference](api.md)
- **Fix an issue** → [Troubleshooting](troubleshooting.md)
- **Contribute** → [Development Guide](development.md)
- **Test locally** → [Development Guide - Testing](development.md#testing)

<br/>

### By Topic

**Operators:**
- [Comparison operators](operators.md#comparison-operators) - `==`, `!=`, `<`, `>`, etc.
- [Logical operators](operators.md#logical-operators) - `&&`, `||`
- [IN operator](operators.md#special-operators) - Check multiple values

<br/>

**Examples:**
- [Basic examples](usage.md#basic-examples) - Simple conditions
- [Advanced patterns](usage.md#advanced-patterns) - Complex scenarios
- [Real-world scenarios](usage.md#real-world-scenarios) - Production use cases
- [Integration examples](usage.md#integration-examples) - With other actions

<br/>

**Reference:**
- [Inputs specification](api.md#inputs)
- [Outputs specification](api.md#outputs)
- [Limits and constraints](api.md#limits-and-constraints)

<br/>

**Troubleshooting:**
- [Common issues](troubleshooting.md#common-issues)
- [Error messages](troubleshooting.md#error-messages)
- [Debugging tips](troubleshooting.md#debugging-tips)

<br/>

**Development:**
- [Testing locally](development.md#testing)
- [Project structure](development.md#project-structure)
- [Contributing guidelines](development.md#contributing)

---

## Reading Guide

<br/>

### For New Users

1. Start with [Main README](../README.md) for overview
2. Check [Usage Examples](usage.md) for patterns
3. Review [Operators Guide](operators.md) for syntax details

<br/>

### For Troubleshooting

1. Check [Troubleshooting](troubleshooting.md) for common issues
2. Enable `debug_mode` in your workflow
3. Test locally with [test scripts](../tests/README.md)

<br/>

### For Contributors

1. Read [Development Guide](development.md)
2. Set up local environment
3. Run tests: `python3 tests/test_local.py`
4. Follow coding guidelines

---

## Document Summaries

<br/>

### [API Reference](api.md)
Complete technical specification of all inputs, outputs, and constraints. Essential for understanding how to use the action programmatically.

**Key Sections:**
- Input parameters and their formats
- Output naming and access patterns
- Maximum limits (10 conditions)
- Array length matching requirements
- Environment variable handling

<br/>

### [Operators Guide](operators.md)
Comprehensive guide to all supported operators with examples and best practices.

**Key Sections:**
- Each operator explained in detail
- Truth tables for logical operators
- IN operator patterns and use cases
- Operator precedence rules
- Complex expression examples

<br/>

### [Usage Examples](usage.md)
Practical, copy-paste-ready examples for common and advanced scenarios.

**Key Sections:**
- Quick start patterns
- Service-specific configuration
- Environment-based deployment
- Multi-region strategies
- Version-based feature flags
- Database migration control
- Resource scaling
- Notification routing

<br/>

### [Troubleshooting](troubleshooting.md)
Solutions to common problems with step-by-step debugging approaches.

**Key Sections:**
- Top 5 common issues with solutions
- Complete error message reference
- Debug mode usage guide
- Performance optimization tips
- How to get help

<br/>

### [Development Guide](development.md)
Everything you need to contribute to the project or test changes locally.

**Key Sections:**
- Local setup instructions
- Testing with Python & Bash suites
- Project structure explanation
- Contributing workflow
- Release process
- Coding guidelines

---

## Getting Help

<br/>

### Documentation Not Helpful?

1. **Search existing issues**: [GitHub Issues](https://github.com/somaz94/ternary-operator/issues)
2. **Ask a question**: [GitHub Discussions](https://github.com/somaz94/ternary-operator/discussions)
3. **Report a bug**: [Create an issue](https://github.com/somaz94/ternary-operator/issues/new)

<br/>

### Before Asking

- [ ] Checked relevant documentation section
- [ ] Enabled `debug_mode: true`
- [ ] Tested locally with test scripts
- [ ] Searched existing issues

<br/>

### When Reporting Issues

Include:
- Your workflow YAML (relevant section)
- Debug output (with `debug_mode: true`)
- Expected vs actual behavior
- Environment details

---

## Documentation Updates

<br/>

This documentation is maintained alongside the codebase. When updating:

1. **Keep it current**: Update docs with code changes
2. **Add examples**: Include real-world usage patterns
3. **Link between docs**: Cross-reference related sections
4. **Test examples**: Ensure all code examples work

---

## Version History

<br/>

- **v1.x** - Initial Python implementation with IN operator
- See [CHANGELOG.md](../CHANGELOG.md) for detailed version history

---

<div align="center">

**📖 Complete | 🔍 Searchable | 💡 Practical**

[Back to Main README](../README.md) | [Report Issue](https://github.com/somaz94/ternary-operator/issues)

</div>
