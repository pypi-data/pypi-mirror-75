from mongoengine import Document, StringField, ListField, ReferenceField
from passport.model.base import Permission, Role


class Group(Document):
    """
    组
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


class User(Document):
    """
    用户
    """
    uuid = StringField(
        required=True,
        max_length=200
    )
    username = StringField(
        required=True,
        max_length=200,
    )
    password = StringField(
        required=True,
        max_length=200
    )
    permissions = ListField(ReferenceField(Permission, reverse_delete_rule=4), verbose_name='权限')
    roles = ListField(ReferenceField(Role, reverse_delete_rule=4), verbose_name='角色')
    groups = ListField(ReferenceField(Group, reverse_delete_rule=4), verbose_name='组')
