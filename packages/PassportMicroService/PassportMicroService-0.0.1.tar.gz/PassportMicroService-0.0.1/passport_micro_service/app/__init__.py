from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from config import config

from core.middleware import Middleware
from passportsdk.client import AppClient


db = None
app_client = AppClient()


def create_app(config_name='dev'):
    _app = Flask(__name__)
    CORS(_app,
         supports_credentials=True,
         origins=[
             'http://www.9abox.cn',
             'http://127.0.0.1:8000',
             'http://localhost:9528',
             'http://localhost:9527'
         ])
    _app.config.from_object(config[config_name])
    config[config_name].init_app(_app)

    _app.secret_key = 'ac5bf3279f969704fc1e63f050c50e10985e50fd340e6069ec7e09df5442'

    global db
    global app_client

    Middleware.init_app(_app)

    db = MongoEngine(_app)

    app_client.init(_app)

    from app.user import user_bp
    _app.register_blueprint(user_bp, url_prefix='/api/user')

    from app.admin import admin_bp
    _app.register_blueprint(admin_bp, url_prefix='/api/admin')

    from app.portal import portal_bp
    _app.register_blueprint(portal_bp, url_prefix='/api/portal')

    return _app
