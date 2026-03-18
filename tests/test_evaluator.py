"""Tests for src/evaluator.py"""

import os
from unittest.mock import patch, PropertyMock
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


class TestIsNumeric:
    def test_integer(self):
        assert TernaryOperator._is_numeric('42') is True

    def test_float(self):
        assert TernaryOperator._is_numeric('3.14') is True

    def test_negative(self):
        assert TernaryOperator._is_numeric('-5') is True

    def test_string(self):
        assert TernaryOperator._is_numeric('game') is False

    def test_empty(self):
        assert TernaryOperator._is_numeric('') is False

    def test_mixed(self):
        assert TernaryOperator._is_numeric('1.2.3') is False


class TestParseComparison:
    def setup_method(self):
        os.environ['INPUT_CONDITIONS'] = ''
        os.environ['INPUT_TRUE_VALUES'] = ''
        os.environ['INPUT_FALSE_VALUES'] = ''

    def test_equal_operator(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        result = op._parse_comparison('SERVICE == game')
        assert result == ('game', '==', 'game')

    def test_not_equal_operator(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        result = op._parse_comparison('SERVICE != batch')
        assert result == ('game', '!=', 'batch')

    def test_less_equal_operator(self, monkeypatch):
        monkeypatch.setenv('VERSION', '1.5')
        op = TernaryOperator()
        result = op._parse_comparison('VERSION <= 2.0')
        assert result == ('1.5', '<=', '2.0')

    def test_greater_equal_operator(self, monkeypatch):
        monkeypatch.setenv('VERSION', '3.0')
        op = TernaryOperator()
        result = op._parse_comparison('VERSION >= 1.0')
        assert result == ('3.0', '>=', '1.0')

    def test_no_operator(self, monkeypatch):
        op = TernaryOperator()
        result = op._parse_comparison('SERVICE game')
        assert result is None

    def test_unset_variable(self, monkeypatch):
        monkeypatch.delenv('MISSING', raising=False)
        op = TernaryOperator()
        result = op._parse_comparison('MISSING == value')
        assert result == ('', '==', 'value')

    def test_lowercase_literal(self, monkeypatch):
        """Lowercase values are not resolved as env vars."""
        op = TernaryOperator()
        result = op._parse_comparison('hello == world')
        assert result == ('hello', '==', 'world')


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

    def test_no_valid_operator(self, monkeypatch):
        op = TernaryOperator()
        assert op.evaluate_condition('INVALID CONDITION') is False

    def test_float_comparison(self, monkeypatch):
        monkeypatch.setenv('VERSION', '1.5')
        op = TernaryOperator()
        assert op.evaluate_condition('VERSION >= 1.5') is True
        assert op.evaluate_condition('VERSION > 1.4') is True
        assert op.evaluate_condition('VERSION < 2.0') is True

    def test_string_comparison_fallback(self, monkeypatch):
        monkeypatch.setenv('SERVICE', 'batch')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == batch') is True
        assert op.evaluate_condition('SERVICE == game') is False


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


class TestCaseSensitive:
    def setup_method(self):
        os.environ['INPUT_CONDITIONS'] = ''
        os.environ['INPUT_TRUE_VALUES'] = ''
        os.environ['INPUT_FALSE_VALUES'] = ''

    def test_case_insensitive_comparison(self, monkeypatch):
        monkeypatch.setenv('INPUT_CASE_SENSITIVE', 'false')
        monkeypatch.setenv('SERVICE', 'Game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == game') is True

    def test_case_sensitive_comparison(self, monkeypatch):
        monkeypatch.setenv('INPUT_CASE_SENSITIVE', 'true')
        monkeypatch.setenv('SERVICE', 'Game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE == game') is False

    def test_case_insensitive_in_operator(self, monkeypatch):
        monkeypatch.setenv('INPUT_CASE_SENSITIVE', 'false')
        monkeypatch.setenv('SERVICE', 'Game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE IN game,batch') is True


class TestDefaultValues:
    def test_default_values_parsed(self, monkeypatch, tmp_path):
        gh_output = tmp_path / "output"
        gh_output.write_text("")
        monkeypatch.setenv('INPUT_CONDITIONS', 'SERVICE == game')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        monkeypatch.setenv('INPUT_DEFAULT_VALUES', 'fallback')
        monkeypatch.setenv('GITHUB_OUTPUT', str(gh_output))
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        op.validate_inputs()
        op.evaluate_conditions()
        content = gh_output.read_text()
        assert 'output_1=yes' in content


class TestResultJsonOutput:
    def test_result_json_output(self, monkeypatch, tmp_path):
        gh_output = tmp_path / "output"
        gh_output.write_text("")
        monkeypatch.setenv('INPUT_CONDITIONS', 'SERVICE == game, ENV == prod')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes,deploy')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no,skip')
        monkeypatch.setenv('GITHUB_OUTPUT', str(gh_output))
        monkeypatch.setenv('SERVICE', 'game')
        monkeypatch.setenv('ENV', 'staging')
        op = TernaryOperator()
        op.validate_inputs()
        op.evaluate_conditions()
        content = gh_output.read_text()
        assert 'output_1=yes' in content
        assert 'output_2=skip' in content
        assert '"output_1": "yes"' in content
        assert '"output_2": "skip"' in content


class TestNewOperatorsInEvaluator:
    def setup_method(self):
        os.environ['INPUT_CONDITIONS'] = ''
        os.environ['INPUT_TRUE_VALUES'] = ''
        os.environ['INPUT_FALSE_VALUES'] = ''

    def test_starts_with(self, monkeypatch):
        monkeypatch.setenv('BRANCH', 'feature/login')
        op = TernaryOperator()
        assert op.evaluate_condition('BRANCH STARTS_WITH feature/') is True

    def test_ends_with(self, monkeypatch):
        monkeypatch.setenv('FILE', 'deploy.yml')
        op = TernaryOperator()
        assert op.evaluate_condition('FILE ENDS_WITH .yml') is True

    def test_matches(self, monkeypatch):
        monkeypatch.setenv('TAG', 'v1.2.3')
        op = TernaryOperator()
        assert op.evaluate_condition(r'TAG MATCHES ^v\d+\.\d+\.\d+$') is True

    def test_matches_no_match(self, monkeypatch):
        monkeypatch.setenv('TAG', 'latest')
        op = TernaryOperator()
        assert op.evaluate_condition(r'TAG MATCHES ^v\d+\.\d+\.\d+$') is False


class TestRecursionDepthLimit:
    def setup_method(self):
        os.environ['INPUT_CONDITIONS'] = ''
        os.environ['INPUT_TRUE_VALUES'] = ''
        os.environ['INPUT_FALSE_VALUES'] = ''

    def test_deep_not_nesting(self, monkeypatch):
        """Deeply nested NOT should hit recursion limit and return False."""
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        # Build NOT (NOT (NOT ... (SERVICE == game))) deeper than MAX_RECURSION_DEPTH
        condition = 'SERVICE == game'
        for _ in range(op.MAX_RECURSION_DEPTH + 5):
            condition = f'NOT ({condition})'
        assert op.evaluate_condition(condition) is False

    def test_normal_nesting_works(self, monkeypatch):
        """Moderate nesting should still work fine."""
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        # Double NOT should return True
        assert op.evaluate_condition('NOT (NOT (SERVICE == game))') is True


class TestDebugModeCoverage:
    """Tests to cover debug mode branches in evaluator."""

    def test_print_debug_enabled(self, monkeypatch, capsys):
        monkeypatch.setenv('INPUT_CONDITIONS', 'SERVICE == game')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        monkeypatch.setenv('INPUT_DEBUG_MODE', 'true')
        monkeypatch.setenv('SERVICE', 'game')
        op = TernaryOperator()
        op.print_debug("test message")
        captured = capsys.readouterr()
        assert 'test message' in captured.out

    def test_validate_inputs_debug_prints(self, monkeypatch, capsys):
        """Covers lines 102, 108-110: debug prints in validate_inputs."""
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        monkeypatch.setenv('INPUT_DEBUG_MODE', 'true')
        op = TernaryOperator()
        op.validate_inputs()
        captured = capsys.readouterr()
        assert 'Raw conditions string' in captured.out
        assert 'Parsed 1 conditions' in captured.out

    def test_validate_invalid_debug_mode(self, monkeypatch):
        """Covers line 98: invalid debug_mode format."""
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        monkeypatch.setenv('INPUT_DEBUG_MODE', 'invalid')
        op = TernaryOperator()
        with pytest.raises(SystemExit):
            op.validate_inputs()


class TestDefaultValuesLengthMismatch:
    """Covers line 256: default_values length mismatch error."""

    def test_default_values_count_mismatch(self, monkeypatch):
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B, C == D')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes,yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no,no')
        monkeypatch.setenv('INPUT_DEFAULT_VALUES', 'fallback')
        monkeypatch.setenv('GITHUB_OUTPUT', '')
        op = TernaryOperator()
        with pytest.raises(SystemExit):
            op.evaluate_conditions()


