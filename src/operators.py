"""
Operator evaluators for different condition types.
"""

import os
import re
from typing import Optional


class OperatorEvaluator:
    """Base class for operator evaluation logic."""
    
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
    
    def print_debug(self, message: str) -> None:
        """Print debug message if debug mode is enabled."""
        if self.debug_mode:
            from .colors import Colors
            print(f"{Colors.OKCYAN}• Debug: {message}{Colors.ENDC}")
    
    def get_var_value(self, varname: str) -> str:
        """Get environment variable value."""
        value = os.getenv(varname, '')
        if not value:
            self.print_debug(f"Warning: Variable {varname} is not set or empty")
        return value


class InOperatorEvaluator(OperatorEvaluator):
    """Evaluator for IN operator."""
    
    def evaluate(self, condition: str) -> bool:
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


class ContainsOperatorEvaluator(OperatorEvaluator):
    """Evaluator for CONTAINS operator."""
    
    def evaluate(self, condition: str) -> bool:
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


class EmptyOperatorEvaluator(OperatorEvaluator):
    """Evaluator for EMPTY and NOT_EMPTY operators."""
    
    def evaluate(self, condition: str) -> bool:
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
