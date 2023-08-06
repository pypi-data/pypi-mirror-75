from flask_restful import Api

from passport.auth.traits import AuthTrait
from passport.core.views import api_common

api = Api()


class PortalUserTrait(object):

    @staticmethod
    def user_register(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.user_register(
                username=request_data['username'],
                password=request_data['password']
            )
        return api_common(code=-1,  data={})

    @staticmethod
    def user_login(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request=request, need_auth=False)
        if checked:
            return app_client.user_login(
                username=request_data['username'],
                password=request_data['password']
            )
        return api_common(code=-1,  data={})

    @staticmethod
    def user_logout(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.user_logout(request.headers['X-Token'])
        return api_common(code=-1,  data={})

    @staticmethod
    def user_info(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.user_info(request.headers['X-Token'])
        return api_common(code=-1,  data={})
