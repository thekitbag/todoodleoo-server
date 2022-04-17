import os
from webapp import create_app, db
from webapp.models import Task, StatusUpdate, Theme, Timebox, Project
from config import Config, TestConfig, StagingConfig, DevelopmentConfig
from dotenv import load_dotenv

load_dotenv()

if os.environ['FLASK_ENV'] == 'development':
    app = create_app(DevelopmentConfig)
elif os.environ['FLASK_ENV'] == 'prod':
    app = create_app(Config)
elif os.environ['FLASK_ENV'] == 'staging':
    app = create_app(StagingConfig)
else:
    print('ENV NOT SET TO dev, staging or prod')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Task': Task, 'StatusUpdate': StatusUpdate, 'Theme': Theme, 'Timebox': Timebox, 'Project': Project}
