from datetime import datetime, timedelta
from typing import Union


class Cache:
    cache: dict = {
        'tomorrow': {},
        'today': {}
    }

    @classmethod
    async def add_weather(cls, city: str, day: str, data: dict) -> None:
        cls.cache[day][city] = {
            'time': datetime.now(),
            'data': data
        }

    @classmethod
    async def get_weather(cls, city: str, day: str) -> Union[bool, dict]:
        """
        Return a weather if it in cache or False if is not
        :param city: city name in english translition
        :param day: "today" or "tomorrow"
        :return: dict if data exists or False if not
        """
        if city in cls.cache[day].keys():
            if datetime.now() - cls.cache[day][city]['time'] < timedelta(hours=2):
                return cls.cache[day][city]['data']
        return False
