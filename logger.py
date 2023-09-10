import logging
from config_manager import logger
import sys


def start():
    handlers = []
    print('Запуск модуля logger')
    # формат вывовда логов
    log_format = '%(asctime)s - %(levelname)s - %(message)s - %(args)s'

    output = logger.output()
    if output == 'file':
        file_handler = logging.FileHandler(logger.file())
        file_handler.setLevel(logger.level())
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.ERROR)
        handlers = [file_handler, stream_handler]
    elif output == 'console':
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        handlers = [stream_handler]
    else:
        raise ValueError('Unexpected value for log out')

    logging.basicConfig(
        handlers=handlers,
        level=logger.level(),
        format=log_format
    )
