from mongoengine import Document, StringField, ReferenceField
from passport.model.app import App


class AppToken(Document):
    """
    应用凭据
    """
    token = StringField(
        required=True,
        max_length=500
    )
    access_key_id = StringField(
        required=True,
        max_length=200,
    )
    app = ReferenceField(App, reverse_delete_rule=4)
