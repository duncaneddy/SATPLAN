import pytest


@pytest.fixture()
def cli_app():
    from satplan.cli.main import app

    return app
