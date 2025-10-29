#!/usr/bin/env python3
"""
Ternary Operator Action - Entry Point
Evaluates multiple conditions and sets corresponding outputs.
"""

import sys
from src.evaluator import TernaryOperator


def main() -> int:
    """Entry point for the script."""
    operator = TernaryOperator()
    return operator.run()


if __name__ == '__main__':
    sys.exit(main())

