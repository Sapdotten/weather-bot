# -*- coding: utf-8 -*-
import aiopygismeteo
from typing import Union
import logging


async def get_weather(id: int, day: int) -> dict[str, Union[int, str]]:
    """
    :param id: Айди города
    :return: словарь с погодой на текущие сутки
    """
    gm = aiopygismeteo.Gismeteo()
    days = await gm.step24.by_id(id, days=3, as_list=True)
    return {
        'min_t': days[day].temperature.air.min.c,
        'max_t': days[day].temperature.air.max.c,
        'comfort': days[day].temperature.comfort.max.c,
        'descr': days[day].description.full
    }


async def get_weather_now(id: int) -> dict[str, Union[int, str]]:
    """
    :param id: Айди города
    :return: словарь с погодой на данный момент
    """
    gm = aiopygismeteo.Gismeteo()
    day = await gm.current.by_id(id)
    return {
        'temp': day.temperature.air.c,
        'comfort': day.temperature.comfort.c,
        'descr': day.description.full
    }


async def city_exists(city: str) -> Union[bool, list]:
    logging.info('Check if city exists', {'query': city})
    gm = aiopygismeteo.Gismeteo()
    try:
        search_results = await gm.search.by_query(city)
        print(search_results)
    except Exception as ex:
        print(ex)
        return False
    if len(search_results) == 0:
        return False
    else:
        offset = await gm.current.by_id(search_results[0].id)
        offset = offset.date.time_zone_offset // 60
        return [search_results[0].id, search_results[0].name, offset]
