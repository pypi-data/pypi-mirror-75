from .core import Session
from .responses import PagedResponse
from . import exceptions
from .models import Image

import logging

log = logging.getLogger(__name__)


class Client(Session):
    def request(self, method, url, *args, **kwargs):
        self.limit = kwargs.pop('limit', -1)
        return super(Session, self).request(method, url, *args, **kwargs)

    def send(self, request, **kwargs):
        response = super(Client, self).send(request, **kwargs)

        if response.headers.get('content-length') == '0':
            return {}

        if response.headers.get('content-type').startswith('application/json'):
            try:
                data = response.json()
            except ValueError:
                raise exceptions.BadJSON(response)

            limit = self.limit
            self.limit = -1  # reset the limit again
            if 'pageItemList' in data:
                return PagedResponse(super(Session, self), response, limit=limit)
            elif 'itemList' in data:
                return data['itemList']
            elif 'testRunList' in data:
                return data['testRunList']
            elif 'dtoSample' in data:
                return data['dtoSample']
            else:
                return data
        elif response.headers.get('content-type').startswith('image/'):
            return Image.from_response(response)
        else:
            log.warning(
                'Do not know how to handle Content-Type: {0:s}.'.format(
                    response.headers.get('content-type')
                )
            )
            return response
