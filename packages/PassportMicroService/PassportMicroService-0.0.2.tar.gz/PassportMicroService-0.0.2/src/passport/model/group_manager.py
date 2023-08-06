from uuid import uuid4
from passport.model.user import Group


class GroupManager(object):
    """
    组别管理
    """
    @staticmethod
    def create_group(name):
        """
        创建组别
        :param name:
        :return:
        """
        group_obj = Group()
        group_obj.uuid = str(uuid4())
        group_obj.name = name
        group_obj.save()
        return group_obj

    @staticmethod
    def list_group():
        """
        组别列表
        :return:
        """
        groups = Group.objects.all()
        return groups

    @staticmethod
    def modify_group(group_uuid, name):
        """
        修改组别
        :param group_uuid:
        :param name:
        :return:
        """
        group_obj = Group.objects.filter(uuid=group_uuid).first()
        if not group_obj:
            group_obj = GroupManager.create_group(name)
        else:
            group_obj.name = name
            group_obj.save()
        return group_obj

    @staticmethod
    def delete_group(group_uuid):
        """
        删除组别
        :param group_uuid:
        :return:
        """
        group_obj = Group.objects.filter(uuid=group_uuid).first()
        if not group_obj:
            return None
        group_obj.delete()
        return True

    @staticmethod
    def list_groups_name():
        """
        组别名列表
        :return:
        """
        groups = Group.objects.all().values_list('name')
        return groups

    @staticmethod
    def get_group_by_uuid(group_uuid):
        """
        获取组别-uuid
        :param group_uuid:
        :return:
        """
        group_obj = Group.objects.filter(uuid=group_uuid).first()
        if not group_obj:
            return None
        return group_obj

    @staticmethod
    def get_group_by_names(group_name):
        """
        获取组别-uuid
        :param group_uuid:
        :return:
        """
        group_objs = Group.objects.filter(uuid=group_name)
        if not group_objs:
            return None
        return group_objs
