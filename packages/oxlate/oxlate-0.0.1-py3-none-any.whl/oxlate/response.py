import json
import re

from .headers import Headers

class Response:
    def __init__(self, status=200, content_type='text/plain', body=None):
        self.set_status(status)
        self.set_content_type(content_type)
        self.set_body(body)
        self._headers = Headers()

    def set_status(self, value):
        self._status = value
        return self

    def set_content_type(self, content_type):
        self._content_type = content_type
        return self

    def set_content_type_json(self):
        self._content_type = "application/json"
        return self

    def set_content_type_html(self):
        self._content_type = "text/html"
        return self

    def set_body(self, body):
        self._body = body
        return self

    def get_headers(self):
        return self._headers

    def to_dict(self):
        result = {
            'status': self._status
        }

        if self._body is not None:
            result['body'] = self.__encoded_body()
            self._headers.set(name='Content-Type', value=self._content_type)

        if self._headers is not None:
            result['headers'] = self._headers.to_dict()

        return result

    def __encoded_body(self):
        if re.search(r'json', self._content_type):
            return json.dumps(self._body)
        else:
            return self._body
