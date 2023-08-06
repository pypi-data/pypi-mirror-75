from datetime import timedelta

from passport.model.token_manager import TokenManager
from passport.model.user_manager import UserManager


class AuthUser(object):
    pass


class AuthManager(object):
    """
    认证管理
    """
    def __init__(self, app=None):
        pass

    @staticmethod
    def register(username=None, password=None):
        """
        注册
        :param username:
        :param password:
        :return:
        """
        if not username:
            return None
        if not password:
            return None

        user_obj = UserManager.get_user_by_username(username=username)
        if user_obj:
            return None

        user_obj = UserManager.create_user(username=username, password=password)

        timeout = timedelta(seconds=365 * 24 * 60 * 60)
        jwt_token = TokenManager.generate_token(user=user_obj, timeout=timeout)

        auth_user = AuthUser()
        auth_user.id = username
        auth_user.uuid = user_obj.uuid
        auth_user.token = jwt_token

        return auth_user

    @staticmethod
    def login(username=None, password=None):
        """
        登录
        :param username:
        :param password:
        :return:
        """
        if not username:
            return None

        if not password:
            return None

        user_obj = UserManager.get_user_by_username(username=username)
        if not user_obj:
            return None

        if user_obj.password != password:
            return None

        timeout = timedelta(seconds=365 * 24 * 60 * 60)
        jwt_token = TokenManager.generate_token(user=user_obj, timeout=timeout)

        auth_user = AuthUser()
        auth_user.id = username
        auth_user.uuid = user_obj.uuid
        auth_user.token = jwt_token

        return auth_user

    @staticmethod
    def logout(token):
        """
        登出
        :param username:
        :return:
        """
        TokenManager.clean_token(token)
