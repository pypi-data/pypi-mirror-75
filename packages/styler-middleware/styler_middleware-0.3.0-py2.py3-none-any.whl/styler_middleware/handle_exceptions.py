""" Middleware that handles exceptions
"""

import logging

from aiohttp import web


def handle_exceptions(
        generic_message='An error has occurred',
        status_code=500):
    """ Generate a middleware that logs unexpected exceptions
        and returns a JSON response.

        Exceptions of type HTTPException won't be handled as they should be
        expected exceptions.
 
        Args:
            generic_message: The message that will be send as an error
            status_code: The HTTP status code (default = 500)
    """
    @web.middleware
    async def middleware(request, handler):
        try:
            response = await handler(request)
            return response
        except web.HTTPException:
            raise
        except Exception as ex:
            message = str(ex)
            logging.exception('Error: %s', message)
            return web.json_response(
                {'error': generic_message},
                status=status_code
            )
    return middleware
