"""Tests for src/evaluator.py"""

import os
import pytest
from src.evaluator import TernaryOperator


class TestTernaryOperatorInit:
    def test_default_debug_mode(self, clean_env, monkeypatch):
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        op = TernaryOperator()
        assert op.debug_mode is False

    def test_debug_mode_true(self, clean_env, monkeypatch):
        monkeypatch.setenv('INPUT_DEBUG_MODE', 'true')
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        op = TernaryOperator()
        assert op.debug_mode is True

    def test_max_conditions_constant(self):
        assert TernaryOperator.MAX_CONDITIONS == 10


class TestValidateInputs:
    def test_missing_conditions(self, clean_env, monkeypatch):
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        op = TernaryOperator()
        with pytest.raises(SystemExit):
            op.validate_inputs()

    def test_missing_true_values(self, clean_env, monkeypatch):
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        op = TernaryOperator()
        with pytest.raises(SystemExit):
            op.validate_inputs()

    def test_missing_false_values(self, clean_env, monkeypatch):
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        op = TernaryOperator()
        with pytest.raises(SystemExit):
            op.validate_inputs()

    def test_exceed_max_conditions(self, clean_env, monkeypatch):
        conditions = ', '.join([f'C{i} == {i}' for i in range(1, 12)])
        monkeypatch.setenv('INPUT_CONDITIONS', conditions)
        monkeypatch.setenv('INPUT_TRUE_VALUES', ','.join(['y'] * 11))
        monkeypatch.setenv('INPUT_FALSE_VALUES', ','.join(['n'] * 11))
        for i in range(1, 12):
            monkeypatch.setenv(f'C{i}', str(i))
        op = TernaryOperator()
        with pytest.raises(SystemExit):
            op.validate_inputs()

    def test_valid_inputs(self, default_env):
        op = TernaryOperator()
        op.validate_inputs()


class TestGetVarValue:
    def test_existing_var(self, clean_env, monkeypatch):
        monkeypatch.setenv('INPUT_CONDITIONS', '')
        monkeypatch.setenv('INPUT_TRUE_VALUES', '')
        monkeypatch.setenv('INPUT_FALSE_VALUES', '')
        monkeypatch.setenv('MY_VAR', 'hello')
        op = TernaryOperator()
        assert op.get_var_value('MY_VAR') == 'hello'

    def test_missing_var(self, clean_env, monkeypatch):
        monkeypatch.setenv('INPUT_CONDITIONS', '')
        monkeypatch.setenv('INPUT_TRUE_VALUES', '')
        monkeypatch.setenv('INPUT_FALSE_VALUES', '')
        monkeypatch.delenv('MISSING_VAR', raising=False)
        op = TernaryOperator()
        assert op.get_var_value('MISSING_VAR') == ''


class TestEvaluateCondition:
    def setup_method(self):
        os.environ['INPUT_CONDITIONS'] = ''
        os.environ['INPUT_TRUE_VALUES'] = ''
        os.environ['INPUT_FALSE_VALUES'] = ''

    def test_equal_true(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == game') is True

    def test_equal_false(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'batch')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == game') is False

    def test_not_equal(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE != batch') is True

    def test_greater_than(self, monkeypatch):
        monkeypatch.setenv('COUNT', '10')
        op = TernaryOperator()
        assert op.evaluate_condition('COUNT > 5') is True

    def test_less_than(self, monkeypatch):
        monkeypatch.setenv('COUNT', '3')
        op = TernaryOperator()
        assert op.evaluate_condition('COUNT < 5') is True

    def test_greater_equal(self, monkeypatch):
        monkeypatch.setenv('COUNT', '10')
        op = TernaryOperator()
        assert op.evaluate_condition('COUNT >= 10') is True

    def test_less_equal(self, monkeypatch):
        monkeypatch.setenv('COUNT', '5')
        op = TernaryOperator()
        assert op.evaluate_condition('COUNT <= 5') is True

    def test_and_both_true(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        monkeypatch.setenv('ENV', 'qa')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == game && ENV == qa') is True

    def test_and_one_false(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        monkeypatch.setenv('ENV', 'qa')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == game && ENV == prod') is False

    def test_or_first_true(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == game || SERVICE == batch') is True

    def test_or_both_false(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'web')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == game || SERVICE == batch') is False

    def test_not_operator(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        assert op.evaluate_condition('NOT (SERVICE == batch)') is True

    def test_not_operator_negates_true(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        assert op.evaluate_condition('NOT (SERVICE == game)') is False

    def test_in_operator(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE IN game,batch,api') is True

    def test_contains_operator(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'feature/login')
        op = TernaryOperator()
        assert op.evaluate_condition('BRANCH CONTAINS feature') is True

    def test_empty_operator(self, monkeypatch):
        monkeypatch.delenv('UNDEFINED_VAR', raising=False)
        op = TernaryOperator()
        assert op.evaluate_condition('UNDEFINED_VAR EMPTY') is True

    def test_not_empty_operator(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE NOT_EMPTY') is True


class TestEvaluateConditions:
    def test_single_true_condition(self, clean_env, monkeypatch, github_output):
        monkeypatch.setenv('INPUT_CONDITIONS', 'SERVICE == game')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'pass')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'fail')
        monkeypatch.setenv('GITHUB_OUTPUT', github_output)
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        op.evaluate_conditions()
        with open(github_output) as f:
            content = f.read()
        assert 'output_1=pass' in content

    def test_single_false_condition(self, clean_env, monkeypatch, github_output):
        monkeypatch.setenv('INPUT_CONDITIONS', 'SERVICE == batch')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'pass')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'fail')
        monkeypatch.setenv('GITHUB_OUTPUT', github_output)
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        op.evaluate_conditions()
        with open(github_output) as f:
            content = f.read()
        assert 'output_1=fail' in content

    def test_multiple_conditions(self, clean_env, monkeypatch, github_output):
        monkeypatch.setenv('INPUT_CONDITIONS', 'SERVICE == game, ENV == prod')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'pass1,pass2')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'fail1,fail2')
        monkeypatch.setenv('GITHUB_OUTPUT', github_output)
        monkeypatch.setenv('SERVICE', 'game')
        monkeypatch.setenv('ENV', 'qa')
        op = TernaryOperator()
        op.evaluate_conditions()
        with open(github_output) as f:
            content = f.read()
        assert 'output_1=pass1' in content
        assert 'output_2=fail2' in content

    def test_mismatched_array_lengths(self, clean_env, monkeypatch):
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B, C == D')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no1,no2')
        op = TernaryOperator()
        with pytest.raises(SystemExit):
            op.evaluate_conditions()


class TestSafeWriteOutput:
    def test_writes_to_file(self, default_env):
        op = TernaryOperator()
        op.safe_write_output('test_key', 'test_value')
        with open(default_env) as f:
            content = f.read()
        assert 'test_key=test_value' in content

    def test_no_github_output(self, clean_env, monkeypatch, capsys):
        monkeypatch.setenv('INPUT_CONDITIONS', '')
        monkeypatch.setenv('INPUT_TRUE_VALUES', '')
        monkeypatch.setenv('INPUT_FALSE_VALUES', '')
        op = TernaryOperator()
        op.safe_write_output('key', 'value')
        captured = capsys.readouterr()
        assert 'key=value' in captured.out


class TestRun:
    def test_successful_run(self, default_env):
        op = TernaryOperator()
        result = op.run()
        assert result == 0

    def test_missing_inputs_exits(self, clean_env, monkeypatch):
        op = TernaryOperator()
        with pytest.raises(SystemExit):
            op.run()
