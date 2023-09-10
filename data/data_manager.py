from asqlite3 import connect as async_con
from sqlite3 import connect
from typing import Union
from modules.helpers import incr_time
import logging
import config_manager

# UPDATE
# DELETE FROM table_name
# INSERT INTO table_name
# count(field_name) as field_result_name- кол-во записей
# sum() - подсчет суммы указанного поля по всем записям выборки
# avr() - вычисление среднего арифметического
# min() - нахождение минимального значения для указанного поля
# max() - нахождение максимального значения для указанного поля
# DISTINCT перед полем выделяет только уникальные поля
# GROUP_BY  - объединяет элементы в группы
# ORDER BY - сортировка DESC - по убыванию
# LIMIT - ограничение на количество записей
# JOIN - объединение данных из таблиц по условию
# UNION - объединение таблиц без повторов данных


def start():
    global base_file
    base_file = config_manager.db_file()
    with connect(base_file) as con:
        cur = con.cursor()
        logging.info('database file created')
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY NOT NULL,
        city TEXT NOT NULL,
        time TEXT DEFAULT "8:00",
        auto_send BOOL DEFAULT TRUE,
        city_id INTEGER NOT NULL DEFAULT NONE,
        offset INTEGER
        )""")
        logging.info('database table created')
        con.commit()


async def add_user(user_id: int, city: str, city_id: int, offset: int):
    logging.info('Adding a user', {id: user_id})
    async with async_con(base_file) as con:
        cur = await con.cursor()
        info = await cur.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""")
        if await info.fetchone() is None:
            await cur.execute(
                f"INSERT INTO users (user_id, city, city_id, offset) VALUES({user_id}, '{city}', {city_id}, {offset})")
            logging.info('New user has been added', {id: user_id})
            await con.commit()
        else:
            await cur.execute(
                f"""UPDATE users SET city = '{city}', city_id = {city_id}, offset = {offset} WHERE user_id = {user_id}""")
            logging.info('User already in db, upgrade data', {id: user_id})
            await con.commit()


async def get_city(user_id: int) -> Union[None, dict[str, Union[str, int]]]:
    async with async_con(base_file) as con:
        cur = await con.cursor()
        city = await cur.execute(f"""SELECT city, city_id FROM users WHERE user_id ={user_id}""")
        city = await city.fetchone()
        if city is None:
            return None
        return {'name': city[0],
                'id': city[1]}


async def get_times() -> list[list[str]]:
    async with async_con(base_file) as con:
        cur = await con.cursor()
        times = await cur.execute(
            f"SELECT DISTINCT time FROM users WHERE auto_send=TRUE"
        )
        times = await times.fetchall()
        return times


async def get_users_with_time_city(time: str, city_id: int) -> list[list[int]]:
    async with async_con(base_file) as con:
        cur = await con.cursor()
        users = await cur.execute(
            f"""SELECT user_id FROM users WHERE
time = '{time}' AND city_id = {city_id} AND auto_send=TRUE"""
        )
        users = await users.fetchall()
        return users


async def get_cities_with_time(time: str) -> list[list[id, str]]:
    async with async_con(base_file) as con:
        cur = await con.cursor()
        cities = await cur.execute(
            f"SELECT DISTINCT city_id, city FROM users WHERE time = '{time}' AND auto_send = TRUE"
        )
        cities = await cities.fetchall()
        return cities


async def get_offset(id: int) -> int:
    async with async_con(base_file) as con:
        cur = await con.cursor()
        try:
            offset = await cur.execute(
                f"SELECT offset FROM users WHERE user_id = {id}"
            )
            offset = await offset.fetchone()
            print(offset)
            return offset[0]
        except Exception as _ex:
            print(_ex)


async def set_time(id: int, time: str) -> bool:
    offset = await get_offset(id)
    time = await incr_time(offset, time)
    async with async_con(base_file) as con:
        cur = await con.cursor()
        try:
            await cur.execute(
                f"UPDATE users SET time = '{time}' WHERE user_id = {id}"
            )
            await con.commit()
            return True
        except Exception:
            print('Не удалось сохранить время в бд')
            pass
        return False


async def get_time_server(id: int) -> Union[None, str]:
    """Возвращает время отправки, согласованное со временем сервера"""
    async with async_con(base_file) as con:
        cur = await con.cursor()
        try:
            time = await cur.execute(
                f"SELECT time FROM users WHERE user_id = {id}"
            )
            time = await time.fetchone()
            return time[0]
        except Exception:
            return None


async def get_auto_send_status(id: int) -> bool:
    async with async_con(base_file) as con:
        cur = await con.cursor()
        try:
            status = await cur.execute(
                f"SELECT auto_send FROM users WHERE user_id = {id}"
            )
        except Exception:
            return False
        status = await status.fetchone()
        return status[0]


async def set_auto_send_status(id: int, status: bool):
    async with async_con(base_file) as con:
        cur = await con.cursor()
        await cur.execute(
            f"UPDATE users SET auto_send = {status} WHERE user_id = {id}"
        )
        await con.commit()


async def get_count_of_users():
    async with async_con(base_file) as con:
        cur = await con.cursor()
        count = await cur.execute(
            "SELECT COUNT(user_id) as users FROM users"
        )
        count = await count.fetchone()
        return count[0]


async def get_users() -> list:
    async with async_con(base_file) as con:
        cur = await con.cursor()
        count = await cur.execute(
            "SELECT * FROM users"
        )
        count = await count.fetchall()
        print(count)
        return count

