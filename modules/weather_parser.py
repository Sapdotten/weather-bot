# -*- coding: utf-8 -*-
import aiopygismeteo
from typing import Union


async def get_weather(id: int) -> dict[str, Union[int, str]]:
    """
    :param id: Айди города
    :return: словарь с погодой
    """
    gm = aiopygismeteo.Gismeteo()
    days = await gm.step24.by_id(id, days=3, as_list=True)
    return {
        'min_t': days[0].temperature.air.min.c,
        'max_t': days[0].temperature.air.max.c,
        'comfort': days[0].temperature.comfort.max.c,
        'descr': days[0].description.full
    }


async def city_exists(city: str) -> Union[bool, list]:
    gm = aiopygismeteo.Gismeteo()
    try:
        search_results = await gm.search.by_query(city)
    except Exception:
        return False
    if len(search_results) == 0:
        return False
    else:
        return [search_results[0].id, search_results[0].name]
