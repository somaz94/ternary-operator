"""
Main evaluator class for the Ternary Operator Action.
"""

import operator
import os
import re
import sys

from .colors import Colors
from .parser import ConditionParser
from .operators import InOperatorEvaluator, ContainsOperatorEvaluator, EmptyOperatorEvaluator


class TernaryOperator:
    """Main class for evaluating conditions and setting outputs."""

    MAX_CONDITIONS = 10
    MAX_RECURSION_DEPTH = 50
    COMPARISON_OPS = {
        '==': operator.eq,
        '!=': operator.ne,
        '<=': operator.le,
        '>=': operator.ge,
        '<': operator.lt,
        '>': operator.gt,
    }
    
    def __init__(self):
        """Initialize with environment variables."""
        self.debug_mode = os.getenv('INPUT_DEBUG_MODE', 'false').lower() == 'true'
        self.conditions = os.getenv('INPUT_CONDITIONS', '')
        self.true_values = os.getenv('INPUT_TRUE_VALUES', '')
        self.false_values = os.getenv('INPUT_FALSE_VALUES', '')
        self.github_output = os.getenv('GITHUB_OUTPUT', '')
        
        # Initialize operator evaluators
        self.in_evaluator = InOperatorEvaluator(self.debug_mode)
        self.contains_evaluator = ContainsOperatorEvaluator(self.debug_mode)
        self.empty_evaluator = EmptyOperatorEvaluator(self.debug_mode)
    
    def print_header(self, message: str) -> None:
        """Print a formatted header."""
        print(f"\n{'=' * 50}")
        print(f"  {message}")
        print(f"{'=' * 50}\n")
    
    def print_debug(self, message: str) -> None:
        """Print debug message if debug mode is enabled."""
        if self.debug_mode:
            print(f"{Colors.OKCYAN}• Debug: {message}{Colors.ENDC}")
    
    def print_error(self, message: str) -> None:
        """Print error message and exit."""
        print(f"{Colors.FAIL}Error: {message}{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)
    
    def print_success(self, message: str) -> None:
        """Print success message."""
        print(f"{Colors.OKGREEN}Success: {message}{Colors.ENDC}")
    
    def safe_write_output(self, key: str, value: str) -> None:
        """Safely write output to both stdout and GITHUB_OUTPUT."""
        output_line = f"{key}={value}"
        print(output_line)
        
        if self.github_output:
            try:
                with open(self.github_output, 'a') as f:
                    f.write(f"{output_line}\n")
            except IOError as e:
                self.print_debug(f"Warning: Could not write to GITHUB_OUTPUT: {e}")
    
    def validate_inputs(self) -> None:
        """Validate all required inputs."""
        missing_inputs = []
        
        if not self.conditions:
            missing_inputs.append('CONDITIONS')
        if not self.true_values:
            missing_inputs.append('TRUE_VALUES')
        if not self.false_values:
            missing_inputs.append('FALSE_VALUES')
        
        if missing_inputs:
            self.print_error(f"Missing required inputs: {', '.join(missing_inputs)}")
        
        # Validate debug_mode format
        debug_input = os.getenv('INPUT_DEBUG_MODE', 'false').lower()
        if debug_input not in ('true', 'false'):
            self.print_error("DEBUG_MODE must be either 'true' or 'false'")
        
        # DEBUG: Print raw conditions
        if self.debug_mode:
            print(f"• Debug: Raw conditions string: '{self.conditions}'")
        
        # Validate maximum conditions
        conditions_list = ConditionParser.parse(self.conditions)
        
        if self.debug_mode:
            print(f"• Debug: Parsed {len(conditions_list)} conditions:")
            for i, cond in enumerate(conditions_list, 1):
                print(f"  {i}. {cond}")
        
        if len(conditions_list) > self.MAX_CONDITIONS:
            self.print_error(
                f"Maximum number of conditions ({self.MAX_CONDITIONS}) exceeded. "
                f"Found {len(conditions_list)} conditions"
            )
    
    def get_var_value(self, varname: str) -> str:
        """Get environment variable value."""
        value = os.getenv(varname, '')
        if not value:
            self.print_debug(f"Warning: Variable {varname} is not set or empty")
        return value
    
    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Check if a string value is numeric (int or float)."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _parse_comparison(self, condition: str):
        """Parse a simple comparison condition into (left, op, right).

        Returns a tuple of (left_value, operator_str, right_value) or None if
        no comparison operator is found.
        """
        # Match operators in order: longest first to avoid <= matching as <
        for op in ('<=', '>=', '!=', '==', '<', '>'):
            if f' {op} ' in condition:
                parts = condition.split(f' {op} ', 1)
                if len(parts) == 2:
                    left_raw = parts[0].strip()
                    right_raw = parts[1].strip()

                    # Resolve environment variables (uppercase names)
                    left_val = self.get_var_value(left_raw) if re.match(r'^[A-Z][A-Z0-9_]*$', left_raw) else left_raw
                    right_val = self.get_var_value(right_raw) if re.match(r'^[A-Z][A-Z0-9_]*$', right_raw) else right_raw

                    self.print_debug(f"Comparison: '{left_val}' {op} '{right_val}'")
                    return left_val, op, right_val
        return None
    
    def _evaluate_logical(self, condition: str, op: str, aggregator) -> bool:
        """Evaluate a logical operator (|| or &&) by splitting and aggregating results."""
        parts = condition.split(op)
        return aggregator(
            self.evaluate_condition(part.strip(), self._depth + 1)
            for part in parts
        )

    def evaluate_condition(self, condition: str, depth: int = 0) -> bool:
        """Evaluate a single condition with support for all operators."""
        self._depth = depth
        if depth >= self.MAX_RECURSION_DEPTH:
            self.print_debug(f"Max recursion depth ({self.MAX_RECURSION_DEPTH}) exceeded")
            return False

        # Handle NOT operator first (highest priority)
        if condition.strip().upper().startswith('NOT '):
            inner_condition = condition[4:].strip()
            # Remove surrounding parentheses if present
            if inner_condition.startswith('(') and inner_condition.endswith(')'):
                inner_condition = inner_condition[1:-1].strip()
            result = self.evaluate_condition(inner_condition, depth + 1)
            self.print_debug(f"NOT operator: negating {result} -> {not result}")
            return not result

        # Check if condition contains logical operators (|| or &&)
        if '||' in condition:
            return self._evaluate_logical(condition, '||', any)
        if '&&' in condition:
            return self._evaluate_logical(condition, '&&', all)

        # Check for IN operator
        if ' IN ' in condition.upper():
            return self.in_evaluator.evaluate(condition)

        # Check for CONTAINS operator
        if ' CONTAINS ' in condition.upper():
            return self.contains_evaluator.evaluate(condition)

        # Check for EMPTY/NOT_EMPTY operators
        if ' EMPTY' in condition.upper() or ' NOT_EMPTY' in condition.upper():
            return self.empty_evaluator.evaluate(condition)

        # Simple comparison operator
        parsed = self._parse_comparison(condition)
        if parsed is None:
            self.print_debug(f"No valid operator found in condition: '{condition}'")
            return False

        left_val, op_str, right_val = parsed
        op_func = self.COMPARISON_OPS.get(op_str)
        if op_func is None:
            self.print_debug(f"Unsupported operator: '{op_str}'")
            return False

        try:
            # Compare as numbers if both sides are numeric
            if self._is_numeric(left_val) and self._is_numeric(right_val):
                result = op_func(float(left_val), float(right_val))
            else:
                result = op_func(left_val, right_val)
            self.print_debug(f"Result: '{left_val}' {op_str} '{right_val}' = {result}")
            return bool(result)
        except (TypeError, ValueError) as e:
            self.print_debug(f"Error evaluating condition '{condition}': {e}")
            return False
    
    def evaluate_conditions(self) -> None:
        """Evaluate all conditions and set outputs."""
        # Parse conditions
        conditions_list = ConditionParser.parse(self.conditions)
        true_values_list = [v.strip() for v in self.true_values.split(',') if v.strip()]
        false_values_list = [v.strip() for v in self.false_values.split(',') if v.strip()]
        
        # Validate array lengths match
        if len(conditions_list) != len(true_values_list) or len(conditions_list) != len(false_values_list):
            self.print_error(
                f"Number of conditions ({len(conditions_list)}), "
                f"true values ({len(true_values_list)}), "
                f"and false values ({len(false_values_list)}) must match"
            )
        
        self.print_debug(f"Processing {len(conditions_list)} conditions")
        
        for i, condition in enumerate(conditions_list, 1):
            print(f"\nEvaluating Condition {i}: {condition}")
            
            # Evaluate the condition
            if self.evaluate_condition(condition):
                result = true_values_list[i - 1]
                self.print_success(f"Condition {i} is TRUE")
            else:
                result = false_values_list[i - 1]
                self.print_debug(f"Condition {i} is FALSE")
            
            self.safe_write_output(f"output_{i}", result)
    
    def run(self) -> int:
        """Main execution method."""
        try:
            self.print_header("Condition Evaluator")
            
            self.print_debug("Starting validation")
            self.validate_inputs()
            
            self.print_debug("Starting condition evaluation")
            self.evaluate_conditions()
            
            self.print_header("Process Completed Successfully")
            return 0
        
        except (ValueError, TypeError, IOError, OSError) as e:
            self.print_error(f"Script execution failed: {e}")
            return 1
