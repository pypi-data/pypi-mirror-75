from urllib.parse import quote_plus
from core.config import DefaultConfig


class Config:

    HOST = DefaultConfig.HOST
    # HOST = 'http://192.168.3.170:50080'
    # HOST = 'http://127.0.0.1:50080'
    # MONGO_HOST = DefaultConfig.MONGO_HOST
    # MONGO_PORT = DefaultConfig.MONGO_PORT
    MONGO_HOST = '192.168.3.170'
    MONGO_PORT = 27017
    MONGO_USERNAME = DefaultConfig.MONGO_USERNAME
    MONGO_PASSWORD = DefaultConfig.MONGO_PASSWORD
    MONGO_DBNAME = DefaultConfig.MONGO_DBNAME

    MONGODB_SETTINGS = DefaultConfig.MONGODB_SETTINGS
    MONGODB_SETTINGS['host'] = MONGO_HOST
    MONGODB_SETTINGS['port'] = MONGO_PORT

    MIDDLE_WARES = DefaultConfig.MIDDLE_WARES

    PASSPORT_SERVICE_URL = '%s/api' % HOST
    DEFAULT_APP_URL = '%s/api' % HOST
    DEFAULT_APP_ACCESS_KEY_ID = 'abcdefg'
    DEFAULT_APP_ACCESS_KEY_SECRET = '11111111'

    @staticmethod
    def init_app(app):
        pass


class AdminConfig:
    MONGO_HOST = Config.MONGO_HOST
    MONGO_PORT = Config.MONGO_PORT
    MONGO_USERNAME = Config.MONGO_USERNAME
    MONGO_PASSWORD = Config.MONGO_PASSWORD
    MONGO_DBNAME = Config.MONGO_DBNAME

    @staticmethod
    def init_app(app):
        pass


config = {
    'dev': Config,
}
