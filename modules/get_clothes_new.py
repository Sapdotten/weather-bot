up_clothes: dict[tuple[int, int], str] = {
    (-60, -30): 'теплый пуховик и кофта',
    (-29, -20): 'теплый пуховик',
    (-19, -10): 'куртка и толстовка',
    (-9, 0): 'легкая куртка и теплая толстовка',
    (1, 10): 'теплая толстовка',
    (11, 20): 'футболка и легкая толстовка с собой',
    (21, 25): 'футболка или рубашка',
    (26, 35): 'легкая футболка',
    (36, 50): 'майка'
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
    end = 'Ваш злодейский образ на сегодня: \n'
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
    res= _title+'\n\n'
    if _head != '':
        res += _head +'\n'
    res +=end+'- '+_up_clothes+'\n'+'- '+_down_clothes+'\n'+'- '+_shoes+'\n'

    if 'дождь' in descr:
        res += '\nИ не забудьте про зонт!'
    return res
