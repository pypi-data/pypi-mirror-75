""" Middleware that handles invalid JSON body from requests
"""

import logging
from json.decoder import JSONDecodeError

from aiohttp import web


def handle_invalid_json(
        generic_message='Invalid JSON data',
        status_code=400,
        methods=None,
        exclude=None):
    """ Generate a middleware that validates JSON data from the request
        and returns a 400 error if it is invalid.
 
        Args:
            generic_message: The message that will be send as an error
            status_code: The HTTP status code (default = 400)
            methods: a set of methods (default: POST, PATCH, PUT)
            exclude: a set of endpoints to be excluded
    """
    if not methods:
        methods = {'POST', 'PATCH', 'PUT'}
    if exclude is None:
        exclude = {}
    @web.middleware
    async def middleware(request, handler):
        if request.method in methods and request.path not in exclude:
            try:
                await request.json()
            except JSONDecodeError:
                logging.exception('Invalid JSON')
                return web.json_response(
                    {'error': generic_message},
                    status=status_code
                )
        response = await handler(request)
        return response
    return middleware
