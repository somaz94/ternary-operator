"""Tests for src/operators.py"""

import os
from unittest.mock import patch
import pytest
from src.operators import (
    InOperatorEvaluator, ContainsOperatorEvaluator, StartsEndsWithOperatorEvaluator,
    MatchesOperatorEvaluator, EmptyOperatorEvaluator,
)


class TestInOperatorEvaluator:
    def setup_method(self):
        self.evaluator = InOperatorEvaluator(debug_mode=False)

    def test_match_found(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        assert self.evaluator.evaluate('SERVICE IN game,batch,api') is True

    def test_no_match(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'web')
        assert self.evaluator.evaluate('SERVICE IN game,batch,api') is False

    def test_single_value(self, monkeypatch):
        monkeypatch.setenv('ENV', 'prod')
        assert self.evaluator.evaluate('ENV IN prod') is True

    def test_case_sensitive(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        assert self.evaluator.evaluate('SERVICE IN Game,Batch') is False

    def test_unset_variable(self, monkeypatch):
        monkeypatch.delenv('UNDEFINED_VAR', raising=False)
        assert self.evaluator.evaluate('UNDEFINED_VAR IN a,b,c') is False

    def test_invalid_syntax(self):
        assert self.evaluator.evaluate('SERVICE game,batch') is False

    def test_multiple_values(self, monkeypatch):
        monkeypatch.setenv('ENV', 'qa')
        assert self.evaluator.evaluate('ENV IN dev,qa,stage,prod') is True

    def test_debug_mode(self, monkeypatch, capsys):
        evaluator = InOperatorEvaluator(debug_mode=True)
        monkeypatch.setenv('SERVICE', 'game')
        evaluator.evaluate('SERVICE IN game,batch')
        captured = capsys.readouterr()
        assert 'Debug' in captured.out


class TestContainsOperatorEvaluator:
    def setup_method(self):
        self.evaluator = ContainsOperatorEvaluator(debug_mode=False)

    def test_substring_found(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'feature/new-login')
        assert self.evaluator.evaluate('BRANCH CONTAINS feature') is True

    def test_no_match(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'feature/new-login')
        assert self.evaluator.evaluate('BRANCH CONTAINS hotfix') is False

    def test_case_sensitive(self, monkeypatch):
        monkeypatch.setenv('MSG', 'feature: add login')
        assert self.evaluator.evaluate('MSG CONTAINS Feature') is False

    def test_exact_match(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'main')
        assert self.evaluator.evaluate('BRANCH CONTAINS main') is True

    def test_empty_variable(self, monkeypatch):
        monkeypatch.setenv('BRANCH', '')
        assert self.evaluator.evaluate('BRANCH CONTAINS feature') is False

    def test_unset_variable(self, monkeypatch):
        monkeypatch.delenv('UNDEFINED', raising=False)
        assert self.evaluator.evaluate('UNDEFINED CONTAINS test') is False

    def test_invalid_syntax(self):
        assert self.evaluator.evaluate('BRANCH feature') is False


class TestStartsEndsWithOperatorEvaluator:
    def setup_method(self):
        self.evaluator = StartsEndsWithOperatorEvaluator(debug_mode=False)

    def test_starts_with_match(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'feature/new-login')
        assert self.evaluator.evaluate('BRANCH STARTS_WITH feature/') is True

    def test_starts_with_no_match(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'hotfix/bug')
        assert self.evaluator.evaluate('BRANCH STARTS_WITH feature/') is False

    def test_ends_with_match(self, monkeypatch):
        monkeypatch.setenv('FILE', 'config.yml')
        assert self.evaluator.evaluate('FILE ENDS_WITH .yml') is True

    def test_ends_with_no_match(self, monkeypatch):
        monkeypatch.setenv('FILE', 'config.json')
        assert self.evaluator.evaluate('FILE ENDS_WITH .yml') is False

    def test_unset_variable(self, monkeypatch):
        monkeypatch.delenv('UNDEFINED', raising=False)
        assert self.evaluator.evaluate('UNDEFINED STARTS_WITH test') is False

    def test_case_insensitive(self, monkeypatch):
        evaluator = StartsEndsWithOperatorEvaluator(debug_mode=False, case_sensitive=False)
        monkeypatch.setenv('BRANCH', 'Feature/login')
        assert evaluator.evaluate('BRANCH STARTS_WITH feature/') is True

    def test_invalid_syntax(self):
        assert self.evaluator.evaluate('BRANCH something') is False

    def test_debug_mode(self, monkeypatch, capsys):
        evaluator = StartsEndsWithOperatorEvaluator(debug_mode=True)
        monkeypatch.setenv('BRANCH', 'feature/test')
        evaluator.evaluate('BRANCH STARTS_WITH feature/')
        captured = capsys.readouterr()
        assert 'Debug' in captured.out


class TestMatchesOperatorEvaluator:
    def setup_method(self):
        self.evaluator = MatchesOperatorEvaluator(debug_mode=False)

    def test_simple_match(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'feature/new-login')
        assert self.evaluator.evaluate('BRANCH MATCHES ^feature/.*') is True

    def test_no_match(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'main')
        assert self.evaluator.evaluate('BRANCH MATCHES ^feature/.*') is False

    def test_semver_pattern(self, monkeypatch):
        monkeypatch.setenv('TAG', 'v1.2.3')
        assert self.evaluator.evaluate(r'TAG MATCHES ^v[0-9]+\.[0-9]+\.[0-9]+$') is True

    def test_semver_no_match(self, monkeypatch):
        monkeypatch.setenv('TAG', 'latest')
        assert self.evaluator.evaluate(r'TAG MATCHES ^v[0-9]+\.[0-9]+\.[0-9]+$') is False

    def test_partial_match(self, monkeypatch):
        monkeypatch.setenv('MSG', 'fix: resolve login bug')
        assert self.evaluator.evaluate('MSG MATCHES fix:') is True

    def test_unset_variable(self, monkeypatch):
        monkeypatch.delenv('UNDEFINED', raising=False)
        assert self.evaluator.evaluate('UNDEFINED MATCHES ^test$') is False

    def test_invalid_regex(self, monkeypatch):
        monkeypatch.setenv('VAR', 'test')
        assert self.evaluator.evaluate('VAR MATCHES [invalid') is False

    def test_invalid_syntax(self):
        assert self.evaluator.evaluate('BRANCH something') is False

    def test_debug_mode(self, monkeypatch, capsys):
        evaluator = MatchesOperatorEvaluator(debug_mode=True)
        monkeypatch.setenv('BRANCH', 'feature/test')
        evaluator.evaluate('BRANCH MATCHES ^feature/')
        captured = capsys.readouterr()
        assert 'Debug' in captured.out


class TestEmptyOperatorEvaluator:
    def setup_method(self):
        self.evaluator = EmptyOperatorEvaluator(debug_mode=False)

    def test_empty_string(self, monkeypatch):
        monkeypatch.setenv('VAR', '')
        assert self.evaluator.evaluate('VAR EMPTY') is True

    def test_not_set(self, monkeypatch):
        monkeypatch.delenv('UNSET_VAR', raising=False)
        assert self.evaluator.evaluate('UNSET_VAR EMPTY') is True

    def test_has_value(self, monkeypatch):
        monkeypatch.setenv('VAR', 'some-value')
        assert self.evaluator.evaluate('VAR EMPTY') is False

    def test_not_empty_has_value(self, monkeypatch):
        monkeypatch.setenv('VAR', 'value')
        assert self.evaluator.evaluate('VAR NOT_EMPTY') is True

    def test_not_empty_empty_string(self, monkeypatch):
        monkeypatch.setenv('VAR', '')
        assert self.evaluator.evaluate('VAR NOT_EMPTY') is False

    def test_not_empty_not_set(self, monkeypatch):
        monkeypatch.delenv('UNSET_VAR', raising=False)
        assert self.evaluator.evaluate('UNSET_VAR NOT_EMPTY') is False

    def test_whitespace_only(self, monkeypatch):
        monkeypatch.setenv('VAR', '   ')
        assert self.evaluator.evaluate('VAR EMPTY') is True

    def test_debug_mode(self, monkeypatch, capsys):
        evaluator = EmptyOperatorEvaluator(debug_mode=True)
        monkeypatch.setenv('VAR', '')
        evaluator.evaluate('VAR EMPTY')
        captured = capsys.readouterr()
        assert 'Debug' in captured.out

    def test_invalid_empty_syntax(self):
        """Covers lines 243-244: invalid EMPTY syntax."""
        assert self.evaluator.evaluate(' EMPTY') is False


class TestOperatorExceptBlocks:
    """Tests to cover except blocks in operator evaluators (lines 79-81, 125-127, 165-167, 209-211, 263-265)."""

    def test_in_operator_exception(self, monkeypatch):
        evaluator = InOperatorEvaluator(debug_mode=False)
        monkeypatch.setenv('SERVICE', 'game')
        with patch.object(evaluator, 'get_var_value', side_effect=AttributeError("mock")):
            assert evaluator.evaluate('SERVICE IN game,batch') is False

    def test_contains_operator_exception(self, monkeypatch):
        evaluator = ContainsOperatorEvaluator(debug_mode=False)
        monkeypatch.setenv('BRANCH', 'feature/test')
        with patch.object(evaluator, 'get_var_value', side_effect=ValueError("mock")):
            assert evaluator.evaluate('BRANCH CONTAINS feature') is False

    def test_starts_ends_with_exception(self, monkeypatch):
        evaluator = StartsEndsWithOperatorEvaluator(debug_mode=False)
        monkeypatch.setenv('BRANCH', 'feature/test')
        with patch.object(evaluator, 'get_var_value', side_effect=AttributeError("mock")):
            assert evaluator.evaluate('BRANCH STARTS_WITH feature/') is False

    def test_matches_operator_value_error(self, monkeypatch):
        evaluator = MatchesOperatorEvaluator(debug_mode=False)
        monkeypatch.setenv('VAR', 'test')
        with patch.object(evaluator, 'get_var_value', side_effect=ValueError("mock")):
            assert evaluator.evaluate('VAR MATCHES ^test$') is False

    def test_empty_operator_exception(self, monkeypatch):
        evaluator = EmptyOperatorEvaluator(debug_mode=False)
        monkeypatch.setenv('VAR', 'test')
        with patch.object(evaluator, 'get_var_value', side_effect=AttributeError("mock")):
            assert evaluator.evaluate('VAR EMPTY') is False
