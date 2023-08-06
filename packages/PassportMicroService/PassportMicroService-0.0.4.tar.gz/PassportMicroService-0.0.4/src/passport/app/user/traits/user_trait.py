from flask_restful import Api
from passport.auth.auth_manager import AuthManager
from passport.auth.traits import AuthTrait
from passport.core.views import api_common
from passport.model.app_manager import AppManager

api = Api()


class UserTrait(object):

    @staticmethod
    def user_access_token(request):
        request_data = request.get_json(silent=True)
        access_token = AppManager.access_token(
            access_key_id=request_data['access_key_id'],
            access_key_secret=request_data['access_key_secret']
        )
        if access_token:
            response_data = {
                'access_token': str(access_token)
            }
            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def user_register(request):
        request_data = request.get_json(silent=True)

        auth_user = AuthManager.register(
            username=request_data['username'],
            password=request_data['password']
        )
        if auth_user:
            response_data = {
                'token': auth_user.token
            }
            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def user_login(request):
        request_data = request.get_json(silent=True)

        auth_user = AuthManager.login(
            username=request_data['username'],
            password=request_data['password']
        )
        if auth_user:
            response_data = {
                'token': auth_user.token
            }
            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def user_logout(request):
        request_data = request.get_json(silent=True)

        AuthManager.logout(
            token=request_data['token']
        )
        response_data = {}
        return api_common(code=20000, data=response_data)

    @staticmethod
    def user_info(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)
        if cur_user_obj:

            permissions_data = []
            roles_data = []
            groups_data = []

            for permission in cur_user_obj.permissions:
                permissions_data.append(permission.name)
            for role in cur_user_obj.roles:
                roles_data.append(role.name)
            for group in cur_user_obj.groups:
                groups_data.append(group.name)
            response_data = {
                'uuid': cur_user_obj.uuid,
                'name': cur_user_obj.username,
                'permissions': permissions_data,
                'roles': roles_data,
                'groups': groups_data
            }
            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})
