from uuid import uuid4
from passport.model.base import Role


class RoleManager(object):
    """
    权限管理
    """

    @staticmethod
    def create_role(name):
        """
        创建组别
        :param name:
        :return:
        """
        role_obj = Role()
        role_obj.uuid = str(uuid4())
        role_obj.name = name
        role_obj.save()
        return role_obj

    @staticmethod
    def list_role():
        """
        角色列表
        :return:
        """
        roles = Role.objects.all()
        return roles

    @staticmethod
    def modify_role(role_uuid, name):
        """
        修改角色
        :param role_uuid:
        :param name:
        :return:
        """
        role_obj = Role.objects.filter(uuid=role_uuid).first()
        if not role_obj:
            role_obj = RoleManager.create_role(name)
        else:
            role_obj.name = name
            role_obj.save()
        return role_obj

    @staticmethod
    def delete_role(role_uuid):
        """
        删除组别
        :param role_uuid:
        :return:
        """
        role_obj = Role.objects.filter(uuid=role_uuid).first()
        if not role_obj:
            return None
        role_obj.delete()
        return True

    @staticmethod
    def list_roles_name():
        """
        角色名列表
        :return:
        """
        roles = Role.objects.all().values_list('name')
        return roles

    @staticmethod
    def get_role_by_uuid(role_uuid):
        """
        获取角色信息-uuid
        :param role_uuid:
        :return:
        """
        role_obj = Role.objects.filter(uuid=role_uuid).first()
        if not role_obj:
            return None
        return role_obj

    @staticmethod
    def get_role_by_names(role_names):
        """
        获取角色信息-uuid
        :param role_uuid:
        :return:
        """
        role_objs = Role.objects.filter(name__in=role_names)
        if not role_objs:
            return None
        return role_objs
