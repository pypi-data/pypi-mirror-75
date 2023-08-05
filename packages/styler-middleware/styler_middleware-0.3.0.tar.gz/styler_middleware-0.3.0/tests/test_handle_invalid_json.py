#!/usr/bin/env python
""" Tests for handle_invalid_json.
"""

from json.decoder import JSONDecodeError
from unittest.mock import AsyncMock, Mock, patch
import asyncio

from aiohttp.web import HTTPException
from styler_middleware import handle_invalid_json
import pytest


@pytest.fixture
def middleware():
    yield handle_invalid_json(
        generic_message='msg',
        status_code=333,
        methods={'POST', 'PUT', 'PATCH'},
        exclude={'/exclude/this/path'})


def test_generator():
    mid = handle_invalid_json(generic_message='msg', status_code=333)

    assert callable(mid)


def test_normal_flow(middleware):
    request = Mock()
    request.method = 'GET'
    handler = AsyncMock(return_value='response')

    resp = asyncio.run(middleware(request, handler))

    assert resp == 'response'


def test_exclude_path(middleware):
    request = Mock()
    request.method = 'POST'
    request.path = '/exclude/this/path'
    handler = AsyncMock(return_value='response')

    resp = asyncio.run(middleware(request, handler))

    assert resp == 'response'


@patch('aiohttp.web.json_response')
@patch('logging.exception')
def test_invalid_JSON(mocked_log, mocked_resp, middleware):
    request = Mock()
    request.method = 'POST'
    request.json.side_effect = JSONDecodeError(msg='Invalid JSON', doc='', pos=0)
    handler = AsyncMock(side_effect=HTTPException(text='msg'))

    _ = asyncio.run(middleware(request, handler))

    mocked_log.assert_called_once()
    mocked_resp.assert_called_with({'error': 'msg'}, status=333)
