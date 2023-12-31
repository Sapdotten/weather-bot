from data import data_manager as db
from modules.weather_manager import Weather
from modules.helpers import translite_ru_to_eng, translite_eng_to_ru
from typing import Union


class User:
    @classmethod
    async def add_user(cls, uid: int, city: str) -> Union[bool, str]:
        """
        Save user to db with city. If city does not exist returns False
        :param uid: id of user in tg
        :param city: answer of user about city
        :return: found city if user have been added or False if not
        """
        city = ''.join(x for x in city if x.isalpha())
        city = await translite_ru_to_eng(city)
        data = await Weather.get_offset(city)
        if data is None:
            return False
        else:
            city_ru = await translite_eng_to_ru(data['city'])
            await db.add_user(uid, city_ru, city, data['timezone'])
            return city_ru
