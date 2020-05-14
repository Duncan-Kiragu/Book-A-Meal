from flask import Blueprint

auth_admin = Blueprint('auth_admin', __name__)

from . import views,forms