import yaml
import os

try:
    from dotenv import load_dotenv
except Exception:
    pass

global config


def start():
    global config
    print('config_manager starts')
    with open('configs.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    if config['env_mode'] == 'getenv':
        load_dotenv('.env')


def token() -> str:
    if config['env_mode'] == 'getenv':
        return os.getenv('TOKEN_API')
    elif config['env_mode'] == 'environ':
        return os.environ["TOKEN_API"]


def db_file():
    return config['db_file']


def timezone():
    return config['time_zone']


class weather_api:
    @staticmethod
    def api() -> str:
        """Returns a key api as string"""
        if config['env_mode'] == 'getenv':
            return os.getenv('WEATHER_API')
        elif config['env_mode'] == 'environ':
            return os.environ["WEATHER_API"]

    @staticmethod
    def address() -> str:
        """Returns an address of api as string"""
        return config['weather_api_address']


class logger:
    global config

    @classmethod
    def level(cls):
        return config['logging']['level']

    @classmethod
    def file(cls):
        return config['logging']['file']

    @classmethod
    def output(cls):
        return config['logging']['out']
