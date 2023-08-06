import json
import pytest
import ipdb

from oxlate import Request
from oxlate import Headers

def new_request(fragment):
    data = {
        'uri': '/foo',
        'headers': {
            'cloudfront-viewer-country': [
                {
                    'key': 'CloudFront-Viewer-Country',
                    'value': 'US'
                }
            ],
            'cookie': [
                {
                    'key': 'cookie',
                    'value': 'somename=put_a_cookie_value_here'
                }
            ],
        }
    }

    data.update(fragment)
    return Request(data)

def test_get_uri():
    request = new_request({'uri': '/psychology'})
    assert request.get_uri() == '/psychology'

def test_set_uri():
    request = new_request({'uri': 'foo'})
    request.set_uri('bar')
    assert request.get_uri() == 'bar'

def test_get_headers_returns_Headers_instance():
    request = new_request({
        'headers': {
            'some_key': [{
                'key':   'some_key',
                'value': 'some_value',
            }]
        }
    })

    headers = request.get_headers()
    assert isinstance(headers, Headers)

def test_get_headers_maps_Headers_instance_to_underlying_data():
    request = new_request({
        'headers': {
            'some_key': [{
                'key':   'some_key',
                'value': 'some_value',
            }]
        }
    })

    headers = request.get_headers()
    headers.set(name='another_key', value='another_value')

    new_headers = request.get_headers()

    assert new_headers.get(name='some_key')    == [{'key': 'some_key',    'value': 'some_value'}]
    assert new_headers.get(name='another_key') == [{'key': 'another_key', 'value': 'another_value'}]

def test_get_viewer_country_when_header_present():
    request = new_request({
        'headers': {
            'cloudfront-viewer-country': [
                {
                    'key': 'CloudFront-Viewer-Country',
                    'value': 'US'
                }
            ]
        }
    })
    assert request.get_viewer_country() == 'US'

def test_get_viewer_country_when_header_absent():
    request = new_request({'headers': {}})
    assert request.get_viewer_country() == None

def test_to_dict_returns_copy_of_underlying_data():
    orig_data = {
        'uri': '/orig-uri',
    }
    request = Request(orig_data)

    new_data = request.to_dict()
    assert new_data == orig_data

    request.set_uri('/new-uri')
    assert orig_data['uri'] == '/new-uri'
    assert new_data['uri']  == '/orig-uri'
