"""Tests for the CLI commands."""
from pathlib import Path
from typer.testing import CliRunner
from pcb_autoplacer.cli import app

runner = CliRunner()
FIXTURES = Path(__file__).parent / "fixtures"


class TestCLI:
    def test_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "pcb-autoplacer" in result.stdout.lower() or "Automated" in result.stdout

    def test_parse_missing_file(self):
        result = runner.invoke(app, ["parse", "/nonexistent/file.net"])
        assert result.exit_code != 0

    def test_place_missing_file(self):
        result = runner.invoke(app, ["place", "/nonexistent/file.net"])
        assert result.exit_code != 0
