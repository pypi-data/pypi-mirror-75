from flask import request
from flask_restful import Api, Resource

from app.user.traits.user_trait import UserTrait

api = Api()

"""
user
"""


@api.resource('/access/token')
class APIUserAccessToken(Resource):
    def post(self): return UserTrait.user_access_token(request=request)


@api.resource('/register')
class APIUserRegister(Resource):
    def post(self): return UserTrait.user_register(request=request)


@api.resource('/login')
class APIUserLogin(Resource):
    def post(self): return UserTrait.user_login(request=request)


@api.resource('/logout')
class APIUserLogout(Resource):
    def post(self): return UserTrait.user_logout(request=request)


@api.resource('/info')
class APIUserInfo(Resource):
    def post(self): return UserTrait.user_info(request=request)
