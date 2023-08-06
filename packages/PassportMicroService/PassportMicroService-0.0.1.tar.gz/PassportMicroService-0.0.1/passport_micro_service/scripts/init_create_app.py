import sys
from uuid import uuid4

from mongoengine import *

sys.path.append('.')

from config import AdminConfig
from model.app import App

connect(
    AdminConfig.MONGO_DBNAME,
    host=AdminConfig.MONGO_HOST,
    port=AdminConfig.MONGO_PORT,
    username=AdminConfig.MONGO_USERNAME,
    password=AdminConfig.MONGO_PASSWORD,
)

default_app = App()
default_app.uuid = str(uuid4())
default_app.name = 'default_app'
default_app.access_key_id = 'abcdefg'
default_app.access_key_secret = '11111111'
default_app.save()
