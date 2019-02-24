
import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


_DEF_VAL = {
    'LOCAL_DB': 'sqlite:///' + os.path.join(base_dir, 'data', 'app.db'),
    'LOG_DIR': os.path.join(base_dir, 'logs'),
    "GTFS_DIR": os.path.join(base_dir, 'data', 'versions'),
    "TRANSITFEED_API_URL": "https://api.transitfeeds.com/",
    "TRANSITFEED_API_VERSION": "v1",
    "STIB_ID": "societe-des-transports-intercommunaux-de-bruxelles/527",

}


class Config(object):
    DEFAULTS = _DEF_VAL

    DEBUG = os.environ.get('DEBUG', True)

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', False)

    LOG_DIR = os.environ.get('LOG_DIR', _DEF_VAL['LOG_DIR'])
    GTFS_DIR = os.environ.get('GTFS_DIR', _DEF_VAL['GTFS_DIR'])

    TRANSITFEED_API_KEY = os.environ.get('TRANSITFEED_API_KEY')
    TRANSITFEED_API_URL = os.environ.get(
        'TRANSITFEED_API_URL', _DEF_VAL['TRANSITFEED_API_URL'])
    TRANSITFEED_API_VERSION = os.environ.get(
        'TRANSITFEED_API_VERSION', _DEF_VAL['TRANSITFEED_API_VERSION'])

    TRANSITFEED_STIB_ID = os.environ.get('STIB_ID', _DEF_VAL['STIB_ID'])

    DB_URI = os.environ.get('DB_URI', _DEF_VAL['LOCAL_DB'])

    # SECRET_KEY = os.environ.get('SECRET_KEY') or _rand_string()
