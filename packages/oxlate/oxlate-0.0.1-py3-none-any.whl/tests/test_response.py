from oxlate import Response, ResponseCookie

import json
import pytest

from .pytest_regex import pytest_regex
import ipdb

def test_basic():
    response = Response(body="Hi")
    assert response.to_dict() == {
        'status': 200,
        'body': 'Hi',
        'headers': {
            'Content-Type': [
                {
                    'key': 'Content-Type',
                    'value': 'text/plain'
                }
            ]
        }
    }

def test_more(mocker):
    response = Response(status=201) \
                   .set_status(204) \
                   .set_content_type_json() \
                   .set_body("howdy")
    response.get_headers() \
            .set_response_cookie(ResponseCookie(name="foo", value="bar")) \
            .set_response_cookie(ResponseCookie(name="yoyo", value="ma")) \
            .set(name="HI", value="THERE")

    assert response.to_dict() == {
        'status': 204,
        'body': '"howdy"',
        'headers': {
            'Content-Type': [
                {
                    'key': 'Content-Type',
                    'value': 'application/json'
                }
            ],
            'set-cookie': [
                {
                    'key': 'set-cookie',
                    'value': 'foo=bar'
                }
            ],
            'set-cookiE': [
                {
                    'key': 'set-cookiE',
                    'value': 'yoyo=ma'
                }
            ],
            'HI': [
                {
                    'key': 'HI',
                    'value': 'THERE'
                }
            ]
        }
    }
