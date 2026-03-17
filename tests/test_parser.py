"""Tests for src/parser.py"""

from src.parser import ConditionParser


class TestConditionParser:
    def test_empty_string(self):
        assert ConditionParser.parse('') == []

    def test_single_condition(self):
        result = ConditionParser.parse('SERVICE == game')
        assert result == ['SERVICE == game']

    def test_multiple_conditions(self):
        result = ConditionParser.parse('SERVICE == game, ENVIRONMENT == qa')
        assert result == ['SERVICE == game', 'ENVIRONMENT == qa']

    def test_in_operator_preserves_commas(self):
        result = ConditionParser.parse('SERVICE IN game,batch,api')
        assert result == ['SERVICE IN game,batch,api']

    def test_in_operator_with_other_condition(self):
        result = ConditionParser.parse('SERVICE IN game,batch,api, ENVIRONMENT == dev')
        assert result == ['SERVICE IN game,batch,api', 'ENVIRONMENT == dev']

    def test_in_operator_with_logical_and(self):
        result = ConditionParser.parse('SERVICE IN game,batch && ENV == qa, TEST == prod')
        assert result == ['SERVICE IN game,batch && ENV == qa', 'TEST == prod']

    def test_not_operator_with_in(self):
        result = ConditionParser.parse('NOT (SERVICE IN batch,api), ENVIRONMENT == qa')
        assert result == ['NOT (SERVICE IN batch,api)', 'ENVIRONMENT == qa']

    def test_parentheses_preserved(self):
        result = ConditionParser.parse('NOT (SERVICE == game), TEST == prod')
        assert result == ['NOT (SERVICE == game)', 'TEST == prod']

    def test_contains_operator(self):
        result = ConditionParser.parse('BRANCH CONTAINS feature, ENV == qa')
        assert result == ['BRANCH CONTAINS feature', 'ENV == qa']

    def test_empty_not_empty_operators(self):
        result = ConditionParser.parse('VAR EMPTY, OTHER NOT_EMPTY')
        assert result == ['VAR EMPTY', 'OTHER NOT_EMPTY']

    def test_mixed_operators(self):
        result = ConditionParser.parse(
            'BRANCH CONTAINS qa && SERVICE NOT_EMPTY, NOT (SERVICE IN batch,api)'
        )
        assert result == [
            'BRANCH CONTAINS qa && SERVICE NOT_EMPTY',
            'NOT (SERVICE IN batch,api)'
        ]

    def test_ten_conditions(self):
        conditions = ', '.join([f'C{i} == {i}' for i in range(1, 11)])
        result = ConditionParser.parse(conditions)
        assert len(result) == 10

    def test_whitespace_trimming(self):
        result = ConditionParser.parse('  SERVICE == game  ,  ENV == qa  ')
        assert result == ['SERVICE == game', 'ENV == qa']

    def test_unmatched_parentheses_still_parses(self):
        """Unmatched parentheses should not crash, just parse best-effort."""
        result = ConditionParser.parse('NOT (SERVICE == game, ENV == qa')
        assert len(result) >= 1

    def test_nested_parentheses(self):
        result = ConditionParser.parse('NOT (A == B && (C == D)), E == F')
        assert result == ['NOT (A == B && (C == D))', 'E == F']
