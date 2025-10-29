#!/usr/bin/env python3
"""
Local Test Suite for Ternary Operator Action
This script provides comprehensive testing before pushing to GitHub
"""

import os
import sys
import subprocess
import tempfile
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TestCase:
    """Represents a single test case"""
    name: str
    conditions: str
    true_values: str
    false_values: str
    expected_outputs: Dict[str, str]
    env_vars: Dict[str, str]
    should_fail: bool = False
    expected_error: Optional[str] = None


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'


class TestRunner:
    """Runs test cases and collects results"""
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.results = []
    
    def print_header(self, message: str):
        """Print a formatted header"""
        print(f"\n{Colors.BLUE}{'=' * 50}{Colors.NC}")
        print(f"{Colors.BLUE}{message}{Colors.NC}")
        print(f"{Colors.BLUE}{'=' * 50}{Colors.NC}")
    
    def print_result(self, test_name: str, passed: bool, details: str = ""):
        """Print test result"""
        if passed:
            print(f"{Colors.GREEN}✅ PASS{Colors.NC}: {test_name}")
            self.passed_tests += 1
        else:
            print(f"{Colors.RED}❌ FAIL{Colors.NC}: {test_name}")
            if details:
                print(f"   {details}")
            self.failed_tests += 1
        self.total_tests += 1
    
    def run_test(self, test: TestCase) -> bool:
        """Run a single test case"""
        print(f"\n{Colors.YELLOW}Testing: {test.name}{Colors.NC}")
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            output_file = f.name
        
        try:
            # Set up environment
            env = os.environ.copy()
            env.update(test.env_vars)
            env['INPUT_CONDITIONS'] = test.conditions
            env['INPUT_TRUE_VALUES'] = test.true_values
            env['INPUT_FALSE_VALUES'] = test.false_values
            env['INPUT_DEBUG_MODE'] = 'false'
            env['GITHUB_OUTPUT'] = output_file
            
            # Run the script
            result = subprocess.run(
                ['python3', 'entrypoint.py'],
                env=env,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Check if it should have failed
            if test.should_fail:
                if result.returncode != 0:
                    # Check error message if specified
                    if test.expected_error:
                        if test.expected_error in result.stdout or test.expected_error in result.stderr:
                            self.print_result(test.name, True, f"Correctly failed with expected error")
                            return True
                        else:
                            self.print_result(test.name, False, 
                                f"Failed but with wrong error. Expected '{test.expected_error}'")
                            return False
                    else:
                        self.print_result(test.name, True, "Correctly failed as expected")
                        return True
                else:
                    self.print_result(test.name, False, "Should have failed but succeeded")
                    return False
            
            # Check if it should have succeeded
            if result.returncode != 0:
                self.print_result(test.name, False, 
                    f"Script failed with exit code {result.returncode}")
                print(f"   STDOUT: {result.stdout[:200]}")
                print(f"   STDERR: {result.stderr[:200]}")
                return False
            
            # Read outputs from file
            actual_outputs = {}
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            actual_outputs[key] = value
            
            # Verify outputs
            all_match = True
            for key, expected_value in test.expected_outputs.items():
                actual_value = actual_outputs.get(key)
                if actual_value != expected_value:
                    all_match = False
                    self.print_result(test.name, False, 
                        f"{key}: expected '{expected_value}', got '{actual_value}'")
                    return False
            
            if all_match:
                self.print_result(test.name, True)
                return True
            
        except subprocess.TimeoutExpired:
            self.print_result(test.name, False, "Test timed out")
            return False
        except Exception as e:
            self.print_result(test.name, False, f"Exception: {str(e)}")
            return False
        finally:
            # Cleanup
            if os.path.exists(output_file):
                os.unlink(output_file)
        
        return False
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("📊 Test Summary")
        print(f"Total Tests: {self.total_tests}")
        print(f"{Colors.GREEN}Passed: {self.passed_tests}{Colors.NC}")
        if self.failed_tests > 0:
            print(f"{Colors.RED}Failed: {self.failed_tests}{Colors.NC}")
        else:
            print(f"Failed: {self.failed_tests}")
        print()
        
        if self.failed_tests > 0:
            print(f"{Colors.RED}❌ Some tests failed{Colors.NC}")
            return False
        else:
            print(f"{Colors.GREEN}✅ All tests passed!{Colors.NC}")
            return True


def create_test_suite() -> List[TestCase]:
    """Create the test suite"""
    tests = []
    
    # Comparison Operators
    tests.append(TestCase(
        name="Equal operator (==)",
        conditions="SERVICE == game",
        true_values="service-pass",
        false_values="service-fail",
        expected_outputs={"output_1": "service-pass"},
        env_vars={"SERVICE": "game"}
    ))
    
    tests.append(TestCase(
        name="Not equal operator (!=)",
        conditions="SERVICE != batch",
        true_values="not-equal-pass",
        false_values="not-equal-fail",
        expected_outputs={"output_1": "not-equal-pass"},
        env_vars={"SERVICE": "game"}
    ))
    
    tests.append(TestCase(
        name="Greater than operator (>)",
        conditions="COUNT > 5",
        true_values="greater-pass",
        false_values="greater-fail",
        expected_outputs={"output_1": "greater-pass"},
        env_vars={"COUNT": "10"}
    ))
    
    tests.append(TestCase(
        name="Less than operator (<)",
        conditions="COUNT < 5",
        true_values="less-pass",
        false_values="less-fail",
        expected_outputs={"output_1": "less-pass"},
        env_vars={"COUNT": "3"}
    ))
    
    tests.append(TestCase(
        name="Greater than or equal (>=)",
        conditions="COUNT >= 10",
        true_values="gte-pass",
        false_values="gte-fail",
        expected_outputs={"output_1": "gte-pass"},
        env_vars={"COUNT": "10"}
    ))
    
    tests.append(TestCase(
        name="Less than or equal (<=)",
        conditions="COUNT <= 5",
        true_values="lte-pass",
        false_values="lte-fail",
        expected_outputs={"output_1": "lte-pass"},
        env_vars={"COUNT": "5"}
    ))
    
    # Logical Operators
    tests.append(TestCase(
        name="AND operator (&&) - both true",
        conditions="SERVICE == game && ENVIRONMENT == qa",
        true_values="and-pass",
        false_values="and-fail",
        expected_outputs={"output_1": "and-pass"},
        env_vars={"SERVICE": "game", "ENVIRONMENT": "qa"}
    ))
    
    tests.append(TestCase(
        name="AND operator (&&) - one false",
        conditions="SERVICE == game && ENVIRONMENT == prod",
        true_values="and-pass",
        false_values="and-fail",
        expected_outputs={"output_1": "and-fail"},
        env_vars={"SERVICE": "game", "ENVIRONMENT": "qa"}
    ))
    
    tests.append(TestCase(
        name="OR operator (||) - first true",
        conditions="SERVICE == game || SERVICE == batch",
        true_values="or-pass",
        false_values="or-fail",
        expected_outputs={"output_1": "or-pass"},
        env_vars={"SERVICE": "game"}
    ))
    
    tests.append(TestCase(
        name="OR operator (||) - second true",
        conditions="SERVICE == api || SERVICE == game",
        true_values="or-pass",
        false_values="or-fail",
        expected_outputs={"output_1": "or-pass"},
        env_vars={"SERVICE": "game"}
    ))
    
    tests.append(TestCase(
        name="OR operator (||) - both false",
        conditions="SERVICE == api || SERVICE == batch",
        true_values="or-pass",
        false_values="or-fail",
        expected_outputs={"output_1": "or-fail"},
        env_vars={"SERVICE": "game"}
    ))
    
    # IN Operator
    tests.append(TestCase(
        name="IN operator - match found",
        conditions="SERVICE IN game,batch,api",
        true_values="in-pass",
        false_values="in-fail",
        expected_outputs={"output_1": "in-pass"},
        env_vars={"SERVICE": "game"}
    ))
    
    tests.append(TestCase(
        name="IN operator - no match",
        conditions="SERVICE IN batch,api,web",
        true_values="in-pass",
        false_values="in-fail",
        expected_outputs={"output_1": "in-fail"},
        env_vars={"SERVICE": "game"}
    ))
    
    tests.append(TestCase(
        name="IN operator - multiple values",
        conditions="ENVIRONMENT IN dev,qa,stage,prod",
        true_values="env-pass",
        false_values="env-fail",
        expected_outputs={"output_1": "env-pass"},
        env_vars={"ENVIRONMENT": "qa"}
    ))
    
    tests.append(TestCase(
        name="IN operator - case sensitive",
        conditions="SERVICE IN Game,Batch",
        true_values="in-pass",
        false_values="in-fail",
        expected_outputs={"output_1": "in-fail"},
        env_vars={"SERVICE": "game"}
    ))
    
    # Mixed Operators
    tests.append(TestCase(
        name="IN with AND - both true",
        conditions="SERVICE IN game,batch && ENVIRONMENT == qa",
        true_values="mixed-pass",
        false_values="mixed-fail",
        expected_outputs={"output_1": "mixed-pass"},
        env_vars={"SERVICE": "game", "ENVIRONMENT": "qa"}
    ))
    
    tests.append(TestCase(
        name="IN with AND - first false",
        conditions="SERVICE IN batch,api && ENVIRONMENT == qa",
        true_values="mixed-pass",
        false_values="mixed-fail",
        expected_outputs={"output_1": "mixed-fail"},
        env_vars={"SERVICE": "game", "ENVIRONMENT": "qa"}
    ))
    
    tests.append(TestCase(
        name="IN with OR - first true",
        conditions="SERVICE == game || BRANCH IN main,develop",
        true_values="mixed-pass",
        false_values="mixed-fail",
        expected_outputs={"output_1": "mixed-pass"},
        env_vars={"SERVICE": "game", "BRANCH": "qa"}
    ))
    
    tests.append(TestCase(
        name="IN with OR - second true",
        conditions="SERVICE == api || BRANCH IN main,develop",
        true_values="mixed-pass",
        false_values="mixed-fail",
        expected_outputs={"output_1": "mixed-pass"},
        env_vars={"SERVICE": "game", "BRANCH": "main"}
    ))
    
    tests.append(TestCase(
        name="Complex mixed expression",
        conditions="SERVICE IN game,batch && ENVIRONMENT == qa || BRANCH == main",
        true_values="complex-pass",
        false_values="complex-fail",
        expected_outputs={"output_1": "complex-pass"},
        env_vars={"SERVICE": "game", "ENVIRONMENT": "qa", "BRANCH": "dev"}
    ))
    
    # Multiple Conditions
    tests.append(TestCase(
        name="Multiple conditions - all true",
        conditions="SERVICE == game, ENVIRONMENT == qa, BRANCH IN main,develop",
        true_values="s-pass,e-pass,b-pass",
        false_values="s-fail,e-fail,b-fail",
        expected_outputs={
            "output_1": "s-pass",
            "output_2": "e-pass",
            "output_3": "b-pass"
        },
        env_vars={"SERVICE": "game", "ENVIRONMENT": "qa", "BRANCH": "main"}
    ))
    
    tests.append(TestCase(
        name="Multiple conditions - mixed results",
        conditions="SERVICE == game, ENVIRONMENT == prod, BRANCH IN main,develop",
        true_values="s-pass,e-pass,b-pass",
        false_values="s-fail,e-fail,b-fail",
        expected_outputs={
            "output_1": "s-pass",
            "output_2": "e-fail",
            "output_3": "b-pass"
        },
        env_vars={"SERVICE": "game", "ENVIRONMENT": "qa", "BRANCH": "main"}
    ))
    
    tests.append(TestCase(
        name="10 conditions (maximum)",
        conditions=", ".join([f"C{i} == {i}" for i in range(1, 11)]),
        true_values=",".join([f"pass-{i}" for i in range(1, 11)]),
        false_values=",".join([f"fail-{i}" for i in range(1, 11)]),
        expected_outputs={f"output_{i}": f"pass-{i}" for i in range(1, 11)},
        env_vars={f"C{i}": str(i) for i in range(1, 11)}
    ))
    
    # Error Cases
    tests.append(TestCase(
        name="Exceed maximum conditions (11)",
        conditions=", ".join([f"C{i} == {i}" for i in range(1, 12)]),
        true_values=",".join([f"pass-{i}" for i in range(1, 12)]),
        false_values=",".join([f"fail-{i}" for i in range(1, 12)]),
        expected_outputs={},
        env_vars={f"C{i}": str(i) for i in range(1, 12)},
        should_fail=True,
        expected_error="Maximum number of conditions"
    ))
    
    tests.append(TestCase(
        name="Mismatched array lengths",
        conditions="SERVICE == game, ENVIRONMENT == qa",
        true_values="pass1",
        false_values="fail1,fail2",
        expected_outputs={},
        env_vars={"SERVICE": "game", "ENVIRONMENT": "qa"},
        should_fail=True,
        expected_error="must match"
    ))
    
    return tests


def main():
    """Main test execution"""
    print(f"{Colors.BOLD}🧪 Local Test Suite for Ternary Operator Action{Colors.NC}")
    
    # Determine the root directory (parent of tests directory or current if entrypoint.py exists)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir) if os.path.basename(script_dir) == 'tests' else script_dir
    
    # Check if entrypoint.py exists
    entrypoint_path = os.path.join(root_dir, 'entrypoint.py')
    if not os.path.exists(entrypoint_path):
        print(f"{Colors.RED}❌ Error: entrypoint.py not found{Colors.NC}")
        print(f"Looking in: {entrypoint_path}")
        print("Please run this script from the ternary-operator root directory or tests directory")
        return 1
    
    # Change to root directory for running tests
    original_dir = os.getcwd()
    os.chdir(root_dir)
    print(f"Working directory: {root_dir}\n")
    
    try:
        runner = TestRunner()
        
        # Create test suite
        runner.print_header("🔧 Creating Test Suite")
        tests = create_test_suite()
        print(f"Created {len(tests)} test cases")
        
        # Run tests by category
        categories = {
            "Comparison Operators": tests[0:6],
            "Logical Operators": tests[6:11],
            "IN Operator": tests[11:15],
            "Mixed Operators": tests[15:20],
            "Multiple Conditions": tests[20:23],
            "Error Cases": tests[23:25]
        }
        
        for category, category_tests in categories.items():
            runner.print_header(f"📋 {category}")
            for test in category_tests:
                runner.run_test(test)
        
        # Print summary
        runner.print_summary()
        
        return 0 if runner.failed_tests == 0 else 1
    
    finally:
        # Restore original directory
        os.chdir(original_dir)


if __name__ == "__main__":
    sys.exit(main())
