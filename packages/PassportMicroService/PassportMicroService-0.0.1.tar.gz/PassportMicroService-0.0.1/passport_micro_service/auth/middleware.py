from flask import request
from core.views import api_common
from model.user_manager import UserManager
from model.token_manager import TokenManager
from model.app_token_manager import AppTokenManager


class UserAuthMiddleware(object):

    def __init__(self, app):
        @app.before_request
        def middleware_before_request():
            if not request.path.startswith('/api/user') and\
                    not request.path.startswith('/api/admin'):
                if request.path not in [
                    '/api/portal/user/register',
                    '/api/portal/user/login',
                ]:
                    if 'X-Token' in request.headers:
                        print('[UserAuthMiddleware] X-Token: ', len(request.headers['X-Token']))
                    else:
                        return api_common(
                            code=-1,
                            data={
                                'message': 'X-Token invaild'
                            }
                        )


class AppAuthMiddleware(object):

    def __init__(self, app):
        @app.before_request
        def middleware_before_request():
            if request.path.startswith('/api/user') or\
                    request.path.startswith('/api/admin'):
                if request.path not in [
                    # '/api/user/register',
                    # '/api/user/login',
                    # '/api/user/logout',
                    '/api/user/access/token'
                ]:
                    if 'X-AccessToken' in request.headers:
                        print('[AppAuthMiddleware] X-AccessToken: ', len(request.headers['X-AccessToken']))
                    else:
                        return api_common(
                            code=-1,
                            data={
                                'message': 'X-AccessToken invaild'
                            }
                        )
