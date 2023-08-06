from passport.auth.traits import AuthTrait
from passport.core.paginator_tools import paginator
from passport.core.views import api_common
from passport.model.group_manager import GroupManager
from passport.model.permission_manager import PermissionManager
from passport.model.role_manager import RoleManager
from passport.model.user import User
from passport.model.user_manager import UserManager


class AdminUserTrait(object):

    @staticmethod
    def user_list(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            user_objs = User.objects.all()

            users_page = paginator(flask_request=request, items=user_objs)
            response_data = users_page.params()

            user_objs_data = []
            for user_obj in users_page.items:
                roles_data = []
                for role in user_obj.roles:
                    roles_data.append({
                        'uuid': role.uuid,
                        'name': role.name
                    })

                user_objs_data.append({
                    'uuid': user_obj.uuid,
                    'name': user_obj.username,
                    'mobile': '',
                    'roles': roles_data
                })
            response_data['users'] = user_objs_data

            return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def user_info(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            user_obj = User.objects.filter(
                uuid=request_data['user_uuid']
            ).first()
            if user_obj:
                permissions_data = []
                roles_data = []
                groups_data = []

                # for permission in user_obj.permissions:
                #     permissions_data.append(permission.name)
                for role in user_obj.roles:
                    roles_data.append(role.name)
                # for group in user_obj.groups:
                #     groups_data.append(group.name)
                response_data = {
                    'uuid': user_obj.uuid,
                    'name': user_obj.username,
                    'permissions': permissions_data,
                    'roles': roles_data,
                    'groups': groups_data
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1,  data={})

    @staticmethod
    def user_modify(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            user_obj = User.objects.filter(
                uuid=request_data.get('user_uuid', '')
            ).first()
            if not user_obj:
                user_obj = UserManager.create_user(
                    username=request_data.get('username', ''),
                    password=request_data.get('password', '')
                )

            permission_objs = []
            if 'permissions' in request_data:
                permissions = request_data['permissions']
                permission_objs = PermissionManager.get_permission_by_names(permissions)

            role_objs = []
            if 'roles' in request_data:
                roles = request_data['roles']
                role_objs = RoleManager.get_role_by_names(roles)

            group_objs = []
            if 'groups' in request_data:
                groups = request_data['groups']
                group_objs = GroupManager.get_group_by_names(groups)

            UserManager.modify_user(
                user_uuid=user_obj.uuid,
                username=user_obj.username,
                password=request_data.get('password', ''),
                permissions=permission_objs,
                roles=role_objs,
                groups=group_objs,
            )
            response_data = {
                'uuid': user_obj.uuid,
                'name': user_obj.username,
            }
            return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})

    @staticmethod
    def user_delete(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            user_obj = User.objects.filter(
                uuid=request_data.get('user_uuid', '')
            ).first()
            if user_obj:
                result = UserManager.delete_user(
                    user_uuid=request_data.get('user_uuid', '')
                )
                if result:
                    response_data = {}
                    return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})

    @staticmethod
    def group_list(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            groups = GroupManager.list_group()
            groups_page = paginator(flask_request=request, items=groups)
            response_data = groups_page.params()
            group_objs_data = []
            for group_obj in groups_page.items:
                group_objs_data.append({
                    'uuid': group_obj.uuid,
                    'name': group_obj.name
                })
            response_data['groups'] = group_objs_data

            return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})

    @staticmethod
    def group_info(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            group_obj = GroupManager.get_group_by_uuid(group_uuid=request_data['group_uuid'])

            if group_obj:
                response_data = {
                    'uuid': group_obj.uuid,
                    'name': group_obj.name
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})

    @staticmethod
    def group_modify(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            group_obj = GroupManager.modify_group(
                group_uuid=request_data['group_uuid'],
                name=request_data['name']
            )
            if group_obj:
                response_data = {
                    'uuid': group_obj.uuid,
                    'name': group_obj.name
                }
                return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})

    @staticmethod
    def group_delete(request):
        cur_user_obj, request_data = AuthTrait.auth_check(request=request)

        # TODO: cur_user_obj.roles admin
        if cur_user_obj:

            GroupManager.delete_group(
                group_uuid=request_data['group_uuid'],
            )
            response_data = {}
            return api_common(code=20000, data=response_data)
        return api_common(code=-1, data={})
