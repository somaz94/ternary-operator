"""Tests for src/operators.py"""

import os
import pytest
from src.operators import InOperatorEvaluator, ContainsOperatorEvaluator, EmptyOperatorEvaluator


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
