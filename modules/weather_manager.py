import http.client
import logging
import json
from config_manager import weather_api
from string import Template
from typing import Union


class Weather:
    api_key: str = None
    api_address: str = None
    queries: dict = {
        "now": Template("/current.json?q=$city&lang=ru"),
        "day": Template("/forecast.json?q=$city&days=$day&lang=ru"),
        "timezone": Template("/timezone.json?q=$city")
    }

    @classmethod
    def init_class(cls):
        cls.api_address = weather_api.address()
        cls.api_key = weather_api.api()
        logging.info("Initializate a weather parser")

    @classmethod
    def _make_query(cls, query: str) -> Union[dict, None]:
        """
        Makes a queery to api-service
        :param query: text of query
        :return: dict with weather data
        """
        conn = http.client.HTTPSConnection(cls.api_address)
        headers = {
            'X-RapidAPI-Key': cls.api_key,
            'X-RapidAPI-Host': cls.api_address
        }
        conn.request("GET",
                     query,
                     headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        if 'error' in data:
            logging.error("Error in parsing weather", data['error'])
            return None
        return data

    @classmethod
    def get_weather(cls, city: str, weather_time: str) -> Union[dict, None]:
        """
        Makes a query to api
        :param city: name of city in enf transliteration or coordinates
        :param weather_time: "now", "today" or "tomorrow"
        :return: a dict with data
        """
        logging.info("Start a parcing weather", {"city": city,
                                                 "day": weather_time})
        if weather_time == "now":
            weather = cls._make_query(cls.queries['now'].substitute(city=city))
            if weather is None:
                return None
            weather = weather['current']
            return {'temp': {'real': weather['temp_c'],
                             'feel': weather['feelslike_c']},
                    'description': weather['condition']['text'],
                    'wind': weather['wind_kph']
                    }
        elif weather_time == "today":
            weather = cls._make_query(cls.queries['day'].substitute(city=city, day=1))
            if weather is None:
                return None
            weather = weather['forecast']["forecastday"][0][
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
        elif weather_time == "tomorrow":
            weather = cls._make_query(cls.queries['day'].substitute(city=city, day=2))
            if weather is None:
                return None
            weather = weather['forecast']["forecastday"][1][
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
        else:
            logging.error("Uncorrect weather_time in try to parsing weather")
            return None

    @classmethod
    def get_offset(cls, city: str) -> Union[dict, None]:
        """
        Return a dict with data about searching city
        :param city: name of city or coords
        :return: dict{'city': name of found city in english translition,
                    'timezone': timezone of city}
        """
        data = cls._make_query(cls.queries['timezone'].substitute(city=city))
        if data is None:
            return None
        return {'city': data['location']['name'],
                'timezone': data['location']['tz_id']}
