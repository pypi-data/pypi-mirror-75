from urllib.parse import quote_plus


class DefaultConfig(object):

    HOST = 'http://127.0.0.1:8000'
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'root'
    MONGO_PASSWORD = 'root.123'
    MONGO_DBNAME = 'test'

    MONGODB_SETTINGS = {
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'db': MONGO_DBNAME,
        'username': MONGO_USERNAME,
        'password': MONGO_PASSWORD
    }

    MIDDLE_WARES = [
        'passport.auth.middleware.AppAuthMiddleware',
        'passport.auth.middleware.UserAuthMiddleware'
    ]

    DEFAULT_APP_URL = '%s/api' % HOST
    DEFAULT_APP_ACCESS_KEY_ID = 'abcdefg'
    DEFAULT_APP_ACCESS_KEY_SECRET = '1111111'

    @staticmethod
    def init_app(app):
        pass
