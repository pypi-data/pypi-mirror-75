from uuid import uuid4
from passport.model.user import User


class UserManager(object):
    """
    用户管理
    """
    @staticmethod
    def create_user(username, password):
        """
        创建用户
        :param username:
        :param password:
        :return:
        """
        user_obj = User()
        user_obj.uuid = str(uuid4())
        user_obj.username = username
        user_obj.password = password
        user_obj.save()
        return user_obj

    @staticmethod
    def list_user():
        """
        用户列表
        :return:
        """
        users = User.objects.all()
        return users

    @staticmethod
    def modify_user(user_uuid, username, password, permissions, roles, groups):
        """
        修改用户
        :param user_uuid:
        :param username:
        :param password:
        :return:
        """
        user_obj = User.objects.filter(uuid=user_uuid).first()
        if not user_obj:
            return None
        user_obj.username = username
        user_obj.password = password
        user_obj.permissions = permissions
        user_obj.roles = roles
        user_obj.groups = groups
        user_obj.save()

    @staticmethod
    def delete_user(user_uuid):
        """
        删除用户
        :param user_uuid:
        :return:
        """
        # TODO: need remote user Token before you can delete the User
        user_obj = User.objects.filter(uuid=user_uuid).first()
        if not user_obj:
            return None
        user_obj.delete()
        return True

    @staticmethod
    def list_users_name():
        """
        用户名列表
        :return:
        """
        users = User.objects.all().values_list('username')
        return users

    @staticmethod
    def get_user_by_uuid(user_uuid):
        """
        获取用户-uuid
        :param username:
        :return:
        """
        user_obj = User.objects.filter(uuid=user_uuid).first()
        if not user_obj:
            return None
        return user_obj

    @staticmethod
    def get_user_by_username(username):
        """
        获取用户-用户名
        :param username:
        :return:
        """
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            return None
        return user_obj
