from texts import RAINY_WEATHER_CLOTHES, SIMPLE_WEATHER_CLOTHES, SNOWY_WEATHER_CLOTHES


async def rainy_weather(temp: int) -> str:
    """
    Возвращает строку с одеждой для дождливой погоды
    :param temp: температура воздуха
    :return: строка одежды
    """
    if temp <= RAINY_WEATHER_CLOTHES['min_t']:
        return RAINY_WEATHER_CLOTHES[RAINY_WEATHER_CLOTHES['min_t']]
    elif temp >= RAINY_WEATHER_CLOTHES['max_t']:
        return RAINY_WEATHER_CLOTHES[RAINY_WEATHER_CLOTHES['max_t']]
    else:
        return RAINY_WEATHER_CLOTHES[temp]


async def snowy_weather(temp: int) -> str:
    """
    Возвращает строку с одеждой для снежной погоды
    :param temp: температура воздуха
    :return: строка одежды
    """
    if temp <= SNOWY_WEATHER_CLOTHES['min_t']:
        return SNOWY_WEATHER_CLOTHES[SNOWY_WEATHER_CLOTHES['min_t']]
    elif temp >= SNOWY_WEATHER_CLOTHES['max_t']:
        return SNOWY_WEATHER_CLOTHES[SNOWY_WEATHER_CLOTHES['max_t']]
    else:
        return SNOWY_WEATHER_CLOTHES[temp]


async def simple_weather(temp: int) -> str:
    """
        Возвращает строку с одеждой для обычной погоды
        :param temp: температура воздуха
        :return: строка одежды
        """
    if temp <= SIMPLE_WEATHER_CLOTHES['min_t']:
        return SIMPLE_WEATHER_CLOTHES[SIMPLE_WEATHER_CLOTHES['min_t']]
    elif temp >= SIMPLE_WEATHER_CLOTHES['max_t']:
        return SIMPLE_WEATHER_CLOTHES[SIMPLE_WEATHER_CLOTHES['max_t']]
    else:
        return SIMPLE_WEATHER_CLOTHES[temp]


async def what_to_wear(temp: int, descr: str) -> str:
    """
    Возвращает строку с вариантом одежды
    :param temp: температура по ощущениям
    :param descr: описание погоды
    :return: строка с одеждой
    """
    temp = temp//1
    print(temp)
    descr = descr.lower()
    if 'дождь' in descr:
        return await rainy_weather(temp)
    elif 'снег' in descr:
        return await snowy_weather(temp)
    else:
        return await simple_weather(temp)
