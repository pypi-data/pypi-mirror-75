from mongoengine import Document, StringField, ListField, ReferenceField
from passport.model.app import App


class Permission(Document):
    """
    权限
    """
    uuid = StringField(
        required=True,
        max_length=200
    )
    name = StringField(
        required=True,
        max_length=200
    )
    app = ListField(ReferenceField(App, reverse_delete_rule=4), verbose_name='应用')


class Role(Document):
    """
    角色
    """
    uuid = StringField(
        required=True,
        max_length=200
    )
    name = StringField(
        required=True,
        max_length=200
    )
    permission = ListField(ReferenceField(Permission, reverse_delete_rule=4), verbose_name='权限')
