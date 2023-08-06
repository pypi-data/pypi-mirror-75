import json
import pytest
import ipdb

from oxlate import Event, Request

REQUEST_EVENT = {
  "Records": [
    {
      "cf": {
        "request": {
          "uri": "/psychology",
          "headers": {
            "cloudfront-viewer-country": [
              {
                "key": "CloudFront-Viewer-Country",
                "value": "JP"
              }
            ]
          }
        }
      }
    }
  ]
}

RESPONSE_EVENT = {
  "Records": [
    {
      "cf": {
        "response": {
        }
      }
    }
  ]
}

def test_returns_request_when_in_data(mocker):
    event = Event(REQUEST_EVENT)
    assert type(event.request()) is Request

def test_returns_none_request_when_not_in_data(mocker):
    event = Event(RESPONSE_EVENT)
    with pytest.raises(ValueError, match=r".*no request record.*"):
        event.request()

