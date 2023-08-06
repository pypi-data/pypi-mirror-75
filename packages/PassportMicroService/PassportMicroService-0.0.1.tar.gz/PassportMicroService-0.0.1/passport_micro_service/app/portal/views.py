from flask import request
from flask_restful import Api, Resource

from app.portal.traits.portal_admin_app_trait import PortalAdminAppTrait
from app.portal.traits.portal_admin_base_trait import PortalAdminBaseTrait
from app.portal.traits.portal_admin_user_trait import PortalAdminUserTrait
from app.portal.traits.portal_user_trait import PortalUserTrait

api = Api()

"""
portal user
"""


@api.resource('/user/register')
class APIPortalUserRegister(Resource):
    def post(self): return PortalUserTrait.user_register(request=request)


@api.resource('/user/login')
class APIPortalUserLogin(Resource):
    def post(self): return PortalUserTrait.user_login(request=request)


@api.resource('/user/logout')
class APIPortalUserLogout(Resource):
    def post(self): return PortalUserTrait.user_logout(request=request)


@api.resource('/user/info')
class APIPortalUserInfo(Resource):
    def post(self): return PortalUserTrait.user_info(request=request)


"""
portal admin user
"""


@api.resource('/admin/user/list')
class APIPortalAdminUserList(Resource):
    def post(self): return PortalAdminUserTrait.portal_admin_user_list(request=request)


@api.resource('/admin/user/info')
class APIPortalAdminUserInfo(Resource):
    def post(self): return PortalAdminUserTrait.portal_admin_user_info(request=request)


@api.resource('/admin/user/modify')
class APIPortalAdminUserModify(Resource):
    def post(self): return PortalAdminUserTrait.portal_admin_user_modify(request=request)


@api.resource('/admin/user/delete')
class APIPortalAdminUserDelete(Resource):
    def post(self): return PortalAdminUserTrait.portal_admin_user_delete(request=request)


"""
portal admin group
"""


@api.resource('/admin/group/list')
class APIPortalAdminGroupList(Resource):
    def post(self): return PortalAdminUserTrait.portal_admin_group_list(request=request)


@api.resource('/admin/group/info')
class APIPortalAdminGroupInfo(Resource):
    def post(self): return PortalAdminUserTrait.portal_admin_group_info(request=request)


@api.resource('/admin/group/modify')
class APIPortalAdminGroupModify(Resource):
    def post(self): return PortalAdminUserTrait.portal_admin_group_modify(request=request)


@api.resource('/admin/group/delete')
class APIPortalAdminGroupDelete(Resource):
    def post(self): return PortalAdminUserTrait.portal_admin_group_delete(request=request)


"""
portal admin permission
"""


@api.resource('/admin/permission/list')
class APIPortalAdminPermissionList(Resource):
    def post(self): return PortalAdminBaseTrait.portal_admin_permission_list(request=request)


@api.resource('/admin/permission/info')
class APIPortalAdminPermissionInfo(Resource):
    def post(self): return PortalAdminBaseTrait.portal_admin_permission_info(request=request)


@api.resource('/admin/permission/modify')
class APIPortalAdminPermissionModify(Resource):
    def post(self): return PortalAdminBaseTrait.portal_admin_permission_modify(request=request)


@api.resource('/admin/permission/delete')
class APIPortalAdminPermissionDelete(Resource):
    def post(self): return PortalAdminBaseTrait.portal_admin_permission_delete(request=request)


"""
portal admin role
"""


@api.resource('/admin/role/list')
class APIPortalAdminRoleList(Resource):
    def post(self): return PortalAdminBaseTrait.portal_admin_role_list(request=request)


@api.resource('/admin/role/info')
class APIPortalAdminRoleInfo(Resource):
    def post(self): return PortalAdminBaseTrait.portal_admin_role_info(request=request)


@api.resource('/admin/role/modify')
class APIPortalAdminRoleModify(Resource):
    def post(self): return PortalAdminBaseTrait.portal_admin_role_modify(request=request)


@api.resource('/admin/role/delete')
class APIPortalAdminRoleDelete(Resource):
    def post(self): return PortalAdminBaseTrait.portal_admin_role_delete(request=request)


"""
portal admin app
"""


@api.resource('/admin/app/list')
class APIPortalAdminAppList(Resource):
    def post(self): return PortalAdminAppTrait.portal_admin_app_list(request=request)


@api.resource('/admin/app/info')
class APIPortalAdminAppInfo(Resource):
    def post(self): return PortalAdminAppTrait.portal_admin_app_info(request=request)


@api.resource('/admin/app/modify')
class APIPortalAdminAppModify(Resource):
    def post(self): return PortalAdminAppTrait.portal_admin_app_modify(request=request)


@api.resource('/admin/app/delete')
class APIPortalAdminAppDelete(Resource):
    def post(self): return PortalAdminAppTrait.portal_admin_app_delete(request=request)
