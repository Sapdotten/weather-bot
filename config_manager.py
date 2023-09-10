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


def token() -> str:
    if config['env_mode'] == 'getenv':
        load_dotenv('.env')
        return os.getenv('TOKEN_API')
    elif config['env_mode'] == 'environ':
        return os.environ["TOKEN_API"]


def db_file():
    return config['db_file']


def timezone():
    return config['time_zone']


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
