# -*- coding: utf-8 -*-
import aiopygismeteo
from typing import Union


async def get_weather_today(id: int) -> dict[str, Union[int, str]]:
    """
    :param id: Айди города
    :return: словарь с погодой на текущие сутки
    """
    gm = aiopygismeteo.Gismeteo()
    days = await gm.step24.by_id(id, days=3, as_list=True)
    return {
        'min_t': days[0].temperature.air.min.c,
        'max_t': days[0].temperature.air.max.c,
        'comfort': days[0].temperature.comfort.max.c,
        'descr': days[0].description.full
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
    print(f'Is city {city} exists?')
    gm = aiopygismeteo.Gismeteo()
    try:
        search_results = await gm.search.by_query(city)
    except Exception:
        return False
    if len(search_results) == 0:
        return False
    else:
        offset = await gm.current.by_id(search_results[0].id)
        offset = offset.date.time_zone_offset // 60 
        return [search_results[0].id, search_results[0].name, offset]

