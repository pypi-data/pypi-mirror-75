from datetime import timedelta
from uuid import uuid4
from passport.model.app import App
from passport.model.app_token_manager import AppTokenManager


class AppManager(object):
    """
    应用管理
    """
    @staticmethod
    def access_token(access_key_id, access_key_secret):
        """
        创建应用
        :param access_key_id:
        :param access_key_secret:
        :return:
        """

        app_obj = App.objects.filter(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        ).first()
        if not app_obj:
            return None

        timeout = timedelta(seconds=365 * 24 * 60 * 60)
        access_token = AppTokenManager.generate_app_token(app_obj, timeout)
        return access_token

    @staticmethod
    def create_app(name, access_key_id, access_key_secret):
        """
        创建应用
        :param access_key_id:
        :param access_key_secret:
        :return:
        """
        app_obj = App()
        app_obj.uuid = str(uuid4())
        app_obj.name = name
        app_obj.access_key_id = access_key_id
        app_obj.access_key_secret = access_key_secret
        app_obj.save()
        return app_obj

    @staticmethod
    def list_app():
        """
        应用列表
        :return:
        """
        apps = App.objects.all()
        return apps

    @staticmethod
    def modify_app(app_uuid, name, access_key_id, access_key_secret):
        """
        修改应用
        :param app_uuid:
        :param access_key_id:
        :param access_key_secret:
        :return:
        """
        app_obj = App.objects.filter(uuid=app_uuid).first()
        if not app_obj:
            app_obj = App()
            app_obj.uuid = str(uuid4())
        app_obj.name = name
        app_obj.access_key_id = access_key_id
        app_obj.access_key_secret = access_key_secret
        app_obj.save()

    @staticmethod
    def delete_app(app_uuid):
        """
        删除应用
        :param app_uuid:
        :return:
        """
        app_obj = App.objects.filter(uuid=app_uuid).first()
        if not app_obj:
            return None
        app_obj.delete()
        return True

    @staticmethod
    def get_app_by_uuid(app_uuid):
        app_obj = App.objects.filter(uuid=app_uuid).first()
        if not app_obj:
            return None
        return app_obj
