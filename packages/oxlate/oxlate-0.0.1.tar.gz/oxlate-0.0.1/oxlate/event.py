from .request import Request

class Event:
    def __init__(self, data):
        self._data = data
        self._cf = data['Records'][0]['cf']

    @property
    def data(self):
        return dict(self._data)

    def request(self):
        if self._cf.get('request'):
            return Request(self._cf.get('request'))
        else:
            raise ValueError('There is no request record in the provided event data')
