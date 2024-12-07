# Introduction

This is a project for the AGH classes `Technologie Telekomunikacyjne`. The goal is to
implement tic-tac-toe game in client-server architecture, using Python, TCP and TLS.

# Development

* Create and activate python [venv](https://docs.python.org/3/library/venv.html)
* Install package and dev dependencies in editable mode `pip install -e ".[dev]"`

It will install two commands: `gamed` for server, and `game` for client.

Project uses [pytest](https://docs.pytest.org/en/stable/) framework for testing,
and is configured to use [mypy](https://mypy-lang.org/) for type checks.