class TestEvaluateConditionEdgeCases:
    def setup_method(self):
        os.environ['INPUT_CONDITIONS'] = ''
        os.environ['INPUT_TRUE_VALUES'] = ''
        os.environ['INPUT_FALSE_VALUES'] = ''

    def test_case_insensitive_string_comparison(self, monkeypatch):
        """Covers lines 226-228: case insensitive string comparison."""
        monkeypatch.setenv('INPUT_CASE_SENSITIVE', 'false')
        monkeypatch.setenv('SERVICE', 'Game')
        op = TernaryOperator()
        assert op.evaluate_condition('SERVICE != game') is False


class TestSafeWriteOutputIOError:
    """Covers lines 78-79: IOError in safe_write_output."""

    def test_write_to_invalid_path(self, monkeypatch, capsys):
        monkeypatch.setenv('INPUT_CONDITIONS', '')
        monkeypatch.setenv('INPUT_TRUE_VALUES', '')
        monkeypatch.setenv('INPUT_FALSE_VALUES', '')
        monkeypatch.setenv('INPUT_DEBUG_MODE', 'true')
        monkeypatch.setenv('GITHUB_OUTPUT', '/nonexistent/path/output')
        op = TernaryOperator()
        op.safe_write_output('test', 'value')
        captured = capsys.readouterr()
        assert 'Could not write to GITHUB_OUTPUT' in captured.out


