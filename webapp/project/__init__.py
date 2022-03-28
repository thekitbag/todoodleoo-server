from flask import Blueprint

bp = Blueprint('project', __name__)

from webapp.project import routes

from flask import Blueprint