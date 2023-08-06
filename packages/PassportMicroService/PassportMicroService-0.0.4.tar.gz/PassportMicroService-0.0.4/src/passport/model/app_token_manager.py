from datetime import datetime
from flask import request
import jwt

from passport.model.app_token import AppToken


class AppTokenManager(object):
    """
    应用凭据管理
    """
    def __init__(self, app=None):
        pass

    @staticmethod
    def generate_app_token(client_app, timeout):
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
            'user_id': str(client_app.id),
            'uuid': client_app.uuid,
        }, 'secret', algorithm='HS256').decode('utf-8')

        token_obj = AppToken.objects.filter(app=client_app).first()
        if token_obj:
            token_obj.delete()

        token_obj = AppToken()
        token_obj.token = jwt_token
        token_obj.access_key_id = client_app.access_key_id
        token_obj.app = client_app
        token_obj.save()

        return jwt_token

    @staticmethod
    def clean_app_token():
        """
        清除应用凭据
        :return:
        """

        token = request.headers['X-AccessToken']

        if token:
            token_obj = AppToken.objects.filter(token=token).first()
            if token_obj:
                token_obj.delete()

    @staticmethod
    def get_app_by_token(token):
        if token:
            token_obj = AppToken.objects.filter(token=token).first()
            if token_obj and token_obj.app:
                return token_obj.app
        return None
