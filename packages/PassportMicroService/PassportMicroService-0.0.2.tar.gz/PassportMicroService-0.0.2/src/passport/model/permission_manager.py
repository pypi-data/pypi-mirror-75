from uuid import uuid4
from passport.model.base import Permission


class PermissionManager(object):
    """
    权限管理
    """

    @staticmethod
    def create_group(name):
        """
        创建组别
        :param name:
        :return:
        """
        permission_obj = Permission()
        permission_obj.uuid = str(uuid4())
        permission_obj.name = name
        permission_obj.save()
        return permission_obj

    @staticmethod
    def list_permission():
        """
        权限列表
        :return:
        """
        permissions = Permission.objects.all()
        return permissions

    @staticmethod
    def modify_permission(permission_uuid, name):
        """
        修改权限
        :param permission_uuid:
        :param name:
        :return:
        """
        permission_obj = Permission.objects.filter(uuid=permission_uuid).first()
        if not permission_obj:
            permission_obj = PermissionManager.create_group(name)
        else:
            permission_obj.name = name
            permission_obj.save()
        return permission_obj

    @staticmethod
    def delete_group(permission_uuid):
        """
        删除组别
        :param group_uuid:
        :return:
        """
        permission_obj = Permission.objects.filter(uuid=permission_uuid).first()
        if not permission_obj:
            return None
        permission_obj.delete()
        return True

    @staticmethod
    def list_permissions_name():
        """
        权限名列表
        :return:
        """
        permissions = Permission.objects.all().values_list('name')
        return permissions

    @staticmethod
    def get_permission_by_uuid(permission_uuid):
        """
        获取权限信息-uuid
        :param permission_uuid:
        :return:
        """
        permission_obj = Permission.objects.filter(uuid=permission_uuid).first()
        if not permission_obj:
            return None
        return permission_obj

    @staticmethod
    def get_permission_by_names(permission_names):
        """
        获取权限信息-uuid
        :param permission_uuid:
        :return:
        """
        permission_objs = Permission.objects.filter(name__in=permission_names)
        if not permission_objs:
            return None
        return permission_objs
