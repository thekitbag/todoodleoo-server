from webapp.models import Task, Theme, Timebox, Project, User
from datetime import datetime, timedelta

def test_new_project():
	"""
	WHEN a new Project is created
	THEN it should have the given name
	"""
	p = Project(title='test project')
	assert p.title == 'test project'

def test_new_task(project):
	"""
	GIVEN a project
	WHEN a new Task is created with that project
	THEN it should have the given name and be in that project
	"""

	t = Task(title='Test Task', project=project)
	assert t.title == 'Test Task'
	assert t. project == project
	assert t in project.tasks	

def test_new_theme(project):
	"""
	GIVEN a project
	WHEN a new Theme is created
	THEN it should have the given name
	"""
	th = Theme(title='Test Theme', project=project)
	assert th.title == 'Test Theme'
	assert th.project == project 
	assert th in project.themes

def test_new_timebox(project):
	"""
	GIVEN a project
	WHEN a new Timebox is created
	THEN it should have the given name and dates
	"""
	tb = Timebox(title='To do before Christmas', start_time=datetime.now(), end_time=datetime.now() + timedelta(days=1))
	assert tb.title == 'To do before Christmas'
	assert tb.start_time - datetime.now() < timedelta(seconds=1)
	assert tb.end_time  - (datetime.now() + timedelta(days=1)) < timedelta(seconds=1)

def test_add_task_to_theme(random_data):
	"""
	GIVEN some sample data
	WHEN I create a task with a theme from the sample data
	THEN the task appears in the tasks for that theme and that task has that epic
	"""
	p = random_data['projects'][0]
	t = Task(title='Do Something Else', project=p)
	th = random_data['themes'][0]
	t.theme = th
	assert t in th.tasks
	assert t.theme == th

def test_add_task_to_timebox(random_data):
	"""
	GIVEN some sample data
	WHEN I create a task with a theme from the sample data
	THEN the task appears in the tasks for that theme and that task has that epic
	"""
	p = random_data['projects'][0]
	t = Task(title='Do Something cool', project=p)
	tb = random_data['timeboxes'][0]
	t.add_to_timebox(tb)
	assert t in tb.tasks
	assert t.timebox == tb

def test_user():
	"""
	GIVEN a user model
	WHEN a user is created
	THEN it should have the given username
	"""
	u = User(username='testy mctesterson')
	assert u.username == 'testy mctesterson'
	u.set_password('password1')
	assert u.check_password('password2') == False
	assert u.check_password('password1') == True


	