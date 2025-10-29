#!/bin/bash

# Local Test Script for Ternary Operator Action
# This script tests the entrypoint.py locally before pushing to GitHub

set -e

# Determine the root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$(basename "$SCRIPT_DIR")" == "tests" ]]; then
    ROOT_DIR="$(dirname "$SCRIPT_DIR")"
else
    ROOT_DIR="$SCRIPT_DIR"
fi

# Change to root directory
cd "$ROOT_DIR"
echo "Working directory: $ROOT_DIR"
echo ""

# Check if entrypoint.py exists
if [ ! -f "entrypoint.py" ]; then
    echo "❌ Error: entrypoint.py not found in $ROOT_DIR"
    echo "Please run this script from the ternary-operator root directory or tests directory"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print test header
print_header() {
    echo ""
    echo -e "${BLUE}=================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=================================================${NC}"
}

# Function to print test result
print_result() {
    local test_name="$1"
    local expected="$2"
    local actual="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$expected" == "$actual" ]; then
        echo -e "${GREEN}✅ PASS${NC}: $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: $test_name"
        echo -e "   Expected: $expected"
        echo -e "   Got: $actual"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to run a test
run_test() {
    local test_name="$1"
    local conditions="$2"
    local true_values="$3"
    local false_values="$4"
    local expected_output="$5"
    local env_vars="$6"
    
    echo ""
    echo -e "${YELLOW}Testing: $test_name${NC}"
    
    # Set environment variables
    export GITHUB_OUTPUT="/tmp/test_output_$$"
    rm -f "$GITHUB_OUTPUT"
    
    # Parse and export environment variables
    if [ -n "$env_vars" ]; then
        eval "$env_vars"
    fi
    
    export INPUT_CONDITIONS="$conditions"
    export INPUT_TRUE_VALUES="$true_values"
    export INPUT_FALSE_VALUES="$false_values"
    export INPUT_DEBUG_MODE="false"
    
    # Run the script
    if python3 entrypoint.py > /tmp/test_run_$$.log 2>&1; then
        # Extract output from GITHUB_OUTPUT file
        if [ -f "$GITHUB_OUTPUT" ]; then
            actual=$(grep "^output_1=" "$GITHUB_OUTPUT" | cut -d= -f2)
        else
            actual="NO_OUTPUT_FILE"
        fi
    else
        actual="ERROR"
    fi
    
    print_result "$test_name" "$expected_output" "$actual"
    
    # Cleanup
    rm -f "$GITHUB_OUTPUT" "/tmp/test_run_$$.log"
}

# Main test execution
print_header "🧪 Local Testing for Ternary Operator Action"

print_header "Test 1: Comparison Operators"

run_test "Equal operator (==)" \
    "SERVICE == game" \
    "service-pass" \
    "service-fail" \
    "service-pass" \
    "export SERVICE=game"

run_test "Not equal operator (!=)" \
    "SERVICE != batch" \
    "not-equal-pass" \
    "not-equal-fail" \
    "not-equal-pass" \
    "export SERVICE=game"

run_test "Greater than operator (>)" \
    "COUNT > 5" \
    "greater-pass" \
    "greater-fail" \
    "greater-pass" \
    "export COUNT=10"

run_test "Less than operator (<)" \
    "COUNT < 5" \
    "less-pass" \
    "less-fail" \
    "less-pass" \
    "export COUNT=3"

print_header "Test 2: Logical Operators"

run_test "AND operator (&&)" \
    "SERVICE == game && ENVIRONMENT == qa" \
    "and-pass" \
    "and-fail" \
    "and-pass" \
    "export SERVICE=game; export ENVIRONMENT=qa"

run_test "OR operator (||)" \
    "SERVICE == game || SERVICE == batch" \
    "or-pass" \
    "or-fail" \
    "or-pass" \
    "export SERVICE=game"

run_test "Complex logical expression" \
    "SERVICE == game && ENVIRONMENT == qa || ENVIRONMENT == dev" \
    "complex-pass" \
    "complex-fail" \
    "complex-pass" \
    "export SERVICE=game; export ENVIRONMENT=qa"

print_header "Test 3: IN Operator"

run_test "IN operator with match" \
    "SERVICE IN game,batch,api" \
    "in-pass" \
    "in-fail" \
    "in-pass" \
    "export SERVICE=game"

