# Usage Examples

Practical examples and patterns for using the Ternary Operator Action.

<br/>

## Table of Contents
- [Quick Start](#quick-start)
- [Basic Examples](#basic-examples)
- [String Operator Examples](#string-operator-examples)
- [Validation Operator Examples](#validation-operator-examples)
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

## String Operator Examples

<br/>

### Example 1: Branch Pattern Matching with CONTAINS

```yaml
- name: Check Branch Type
  uses: somaz94/ternary-operator@v1
  id: branch_type
  with:
    conditions: >-
      BRANCH_NAME CONTAINS feature,
      BRANCH_NAME CONTAINS hotfix,
      BRANCH_NAME CONTAINS release
    true_values: 'feature-branch,hotfix-branch,release-branch'
    false_values: 'other-branch,other-branch,other-branch'
  env:
    BRANCH_NAME: ${{ github.ref_name }}

- name: Run Branch-Specific Tests
  run: |
    case "${{ steps.branch_type.outputs.output_1 }}" in
      feature-branch)
        echo "Running feature tests..."
        npm run test:feature
        ;;
      hotfix-branch)
        echo "Running critical tests only..."
        npm run test:critical
        ;;
      *)
        echo "Running standard tests..."
        npm run test
        ;;
    esac
```

<br/>

### Example 2: Commit Message Filtering with CONTAINS

```yaml
- name: Check Commit Message
  uses: somaz94/ternary-operator@v1
  id: commit_check
  with:
    conditions: >-
      COMMIT_MESSAGE CONTAINS [skip ci],
      COMMIT_MESSAGE CONTAINS [docs only]
    true_values: 'skip,docs-only'
    false_values: 'run,full-build'
  env:
    COMMIT_MESSAGE: ${{ github.event.head_commit.message }}

- name: Conditional Build
  if: steps.commit_check.outputs.output_1 != 'skip'
  run: npm run build

- name: Run Tests
  if: steps.commit_check.outputs.output_2 != 'docs-only'
  run: npm test
```

<br/>

### Example 3: Using NOT Operator

```yaml
- name: Non-Production Safety Check
  uses: somaz94/ternary-operator@v1
  id: safety
  with:
    conditions: >-
      NOT (ENVIRONMENT == prod),
      NOT (SERVICE IN critical-api,payment-service)
    true_values: 'safe,non-critical'
    false_values: 'requires-review,critical-service'
  env:
    ENVIRONMENT: ${{ inputs.environment }}
    SERVICE: ${{ github.event.repository.name }}

- name: Auto Deploy
  if: |
    steps.safety.outputs.output_1 == 'safe' &&
    steps.safety.outputs.output_2 == 'non-critical'
  run: ./deploy.sh --auto

- name: Manual Review Required
  if: |
    steps.safety.outputs.output_1 != 'safe' ||
    steps.safety.outputs.output_2 != 'non-critical'
  run: |
    echo "::warning::Manual review required for production or critical service"
    exit 1
```

<br/>

### Example 4: Tag Version Detection with CONTAINS

```yaml
- name: Check Tag Type
  uses: somaz94/ternary-operator@v1
  id: tag_check
  with:
    conditions: >-
      TAG_NAME CONTAINS -rc,
      TAG_NAME CONTAINS -beta,
      TAG_NAME CONTAINS -alpha
    true_values: 'release-candidate,beta-release,alpha-release'
    false_values: 'stable,stable,stable'
  env:
    TAG_NAME: ${{ github.ref_name }}

- name: Deploy to Environment
  run: |
    case "${{ steps.tag_check.outputs.output_1 }}" in
      release-candidate)
        echo "Deploying to staging..."
        ./deploy.sh --env staging
        ;;
      beta-release|alpha-release)
        echo "Deploying to dev..."
        ./deploy.sh --env dev
        ;;
      stable)
        echo "Deploying to production..."
        ./deploy.sh --env prod
        ;;
    esac
```

---

## Validation Operator Examples

<br/>

### Example 1: Required Configuration Validation with NOT_EMPTY

```yaml
- name: Validate Required Variables
  uses: somaz94/ternary-operator@v1
  id: validate
  with:
    conditions: >-
      DATABASE_URL NOT_EMPTY,
      API_KEY NOT_EMPTY,
      SECRET_KEY NOT_EMPTY
    true_values: 'valid,valid,valid'
    false_values: 'missing,missing,missing'
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    API_KEY: ${{ secrets.API_KEY }}
    SECRET_KEY: ${{ secrets.SECRET_KEY }}

- name: Check All Required
  id: all_valid
  run: |
    if [[ "${{ steps.validate.outputs.output_1 }}" == "valid" ]] && \
       [[ "${{ steps.validate.outputs.output_2 }}" == "valid" ]] && \
       [[ "${{ steps.validate.outputs.output_3 }}" == "valid" ]]; then
      echo "valid=true" >> $GITHUB_OUTPUT
    else
      echo "valid=false" >> $GITHUB_OUTPUT
      echo "::error::Missing required configuration"
    fi

- name: Deploy Application
  if: steps.all_valid.outputs.valid == 'true'
  run: ./deploy.sh
```

<br/>

### Example 2: Optional Configuration with EMPTY

```yaml
- name: Check Optional Variables
  uses: somaz94/ternary-operator@v1
  id: optional
  with:
    conditions: >-
      CUSTOM_DOMAIN EMPTY,
      SLACK_WEBHOOK EMPTY,
      DOCKER_TAG EMPTY
    true_values: 'use-default,skip-notification,use-latest'
    false_values: 'use-custom,send-notification,use-tag'
  env:
    CUSTOM_DOMAIN: ${{ inputs.custom_domain }}
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
    DOCKER_TAG: ${{ inputs.docker_tag }}

- name: Set Domain
  run: |
    if [ "${{ steps.optional.outputs.output_1 }}" == "use-default" ]; then
      echo "DOMAIN=app.example.com" >> $GITHUB_ENV
    else
      echo "DOMAIN=${{ inputs.custom_domain }}" >> $GITHUB_ENV
    fi

- name: Notify Slack
  if: steps.optional.outputs.output_2 == 'send-notification'
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -d '{"text":"Deployment started for ${{ github.repository }}"}'

- name: Set Docker Tag
  run: |
    if [ "${{ steps.optional.outputs.output_3 }}" == "use-latest" ]; then
      echo "TAG=latest" >> $GITHUB_ENV
    else
      echo "TAG=${{ inputs.docker_tag }}" >> $GITHUB_ENV
    fi
```

<br/>

### Example 3: Combined Validation and Logic

```yaml
- name: Pre-Deployment Checks
  uses: somaz94/ternary-operator@v1
  id: pre_deploy
  with:
    conditions: >-
      API_KEY NOT_EMPTY && ENVIRONMENT == prod,
      NOT (TAG_NAME EMPTY) || BRANCH_NAME == main,
      DATABASE_URL NOT_EMPTY && NOT (ENVIRONMENT == dev)
    true_values: 'prod-ready,tag-valid,db-required'
    false_values: 'missing-key,no-tag,db-optional'
  env:
    API_KEY: ${{ secrets.API_KEY }}
    ENVIRONMENT: ${{ inputs.environment }}
    TAG_NAME: ${{ github.ref_type == 'tag' && github.ref_name || '' }}
    BRANCH_NAME: ${{ github.ref_name }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}

- name: Production Deployment
  if: |
    steps.pre_deploy.outputs.output_1 == 'prod-ready' &&
    steps.pre_deploy.outputs.output_2 == 'tag-valid' &&
    steps.pre_deploy.outputs.output_3 == 'db-required'
  run: ./deploy.sh --env prod

- name: Development Deployment
  if: steps.pre_deploy.outputs.output_1 == 'missing-key'
  run: ./deploy.sh --env dev --no-api-key
```

<br/>

### Example 4: Feature Flag Validation

```yaml
- name: Check Feature Flags
  uses: somaz94/ternary-operator@v1
  id: features
  with:
    conditions: >-
      FEATURE_NEW_UI NOT_EMPTY && NOT (ENVIRONMENT == prod),
      FEATURE_BETA_API NOT_EMPTY,
      FEATURE_DEBUG NOT_EMPTY && ENVIRONMENT IN dev,qa
    true_values: 'enable-new-ui,enable-beta-api,enable-debug'
    false_values: 'use-old-ui,use-stable-api,no-debug'
  env:
    FEATURE_NEW_UI: ${{ vars.FEATURE_NEW_UI }}
    FEATURE_BETA_API: ${{ vars.FEATURE_BETA_API }}
    FEATURE_DEBUG: ${{ vars.FEATURE_DEBUG }}
    ENVIRONMENT: ${{ inputs.environment }}

- name: Build with Flags
  run: |
    FLAGS=""
    [ "${{ steps.features.outputs.output_1 }}" == "enable-new-ui" ] && FLAGS="$FLAGS --new-ui"
    [ "${{ steps.features.outputs.output_2 }}" == "enable-beta-api" ] && FLAGS="$FLAGS --beta-api"
    [ "${{ steps.features.outputs.output_3 }}" == "enable-debug" ] && FLAGS="$FLAGS --debug"
    
    echo "Building with flags: $FLAGS"
    npm run build $FLAGS
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
