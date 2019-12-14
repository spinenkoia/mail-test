import redis

from typing import Dict

class Currencies:
    def __init__(self):
        self.__client = redis.Redis('localhost', 6379, charset="utf-8", decode_responses=True)

    def close(self):
        self.__client.close()

    def get(self, currenci: str) -> float:
        if currenci == 'RUR':
            return 1.0

        data = self.__client.hget('currencies', currenci)
        if data is None:
            raise ValueError('Currenci %r not found.' % currenci)

        return float(data)

    def getall(self):
        return {key: float(value) for key, value in self.__client.hgetall('currencies').items()}

    def update(self, data: Dict[str, float]):
        self.__client.hmset('currencies', data)

    def clean(self):
        self.__client.flushdb()
