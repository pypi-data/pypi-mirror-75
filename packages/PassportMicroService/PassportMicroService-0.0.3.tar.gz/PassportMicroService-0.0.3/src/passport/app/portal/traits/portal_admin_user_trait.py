from flask_restful import Api

from passport.auth.traits import AuthTrait
from passport.core.views import api_common

api = Api()


class PortalAdminUserTrait(object):

    @staticmethod
    def portal_admin_user_list(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_user_list(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_user_info(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_user_info(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_user_modify(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_user_modify(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_user_delete(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_user_delete(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_group_list(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_group_list(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_group_info(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_group_info(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_group_modify(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_group_modify(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})

    @staticmethod
    def portal_admin_group_delete(request):
        checked, app_client, request_data = AuthTrait.portal_auth_check(request)
        if checked:
            return app_client.admin_group_delete(
                user_token=request.headers['X-Token'],
                request_data=request_data
            )
        return api_common({})
