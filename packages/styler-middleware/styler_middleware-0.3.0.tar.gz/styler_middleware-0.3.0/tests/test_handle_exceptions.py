#!/usr/bin/env python
""" Tests for handle_exceptions.
"""

from unittest.mock import AsyncMock, Mock, patch
import asyncio

from aiohttp.web import HTTPException
from styler_middleware import handle_exceptions
import pytest


@pytest.fixture
def middleware():
    yield handle_exceptions(generic_message='msg', status_code=333)


def test_generator():
    mid = handle_exceptions(generic_message='msg', status_code=333)

    assert callable(mid)


def test_normal_flow(middleware):
    request = Mock()
    handler = AsyncMock(return_value='response')

    resp = asyncio.run(middleware(request, handler))

    assert resp == 'response'


def test_HTTP_exception(middleware):
    request = Mock()
    handler = AsyncMock(side_effect=HTTPException(text='msg'))

    with pytest.raises(HTTPException) as expected:
        _ = asyncio.run(middleware(request, handler))

    assert str(expected.value.text) == 'msg'


@patch('aiohttp.web.json_response')
@patch('logging.exception')
def test_exception(mocked_log, mocked_resp, middleware):
    request = Mock()
    handler = AsyncMock(side_effect=ValueError('msg'))

    _ = asyncio.run(middleware(request, handler))

    mocked_log.assert_called_once()
    mocked_resp.assert_called_with({'error': 'msg'}, status=333)
