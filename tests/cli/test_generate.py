from typer.testing import CliRunner

runner = CliRunner()


def test_generate(cli_app):
    result = runner.invoke(cli_app, ["generate"])
    assert result.exit_code == 0
    assert "Generating datasets" in result.output
