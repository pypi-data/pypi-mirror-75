from oxlate import Headers
from oxlate import ResponseCookie

import datetime
import json
import pytest

import ipdb

def test_get_missing_header_no_default_returns_None():
    headers = Headers()
    assert headers.get(name='missing') == None

def test_get_missing_header_with_default_returns_given_default():
    headers = Headers()
    assert headers.get(name='missing', default='abc') == 'abc'

def test_get_existing_header_returns_array_of_dict():
    headers = Headers({
        'header-name': [{
            'key':   'header-name',
            'value': 'some-value',
        }]
    })

    assert headers.get(name='header-name') is not None
    assert isinstance(headers.get(name='header-name'), type([]))
    assert headers.get(name='header-name')[0]['key']   == 'header-name'
    assert headers.get(name='header-name')[0]['value'] == 'some-value'

def test_get_value_missing_header_no_default_returns_None():
    headers = Headers()
    assert headers.get_value(name='missing') == None

def test_get_value_missing_header_with_default_returns_given_default():
    headers = Headers()
    assert headers.get_value(name='missing', default='abc') == 'abc'

def test_get_value_existing_header_returns_value_field():
    headers = Headers({
        'header-name': [{
            'key':   'header-name',
            'value': 'some-value',
        }]
    })
    assert headers.get_value('header-name') == 'some-value'

def test_set_new_header():
    headers = Headers({
        'existing-header': [{
            'key':   'existing-header',
            'value': 'existing-value',
        }]
    })
    headers.set(name='foo', value='bar')

    assert headers.get(name='foo') == [{'key': 'foo', 'value': 'bar'}]
    assert headers.get_value(name='existing-header') == 'existing-value'

def test_set_existing_header():
    headers = Headers({
        'foo': [{
            'key':   'foo',
            'value': 'orig-foo-value',
        }]
    })

    assert headers.get_value(name='foo') == 'orig-foo-value'
    headers.set(name='foo', value='new-foo-value')
    assert headers.get_value(name='foo') == 'new-foo-value'

def test_Headers_overlays_given_data():
    orig_data = {
        'foo': [{
            'key':   'foo',
            'value': 'orig-foo-value',
        }]
    }
    headers = Headers(data=orig_data)

    assert headers.get_value(name='foo') == 'orig-foo-value'
    headers.set(name='foo', value='new-foo-value')
    assert headers.get_value(name='foo') == 'new-foo-value'
    assert orig_data['foo'][0]['value'] == 'new-foo-value'

def test_to_dict_returns_copy_of_overlaid_data():
    orig_data = {
        'foo': [{
            'key':   'foo',
            'value': 'orig-foo-value',
        }]
    }
    headers = Headers(data=orig_data)

    new_data = headers.to_dict()
    assert new_data == orig_data

    new_data['foo'][0]['value'] = 'new-foo-value'
    assert orig_data['foo'][0]['value'] == 'orig-foo-value'

def test_set_allowing_duplicates():
    headers = Headers()
    headers.set(name="Set-Cookie", value="bar",   adjust_case_to_allow_duplicates=True)
    headers.set(name="Set-Cookie", value="howdy", adjust_case_to_allow_duplicates=True)
    headers.set(name="Set-Cookie", value="yoyo",  adjust_case_to_allow_duplicates=True)

    assert headers.to_dict() == {
        "set-cookie": [{
            'key':   'set-cookie',
            'value': 'bar',
        }],
        "set-cookiE": [{
            'key':   'set-cookiE',
            'value': 'howdy',
        }],
        "set-cookIe": [{
            'key':   'set-cookIe',
            'value': 'yoyo',
        }],
    }

def test_set_allowing_duplicates_left_of_hyphen():
    headers = Headers()
    headers.set(name="a-a", value="bar",   adjust_case_to_allow_duplicates=True)
    headers.set(name="A-A", value="howdy", adjust_case_to_allow_duplicates=True)
    headers.set(name="A-a", value="yoyo",  adjust_case_to_allow_duplicates=True)
    headers.set(name="a-A", value="boo",   adjust_case_to_allow_duplicates=True)

    assert headers.to_dict() == {
        "a-a": [{
            'key':   'a-a',
            'value': 'bar',
        }],
        "a-A": [{
            'key':   'a-A',
            'value': 'howdy',
        }],
        "A-a": [{
            'key':   'A-a',
            'value': 'yoyo',
        }],
        "A-A": [{
            'key':   'A-A',
            'value': 'boo',
        }],
    }

    with pytest.raises(RuntimeError, match=r".*no more case variants.*"):
        headers.set(name="a-a", value="yoyo", adjust_case_to_allow_duplicates=True)

def test_set_allowing_duplicates_but_none_left():
    headers = Headers()
    headers.set(name="a", value="bar",   adjust_case_to_allow_duplicates=True)
    headers.set(name="A", value="howdy", adjust_case_to_allow_duplicates=True)

    with pytest.raises(RuntimeError, match=r".*no more case variants.*"):
        headers.set(name="a", value="yoyo", adjust_case_to_allow_duplicates=True)

