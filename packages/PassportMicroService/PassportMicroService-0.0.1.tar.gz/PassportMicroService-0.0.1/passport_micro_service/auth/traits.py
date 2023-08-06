from core.paginator_tools import paginator
from core.views import api_common
from model.permission_manager import PermissionManager
from model.role_manager import RoleManager
from model.token_manager import TokenManager
from app import app_client


class AuthTrait(object):

    @staticmethod
    def portal_auth_check(request):
        """
        认证检查
        :param request:
        :return:
        """
        if 'X-Token' in request.headers:
            if app_client and app_client.get_access_token():
                request_data = request.get_json(silent=True)
                return True, app_client, request_data
        return False, app_client, None

    @staticmethod
    def auth_check(request):
        """
        登录检查
        :param request:
        :return:
        """
        request_data = request.get_json(silent=True)

        if request_data['token']:

            cur_user_obj = TokenManager.get_user_by_token(
                token=request_data['token']
            )

            # TODO: cur_user_obj.roles admin
            if cur_user_obj:
                return cur_user_obj, request_data
        return None, request_data
