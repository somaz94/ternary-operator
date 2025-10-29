"""
Main evaluator class for the Ternary Operator Action.
"""

import os
import re
import sys
from typing import List

from .colors import Colors
from .parser import ConditionParser
from .operators import InOperatorEvaluator, ContainsOperatorEvaluator, EmptyOperatorEvaluator


class TernaryOperator:
    """Main class for evaluating conditions and setting outputs."""
    
    MAX_CONDITIONS = 10
    
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
        print(f"▶️ {message}")
        print(f"{'=' * 50}\n")
    
    def print_debug(self, message: str) -> None:
        """Print debug message if debug mode is enabled."""
        if self.debug_mode:
            print(f"{Colors.OKCYAN}• Debug: {message}{Colors.ENDC}")
    
    def print_error(self, message: str) -> None:
        """Print error message and exit."""
        print(f"{Colors.FAIL}❌ Error: {message}{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)
    
    def print_success(self, message: str) -> None:
        """Print success message."""
        print(f"{Colors.OKGREEN}✅ Success: {message}{Colors.ENDC}")
    
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
    
    def process_condition(self, condition: str) -> str:
        """Process a condition by replacing variables and values with quoted strings or numbers."""
        processed = condition
        
        # First, find and replace all uppercase variable names (environment variables)
        # Pattern: starts with uppercase letter, can contain uppercase letters, numbers, and underscores
        variables = re.findall(r'\b[A-Z][A-Z0-9_]*\b', condition)
        for varname in variables:
            value = self.get_var_value(varname)
            if value:
                self.print_debug(f"Variable {varname} = {value}")
                # Check if value is numeric - if so, don't quote it
                if value.isdigit() or (value.replace('.', '', 1).isdigit() and value.count('.') <= 1):
                    # It's a number, don't quote
                    processed = processed.replace(varname, value)
                else:
                    # It's a string, quote it
                    processed = processed.replace(varname, f'"{value}"')
        
        # Then, find all unquoted lowercase/mixed-case words and quote them
        # This handles comparison values like: game, batch, dev, prod, etc.
        # But skip numeric values
        # Pattern matches words that are not already in quotes and not numbers
        def quote_if_not_number(match):
            word = match.group(1)
            # Don't quote if it's a number
            if word.isdigit() or (word.replace('.', '', 1).isdigit() and word.count('.') <= 1):
                return word
            return f'"{word}"'
        
        processed = re.sub(r'(?<!")(?<!\w)([a-z_][a-z0-9_.-]*)(?!")(?!\w)', quote_if_not_number, processed)
        
        return processed
    
    def evaluate_condition(self, condition: str) -> bool:
        """Evaluate a single condition with support for all operators."""
        # Handle NOT operator first (highest priority)
        if condition.strip().upper().startswith('NOT '):
            inner_condition = condition[4:].strip()
            # Remove surrounding parentheses if present
            if inner_condition.startswith('(') and inner_condition.endswith(')'):
                inner_condition = inner_condition[1:-1].strip()
            result = self.evaluate_condition(inner_condition)
            self.print_debug(f"NOT operator: negating {result} -> {not result}")
            return not result
        
        # Check if condition contains logical operators (|| or &&)
        if '||' in condition or '&&' in condition:
            # Split by logical operators and evaluate each part
            # Handle || (OR) - if any part is true, return true
            if '||' in condition:
                parts = condition.split('||')
                results = []
                for part in parts:
                    part = part.strip()
                    # Recursively evaluate each part (might contain &&)
                    result = self.evaluate_condition(part)
                    results.append(result)
                return any(results)
            
            # Handle && (AND) - all parts must be true
            if '&&' in condition:
                parts = condition.split('&&')
                results = []
                for part in parts:
                    part = part.strip()
                    # Recursively evaluate each part
                    result = self.evaluate_condition(part)
                    results.append(result)
                return all(results)
        
        # Check for IN operator (no logical operators at this point)
        if ' IN ' in condition.upper():
            return self.in_evaluator.evaluate(condition)
        
        # Check for CONTAINS operator
        if ' CONTAINS ' in condition.upper():
            return self.contains_evaluator.evaluate(condition)
        
        # Check for EMPTY/NOT_EMPTY operators
        if ' EMPTY' in condition.upper() or ' NOT_EMPTY' in condition.upper():
            return self.empty_evaluator.evaluate(condition)
        
        # Simple comparison operator
        processed_condition = self.process_condition(condition)
        self.print_debug(f"Processed condition: {processed_condition}")
        
        try:
            # Evaluate the simple comparison
            self.print_debug(f"Evaluating: {processed_condition}")
            result = eval(processed_condition)
            return bool(result)
            
        except Exception as e:
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
            print(f"\n📋 Evaluating Condition {i}: {condition}")
            
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
        
        except Exception as e:
            self.print_error(f"Script execution failed: {e}")
            return 1
