import sys

from pymongo import MongoClient

sys.path.append('.')

from config import AdminConfig

client = MongoClient(AdminConfig.MONGO_HOST, AdminConfig.MONGO_PORT)
db = client.admin
db.authenticate(AdminConfig.MONGO_USERNAME, AdminConfig.MONGO_PASSWORD)

db = client.test
db.command("createUser", AdminConfig.MONGO_USERNAME, pwd=AdminConfig.MONGO_PASSWORD, roles=["readWrite"])
