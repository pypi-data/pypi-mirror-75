"""
This module contains common middlware that is used by web applications.
"""

import types
import typing
import re
import traceback
import pydoc
from flask import Flask
from flask import Response
from flask import jsonify
from werkzeug.exceptions import HTTPException


def add_cors_headers(response: Response, *, origin: str = '*', methods: typing.List[str] = None,
                     headers: typing.List[str] = None, max_age: int = 86400) -> Response:
    """
    Add CORS headers to a response.
    """
    methods = methods or ['GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE']
    headers = headers or ['*']
    items = {
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Methods': ', '.join(methods),
        'Access-Control-Allow-Headers': ', '.join(headers),
        'Access-Control-Max-Age': str(max_age),
    }

    for key, value in items.items():
        response.headers[key] = value

    return response


def add_info_endpoint(package: typing.Union[str, types.ModuleType]) -> typing.Callable:
    """
    Register the API information endpoint for a specific app.
    """
    if isinstance(package, str):
        package = pydoc.locate(package)

    def get_api_info() -> Response:
        response = jsonify({
            'name': package.__name__,
            'version_string': package.__version__,
            'version_number': package.__versiont__,
        })
        response.status_code = 200
        return response

    return get_api_info


def handle_error(ex: Exception, *, status_code: int = 500) -> Response:
    """
    Generic error handler that can be called from other error handlers.
    """
    response = jsonify({
        'error': ex.__class__.__name__,
        'message': re.sub('[0-9]{3} [a-zA-Z ]+: *', '', str(ex)),
    })
    response.status_code = status_code
    return response


def add_error_handlers(
        app: Flask,
        extras: typing.List[typing.Tuple[Exception, int]] = None,
    ) -> None:
    """
    Register the common error handlers for the application.
    """
    def get_error_handler(status_code: int) -> typing.Callable:
        def error_handler(ex):
            return handle_error(ex, status_code=status_code)
        return error_handler

    for ex, status_code in extras or []:
        app.register_error_handler(ex, get_error_handler(status_code))

    @app.errorhandler(HTTPException)
    def error_http(ex: HTTPException) -> Response:  # pylint: disable=unused-variable
        """
        Handle werkzeug HTTP exceptions.
        """
        return handle_error(ex, status_code=ex.code)

    @app.errorhandler(Exception)
    def error_generic(ex: Exception) -> Response:  # pylint: disable=unused-variable
        """
        Handle any other errors.
        """
        content = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
        app.logger.critical('uncaught exception\n%s', content)
        return handle_error(ex, status_code=500)
