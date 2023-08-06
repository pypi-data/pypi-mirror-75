import sys
from uuid import uuid4

from mongoengine import *

sys.path.append('.')

from config import AdminConfig
from model.base import Permission

connect(
    AdminConfig.MONGO_DBNAME,
    host=AdminConfig.MONGO_HOST,
    port=AdminConfig.MONGO_PORT,
    username=AdminConfig.MONGO_USERNAME,
    password=AdminConfig.MONGO_PASSWORD,
)

permission = Permission()
permission.uuid = str(uuid4())
permission.name = 'user_view'
permission.app = []
permission.save()

permission = Permission()
permission.uuid = str(uuid4())
permission.name = 'user_add'
permission.app = []
permission.save()

permission = Permission()
permission.uuid = str(uuid4())
permission.name = 'user_modify'
permission.app = []
permission.save()

permission = Permission()
permission.uuid = str(uuid4())
permission.name = 'user_delete'
permission.app = []
permission.save()
