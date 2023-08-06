from passport.model.token_manager import TokenManager

from app import app_client


class AuthTrait(object):

    @staticmethod
    def portal_auth_check(request, need_auth=True):
        """
        认证检查
        :param request:
        :return:
        """
        request_data = request.get_json(silent=True)
        if app_client and app_client.get_access_token():
            if need_auth:
                if 'X-Token' in request.headers:
                    return True, app_client, request_data
            else:
                return True, app_client, request_data
        return False, app_client, request_data

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
