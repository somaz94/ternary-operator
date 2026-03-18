"""
Operator evaluators for different condition types.
"""

import os
import re

from .colors import Colors


class OperatorEvaluator:
    """Base class for operator evaluation logic."""

    def __init__(self, debug_mode: bool = False, case_sensitive: bool = True):
        self.debug_mode = debug_mode
        self.case_sensitive = case_sensitive

    def _normalize(self, value: str) -> str:
        """Normalize value based on case sensitivity setting."""
        return value if self.case_sensitive else value.lower()

    def print_debug(self, message: str) -> None:
        """Print debug message if debug mode is enabled."""
        if self.debug_mode:
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
            result = self._normalize(var_value) in [self._normalize(v) for v in allowed_values]
            self.print_debug(f"IN operator result: {result}")
            
            return result
            
        except (ValueError, KeyError, AttributeError) as e:
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
            
            # Check if left contains right
            result = self._normalize(right_value) in self._normalize(left_value)
            self.print_debug(f"CONTAINS operator result: {result}")
            
            return result
            
        except (ValueError, KeyError, AttributeError) as e:
            self.print_debug(f"Error evaluating CONTAINS operator '{condition}': {e}")
            return False


class StartsEndsWithOperatorEvaluator(OperatorEvaluator):
    """Evaluator for STARTS_WITH and ENDS_WITH operators."""

    def evaluate(self, condition: str) -> bool:
        """
        Evaluate STARTS_WITH or ENDS_WITH operator condition.

        Examples:
            'BRANCH STARTS_WITH feature/' -> checks if BRANCH starts with 'feature/'
            'FILE ENDS_WITH .yml' -> checks if FILE ends with '.yml'
        """
        try:
            is_starts = 'STARTS_WITH' in condition
            op_name = 'STARTS_WITH' if is_starts else 'ENDS_WITH'

            parts = re.split(rf'\s+{op_name}\s+', condition, maxsplit=1)
            if len(parts) != 2:
                self.print_debug(f"Invalid {op_name} operator syntax: {condition}")
                return False

            var_name = parts[0].strip()
            target = parts[1].strip()

            var_value = self.get_var_value(var_name)

            self.print_debug(f"Checking if {var_name}='{var_value}' {op_name} '{target}'")

            left = self._normalize(var_value)
            right = self._normalize(target)

            result = left.startswith(right) if is_starts else left.endswith(right)
            self.print_debug(f"{op_name} operator result: {result}")

            return result

        except (ValueError, KeyError, AttributeError) as e:
            self.print_debug(f"Error evaluating {op_name} operator '{condition}': {e}")
            return False


class MatchesOperatorEvaluator(OperatorEvaluator):
    """Evaluator for MATCHES operator (regex pattern matching)."""

    def evaluate(self, condition: str) -> bool:
        """
        Evaluate MATCHES operator condition using regex.

        Examples:
            'BRANCH MATCHES ^feature/.*' -> checks if BRANCH matches the regex
            'TAG MATCHES ^v[0-9]+\\.[0-9]+\\.[0-9]+$' -> checks if TAG is a semver tag

        Args:
            condition: Condition string with MATCHES operator

        Returns:
            True if variable value matches the regex pattern, False otherwise
        """
        try:
            parts = re.split(r'\s+MATCHES\s+', condition, maxsplit=1)
            if len(parts) != 2:
                self.print_debug(f"Invalid MATCHES operator syntax: {condition}")
                return False

            var_name = parts[0].strip()
            pattern = parts[1].strip()

            var_value = self.get_var_value(var_name)

            self.print_debug(f"Checking if {var_name}='{var_value}' MATCHES '{pattern}'")

            flags = 0 if self.case_sensitive else re.IGNORECASE
            result = bool(re.search(pattern, var_value, flags))
            self.print_debug(f"MATCHES operator result: {result}")

            return result

        except re.error as e:
            self.print_debug(f"Invalid regex pattern '{pattern}': {e}")
            return False
        except (ValueError, KeyError, AttributeError) as e:
            self.print_debug(f"Error evaluating MATCHES operator '{condition}': {e}")
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
            
        except (ValueError, KeyError, AttributeError) as e:
            self.print_debug(f"Error evaluating EMPTY/NOT_EMPTY operator '{condition}': {e}")
            return False
