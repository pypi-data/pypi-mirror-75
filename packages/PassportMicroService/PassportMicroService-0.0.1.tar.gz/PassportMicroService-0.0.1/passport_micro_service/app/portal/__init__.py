from flask import Blueprint
portal_bp = Blueprint('portal', __name__)
from app.portal.views import api
api.init_app(portal_bp)
