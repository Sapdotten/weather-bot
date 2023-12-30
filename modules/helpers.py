from transliterate import translit


async def incr_time(offset: int, time: str) -> str:
    time = time.split(':')
    print(f'offset is {offset}')
    offset = int(time[0]) - offset
    offset = offset % 24
    print(f'final hour is: {offset}')
    time = str(offset) + ':' + time[1]
    return time


async def translite_ru_to_eng(ru_text: str) -> str:
    return translit(ru_text, language_code='ru', reversed=True)


async def translite_eng_to_ru(ru_text: str) -> str:
    return translit(ru_text, language_code='ru')