run_test "IN operator without match" \
    "SERVICE IN batch,api,web" \
    "in-pass" \
    "in-fail" \
    "in-fail" \
    "export SERVICE=game"

run_test "IN operator with multiple values" \
    "ENVIRONMENT IN dev,qa,stage,prod" \
    "env-pass" \
    "env-fail" \
    "env-pass" \
    "export ENVIRONMENT=qa"

print_header "Test 4: Mixed Operators"

run_test "IN operator with AND" \
    "SERVICE IN game,batch && ENVIRONMENT == qa" \
    "mixed-pass" \
    "mixed-fail" \
    "mixed-pass" \
    "export SERVICE=game; export ENVIRONMENT=qa"

run_test "IN operator with OR" \
    "SERVICE == game || BRANCH IN main,develop" \
    "mixed-pass" \
    "mixed-fail" \
    "mixed-pass" \
    "export SERVICE=game; export BRANCH=qa"

run_test "Complex mixed expression" \
    "SERVICE IN game,batch && ENVIRONMENT == qa || BRANCH == main" \
    "complex-pass" \
    "complex-fail" \
    "complex-pass" \
    "export SERVICE=game; export ENVIRONMENT=qa; export BRANCH=dev"

print_header "Test 5: Multiple Conditions"

# Test with multiple conditions
export SERVICE=game
export ENVIRONMENT=qa
export BRANCH=main
export INPUT_CONDITIONS="SERVICE == game, ENVIRONMENT == qa, BRANCH IN main,develop"
export INPUT_TRUE_VALUES="s-pass,e-pass,b-pass"
export INPUT_FALSE_VALUES="s-fail,e-fail,b-fail"
export INPUT_DEBUG_MODE="false"
export GITHUB_OUTPUT="/tmp/test_multi_$$"

echo ""
echo -e "${YELLOW}Testing: Multiple conditions${NC}"

if python3 entrypoint.py > /tmp/test_multi_run_$$.log 2>&1; then
    output1=$(grep "^output_1=" "$GITHUB_OUTPUT" | cut -d= -f2)
    output2=$(grep "^output_2=" "$GITHUB_OUTPUT" | cut -d= -f2)
    output3=$(grep "^output_3=" "$GITHUB_OUTPUT" | cut -d= -f2)
    
    print_result "Condition 1" "s-pass" "$output1"
    print_result "Condition 2" "e-pass" "$output2"
    print_result "Condition 3" "b-pass" "$output3"
else
    echo -e "${RED}❌ Multiple conditions test failed${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 3))
    TOTAL_TESTS=$((TOTAL_TESTS + 3))
fi

rm -f "$GITHUB_OUTPUT" "/tmp/test_multi_run_$$.log"

print_header "Test 6: Error Cases"

# Test exceeding maximum conditions
export INPUT_CONDITIONS="C1 == 1, C2 == 2, C3 == 3, C4 == 4, C5 == 5, C6 == 6, C7 == 7, C8 == 8, C9 == 9, C10 == 10, C11 == 11"
export INPUT_TRUE_VALUES="1,2,3,4,5,6,7,8,9,10,11"
export INPUT_FALSE_VALUES="1,2,3,4,5,6,7,8,9,10,11"
export INPUT_DEBUG_MODE="false"
export GITHUB_OUTPUT="/tmp/test_error_$$"

echo ""
echo -e "${YELLOW}Testing: Maximum conditions exceeded${NC}"

if python3 entrypoint.py > /tmp/test_error_run_$$.log 2>&1; then
    echo -e "${RED}❌ FAIL${NC}: Should have failed with too many conditions"
    FAILED_TESTS=$((FAILED_TESTS + 1))
else
    if grep -q "Maximum number of conditions" /tmp/test_error_run_$$.log; then
        echo -e "${GREEN}✅ PASS${NC}: Correctly rejected too many conditions"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: Failed but with wrong error message"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
fi

TOTAL_TESTS=$((TOTAL_TESTS + 1))
rm -f "$GITHUB_OUTPUT" "/tmp/test_error_run_$$.log"

# Print summary
print_header "📊 Test Summary"
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
else
    echo -e "Failed: $FAILED_TESTS"
fi
echo ""

# Exit with appropriate code
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
else
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
fi
