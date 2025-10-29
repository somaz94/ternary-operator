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
        
        # DEBUG: Print raw conditions
        if self.debug_mode:
            print(f"• Debug: Raw conditions string: '{self.conditions}'")
        
        # Validate maximum conditions
        conditions_list = self._parse_conditions(self.conditions)
        
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
        """Evaluate a single condition with support for ||, &&, ==, !=, <, >, <=, >=, IN, CONTAINS, NOT, EMPTY, NOT_EMPTY operators."""
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
            return self._evaluate_in_operator(condition)
        
        # Check for CONTAINS operator
        if ' CONTAINS ' in condition.upper():
            return self._evaluate_contains_operator(condition)
        
        # Check for EMPTY/NOT_EMPTY operators
        if ' EMPTY' in condition.upper() or ' NOT_EMPTY' in condition.upper():
            return self._evaluate_empty_operator(condition)
        
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
    
    def _evaluate_in_operator(self, condition: str) -> bool:
        """
        Evaluate IN operator condition.
        
        Examples:
            'SERVICE IN game,batch,api' -> checks if SERVICE is one of [game, batch, api]
            'ENV IN dev,qa,stage,prod' -> checks if ENV is one of [dev, qa, stage, prod]
        
        Args:
            condition: Condition string with IN operator
            
        Returns:
            True if variable value is in the list, False otherwise
        """
        try:
            # Split by IN operator
            parts = condition.split(' IN ')
            if len(parts) != 2:
                self.print_debug(f"Invalid IN operator syntax: {condition}")
                return False
            
            var_name = parts[0].strip()
            values_str = parts[1].strip()
            
            # Get variable value
            var_value = self.get_var_value(var_name)
            if not var_value:
                self.print_debug(f"Variable {var_name} is not set")
                return False
            
            # Parse comma-separated values
            allowed_values = [v.strip() for v in values_str.split(',') if v.strip()]
            
            self.print_debug(f"Checking if {var_name}='{var_value}' IN [{', '.join(allowed_values)}]")
            
            # Check if variable value is in the allowed values list
            result = var_value in allowed_values
            self.print_debug(f"IN operator result: {result}")
            
            return result
            
        except Exception as e:
            self.print_debug(f"Error evaluating IN operator '{condition}': {e}")
            return False
    
    def _evaluate_contains_operator(self, condition: str) -> bool:
        """
        Evaluate CONTAINS operator condition (case-sensitive).
        
        Examples:
            'BRANCH_NAME CONTAINS feature' -> checks if BRANCH_NAME contains 'feature'
            'MESSAGE CONTAINS hotfix' -> checks if MESSAGE contains 'hotfix'
        
        Args:
            condition: Condition string with CONTAINS operator
            
        Returns:
            True if left value contains right value, False otherwise
        """
        try:
            # Split by CONTAINS operator (case-insensitive split)
            parts = re.split(r'\s+CONTAINS\s+', condition, flags=re.IGNORECASE)
            if len(parts) != 2:
                self.print_debug(f"Invalid CONTAINS operator syntax: {condition}")
                return False
            
            left_part = parts[0].strip()
            right_part = parts[1].strip()
            
            # Get variable value for left side
            left_value = self.get_var_value(left_part)
            
            # Get variable value for right side, or use as literal
            right_value = self.get_var_value(right_part) if right_part.isupper() else right_part
            
            self.print_debug(f"Checking if '{left_value}' CONTAINS '{right_value}'")
            
            # Check if left contains right (case-sensitive)
            result = right_value in left_value
            self.print_debug(f"CONTAINS operator result: {result}")
            
            return result
            
        except Exception as e:
            self.print_debug(f"Error evaluating CONTAINS operator '{condition}': {e}")
            return False
    
    def _evaluate_empty_operator(self, condition: str) -> bool:
        """
        Evaluate EMPTY or NOT_EMPTY operator condition.
        
        Examples:
            'VAR EMPTY' -> checks if VAR is empty or not set
            'VAR NOT_EMPTY' -> checks if VAR is not empty
        
        Args:
            condition: Condition string with EMPTY or NOT_EMPTY operator
            
        Returns:
            True if condition is satisfied, False otherwise
        """
        try:
            # Check which operator is used
            is_not_empty = 'NOT_EMPTY' in condition.upper()
            
            if is_not_empty:
                # Split by NOT_EMPTY
                parts = re.split(r'\s+NOT_EMPTY\s*', condition, flags=re.IGNORECASE)
            else:
                # Split by EMPTY
                parts = re.split(r'\s+EMPTY\s*', condition, flags=re.IGNORECASE)
            
            if len(parts) < 1 or not parts[0].strip():
                self.print_debug(f"Invalid EMPTY/NOT_EMPTY operator syntax: {condition}")
                return False
            
            var_name = parts[0].strip()
            
            # Get variable value
            var_value = self.get_var_value(var_name)
            
            # Check if empty
            is_empty = not var_value or var_value.strip() == ''
            
            if is_not_empty:
                result = not is_empty
                self.print_debug(f"Checking if {var_name}='{var_value}' NOT_EMPTY: {result}")
            else:
                result = is_empty
                self.print_debug(f"Checking if {var_name}='{var_value}' EMPTY: {result}")
            
            return result
            
        except Exception as e:
            self.print_debug(f"Error evaluating EMPTY/NOT_EMPTY operator '{condition}': {e}")
            return False
    
    def evaluate_conditions(self) -> None:
        """Evaluate all conditions and set outputs."""
        # Parse conditions manually to handle IN operator with commas
        conditions_list = self._parse_conditions(self.conditions)
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
    
    def _parse_conditions(self, conditions_str: str) -> List[str]:
        """
        Parse conditions string handling IN operator with commas.
        
        Strategy:
        1. Find all IN operators and their values (e.g., "VAR IN val1,val2,val3")
        2. Replace commas within IN values with a placeholder
        3. Split by comma to get conditions
        4. Restore the commas in IN values
        
        Examples:
        - "SERVICE IN game,batch,api, ENVIRONMENT == dev"
          → ["SERVICE IN game,batch,api", "ENVIRONMENT == dev"]
        - "SERVICE IN game,batch && ENV == qa, TEST == prod"
          → ["SERVICE IN game,batch && ENV == qa", "TEST == prod"]
        
        Args:
            conditions_str: Raw conditions string
            
        Returns:
            List of individual condition strings
        """
        if not conditions_str:
            return []
        
        # Placeholder for commas inside IN operators
        COMMA_PLACEHOLDER = "<<<COMMA>>>"
        
        # Pattern to match IN operators with their values
        # Matches: VAR IN val1,val2,val3 (until we hit &&, ||, or end/comma followed by new condition)
        # We need to capture until we see a condition separator or logical operator not part of the current condition
        
        working_str = conditions_str
        
        # Find and protect commas within IN operators
        # Pattern: word IN word,word,word... (stop at &&, ||, or comma followed by new variable with operator)
        import re
        
        # This regex finds "VAR IN values" where values can contain commas
        # It stops when it encounters &&, ||, or a comma followed by whitespace and a word with operator
        pattern = r'(\w+)\s+IN\s+([^,]+(?:,[^,]+)*?)(?=\s*(?:&&|\|\||,\s*\w+\s*(?:==|!=|<=|>=|<|>|IN\s)|$))'
        
        def replace_in_commas(match):
            var_name = match.group(1)
            values = match.group(2)
            # Replace commas in the values part with placeholder
            protected_values = values.replace(',', COMMA_PLACEHOLDER)
            return f'{var_name} IN {protected_values}'
        
        # Protect commas in IN operators
        working_str = re.sub(pattern, replace_in_commas, working_str, flags=re.IGNORECASE)
        
        # Now split by comma to get individual conditions
        conditions = [c.strip() for c in working_str.split(',') if c.strip()]
        
        # Restore commas in IN operators
        conditions = [c.replace(COMMA_PLACEHOLDER, ',') for c in conditions]
        
        return conditions
    
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
