"""Tests for src/colors.py"""

from src.colors import Colors


class TestColors:
    def test_color_codes_exist(self):
        assert Colors.HEADER == '\033[95m'
        assert Colors.OKBLUE == '\033[94m'
        assert Colors.OKCYAN == '\033[96m'
        assert Colors.OKGREEN == '\033[92m'
        assert Colors.WARNING == '\033[93m'
        assert Colors.FAIL == '\033[91m'
        assert Colors.ENDC == '\033[0m'
        assert Colors.BOLD == '\033[1m'

    def test_color_codes_are_strings(self):
        for attr in ['HEADER', 'OKBLUE', 'OKCYAN', 'OKGREEN', 'WARNING', 'FAIL', 'ENDC', 'BOLD']:
            assert isinstance(getattr(Colors, attr), str)