def test_set_allowing_duplicates_with_given_data():
    headers = Headers({
        "a-a": [{
            'key':   'a-a',
            'value': 'bar',
        }],
        "a-A": [{
            'key':   'a-A',
            'value': 'howdy',
        }],
    })

    headers.set(name="A-a", value="yoyo",  adjust_case_to_allow_duplicates=True)

    assert headers.to_dict() == {
        "a-a": [{
            'key':   'a-a',
            'value': 'bar',
        }],
        "a-A": [{
            'key':   'a-A',
            'value': 'howdy',
        }],
        "A-a": [{
            'key':   'A-a',
            'value': 'yoyo',
        }],
    }

def test_get_request_cookie_missing_returns_None():
    headers = Headers()
    assert headers.get_request_cookie(name='foo') is None

def test_get_request_cookie_missing_returns_given_default():
    headers = Headers()
    assert headers.get_request_cookie(name='foo', default='abc') == 'abc'

def test_get_request_cookie_returns_cookie_value_empty_string():
    headers = Headers({
        'cookie': [{
            'key': 'Cookie',
            'value': 'biz=buz; foo=; yo=dawg',
        }]
    })
    assert headers.get_request_cookie(name='foo') == ''

def test_get_request_cookie_returns_cookie_value():
    headers = Headers({
        'cookie': [{
            'key': 'Cookie',
            'value': 'biz=buz; foo=bar; yo=dawg',
        }]
    })
    assert headers.get_request_cookie(name='foo') == 'bar'

def test_set_new_request_cookie_with_no_cookies_present():
    headers = Headers()
    headers.set_request_cookie(name='foo', value='bar')
    assert headers.get_request_cookie(name='foo') == 'bar'

def test_set_new_request_cookie_with_cookies_present():
    headers = Headers({
        'cookie': [{
            'key': 'Cookie',
            'value': 'biz=buz; baz=bar',
        }]
    })

    headers.set_request_cookie(name='foo', value='bar')

    assert headers.get_request_cookie(name='biz') == 'buz'
    assert headers.get_request_cookie(name='baz') == 'bar'
    assert headers.get_request_cookie(name='foo') == 'bar'

def test_set_existing_request_cookie():
    headers = Headers({
        'cookie': [{
            'key': 'Cookie',
            'value': 'biz=buz; foo=bar; baz=bar',
        }]
    })

    headers.set_request_cookie(name='foo', value='bub')

    assert headers.get_request_cookie(name='biz') == 'buz'
    assert headers.get_request_cookie(name='baz') == 'bar'
    assert headers.get_request_cookie(name='foo') == 'bub'

def test_get_response_cookie_missing_returns_None():
    headers = Headers()
    assert headers.get_response_cookie(name='foo') is None

def test_get_response_cookie_returns_ResponseCookie():
    headers = Headers({
        'set-cookie': [
            {'key': 'set-cookie', 'value': 'bar=baz'},
        ],
        'set-cookiE': [
            {'key': 'set-cookiE', 'value': 'foo=bar'},
        ],
        'set-cookIe': [
            {'key': 'set-cookIe', 'value': 'boo=baz'},
        ],
    })

    cookie = headers.get_response_cookie(name='foo')

    assert isinstance(cookie, ResponseCookie)
    assert cookie.name()  == 'foo'
    assert cookie.value() == 'bar'

def test_set_new_response_cookie_no_cookies_present():
    headers = Headers()
    cookie = ResponseCookie(
        name='foo',
        value='bar',
    )
    headers.set_response_cookie(cookie)

    assert headers.get_response_cookie(name='foo').value() == 'bar'

def test_set_new_response_cookie_cookies_present():
    headers = Headers({
        'set-cookie': [
            {'key': 'set-cookie', 'value': 'bar=baz'},
        ],
        'set-cookiE': [
            {'key': 'set-cookIe', 'value': 'boo=baz'},
        ],
    })
    cookie = ResponseCookie(
        name='foo',
        value='bar',
    )
    headers.set_response_cookie(cookie)

    assert headers.get_response_cookie(name='bar').value() == 'baz'
    assert headers.get_response_cookie(name='boo').value() == 'baz'
    assert headers.get_response_cookie(name='foo').value() == 'bar'

def test_set_existing_response_cookie():
    headers = Headers({
        'set-cookie': [
            {'key': 'set-cookie', 'value': 'bar=baz'},
        ],
        'set-cookiE': [
            {'key': 'set-cookiE', 'value': 'foo=bar'},
        ],
        'set-cookIe': [
            {'key': 'set-cookIe', 'value': 'boo=baz'},
        ],
    })

    cookie = ResponseCookie(
        name='foo',
        value='new',
    )
    headers.set_response_cookie(cookie)

    assert headers.get_response_cookie(name='bar').value() == 'baz'
    assert headers.get_response_cookie(name='foo').value() == 'new'
    assert headers.get_response_cookie(name='boo').value() == 'baz'

def test_set_response_cookie_sets_all_cookie_fields():
    headers = Headers()

    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=3.1415)

    cookie = ResponseCookie(
        name       = 'foo',
        value      = 'bar',
        expires_at = expires_at,
        path       = '/path',
        domain     = 'mydomain.com',
    )
    headers.set_response_cookie(cookie)

    assert headers.get_response_cookie(name='foo').name()       == 'foo'
    assert headers.get_response_cookie(name='foo').value()      == 'bar'
    assert headers.get_response_cookie(name='foo').expires_at() == expires_at
    assert headers.get_response_cookie(name='foo').path()       == '/path'
    assert headers.get_response_cookie(name='foo').domain()     == 'mydomain.com'
