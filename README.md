[![CI](https://github.com/migraf/authup-py/actions/workflows/main.yml/badge.svg)](https://github.com/migraf/authup-py/actions/workflows/main.yml)
# Authup Python Plugins

This repository contains python plugins for using the [Authup](https//authup.org) authentication and authorization
framework in the python language.
The plugins are used to integrate Authup with different python frameworks and libraries.

## Supported Python frameworks

| Plugin                                               | Sync | Async | version |
|------------------------------------------------------|:----:|------:|---------|
| [httpx](https://github.com/encode/httpx)             |  ✅   |     ✅ | 0.0.1   |
| [requests](https://github.com/psf/requests)          |  ✅   |     ❌ | 0.1.0   |
| [FastApi](https://fastapi.tiangolo.com/)             |  ⏳   |     ⏳ |         |
| [Flask](https://flask.palletsprojects.com/en/2.2.x/) |  ⏳   |     ⏳ |         |

## How to use

### Install

### Use

## How to develop

### Install

Requires [poetry](https://python-poetry.org/) and [pre-commit](https://pre-commit.com/) and python 3.7+.

```shell
poetry install --with dev --all-extras
```

Install pre-commit hooks

```shell
pre-commit install
```

### Test

```shell
poetry run pytest
```

