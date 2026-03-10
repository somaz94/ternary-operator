"""Shared pytest fixtures for ternary-operator tests."""

import os
import tempfile
import pytest


@pytest.fixture
def clean_env(monkeypatch):
    """Remove all INPUT_* env vars to start clean."""
    for key in list(os.environ.keys()):
        if key.startswith('INPUT_') or key == 'GITHUB_OUTPUT':
            monkeypatch.delenv(key, raising=False)


@pytest.fixture
def github_output(tmp_path):
    """Create a temporary GITHUB_OUTPUT file."""
    output_file = tmp_path / "github_output.txt"
    output_file.touch()
    return str(output_file)


@pytest.fixture
def default_env(monkeypatch, github_output):
    """Set default environment variables for TernaryOperator."""
    monkeypatch.setenv('INPUT_CONDITIONS', 'SERVICE == game')
    monkeypatch.setenv('INPUT_TRUE_VALUES', 'pass')
    monkeypatch.setenv('INPUT_FALSE_VALUES', 'fail')
    monkeypatch.setenv('INPUT_DEBUG_MODE', 'false')
    monkeypatch.setenv('GITHUB_OUTPUT', github_output)
    monkeypatch.setenv('SERVICE', 'game')
    return github_output
