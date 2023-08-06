from copy import deepcopy
from datetime import datetime
import re

ALPHA_REGEX = re.compile('[^a-zA-Z]')

def _toggle_case_based_on_number(string, number):
    alpha_only_string = ALPHA_REGEX.sub('', string)

    if number >= pow(2,len(alpha_only_string)):
        raise RuntimeError("There are no more case variants for header name " + string)

    number_as_binary_string = ('{0:' + str(len(alpha_only_string)) + 'b}').format(number)

    result = []

    # Move through the 1's and 0's in the binary string, changing cases in the input
    # string for alpha characters only.
    char_idx = 0
    for bit in number_as_binary_string:
        while not string[char_idx].isalpha():
            # skip non alpha characters
            result.append(string[char_idx])
            char_idx += 1

        # switch this letter to be upper or lower based on binary representation
        result.append(string[char_idx].upper() if bit == "1" else string[char_idx].lower())
        char_idx += 1

    return ''.join(result)

class RequestCookies:
    def __init__(self, data):
        self._data = data

    def set(self, name, value=''):
        if 'cookie' not in self._data:
            self._data['cookie'] = [{'key': 'Cookie', 'value': ''}]
        old_cookie_string = self._data['cookie'][0]['value']

        parsed_cookies = RequestCookies._parse_cookies(old_cookie_string)
        parsed_cookies[name] = value

        new_cookie_string = RequestCookies._cookie_string(parsed_cookies)
        self._data['cookie'][0]['value'] = new_cookie_string

        return self

    def get(self, name, default=None):
        cookie_string = self._data \
                            .get('cookie', [{}])[0] \
                            .get('value', '')
        parsed_cookies = RequestCookies._parse_cookies(cookie_string)
        return parsed_cookies.get(name, default)

    @staticmethod
    def _cookie_string(parsed_cookies):
        entries = map(
            lambda elem: '{}={}'.format(elem[0], elem[1]),
            parsed_cookies.items(),
        )
        return ';'.join(entries)

    @staticmethod
    def _parse_cookies(string):
        parsed_cookies = {}
        for cookie_string in string.split(';'):
            if cookie_string:
                parts = cookie_string.split('=')
                parsed_cookies[parts[0].strip()] = parts[1].strip()
        return parsed_cookies

class ResponseCookie:
    def __init__(self, name, value=None, expires_at=None, path=None, domain=None):
        self._name       = name
        self._value      = value
        self._expires_at = expires_at
        self._path       = path
        self._domain     = domain

    def name(self):
        return self._name

    def value(self):
        return self._value

    def expires_at(self):
        return self._expires_at

    def path(self):
        return self._path

    def domain(self):
        return self._domain

    def to_cookie_string(self):
        chunks = []

        chunks.append('{}={}'.format(self._name, self._value))

        if self._expires_at:
            expires_string = self._expires_at.strftime('%a, %d %b %Y %H:%M:%S.%f GMT')
            chunks.append('Expires={}'.format(expires_string))

        if self._path:
            chunks.append('Path={}'.format(self._path))

        if self._domain:
            chunks.append('Domain={}'.format(self._domain))

        return ';'.join(chunks)

    @staticmethod
    def from_cookie_string(string):
        name       = None
        value      = None
        expires_at = None
        path       = None
        domain     = None

        for chunk in string.split(';'):
            match = re.search(r'\AExpires=(.+)\Z', chunk.strip())
            if match:
                expires_at = datetime.strptime(match.group(1), '%a, %d %b %Y %H:%M:%S.%f GMT')
                continue

            match = re.search(r'\APath=(.+)\Z', chunk.strip())
            if match:
                path = match.group(1)
                continue

            match = re.search(r'\ADomain=(.+)\Z', chunk.strip())
            if match:
                domain = match.group(1)
                continue

            match = re.search(r'\A(.+)=(.*)\Z', chunk.strip())
            if match:
                name  = match.group(1)
                value = match.group(2) if len(match.group(2)) > 0 else None
                continue

        return ResponseCookie(
            name       = name,
            value      = value,
            expires_at = expires_at,
            path       = path,
            domain     = domain,
        )

class ResponseCookies:
    def __init__(self, data):
        self._data = data

    def get(self, name, default=None):
        for key,value in self._data.items():
            if key.lower() == 'set-cookie':
                response_cookie = ResponseCookie.from_cookie_string(value[0]['value'])
                if response_cookie.name() == name:
                    return response_cookie
        return default

    def set(self, cookie):
        cookie_string  = cookie.to_cookie_string()
        cookie_counter = 0

        for key,value in self._data.items():
            if key.lower() == 'set-cookie':
                cookie_counter += 1
                current_cookie = ResponseCookie.from_cookie_string(value[0]['value'])
                if current_cookie.name() == cookie.name():
                    value[0]['value'] = cookie_string
                    return self

        key = _toggle_case_based_on_number(
            string = 'set-cookie',
            number = cookie_counter,
        )
        self._data[key] = [{
            'key':   key,
            'value': cookie_string,
        }]

        return self

class Headers:
    def __init__(self, data=None):
        self._data = {} if data is None else data

        self._duplicate_name_counts = {}
        for name in self._data.keys():
            if name.lower() not in self._duplicate_name_counts:
                self._duplicate_name_counts[name.lower()] = -1
            self._duplicate_name_counts[name.lower()] += 1

    def get(self, name, default=None):
        return self._data.get(name, default)

    def get_value(self, name, default=None):
        return self._data.get(name, [{}])[0].get('value', default)

    # See https://forums.aws.amazon.com/thread.jspa?messageID=701434 about the duplicate stuff
    def set(self, name, value, adjust_case_to_allow_duplicates=False):
        if adjust_case_to_allow_duplicates:
            duplicate_name_count = self._duplicate_name_counts[name.lower()] = \
                self._duplicate_name_counts.get(name.lower(), -1) + 1
            adjusted_name = _toggle_case_based_on_number(name, duplicate_name_count)
        else:
            adjusted_name = name

        adjusted_value = [{
            'key':   adjusted_name,
            'value': value,
        }]

        self._data[adjusted_name] = adjusted_value
        return self

    def get_request_cookie(self, name, default=None):
        request_cookies = RequestCookies(self._data)
        return request_cookies.get(name, default)

    def set_request_cookie(self, name, value):
        request_cookies = RequestCookies(self._data)
        request_cookies.set(name, value)
        return self

    def get_response_cookie(self, name):
        response_cookies = ResponseCookies(self._data)
        return response_cookies.get(name, default=None)

    def set_response_cookie(self, cookie):
        response_cookies = ResponseCookies(self._data)
        response_cookies.set(cookie)
        return self

    def to_dict(self):
        return deepcopy(self._data)