class TestComparisonEdgeCases:
    """Covers lines 218-219, 232-234."""

    def setup_method(self):
        os.environ['INPUT_CONDITIONS'] = ''
        os.environ['INPUT_TRUE_VALUES'] = ''
        os.environ['INPUT_FALSE_VALUES'] = ''

    def test_comparison_type_error(self, monkeypatch):
        """Covers lines 232-234: TypeError in comparison."""
        monkeypatch.setenv('INPUT_CONDITIONS', '')
        monkeypatch.setenv('INPUT_TRUE_VALUES', '')
        monkeypatch.setenv('INPUT_FALSE_VALUES', '')
        op = TernaryOperator()
        # Mock _parse_comparison to return values that cause TypeError in op_func
        with patch.object(op, '_parse_comparison', return_value=('a', '==', 'b')):
            with patch.dict(op.COMPARISON_OPS, {'==': lambda a, b: (_ for _ in ()).throw(TypeError("mock"))}):
                assert op.evaluate_condition('A == B') is False


class TestEvaluateConditionsDefaultFallback:
    """Covers lines 275-281: default_values fallback on evaluation error."""

    def test_fallback_with_default_values(self, monkeypatch, tmp_path):
        gh_output = tmp_path / "output"
        gh_output.write_text("")
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        monkeypatch.setenv('INPUT_DEFAULT_VALUES', 'fallback')
        monkeypatch.setenv('GITHUB_OUTPUT', str(gh_output))
        op = TernaryOperator()
        with patch.object(op, 'evaluate_condition', side_effect=TypeError("mock error")):
            op.evaluate_conditions()
        content = gh_output.read_text()
        assert 'output_1=fallback' in content

    def test_fallback_without_default_values(self, monkeypatch, tmp_path):
        gh_output = tmp_path / "output"
        gh_output.write_text("")
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        monkeypatch.setenv('INPUT_DEFAULT_VALUES', '')
        monkeypatch.setenv('GITHUB_OUTPUT', str(gh_output))
        op = TernaryOperator()
        with patch.object(op, 'evaluate_condition', side_effect=TypeError("mock error")):
            op.evaluate_conditions()
        content = gh_output.read_text()
        assert 'output_1=no' in content


class TestRunExceptionHandling:
    """Covers lines 306-307: run() exception handler."""

    def test_run_catches_exception(self, monkeypatch):
        monkeypatch.setenv('INPUT_CONDITIONS', 'A == B')
        monkeypatch.setenv('INPUT_TRUE_VALUES', 'yes')
        monkeypatch.setenv('INPUT_FALSE_VALUES', 'no')
        op = TernaryOperator()
        with patch.object(op, 'validate_inputs', side_effect=ValueError("test error")):
            with pytest.raises(SystemExit):
                op.run()
