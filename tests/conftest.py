import pytest
import config
import random
from datetime import datetime
from flask.testing import FlaskClient
from webapp import create_app, db
from flask import current_app
from webapp.models import Theme, Timebox, Task, Project

@pytest.fixture(scope='function')
def models():
    return {'timebox': Timebox}

@pytest.fixture(scope='function')
def logged_in_client(database, app):

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    r = testing_client.post('/register',
                                    json=dict(username='mark', password='Password1'))
    r2 = testing_client.post('/login',
                                    json=dict(username='mark', password='Password1'))

    yield testing_client  # this is where the testing happens!

    ctx.pop()




@pytest.fixture(scope='session')
def app():
    flask_app = create_app(config.TestConfig)
    return flask_app

@pytest.fixture(scope='function')
def database(app):
    # app is an instance of a flask app, _db a SQLAlchemy DB
    with app.app_context():
        db.create_all()

        yield db

    # Explicitly close DB connection
        db.session.close()

        db.drop_all()

@pytest.fixture(scope='function')
def test_client(database, app):

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='function')
def project(database):
    p = Project(title='test project', project_type='board')
    db.session.add(p)
    db.session.commit()
    return p

@pytest.fixture(scope='function')
def sample_data(database, logged_in_client):
    logged_in_client.post('add_project', json={'title': 'test  project 1', 'project_type': 'board'})
    logged_in_client.post('add_project', json={'title': 'test  project 2', 'project_type': 'board'})

    p1 = Project.query.filter_by(title='test  project 1').first()
    p2 = Project.query.filter_by(title='test  project 2').first()

    logged_in_client.post('/add_theme', json={'project_id': p1.id, 'title': 'test theme 11'})
    logged_in_client.post('/add_theme', json={'project_id': p1.id, 'title': 'test theme 12'})
    logged_in_client.post('/add_theme', json={'project_id': p2.id, 'title': 'test theme 21'})
    logged_in_client.post('/add_theme', json={'project_id': p2.id, 'title': 'test theme 22'})

    logged_in_client.post('add_timebox', json={'project_id': p1.id, 'title': 'To Do This Week', 'goal': []})
    logged_in_client.post('add_timebox', json={'project_id': p2.id, 'title': 'To Do This Week', 'goal': 'feel good'})

    logged_in_client.post('add_task', json={'project_id': p1.id, 'title': 'test task A'})
    logged_in_client.post('add_task', json={'project_id': p1.id, 'title': 'test task B'})
    logged_in_client.post('add_task', json={'project_id': p1.id, 'title': 'test task C'})
    logged_in_client.post('add_task', json={'project_id': p1.id, 'title': 'test task D'})
    logged_in_client.post('add_task', json={'project_id': p2.id, 'title': 'test task E'})
    logged_in_client.post('add_task', json={'project_id': p2.id, 'title': 'test task F'})
    logged_in_client.post('add_task', json={'project_id': p2.id, 'title': 'test task G'})
    logged_in_client.post('add_task', json={'project_id': p2.id, 'title': 'test task H'})

    logged_in_client.post('add_subtask', json={'project_id': p1.id, 'task_id':2, 'title': 'test subtask 1'})

@pytest.fixture(scope='function')
def random_data(database):
    statuses = ['To Do', 'In Progress', 'Done']
    verbs = ['Do', 'Make', 'Watch', 'Learn', 'Find', 'Investigate', 'Tidy', 'Book']
    nouns = ['Garden', 'TV', 'Kitchen', 'TV', 'Cinema', 'Homework', 'Laundry', 'Holiday']
    events = ['Tomorrow', 'Sunday', 'Christmas', 'Holidays', 'Birth', 'Wedding']
    projects = []
    themes = []
    timeboxes = []
    tasks = []
    for i in range(random.randint(1,4)):
        p = Project(title=random.choice(nouns) + ' List ' + str(random.randint(1,10)))
        projects.append(p)
    for p in projects:
        for i in range(random.randint(1,7)):
            th = Theme(project=p, title=random.choice(verbs)+'ing things')
            themes.append(th)
        backlog = Timebox(project=p, title='Backlog', status='To Do')
        timeboxes.append(backlog)
        for i in range(1,3):
            tb = Timebox(project=p, title='To do before ' + random.choice(events),
                status=random.choice(['To Do', 'In Progress', 'Closed']))
            timeboxes.append(tb)
        for i in p.timeboxes.all():
            for j in range(1,10):
                t = Task(project=p,
                    theme=random.choice(p.themes.all()),
                    title=random.choice(verbs) + ' ' + random.choice(nouns),
                    status=random.choice(statuses),
                    priority=j
                    )
                t.add_to_timebox(i)
                tasks.append(t)

    db.session.add_all(projects)
    db.session.add_all(themes)
    db.session.add_all(timeboxes)
    db.session.add_all(tasks)
    db.session.commit()

    data = {
    'projects': projects,
    'themes': themes,
    'timeboxes': timeboxes,
    'tasks': tasks
    }

    return data
