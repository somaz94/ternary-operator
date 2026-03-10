# CLAUDE.md - ternary-operator

GitHub Action that evaluates dynamic conditions and generates outputs based on ternary logic with support for comparison, logical, IN, CONTAINS, EMPTY, and NOT operators.

## Project Structure

```
entrypoint.py                    # Thin wrapper (calls src.evaluator)
src/
  __init__.py                    # Package init (version)
  evaluator.py                   # Main orchestration (TernaryOperator class)
  parser.py                      # Condition parsing (IN operator, logical operators)
  operators.py                   # Specialized operator evaluators (IN, CONTAINS, EMPTY)
  colors.py                      # ANSI color codes for terminal output
tests/
  test_local.py                  # Python integration test suite (42 test cases)
  test_local.sh                  # Bash test suite (17 tests)
  README.md                      # Testing documentation
docs/
  api.md                         # API reference
  operators.md                   # Operator documentation
  usage.md                       # Usage examples
  troubleshooting.md             # Problem solving guide
  development.md                 # Development guide
backup/
  entrypoint.sh.bak              # Original bash version
  Dockerfile.bak
  action.yml.bak
Dockerfile                       # Single-stage (python:3.14-slim)
action.yml                       # GitHub Action definition (4 inputs, 10 outputs)
cliff.toml                       # git-cliff config for release notes
Makefile                         # Test and clean commands
```

## Build & Test

```bash
make test          # Run all tests (alias for test-local)
make test-local    # Run Python integration tests
make test-bash     # Run bash test suite
make clean         # Remove cache and build artifacts
make help          # Show all available commands
```

## Key Inputs

- **Required**: `conditions`, `true_values`, `false_values`
- **Options**: `debug_mode`

## Outputs

`output_1` through `output_10` (max 10 conditions)

## Supported Operators

- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&` (AND), `||` (OR), `NOT`
- **Special**: `IN` (multiple value check)
- **String**: `CONTAINS` (substring check, case-sensitive)
- **Validation**: `EMPTY`, `NOT_EMPTY`

## Workflow Structure

| Workflow | Name | Trigger |
|----------|------|---------|
| `ci.yml` | `Continuous Integration` | push(main), PR, dispatch |
| `release.yml` | `Create release` | tag push `v*` |
| `changelog-generator.yml` | `Generate changelog` | after release, PR merge, issue close |
| `use-action.yml` | `Smoke Test (Released Action)` | after release, dispatch |
| `contributors.yml` | `Generator Contributors` | after changelog, dispatch |

### Workflow Chain
```
tag push v* → Create release
                ├→ Smoke Test (Released Action)
                └→ Generate changelog → Generator Contributors
```

### CI Structure
```
test-local ──────────┐
build-and-push-docker ──→ test-action ──→ ci-result
```

## Conventions

- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `chore:`)
- **Branches**: `main` (production)
- **Secrets**: `PAT_TOKEN` (cross-repo ops), `GITHUB_TOKEN` (changelog, releases)
- **Docker**: Single-stage build, python:3.14-slim base
- **Comments**: English only
- **Testing**: Python integration tests (subprocess-based), bash test suite
- **Release**: `git switch` (not `git checkout`), git-cliff for RELEASE.md
- **cliff.toml**: Skip `^Merge`, `^Update changelog`, `^Auto commit`
- **paths-ignore**: `.github/workflows/**`, `**/*.md`, `backup/**`
- Do NOT commit directly - recommend commit messages only
