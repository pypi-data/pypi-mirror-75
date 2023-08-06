import sys
from uuid import uuid4

from mongoengine import *

sys.path.append('.')

from config import AdminConfig
from model.user import User, Group

connect(
    AdminConfig.MONGO_DBNAME,
    host=AdminConfig.MONGO_HOST,
    port=AdminConfig.MONGO_PORT,
    username=AdminConfig.MONGO_USERNAME,
    password=AdminConfig.MONGO_PASSWORD,
)

group_obj = Group()
group_obj.uuid = str(uuid4())
group_obj.name = 'A'
group_obj.save()

group_obj = Group()
group_obj.uuid = str(uuid4())
group_obj.name = 'B'
group_obj.save()

group_obj = Group()
group_obj.uuid = str(uuid4())
group_obj.name = 'C'
group_obj.save()
