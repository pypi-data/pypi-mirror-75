import sys
from uuid import uuid4

from mongoengine import *

sys.path.append('.')

from config import AdminConfig
from model.base import Role

connect(
    AdminConfig.MONGO_DBNAME,
    host=AdminConfig.MONGO_HOST,
    port=AdminConfig.MONGO_PORT,
    username=AdminConfig.MONGO_USERNAME,
    password=AdminConfig.MONGO_PASSWORD,
)

role_admin = Role()
role_admin.uuid = str(uuid4())
role_admin.name = 'admin'
role_admin.permission = []
role_admin.save()

role_user = Role()
role_user.uuid = str(uuid4())
role_user.name = 'user'
role_user.permission = []
role_user.save()
