
import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


_DEF_VAL = {
    'LOCAL_DB': 'sqlite:///' + os.path.join(base_dir, 'data', 'app.db'),
    'LOG_DIR': os.path.join(base_dir, 'logs'),
    "VERSION_DIR": os.path.join(base_dir, 'data', 'versions'),
}


def _rand_string():
    from random import choice, randint
    from string import ascii_letters, digits

    pattern = digits+ascii_letters + "?&~#-_@%$*!§+"
    return ''.join(choice(pattern) for i in range(randint(17, 39)))


class Config(object):
    DEFAULTS = _DEF_VAL

    DEBUG = os.environ.get('DEBUG', True)

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', False)

    LOG_DIR = os.environ.get('LOG_DIR', _DEF_VAL['LOG_DIR'])
    VERSION_DIR = os.environ.get('VERSION_DIR', _DEF_VAL['VERSION_DIR'])

    TRANSITFEED_API_KEY = os.environ.get(
        'TRANSITFEED_API_KEY', _DEF_VAL['TRANSITFEED_API_KEY'])
    TRANSITFEED_API_URL = os.environ.get(
        'TRANSITFEED_API_URL', _DEF_VAL['TRANSITFEED_API_URL'])
    TRANSITFEED_API_KEY = os.environ.get(
        'TRANSITFEED_API_KEY', _DEF_VAL['TRANSITFEED_API_KEY'])

    DB_URI = os.environ.get('DB_URI', _DEF_VAL['LOCAL_DB'])
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = int(os.environ.get('DB_PORT'))
    DB_USER = os.environ.get('DB_USER')
    DB_PWD = os.environ.get('DB_PWD')
    DB_DB = os.environ.get('DB_DB')

    # SECRET_KEY = os.environ.get('SECRET_KEY') or _rand_string()
