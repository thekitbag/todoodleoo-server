from flask import Blueprint

bp = Blueprint('theme', __name__)

from webapp.theme import routes

from flask import Blueprint