"""
Condition parser for handling complex condition strings.
"""

import re
from typing import List


class ConditionParser:
    """Parser for condition strings with support for IN operator and parentheses."""
    
    @staticmethod
    def parse(conditions_str: str) -> List[str]:
        """
        Parse conditions string handling IN operator with commas and all operators.
        
        Strategy:
        1. Find all IN operators and their values (e.g., "VAR IN val1,val2,val3")
        2. Replace commas within IN values with a placeholder
        3. Split by comma only at top-level (not inside parentheses or logical operators)
        4. Restore the commas in IN values
        
        Examples:
        - "SERVICE IN game,batch,api, ENVIRONMENT == dev"
          → ["SERVICE IN game,batch,api", "ENVIRONMENT == dev"]
        - "SERVICE IN game,batch && ENV == qa, TEST == prod"
          → ["SERVICE IN game,batch && ENV == qa", "TEST == prod"]
        - "BRANCH CONTAINS qa && SERVICE NOT_EMPTY, NOT (SERVICE IN batch,api)"
          → ["BRANCH CONTAINS qa && SERVICE NOT_EMPTY", "NOT (SERVICE IN batch,api)"]
        
        Args:
            conditions_str: Raw conditions string
            
        Returns:
            List of individual condition strings
        """
        if not conditions_str:
            return []
        
        # Placeholder for commas inside IN operators
        COMMA_PLACEHOLDER = "<<<COMMA>>>"
        
        working_str = conditions_str
        
        # Find and protect commas within IN operators using a simpler approach
        # Look for pattern: WORD IN value1,value2,value3
        # Stop at: &&, ||, comma+space+word+operator, or end
        
        # Simple pattern to find IN operators
        # Match: word IN anything until we hit a boundary
        in_pattern = r'(\w+)\s+IN\s+'
        
        # Find all IN operator positions
        matches = list(re.finditer(in_pattern, working_str, re.IGNORECASE))
        
        # Process from right to left to avoid offset issues
        for match in reversed(matches):
            start = match.end()  # Start after "WORD IN "
            
            # Find where the IN values end
            # They end at: &&, ||, or comma followed by new condition
            end = len(working_str)
            
            # Look for terminators
            i = start
            while i < len(working_str):
                # Check for && or ||
                if i < len(working_str) - 1:
                    two_char = working_str[i:i+2]
                    if two_char in ['&&', '||']:
                        end = i
                        break
                
                # Check for comma followed by likely new condition
                if working_str[i] == ',':
                    # Look ahead to see if this is a condition separator
                    remaining = working_str[i+1:].lstrip()
                    # Check if next part looks like a new condition
                    # (starts with word or NOT followed by operator or parenthesis)
                    if remaining and (
                        re.match(r'\w+\s+(?:==|!=|<=|>=|<|>|IN|CONTAINS|EMPTY|NOT_EMPTY)', remaining, re.IGNORECASE) or
                        remaining.startswith('NOT ')
                    ):
                        end = i
                        break
                
                i += 1
            
            # Replace commas in this IN value section
            in_values = working_str[start:end]
            protected_values = in_values.replace(',', COMMA_PLACEHOLDER)
            working_str = working_str[:start] + protected_values + working_str[end:]
        
        # Now split by comma to get individual conditions
        # Only split at top-level commas (not inside parentheses)
        conditions = []
        current = []
        paren_depth = 0
        
        i = 0
        while i < len(working_str):
            char = working_str[i]
            
            if char == '(':
                paren_depth += 1
                current.append(char)
            elif char == ')':
                paren_depth -= 1
                current.append(char)
            elif char == ',' and paren_depth == 0:
                # Top-level comma - split here
                cond = ''.join(current).strip()
                if cond:
                    conditions.append(cond)
                current = []
            else:
                current.append(char)
            
            i += 1
        
        # Add the last condition
        cond = ''.join(current).strip()
        if cond:
            conditions.append(cond)
        
        # Restore commas in IN operators
        conditions = [c.replace(COMMA_PLACEHOLDER, ',') for c in conditions]
        
        return conditions
