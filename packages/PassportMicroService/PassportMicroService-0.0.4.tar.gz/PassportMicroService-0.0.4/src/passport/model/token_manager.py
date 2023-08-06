from datetime import datetime

import jwt

from passport.model.token import Token


class TokenManager(object):
    """
    凭据管理
    """
    def __init__(self, app=None):
        pass

    @staticmethod
    def generate_token(user, timeout):
        """
        生成凭据
        :param user:
        :param timeout:
        :return:
        """

        jwt_token = jwt.encode({
            'exp': datetime.utcnow() + timeout,
            'iss': 'txin.auth',
            'iat': datetime.utcnow(),
            'user_id': str(user.id),
            'uuid': user.uuid,
        }, 'secret', algorithm='HS256').decode('utf-8')

        token_obj = Token.objects.filter(user=user).first()
        if token_obj:
            token_obj.delete()

        token_obj = Token()
        token_obj.token = jwt_token
        token_obj.user_id = str(user.id)
        token_obj.username = user.username
        token_obj.user = user
        token_obj.save()

        return jwt_token

    @staticmethod
    def clean_token(token):
        """
        清除凭据
        :param token:
        :return:
        """
        if token:
            token_obj = Token.objects.filter(token=token).first()
            if token_obj:
                token_obj.delete()

    @staticmethod
    def get_user_by_token(token):
        if token:
            token_obj = Token.objects.filter(token=token).first()
            if token_obj and token_obj.user:
                return token_obj.user
        return None
