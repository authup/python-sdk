[![CI](https://github.com/migraf/authup-py/actions/workflows/main.yml/badge.svg)](https://github.com/migraf/authup-py/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/migraf/authup-py/branch/main/graph/badge.svg?token=qILJEFdh8I)](https://codecov.io/gh/migraf/authup-py)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/authup)
![PyPI - Downloads](https://img.shields.io/pypi/dw/authup)
[![Maintainability](https://api.codeclimate.com/v1/badges/520401d6c07170a6e413/maintainability)](https://codeclimate.com/github/migraf/authup-py/maintainability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Authup Python Plugins

This repository contains python plugins for using the [Authup](https://authup.org) authentication and authorization
framework in the python language.
The plugins are used to integrate Authup with different python frameworks and libraries.

## Supported Python frameworks

### Client
| Plugin                                      | Extra        | Sync | Async |
|---------------------------------------------|--------------|:----:|------:|
| [httpx](https://github.com/encode/httpx)    |              |  ✅   |     ✅ |
| [requests](https://github.com/psf/requests) | `[requests]` |  ✅   |     ❌ |

### Server

| Plugin                                                        | Extra       | Sync | Async | Middleware | User |
|---------------------------------------------------------------|-------------|:----:|------:|------------|------|
| [FastApi](https://fastapi.tiangolo.com/)                      | `[fastapi]` |  ✅   |     ✅ | ✅          | ✅    |
| [ASGI](https://asgi.readthedocs.io/en/latest/specs/main.html) | `[asgi]`    |  ❌   |     ✅ | ✅          | ✅    |
| [Flask](https://flask.palletsprojects.com/en/2.2.x/)          | `[flask]`   |  ⏳   |     ⏳ | ⏳          | ⏳    |

Table of Contents
=================

* [Authup Python Plugins](#authup-python-plugins)
   * [Supported Python frameworks](#supported-python-frameworks)
      * [Client](#client)
      * [Server](#server)
   * [Installation](#installation)
      * [Extra dependencies](#extra-dependencies)
   * [How to use](#how-to-use)
      * [httpx](#httpx)
      * [requests](#requests)
      * [ASGI Middleware](#asgi-middleware)
         * [Optional user injection](#optional-user-injection)
      * [FastAPI Dependency](#fastapi-dependency)
         * [Basic user dependency](#basic-user-dependency)
         * [Require permissions](#require-permissions)
   * [How to develop](#how-to-develop)
      * [Install](#install)
      * [Test](#test)


## Installation

The plugins are available via [PyPi](https://pypi.org/project/authup-py/).

```bash
pip install authup-py
```

### Extra dependencies
The plugin for the project's base library [httpx](https://github.com/encode/httpx) needs no extra dependencies. To
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
For synchronously using the plugin with [httpx](https://github.com/encode/httpx) , you can use the `AuthupHttpx` class and pass an instance to your
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

async with httpx.AsyncClient(auth=authup) as client:
    response = await client.get("https://authup.org")
    print(response.status_code)

```

### requests
Since [requests](https://github.com/psf/requests) is a synchronous library, the plugin is also synchronous. You can use the `AuthupRequests` class and
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

### ASGI Middleware

The `AuthupASGIMiddleware` class can be used as an ASGI middleware for any ASGI framework (i.e. FastAPI, Starlette). 
The middleware will check the incoming requests for a valid token and otherwise return a 401 response. If you pass the
optional `user` parameter, the middleware will inject the user object into the request scope (`r.state.user`).

The first argument is the ASGI application and the second argument is the URL of the authup instance.
> **Note**
> Requires the `asgi` extra to be installed. `pip install authup-py[asgi]`

The following shows a simple example for using the middleware with a FastAPI application but it should work with any ASGI framework.

> **Note**
> Expects a running authup instance available at the given URL.
> 
```python
from fastapi import FastAPI
from authup.plugins.asgi import AuthupASGIMiddleware

app = FastAPI()

authup_url = "https://authup.org"  # change to your authup instance
@app.get("/test")
async def test():
    return {"message": "Hello World"}

# register the middleware pass the authup url as argument
app.add_middleware(AuthupASGIMiddleware, authup_url=authup_url)

```
Now you can access the `/test` endpoint without a token and will receive a 401 response. When using a valid token, you will receive the expected response.

```python
import httpx
from authup.plugins.httpx import AuthupHttpx

# no token or invalid token raises 401
response = httpx.get("http://localhost:8000/test") # 401
print(response.status_code)

# valid token receives the expected response
authup = AuthupHttpx(
    url="https://authup.org",
    username="username",
    password="password",
)

response = httpx.get("http://localhost:8000/test", auth=authup) # 200
print(response.status_code)

```

#### Optional user injection
Set the `user` parameter to `True` when adding the middleware to your ASGI application:

```python
from fastapi import FastAPI, Request
from authup.plugins.asgi import AuthupASGIMiddleware

app = FastAPI()

authup_url = "https://authup.org"  # change to your authup instance
@app.get("/test-user")
async def test(request: Request):
    return {"user": request.state.user}

# register the middleware pass the authup url as argument
app.add_middleware(AuthupASGIMiddleware, authup_url=authup_url, user=True)

```

Calling the `/test-user` endpoint without a token will return a 401 response. When using a valid token, the user object 
will be injected into the request scope, and you will receive the expected response containing your user.

### FastAPI Dependency
The `AuthupUser` class can be used as a FastAPI dependency. 
It will check the incoming requests for a valid token and otherwise return a 401 response. If the token is valid a user object
will be available in the dependency call.

#### Basic user dependency
The following shows a simple example for using the dependency with a FastAPI application that will return the user
object obtained from the token.

```python
from fastapi import FastAPI, Depends
from authup.plugins.fastapi import AuthupUser
from authup import User


app = FastAPI()

user_dependency = AuthupUser(url="http://localhost:3010")

@app.get("/test")
async def user_test(user: User = Depends(user_dependency)):
    return {"user": user.dict()}

```

#### Require permissions
You can also require specific permissions for the user. The following example will only allow users with the 
`client_add` permission and a power level of over `100`. Otherwise, a 401 response will be returned.

```python
from fastapi import FastAPI, Depends
from authup.plugins.fastapi import AuthupUser
from authup import User
from authup.permissions import Permission

permissions = [
        Permission(name="client_add", inverse=False, power=100),
    ]

required_permissions = AuthupUser(
    url="http://localhost:3010",
    permissions=permissions,
)

app = FastAPI()

@app.get("/test")
async def user_test(user: User = Depends(required_permissions)):
    return {"user": user.dict()}

```



## How to develop

### Install

Requires [poetry](https://python-poetry.org/) and [pre-commit](https://pre-commit.com/) and python 3.7+.

```shell
poetry install --with dev --all-extras
```

Install pre-commit hooks

```shell
poetry run pre-commit install
```

### Test

```shell
poetry run pytest
```

