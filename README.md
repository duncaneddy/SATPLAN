<!-- <p align="center">
  <a href="https://github.com/duncaneddy/brahe/"><img src="https://raw.githubusercontent.com/duncaneddy/brahe/main/docs/pages/assets/logo-gold.png" alt="Brahe"></a>
</p> -->
<p align="center">
    <em>SATPLAN - A Toolbox for Satellite Task Planning Benchmarking</em>
</p>
<p align="center">
<a href="https://github.com/duncaneddy/satplan/actions/workflows/ci.yml" target="_blank">
    <img src="https://github.com/duncaneddy/satplan/actions/workflows/ci.yml/badge.svg" alt="Test">
</a>
<a href='https://coveralls.io/github/duncaneddy/satplan?branch=main'><img src='https://coveralls.io/repos/github/duncaneddy/satplan/badge.svg?branch=main' alt='Coverage Status' /></a>
<a href="https://sisl.github.io/astra-rl/index.html" target="_blank">
    <img src="https://img.shields.io/badge/docs-latest-blue.svg" alt="Docs">
</a>
<a href="https://github.com/duncaneddy/satplan/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-green.svg", alt="License">
</a>
</p>

----

# SATPLAN

SATPLAN is a package for training, benchmarking, and reference implementations for satellite task planning.


## Installation

To install the SATPLAN toolbox, you can use pip. The package is available on PyPI, so you can install it directly from there.

```bash
pip install satplan
```

You can then import the library in your Python code:

```python
import satplan
```

## Development

This section provides instructions for setting up the development environment and running tests.

To start, we _STRONGLY_ recommend using [uv](https://docs.astral.sh/uv/) to manage your Python environment. This will ensure that you have the correct dependencies and versions installed.

### Setting Up the Development Environment

1. Clone the repository:

   ```bash
   git clone git@github.com:duncaneddy/satplan.git
   cd satplan
   ```

2. Sync package dependencies:

   ```bash
   uv sync --dev
   ```

   This will create a `.venv` directory in the project root with all the necessary dependencies installed.
   
3. Install pre-commit hooks:

   ```bash
   uv run pre-commit install
   ```
   
   This will ensure that the linter (`ruff`), formatter (`ruff`), and type checker (`mypy`) is happy with your code every time you commit.
   
### Running Tests

Assuming you've set up your environment using `uv`, you can run the tests using the following command:

```bash
pytest
```

or 

```bash
uv run pytest
```

To generate local coverage reports, you can use:

```bash
uv run coverage run -m pytest
uv run coverage report # Generate CLI report
uv run coverage html   # Generate HTML report
```

### Generating Documentation

To generate the documentation, you can use the following command:

```bash
uv run mkdocs serve
```

This will build the documentation and start a local server. You can then view the documentation in your web browser.
