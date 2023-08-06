from flask import Blueprint
user_bp = Blueprint('user', __name__)
from app.user.views import api
api.init_app(user_bp)
