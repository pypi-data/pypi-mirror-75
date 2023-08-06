from mongoengine import Document, StringField


class App(Document):
    """
    应用
    """
    uuid = StringField(
        required=True,
        max_length=200
    )
    name = StringField(
        required=True,
        max_length=200
    )
    access_key_id = StringField(
        required=True,
        max_length=200
    )
    access_key_secret = StringField(
        required=True,
        max_length=200
    )
