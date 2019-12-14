import logging

from typing import Dict, Any

from aiohttp.web import View, json_response, Response
from cerberus import Validator


log = logging.getLogger(__name__)

replace_schema = {
    'USD': {
        'type': 'float',
        'required': True,
        'nullable': False,
        'coerce': float,
    },
    'EUR': {
        'type': 'float',
        'required': True,
        'nullable': False,
        'coerce': float,
    },
}

update_schema = {
    'USD': {
        'type': 'float',
        'required': False,
        'nullable': False,
        'coerce': float,
    },
    'EUR': {
        'type': 'float',
        'required': False,
        'nullable': False,
        'coerce': float,
    },
}

match_schema = {
    'merge': {
        'type': 'integer',
        'required': True,
        'coerce': int,
        'allowed': [0, 1],
    }
}


class DatabaseHandler(View):
    async def get(self):
        return json_response(self.request.app['currencies'].getall())

    async def post(self):
        validator_query = Validator(match_schema)

        if not validator_query.validate(dict(self.request.query)):
            raise ValueError('Data validation error: %r.' % validator_query.errors)

        merge = validator_query.document['merge']
        request = await self.request.json()

        # Если mrege=1, заменяем все целиком, если нет, то частичное обновление.
        validator = Validator(replace_schema if merge == 1 else update_schema)
        if not validator.validate(request):
            raise ValueError('Data validation error: %r.' % validator.errors)

        self.request.app['currencies'].update(request)

        return Response()
