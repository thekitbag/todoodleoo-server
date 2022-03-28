from flask import Blueprint

bp = Blueprint('timebox', __name__)

from webapp.timebox import routes

from flask import Blueprint