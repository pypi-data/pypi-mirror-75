from mongoengine import Document, StringField, ReferenceField

from passport.model.user import User


class Token(Document):
    """
    凭据
    """
    token = StringField(
        required=True,
        max_length=500
    )
    user_id = StringField(
        required=True,
        max_length=200,
    )
    username = StringField(
        required=True,
        max_length=200,
    )
    user = ReferenceField(User, reverse_delete_rule=4)
