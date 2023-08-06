from flask import request
from flask_restful import Api, Resource

from app.admin.traits.admin_app_trait import AdminAppTrait
from app.admin.traits.admin_base_trait import AdminBaseTrait
from app.admin.traits.admin_user_trait import AdminUserTrait

api = Api()

"""
admin user
"""


@api.resource('/user/list')
class APIAdminUserList(Resource):
    def post(self): return AdminUserTrait.user_list(request=request)


@api.resource('/user/info')
class APIAdminUserInfo(Resource):
    def post(self): return AdminUserTrait.user_info(request=request)


@api.resource('/user/modify')
class APIAdminUserModify(Resource):
    def post(self): return AdminUserTrait.user_modify(request=request)


@api.resource('/user/delete')
class APIAdminUserDelete(Resource):
    def post(self): return AdminUserTrait.user_delete(request=request)


"""
admin group
"""


@api.resource('/group/list')
class APIAdminGroupList(Resource):
    def post(self): return AdminUserTrait.group_list(request=request)


@api.resource('/group/info')
class APIAdminGroupInfo(Resource):
    def post(self): return AdminUserTrait.group_info(request=request)


@api.resource('/group/modify')
class APIAdminGroupModify(Resource):
    def post(self): return AdminUserTrait.group_modify(request=request)


@api.resource('/group/delete')
class APIAdminGroupDelete(Resource):
    def post(self): return AdminUserTrait.group_delete(request=request)


"""
admin permission
"""


@api.resource('/permission/list')
class APIAdminPermissionList(Resource):
    def post(self): return AdminBaseTrait.permission_list(request=request)


@api.resource('/permission/info')
class APIAdminPermissionInfo(Resource):
    def post(self): return AdminBaseTrait.permission_info(request=request)


@api.resource('/permission/modify')
class APIAdminPermissionModify(Resource):
    def post(self): return AdminBaseTrait.permission_modify(request=request)


@api.resource('/permission/delete')
class APIAdminPermissionDelete(Resource):
    def post(self): return AdminBaseTrait.permission_delete(request=request)


"""
admin role
"""


@api.resource('/role/list')
class APIAdminRoleList(Resource):
    def post(self): return AdminBaseTrait.role_list(request=request)


@api.resource('/role/info')
class APIAdminRoleInfo(Resource):
    def post(self): return AdminBaseTrait.role_info(request=request)


@api.resource('/role/modify')
class APIAdminRoleModify(Resource):
    def post(self): return AdminBaseTrait.role_modify(request=request)


@api.resource('/role/delete')
class APIAdminRoleDelete(Resource):
    def post(self): return AdminBaseTrait.role_delete(request=request)


"""
admin app
"""


@api.resource('/app/list')
class APIAdminAppList(Resource):
    def post(self): return AdminAppTrait.app_list(request=request)


@api.resource('/app/info')
class APIAdminAppInfo(Resource):
    def post(self): return AdminAppTrait.app_info(request=request)


@api.resource('/app/modify')
class APIAdminAppModify(Resource):
    def post(self): return AdminAppTrait.app_modify(request=request)


@api.resource('/app/delete')
class APIAdminAppDelete(Resource):
    def post(self): return AdminAppTrait.app_delete(request=request)
