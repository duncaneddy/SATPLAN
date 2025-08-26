import pathlib


def get_data_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "data"
