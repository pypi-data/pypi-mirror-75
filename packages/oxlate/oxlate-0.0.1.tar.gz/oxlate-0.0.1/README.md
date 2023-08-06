# late-python

[![Build Status](https://travis-ci.org/openstax/late-python.svg?branch=master)](https://travis-ci.org/openstax/late-python)

A Python package with OpenStax Lambda@Edge ("lAMBDA at eDGE") utilities.

## Overview

`late-python` provides object overlays
to the JSON containers
inside Lambda@Edge events and responses.
These overlay objects handle the details
of accessing and modifying
the containers they overlay.

All `get_*` methods
leave the underlying container intact,
and all `set_*` methods
modify it in place.

## Usage

### Dealing With Request Events

```python
from oxlate import Event, Response

def lambda_handler(event, context):
    request = Event(event).request() ## returns Request overlay

    ## get and set the request uri field
    request.get_uri()
    request.set_uri('/some/new/uri')

    ## get the viewer's country code
    request.get_viewer_country()

    ## return Headers overlay
    headers = request.get_headers()

    ## get the Request event header array-of-hash (or None if missing):
    ##    [{name=..., value=...}]
    headers.get(name='header-name')

    ## get the header value only
    ## (or None if missing and no default given)
    headers.get_value(name='header-name', default='some default')

    ## set or overwrite a header
    headers.set(
        name  = 'header-name',
        value = 'some value',
    )

    ## get a request cookie value
    ## (or None if missing and no default given)
    headers.get_request_cookie('cookie_name', default='some default')

    ## set or overwrite a request cookie value
    headers.set_request_cookie('cookie_name', value='some value')

    ## return a deep copy of the overlaid hashmap
    return request.to_dict()
```

### Dealing With Response Objects
```python
from oxlate import Response

def request_handler(event, context):
    ## construct a Response object
    response = Response(
        status=302,
        content_type='text/plain',
        body=None,
    )

    ## use method chaining to tweak Response
    response.set_status(404) \
            .set_content_type('custom/type') \
            .set_content_type_json() \
            .set_content_type_html() \
            .set_body(json.dumps('some body text'))

    ## get a Headers overlay
    headers = response.get_headers()

    ## get the header value only
    ## (or None if missing and no default given)
    headers.get_value(name='header-name', default='some default')

    ## set or overwrite a header
    headers.set(
        name  = 'header-name',
        value = 'some value',
    )

    ## get a ResponseCookie overlay
    cookie = headers.get_response_cookie('cookie-name')
    print(cookie.name())
    print(cookie.value())
    print(cookie.expires_at())
    print(cookie.path())
    print(cookie.domain())

    ## set or override a ResponseCookie
    cookie = ResponseCookie(
        name       = 'cookie-name',
        value      = 'some value',
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=2),
        path       = '/',
        domain     = 'my.domain.com',
    )
    headers.set_response_cookie(cookie)

    return response.to_dict()
```

## Development

All development is done inside a docker container.  From your host running Docker, in this directory run:

```
$> docker-compose up -d
%> ./docker/bash
```

This will drop you into the running container

## Run tests

From within the container, you can run tests with:

```
$ /code> python -m pytest
```

For debugging, you can use `ipdb`, e.g.

```
import ipdb; ipdb.set_trace()
```

When running tests with the debugger make sure to use the `-s` option to prevent pytest from capturing output.

`$> python -m pytest -s tests -k 'test_decrypts'`

Note that `pytest` is also on the `PATH` so you can call it directly.

## Distributing

...

