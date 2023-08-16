async def incr_time(offset: int, time: str) -> str:
    time = time.split(':')
    print(f'offset is {offset}')
    offset =int(time[0])-offset
    offset = offset % 24
    print(f'final hour is: {offset}')
    time = str(offset) + ':' + time[1]
    return time
