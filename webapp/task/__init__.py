from flask import Blueprint

bp = Blueprint('task', __name__)

from webapp.task import routes

from flask import Blueprint