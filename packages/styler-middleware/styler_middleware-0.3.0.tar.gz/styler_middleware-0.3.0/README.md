# Styler Middleware

[![Pypi link](https://img.shields.io/pypi/v/styler_middleware.svg)](https://pypi.python.org/pypi/styler_middleware)

Utility middlewares for aiohttp web apps.

## Installation

```bash
pipenv install styler-middleware
```

## Usage

### Middleware to handle exceptions

```python
from aiohttp import web
from styler_middleware import handle_exceptions

middleware = handle_exceptions(
        generic_message='msg',          # Default: 'An error has occurred'
        status_code=500                 # Default: 500
)
web.Application(middlewares=[middleware])

```

### Middleware to handle invalid JSON

```python
from aiohttp import web
from styler_middleware import handle_invalid_json

middleware = handle_invalid_json(
        generic_message='msg',          # Default: 'An error has occurred'
        status_code=400,                # Default: 400
        methods={'POST', 'PATCH'}       # Default: {'POST', 'PATCH', 'PUT'}
)
web.Application(middlewares=[middleware])

```
