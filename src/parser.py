"""
Condition parser for handling complex condition strings.
"""

import re
from typing import List

COMMA_PLACEHOLDER = "<<<COMMA>>>"
IN_OPERATOR_PATTERN = re.compile(r'(\w+)\s+IN\s+', re.IGNORECASE)


class ConditionParser:
    """Parser for condition strings with support for IN operator and parentheses."""

    @staticmethod
    def _protect_in_commas(working_str: str) -> str:
        """Replace commas within IN operator values with a placeholder.

        Scans from right to left so earlier offsets remain valid.
        """
        matches = list(IN_OPERATOR_PATTERN.finditer(working_str))

        for match in reversed(matches):
            start = match.end()  # Position right after "WORD IN "
            end = len(working_str)

            i = start
            while i < len(working_str):
                # Check for && or ||
                if i < len(working_str) - 1 and working_str[i:i + 2] in ('&&', '||'):
                    end = i
                    break

                # Check for comma followed by a new condition
                if working_str[i] == ',':
                    remaining = working_str[i + 1:].lstrip()
                    if remaining and (
                        re.match(
                            r'\w+\s+(?:==|!=|<=|>=|<|>|IN|CONTAINS|EMPTY|NOT_EMPTY)',
                            remaining,
                            re.IGNORECASE,
                        )
                        or remaining.startswith('NOT ')
                    ):
                        end = i
                        break

                i += 1

            in_values = working_str[start:end]
            protected = in_values.replace(',', COMMA_PLACEHOLDER)
            working_str = working_str[:start] + protected + working_str[end:]

        return working_str

    @staticmethod
    def _split_top_level(text: str) -> List[str]:
        """Split *text* by top-level commas (not inside parentheses)."""
        conditions: List[str] = []
        current: List[str] = []
        parenthesis_depth = 0

        for char in text:
            if char == '(':
                parenthesis_depth += 1
                current.append(char)
            elif char == ')':
                parenthesis_depth -= 1
                current.append(char)
            elif char == ',' and parenthesis_depth == 0:
                cond = ''.join(current).strip()
                if cond:
                    conditions.append(cond)
                current = []
            else:
                current.append(char)

        # Append the last condition
        cond = ''.join(current).strip()
        if cond:
            conditions.append(cond)

        return conditions

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

        # Step 1-2: protect commas inside IN values
        working_str = ConditionParser._protect_in_commas(conditions_str)

        # Step 3: split by top-level commas
        conditions = ConditionParser._split_top_level(working_str)

        # Step 4: restore commas
        conditions = [c.replace(COMMA_PLACEHOLDER, ',') for c in conditions]

        return conditions
