from flask import Blueprint

auth_user = Blueprint('auth_user', __name__)

from . import views,forms