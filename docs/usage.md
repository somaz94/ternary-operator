# Usage Examples

Practical examples and patterns for using the Ternary Operator Action.

<br/>

## Table of Contents
- [Quick Start](#quick-start)
- [Basic Examples](#basic-examples)
- [Advanced Patterns](#advanced-patterns)
- [Real-World Scenarios](#real-world-scenarios)
- [Integration Examples](#integration-examples)

---

## Quick Start

<br/>

Minimal working example:

```yaml
name: Quick Start
on: [push]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set Environment
        run: echo "ENVIRONMENT=prod" >> $GITHUB_ENV
      
      - name: Evaluate
        uses: somaz94/ternary-operator@v1
        id: check
        with:
          conditions: 'ENVIRONMENT == prod'
          true_values: 'deploy'
          false_values: 'skip'
      
      - name: Result
        run: echo "Action: ${{ steps.check.outputs.output_1 }}"
```

---

## Basic Examples

<br/>

### Example 1: Single Condition Check

```yaml
- name: Check Service
  uses: somaz94/ternary-operator@v1
  id: service_check
  with:
    conditions: 'SERVICE == game'
    true_values: 'game-deploy'
    false_values: 'other-deploy'

- name: Deploy Based on Service
  run: |
    echo "Deploy type: ${{ steps.service_check.outputs.output_1 }}"
```

<br/>

### Example 2: Multiple Value Check with IN

```yaml
- name: Check Valid Environment
  uses: somaz94/ternary-operator@v1
  id: env_check
  with:
    conditions: 'ENVIRONMENT IN dev,qa,stage'
    true_values: 'non-prod'
    false_values: 'production'

- name: Apply Configuration
  run: |
    if [ "${{ steps.env_check.outputs.output_1 }}" == "non-prod" ]; then
      echo "Using non-production config"
    fi
```

<br/>

### Example 3: Combining AND/OR

```yaml
- name: Production Deployment Check
  uses: somaz94/ternary-operator@v1
  id: deploy_check
  with:
    conditions: 'SERVICE IN game,api && ENVIRONMENT == prod'
    true_values: 'approved'
    false_values: 'denied'

- name: Deploy
  if: steps.deploy_check.outputs.output_1 == 'approved'
  run: echo "Deploying to production..."
```

<br/>

### Example 4: Multiple Conditions

```yaml
- name: Multi-Check
  uses: somaz94/ternary-operator@v1
  id: checks
  with:
    conditions: >-
      SERVICE IN game,batch,api,
      ENVIRONMENT == prod,
      BRANCH IN main,release
    true_values: 'service-ok,prod-deploy,branch-ok'
    false_values: 'service-fail,no-deploy,branch-fail'

- name: Use Results
  run: |
    echo "Service check: ${{ steps.checks.outputs.output_1 }}"
    echo "Environment check: ${{ steps.checks.outputs.output_2 }}"
    echo "Branch check: ${{ steps.checks.outputs.output_3 }}"
```

---

## Advanced Patterns

<br/>

### Pattern 1: Service-Specific Configuration

```yaml
name: Service Configuration
jobs:
  configure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set Variables
        id: vars
        uses: somaz94/env-output-setter@v1
        with:
          env_key: 'SERVICE,ENVIRONMENT'
          env_value: 'game,prod'
          output_key: 'SERVICE,ENVIRONMENT'
          output_value: 'game,prod'
      
      - name: Determine Configuration
        uses: somaz94/ternary-operator@v1
        id: config
        with:
          conditions: >-
            SERVICE == game,
            SERVICE == batch,
            SERVICE IN api,worker
          true_values: 'game-config.yml,batch-config.yml,api-config.yml'
          false_values: 'default.yml,default.yml,default.yml'
      
      - name: Apply Configuration
        run: |
          CONFIG_FILE="${{ steps.config.outputs.output_1 }}"
          echo "Using configuration: $CONFIG_FILE"
          kubectl apply -f configs/$CONFIG_FILE
```

<br/>

### Pattern 2: Environment-Based Deployment Strategy

```yaml
name: Smart Deployment
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Determine Strategy
        uses: somaz94/ternary-operator@v1
        id: strategy
        with:
          conditions: >-
            ENVIRONMENT == prod,
            ENVIRONMENT IN qa,stage,
            ENVIRONMENT == dev
          true_values: 'blue-green,canary,rolling'
          false_values: 'rolling,rolling,direct'
          debug_mode: true
      
      - name: Deploy with Strategy
        run: |
          STRATEGY="${{ steps.strategy.outputs.output_1 }}"
          echo "Deploying with $STRATEGY strategy"
          ./deploy.sh --strategy=$STRATEGY
```

<br/>

### Pattern 3: Multi-Region Deployment

```yaml
name: Multi-Region
jobs:
  deploy:
    strategy:
      matrix:
        region: [us-east, us-west, eu-west, ap-south]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set Region
        run: echo "REGION=${{ matrix.region }}" >> $GITHUB_ENV
      
      - name: Check Region Eligibility
        uses: somaz94/ternary-operator@v1
        id: region_check
        with:
          conditions: >-
            REGION IN us-east,us-west && SERVICE IN game,api,
            REGION IN eu-west && SERVICE IN game,
            REGION == ap-south && SERVICE == batch
          true_values: 'deploy,deploy,deploy'
          false_values: 'skip,skip,skip'
      
      - name: Deploy to Region
        if: steps.region_check.outputs.output_1 == 'deploy'
        run: |
          echo "Deploying ${{ env.SERVICE }} to ${{ env.REGION }}"
```

<br/>

### Pattern 4: Version-Based Feature Flags

```yaml
name: Feature Flags
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Feature Availability
        uses: somaz94/ternary-operator@v1
        id: features
        with:
          conditions: >-
            VERSION >= 2.0,
            VERSION >= 1.5 && VERSION < 2.0,
            VERSION < 1.5
          true_values: 'all-features,stable-features,basic-features'
          false_values: 'basic-features,basic-features,basic-features'
      
      - name: Enable Features
        run: |
          FEATURES="${{ steps.features.outputs.output_1 }}"
          echo "Enabling: $FEATURES"
          ./configure-features.sh --profile=$FEATURES
```

---

## Real-World Scenarios

<br/>

### Scenario 1: Conditional Docker Build

```yaml
name: Docker Build and Push
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set Variables
        id: vars
        uses: somaz94/env-output-setter@v1
        with:
          env_key: 'SERVICE,ENVIRONMENT,BRANCH'
          env_value: '${{ github.event.repository.name }},prod,${{ github.ref_name }}'
          output_key: 'SERVICE,ENVIRONMENT,BRANCH'
          output_value: '${{ github.event.repository.name }},prod,${{ github.ref_name }}'
      
      - name: Determine Build Strategy
        uses: somaz94/ternary-operator@v1
        id: build
        with:
          conditions: >-
            SERVICE IN game,batch && BRANCH == main,
            SERVICE IN api,worker && BRANCH IN main,develop,
            ENVIRONMENT == prod
          true_values: 'multi-stage,cached,optimized'
          false_values: 'simple,simple,dev-build'
      
      - name: Build Docker Image
        run: |
          BUILD_TYPE="${{ steps.build.outputs.output_1 }}"
          echo "Building with: $BUILD_TYPE"
          
          case $BUILD_TYPE in
            multi-stage)
              docker build -f Dockerfile.prod -t myapp:latest .
              ;;
            cached)
              docker build --cache-from myapp:latest -t myapp:latest .
              ;;
            *)
              docker build -t myapp:dev .
              ;;
          esac
```

<br/>

### Scenario 2: Database Migration Control

```yaml
name: Database Migration
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Migration Safety
        uses: somaz94/ternary-operator@v1
        id: migration
        with:
          conditions: >-
            ENVIRONMENT == prod && BRANCH == main,
            ENVIRONMENT IN qa,stage,
            ENVIRONMENT == dev
          true_values: 'require-approval,auto-migrate,auto-migrate'
          false_values: 'block,block,auto-migrate'
          debug_mode: true
      
      - name: Request Approval
        if: steps.migration.outputs.output_1 == 'require-approval'
        uses: trstringer/manual-approval@v1
        with:
          approvers: devops-team
          minimum-approvals: 2
      
      - name: Run Migration
        if: steps.migration.outputs.output_1 != 'block'
        run: |
          echo "Running migration for ${{ env.ENVIRONMENT }}"
          ./migrate.sh
```

<br/>

### Scenario 3: Resource Scaling

```yaml
name: Auto Scaling
jobs:
  scale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Determine Replica Count
        uses: somaz94/ternary-operator@v1
        id: replicas
        with:
          conditions: >-
            SERVICE == game && ENVIRONMENT == prod,
            SERVICE IN batch,worker && ENVIRONMENT == prod,
            ENVIRONMENT IN qa,stage,
            ENVIRONMENT == dev
          true_values: '10,5,3,1'
          false_values: '1,1,1,1'
      
      - name: Scale Application
        run: |
          REPLICAS="${{ steps.replicas.outputs.output_1 }}"
          echo "Scaling to $REPLICAS replicas"
          kubectl scale deployment/${{ env.SERVICE }} --replicas=$REPLICAS
```

<br/>

### Scenario 4: Notification Routing

```yaml
name: Notification System
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Determine Notification Channel
        uses: somaz94/ternary-operator@v1
        id: notify
        with:
          conditions: >-
            ENVIRONMENT == prod && STATUS == failed,
            ENVIRONMENT == prod && STATUS == success,
            ENVIRONMENT IN qa,stage && STATUS == failed,
            ENVIRONMENT == dev
          true_values: 'pagerduty,slack-prod,slack-qa,none'
          false_values: 'slack-prod,none,none,none'
      
      - name: Send Notification
        run: |
          CHANNEL="${{ steps.notify.outputs.output_1 }}"
          case $CHANNEL in
            pagerduty)
              ./notify-pagerduty.sh "Production failure!"
              ;;
            slack-prod)
              ./notify-slack.sh "#prod-deploys" "Deploy completed"
              ;;
            slack-qa)
              ./notify-slack.sh "#qa-alerts" "Test failure"
              ;;
            none)
              echo "No notification needed"
              ;;
          esac
```

---

## Integration Examples

<br/>

### With GitHub Environments

```yaml
name: Environment-Aware Deployment
on:
  workflow_dispatch:
    inputs:
      environment:
        type: environment
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Set Environment Variable
        run: echo "ENVIRONMENT=${{ github.event.inputs.environment }}" >> $GITHUB_ENV
      
      - name: Check Deployment Rules
        uses: somaz94/ternary-operator@v1
        id: rules
        with:
          conditions: 'ENVIRONMENT == production'
          true_values: 'require-approval'
          false_values: 'auto-deploy'
      
      - name: Deploy
        run: ./deploy.sh --env=${{ env.ENVIRONMENT }}
```

<br/>

### With env-output-setter

```yaml
name: Complete Integration
jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Step 1: Set multiple variables
      - name: Set Variables
        id: set_vars
        uses: somaz94/env-output-setter@v1
        with:
          env_key: 'SERVICE,ENVIRONMENT,VERSION,REGION'
          env_value: 'game,prod,1.5.0,us-east'
          output_key: 'SERVICE,ENVIRONMENT,VERSION,REGION'
          output_value: 'game,prod,1.5.0,us-east'
      
      # Step 2: Evaluate conditions
      - name: Evaluate Conditions
        uses: somaz94/ternary-operator@v1
        id: evaluate
        with:
          conditions: >-
            SERVICE IN game,batch && ENVIRONMENT == prod,
            VERSION >= 1.5,
            REGION IN us-east,us-west
          true_values: 'deploy-prod,new-features,multi-region'
          false_values: 'deploy-qa,basic-features,single-region'
      
      # Step 3: Use results
      - name: Execute Deployment
        run: |
          echo "Deployment mode: ${{ steps.evaluate.outputs.output_1 }}"
          echo "Feature set: ${{ steps.evaluate.outputs.output_2 }}"
          echo "Region strategy: ${{ steps.evaluate.outputs.output_3 }}"
```

<br/>

### With Matrix Strategy

```yaml
name: Matrix with Conditions
jobs:
  test:
    strategy:
      matrix:
        service: [game, batch, api, worker]
        environment: [dev, qa, prod]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set Matrix Values
        run: |
          echo "SERVICE=${{ matrix.service }}" >> $GITHUB_ENV
          echo "ENVIRONMENT=${{ matrix.environment }}" >> $GITHUB_ENV
      
      - name: Check Test Requirements
        uses: somaz94/ternary-operator@v1
        id: test_check
        with:
          conditions: >-
            SERVICE IN game,api && ENVIRONMENT == prod,
            SERVICE == batch && ENVIRONMENT IN qa,prod,
            SERVICE == worker
          true_values: 'full-test,integration-test,unit-test'
          false_values: 'unit-test,unit-test,skip'
      
      - name: Run Tests
        if: steps.test_check.outputs.output_1 != 'skip'
        run: |
          TEST_SUITE="${{ steps.test_check.outputs.output_1 }}"
          echo "Running $TEST_SUITE for ${{ matrix.service }}"
          npm run test:$TEST_SUITE
```

---

## See Also

- [Operators Reference](operators.md) - Complete operator documentation
- [API Reference](api.md) - Input/output specifications
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [Development](development.md) - Local testing and contributing
