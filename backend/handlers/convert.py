import logging

from aiohttp.web import View, json_response, Response
from cerberus import Validator


log = logging.getLogger(__name__)

query_schema = {
    'from': {
        'type': 'string',
        'required': True,
        'nullable': False,
        'allowed': ['RUR', 'USD', 'EUR'],
    },
    'to': {
        'type': 'string',
        'required': True,
        'nullable': False,
        'allowed': ['RUR', 'USD', 'EUR'],
    },
    'amount': {
        'type': 'float',
        'required': True,
        'nullable': False,
        'coerce': float,
    },
}


class ConvertHandler(View):
    async def get(self):
        validator_query = Validator(query_schema)
        if not validator_query.validate(dict(self.request.query)):
            raise ValueError('Data validation error: %r.' % validator_query.errors)

        query = validator_query.document

        from_cur = self.request.app['currencies'].get(query['from'])
        to_cur = self.request.app['currencies'].get(query['to'])

        return json_response(dict(result=round((from_cur / to_cur) * query['amount'], 2)))
