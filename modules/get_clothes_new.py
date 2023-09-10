up_clothes: dict[tuple[int, int], str] = {
    (-60, -30): 'Теплый пуховик и кофта',
    (-29, -20): 'Теплый пуховик',
    (-19, -10): 'Куртка и толстовка',
    (-9, 0): 'Легкая куртка и теплая толстовка',
    (1, 10): 'Теплая толстовка',
    (11, 20): 'Футболка и легкая толстовка с собой',
    (21, 25): 'Футболка или рубашка',
    (26, 35): 'Легкая футболка',
    (36, 50): 'Майка'
}
down_clothes: dict[tuple[int, int], str] = {
    (-60, -11): 'зимние штаны, подштанники',
    (-20, -11): 'зимние штаны',
    (-10, 4): 'плотные штаны',
    (5, 19): 'джинсы',
    (20, 24): 'легкие штаны',
    (25, 50): 'шорты'
}
shoes: dict[tuple[int, int], str] = {
    (-60, -10): 'теплые ботинки',
    (-9, 0): 'легкая осенняя обувь',
    (1, 10): 'теплые кроссовки',
    (11, 25): 'кроссовки',
    (26, 50): 'сандалии или шлепки'
}
head: dict[tuple[int, int], str] = {
    (-60, -20): 'вязаный шарф и шапка-ушанка',
    (-19, -5): 'шапка и тонкий шарф',
    (-4, 5): 'тонкая шапка и легкий шарф',
    (6, 10): 'легкий шарф'
}
title: dict[tuple[int, int], str] = {
    (-60, -20): 'Даже такой холод не помешает вашим планам!',
    (-19, 0): 'Немного холодно, но это не станет препятствием для вас.',
    (1, 15): 'Легкая бодрящая прохлада ознаменует этот день.',
    (16, 25): 'Приятная погода благоволит вашим планам.',
    (26, 50): 'Немного жарко, но разве вас это остановит?',
}


async def get_clothes(temp: int, descr) -> str:
    temp = temp // 1
    _title = ''
    _up_clothes = ''
    _down_clothes = ''
    _shoes = ''
    _head = ''
    end = ' - ваш злодейский образ на сегодня'
    for key in title.keys():
        if key[0] <= temp <= key[1]:
            _title = title[key]
    for key in up_clothes.keys():
        if key[0] <= temp <= key[1]:
            _up_clothes = up_clothes[key]
    for key in down_clothes.keys():
        if key[0] <= temp <= key[1]:
            _down_clothes = down_clothes[key]
    for key in head.keys():
        if key[0] <= temp <= key[1]:
            _head = head[key]
    for key in shoes.keys():
        if key[0] <= temp <= key[1]:
            _shoes = shoes[key]
    res = f'{_title}\n{_up_clothes}, {_down_clothes}, {_shoes}'
    if _head != '':
        res += ',' + _head + end
    else:
        res += end
    if 'дождь' in descr:
        res += '\nИ не забудьте про зонт!'
    return res
