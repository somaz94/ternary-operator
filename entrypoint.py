#!/usr/bin/env python3
"""
Ternary Operator Action - Python Implementation
Evaluates multiple conditions and sets corresponding outputs.
"""

import os
import re
import sys
import subprocess
from typing import List, Tuple, Optional


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


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
        
        # Validate maximum conditions
        conditions_list = [c.strip() for c in self.conditions.split(',') if c.strip()]
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
        """Process a condition by replacing variables and values with quoted strings."""
        processed = condition
        
        # First, find and replace all uppercase variable names (environment variables)
        variables = re.findall(r'\b[A-Z_]+\b', condition)
        for varname in variables:
            value = self.get_var_value(varname)
            if value:
                self.print_debug(f"Variable {varname} = {value}")
                processed = processed.replace(varname, f'"{value}"')
        
        # Then, find all unquoted lowercase/mixed-case words and quote them
        # This handles comparison values like: game, batch, dev, prod, etc.
        # Pattern matches words that are not already in quotes
        processed = re.sub(r'(?<!")(?<!\w)([a-z_][a-z0-9_-]*)(?!")(?!\w)', r'"\1"', processed)
        
        return processed
    
    def evaluate_condition(self, condition: str) -> bool:
        """Evaluate a single condition with support for ||, &&, ==, !=, <, >, <=, >= operators."""
        processed_condition = self.process_condition(condition)
        self.print_debug(f"Processed condition: {processed_condition}")
        
        try:
            # Replace bash-style operators with Python operators
            eval_condition = processed_condition
            eval_condition = eval_condition.replace('||', ' or ')
            eval_condition = eval_condition.replace('&&', ' and ')
            eval_condition = eval_condition.replace('!=', '!=')
            eval_condition = eval_condition.replace('==', '==')
            
            self.print_debug(f"Evaluating: {eval_condition}")
            
            # Safely evaluate the condition
            result = eval(eval_condition)
            return bool(result)
            
        except Exception as e:
            self.print_debug(f"Error evaluating condition '{condition}': {e}")
            return False
    
    def evaluate_conditions(self) -> None:
        """Evaluate all conditions and set outputs."""
        conditions_list = [c.strip() for c in self.conditions.split(',') if c.strip()]
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


def main() -> int:
    """Entry point for the script."""
    operator = TernaryOperator()
    return operator.run()


if __name__ == '__main__':
    sys.exit(main())
