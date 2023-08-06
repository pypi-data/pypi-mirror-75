import sys
from uuid import uuid4

from mongoengine import *

sys.path.append('.')

from config import AdminConfig
from model.user import User
from model.base import Role

connect(
    AdminConfig.MONGO_DBNAME,
    host=AdminConfig.MONGO_HOST,
    port=AdminConfig.MONGO_PORT,
    username=AdminConfig.MONGO_USERNAME,
    password=AdminConfig.MONGO_PASSWORD,
)

role_admin = Role.objects.filter(name='admin').first()
user_admin = User()
user_admin.uuid = str(uuid4())
user_admin.username = 'admin'
user_admin.password = '11111111'
user_admin.permissions = []
user_admin.roles = [role_admin]
user_admin.groups = []
user_admin.save()

role_user = Role.objects.filter(name='user').first()
user_user = User()
user_user.uuid = str(uuid4())
user_user.username = 'testuser'
user_user.password = '11111111'
user_user.permissions = []
user_user.roles = [role_user]
user_user.groups = []
user_user.save()
