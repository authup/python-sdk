[![CI](https://github.com/migraf/authup-py/actions/workflows/main.yml/badge.svg)](https://github.com/migraf/authup-py/actions/workflows/main.yml)
# Authup Python Plugins

This repository contains python plugins for using the [Authup](https//authup.org) authentication and authorization
framework in the python language.
The plugins are used to integrate Authup with different python frameworks and libraries.

## Supported Python frameworks

| Plugin                                               | Extra        | Sync | Async | version |
|------------------------------------------------------|--------------|:----:|------:|---------|
| [httpx](https://github.com/encode/httpx)             |              |  ✅   |     ✅ | 0.0.1   |
| [requests](https://github.com/psf/requests)          | `[requests]` |  ✅   |     ❌ | 0.1.0   |
| [FastApi](https://fastapi.tiangolo.com/)             | `[fastapi]`  |  ⏳   |     ⏳ |         |
| [Flask](https://flask.palletsprojects.com/en/2.2.x/) | `[flask]`    |  ⏳   |     ⏳ |         |


## Installation

The plugins are available via [PyPi](https://pypi.org/project/authup-py/).

```bash
pip install authup-py
```

### Extra dependencies
The plugin for the project's base library [httpx](https://github.com/encode/httpx) need no extra dependencies. To
use the additional plugins for other libraries, you need to install with the corresponding extra i.e. for `requests`:

```bash
pip install authup-py[requests]
```

## How to use
All the plugins share the underlying `Authup` class. The class is initialized with the url of the Authup server and
the credentials you would like to use (username/password or robot_id/secret).    
The class provides both sync and async methods for the different authentication and authorization flows.

```python

from authup import Authup

authup = Authup(
    url="https://authup.org",
    username="username",
    password="password"
)

authup_robot = Authup(
    url="https://authup.org",
    robot_id="robot",
    robot_secret="secret"
)

```

The following plugins all expect the same arguments as the `Authup` class with the addition of the
app as a first argument for server side libraries (e.g. FastApi, Flask).

### httpx
For synchronously using the plugin with httpx, you can use the `AuthupHttpx` class and pass an instance to your
`httpx.Client` or a basic `httpx.Request` as the `auth` parameter:

```python
import httpx
from authup.plugins.httpx import AuthupHttpx

authup = AuthupHttpx(
    url="https://authup.org",
    username="username",
    password="password",
)

# Use the authup instance as the auth parameter for the httpx client
client = httpx.Client(auth=authup)

with client:
    response = client.get("https://authup.org")
    print(response.status_code)


# Use the authup instance as the auth parameter for a top level request function
request = httpx.get("https://authup.org", auth=authup)

```

It works the same way for the asynchronous httpx client:

```python
import httpx
from authup.plugins.httpx import AuthupHttpxAsync

authup = AuthupHttpxAsync(
    url="https://authup.org",
    username="username",
    password="password",
)

with httpx.AsyncClient(auth=authup) as client:
    response = await client.get("https://authup.org")
    print(response.status_code)

```

### requests
Since requests is a synchronous library, the plugin is also synchronous. You can use the `AuthupRequests` class and
use it with the `requests.Session` or the `requests.request` functions:
> **Note**
> Requires the `requests` extra to be installed. `pip install authup-py[requests]`

```python
import requests
from authup.plugins.requests import AuthupRequests

authup = AuthupRequests(
    url="https://authup.org",
    username="username",
    password="password",
)

# Use the authup instance as the auth parameter for the requests session
with requests.Session() as session:
    session.auth = authup
    response = session.get("https://authup.org")
    print(response.status_code)

# Use the authup instance as the auth parameter for a top level request function
response = requests.get("https://authup.org", auth=authup)
print(response.status_code)

```



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

