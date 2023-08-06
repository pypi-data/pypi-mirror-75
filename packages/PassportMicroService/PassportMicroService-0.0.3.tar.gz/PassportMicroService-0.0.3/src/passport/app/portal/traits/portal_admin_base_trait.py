from flask_restful import Api

from passport.auth.traits import AuthTrait
from passport.core.views import api_common

api = Api()


class PortalAdminBaseTrait(object):

    @staticmethod
    def portal_admin_permission_list(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_permission_list(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_permission_info(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_permission_info(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_permission_modify(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_permission_modify(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_permission_delete(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_permission_delete(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_role_list(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_role_list(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_role_info(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_role_info(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_role_modify(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_role_modify(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_role_delete(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_role_delete(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})
