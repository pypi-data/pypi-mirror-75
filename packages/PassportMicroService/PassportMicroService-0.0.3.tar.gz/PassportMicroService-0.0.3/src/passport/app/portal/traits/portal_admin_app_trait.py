from flask_restful import Api

from passport.auth.traits import AuthTrait
from passport.core.views import api_common

api = Api()


class PortalAdminAppTrait(object):

    @staticmethod
    def portal_admin_app_list(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_app_list(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_app_info(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_app_info(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_app_modify(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_app_modify(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_app_delete(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_app_delete(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})
