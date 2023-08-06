from passport.auth.traits import AuthTrait
from passport.core.paginator_tools import paginator
from passport.core.views import api_common
from passport.model.permission_manager import PermissionManager
from passport.model.role_manager import RoleManager


class AdminBaseTrait(object):

    @staticmethod
    def permission_list(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            permissions = PermissionManager.list_permission()
            permissions_page = paginator(flask_request=request, items=permissions)
            response_data = permissions_page.params()
            permission_objs_data = []
            for permission_obj in permissions_page.items:
                permission_objs_data.append({
                    'uuid': permission_obj.uuid,
                    'name': permission_obj.name,
                    'app': permission_obj.app
                })
            response_data['permissions'] = permission_objs_data

            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def permission_info(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            permission_obj = PermissionManager.get_permission_by_uuid(
                permission_uuid=request_data['permission_uuid']
            )
            if permission_obj:
                response_data = {
                    'uuid': permission_obj.uuid,
                    'name': permission_obj.name,
                    'app': permission_obj.app
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def permission_modify(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            permission_obj = PermissionManager.modify_permission(
                permission_uuid=request_data['permission_uuid'],
                name=request_data['name']
            )
            if permission_obj:
                response_data = {
                    'uuid': permission_obj.uuid,
                    'name': permission_obj.name,
                    'app': permission_obj.app
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def permission_delete(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            PermissionManager.delete_group(
                permission_uuid=request_data['permission_uuid']
            )
            response_data = {}
            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def role_list(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            roles = RoleManager.list_role()
            roles_page = paginator(flask_request=request, items=roles)
            response_data = roles_page.params()
            role_objs_data = []
            for role_obj in roles_page.items:
                role_objs_data.append({
                    'uuid': role_obj.uuid,
                    'name': role_obj.name,
                    'permission': role_obj.permission
                })
            response_data['roles'] = role_objs_data
            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def role_info(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            role_obj = RoleManager.get_role_by_uuid(role_uuid=request_data['role_uuid'])

            if role_obj:
                response_data = {
                    'uuid': role_obj.uuid,
                    'name': role_obj.name,
                    'permission': role_obj.permission
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def role_modify(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            role_obj = RoleManager.modify_role(
                role_uuid=request_data['role_uuid'],
                name=request_data['name']
            )
            if role_obj:
                response_data = {
                    'uuid': role_obj.uuid,
                    'name': role_obj.name,
                    'permission': role_obj.permission
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def role_delete(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            RoleManager.delete_role(
                role_uuid=request_data['role_uuid']
            )
            response_data = {}
            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})
