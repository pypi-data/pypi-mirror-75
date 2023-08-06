from passport.auth.traits import AuthTrait
from passport.core.paginator_tools import paginator
from passport.core.views import api_common
from passport.model.app_manager import AppManager


class AdminAppTrait(object):

    @staticmethod
    def app_list(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            apps = AppManager.list_app()
            apps_page = paginator(flask_request=request, items=apps)
            response_data = apps_page.params()
            apps_objs_data = []
            for apps_obj in apps_page.items:
                apps_objs_data.append({
                    'uuid': apps_obj.uuid,
                    'name': apps_obj.name
                })
            response_data['apps'] = apps_objs_data

            return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})

    @staticmethod
    def app_info(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            apps_obj = AppManager.get_app_by_uuid(app_uuid=request_data['app_uuid'])

            if apps_obj:
                response_data = {
                    'uuid': apps_obj.uuid,
                    'name': apps_obj.name,
                    'access_key_id': apps_obj.access_key_id,
                    'access_key_secret': apps_obj.access_key_secret,
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})

    @staticmethod
    def app_modify(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            apps_obj = AppManager.modify_app(
                app_uuid=request_data['app_uuid'],
                name=request_data['name'],
                access_key_id=request_data['access_key_id'],
                access_key_secret=request_data['access_key_secret'],
            )
            if apps_obj:
                response_data = {
                    'uuid': apps_obj.uuid,
                    'name': apps_obj.name,
                    'access_key_id': request_data['access_key_id'],
                    'access_key_secret': request_data['access_key_secret'],
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})

    @staticmethod
    def app_delete(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            AppManager.delete_app(
                app_uuid=request_data['app_uuid'],
            )
            response_data = {}
            return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})
