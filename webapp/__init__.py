from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager




db = SQLAlchemy()
migrate = Migrate(db)
login = LoginManager()


import webapp.main.routes

from webapp.models import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from webapp.task import bp as task_bp
    app.register_blueprint(task_bp)

    from webapp.timebox import bp as timebox_bp
    app.register_blueprint(timebox_bp)

    from webapp.theme import bp as theme_bp
    app.register_blueprint(theme_bp)

    from webapp.project import bp as project_bp
    app.register_blueprint(project_bp)

    from webapp.main import bp as main_bp
    app.register_blueprint(main_bp)

    from webapp.auth import bp as auth_bp
    app.register_blueprint(auth_bp)


    return app

import webapp.models
