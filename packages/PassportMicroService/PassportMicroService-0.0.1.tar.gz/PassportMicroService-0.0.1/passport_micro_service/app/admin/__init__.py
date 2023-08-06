from flask import Blueprint
admin_bp = Blueprint('admin', __name__)
from app.admin.views import api
api.init_app(admin_bp)
