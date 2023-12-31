import aiohttp
import logging
from config_manager import weather_api
from string import Template
from typing import Union
from cache import Cache


class Weather:
    api_key: str = None
    api_address: str = None
    queries: dict = {
        "now": Template("/current.json?q=$city&lang=ru"),
        "day": Template("/forecast.json?q=$city&days=$day&lang=ru"),
        "timezone": Template("/timezone.json?q=$city")
    }

    @classmethod
    def start(cls):
        cls.api_address = weather_api.address()
        cls.api_key = weather_api.api()
        logging.info("Initializate a weather parser")

    @classmethod
    async def _make_query(cls, query: str) -> Union[dict, None]:
        """
        Makes a queery to api-service
        :param query: text of query
        :return: dict with weather data
        """
        headers = {
            'X-RapidAPI-Key': cls.api_key,
            'X-RapidAPI-Host': cls.api_address
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=f"https://{cls.api_address}{query}", headers=headers) as response:
                    data = await response.json()
                    if 'error' in data:
                        logging.error("Error in parsing weather", data['error'])
                        return None
                    logging.info('Got an answer from api', {'query': query})
                    return data
            except aiohttp.ClientConnectorError as err:
                logging.error("Can't make a session with api service", {'error': err})
                return None

    @classmethod
    async def _get_weather(cls, city: str, weather_time: str) -> Union[dict, None]:
        """
        Makes a query to api
        :param city: name of city in enf transliteration or coordinates
        :param weather_time: "now", "today" or "tomorrow"
        :return: a dict with data
        """
        logging.info("Start a parcing weather", {"city": city,
                                                 "day": weather_time})
        if weather_time == "now":
            weather = await cls._make_query(cls.queries['now'].substitute(city=city))
            if weather is None:
                return None
            weather = weather['current']
            return {'temp': {'real': weather['temp_c'],
                             'feel': weather['feelslike_c']},
                    'description': weather['condition']['text'],
                    'wind': weather['wind_kph']
                    }
        else:
            day = 0
            if weather_time == "tomorrow":
                day = 1

            weather = await cls._make_query(cls.queries['day'].substitute(city=city, day=1))
            if weather is None:
                return None
            weather = weather['forecast']["forecastday"][day][
                "day"]
            return {
                'temp': {
                    'min': weather['mintemp_c'],
                    'max': weather['maxtemp_c'],
                    'avg': weather['avgtemp_c']
                },
                'wind': weather['maxwind_kph'],
                'description': weather['condition']['text']
            }

    @classmethod
    async def get_weather(cls, city: str, period: str) -> dict:
        """
        Return a weather for city in period
        :param city: a city name in english trancliteration
        :param period: "now", "tomorrow" or "today"
        :return: a dict with data
        """
        data = await Cache.get_weather(city, period)
        if data:
            return data
        else:
            data = await cls._get_weather(city, period)
            await Cache.add_weather(city, period, data)
            return data

    @classmethod
    async def get_offset(cls, city: str) -> Union[dict, None]:
        """
        Return a dict with data about searching city
        :param city: name of city or coords
        :return: dict{'city': name of found city in english translition,
                    'timezone': timezone of city}
        """
        data = await cls._make_query(cls.queries['timezone'].substitute(city=city))
        if data is None:
            return None
        return {'city': data['location']['name'],
                'timezone': data['location']['tz_id']}
