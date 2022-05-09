from webapp.models import Task, Theme, Timebox, Project, User, Subtask
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
	THEN it should have the given name and be in that project and have no subtasks
	"""

	t = Task(title='Test Task', project=project)
	assert t.title == 'Test Task'
	assert t.project == project
	assert t.subtasks.all() == []
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

def test_timebox_change_status_to_closed(random_data):
	"""
	GIVEN a timebox with tasks in different statuses
	WHEN change status method is called
	THEN the timebox status is changed and all non-done tasks are returned to the backlog
	"""
	p = random_data['projects'][0]
	tb = p.timeboxes.all()[1]
	tasks = tb.tasks.all()
	non_done_tasks = [t for t in tasks if t.status != 'Done']
	tb.change_status('Closed')
	tasks2 = tb.tasks.all()
	backlog = p.timeboxes.all()[0]
	assert tb.status == 'Closed'
	assert set([t.status for t in tasks2]) == {'Done'}
	for task in non_done_tasks:
		assert task in backlog.tasks.all()

def test_create_subtask(project):
	"""
	GIVEN a task
	WHEN add subtask method of that task is called
	THEN subtask should be in the subtasks of that task
	"""
	t = Task(title='new task', project=project)
	t.add_subtask("I'm a subtask of the new task")
	assert len(t.subtasks.all()) == 1
	st = t.subtasks.first()
	assert st.title == "I'm a subtask of the new task"
	assert st.status == 'To Do'

def test_delete_subtask(project):
	"""
	GIVEN a task with a subtask
	WHEN delete subtask method is called
	THEN subtask should be deleted
	"""
	t = Task(title='new task', project=project)
	t.add_subtask("I'm a subtask of the new task")
	assert len(t.subtasks.all()) == 1
	st = t.subtasks.first()
	stid = st.id
	print('st=',st)
	t.delete_subtask(st)
	assert len(t.subtasks.all()) == 0
	assert Subtask.query.get(stid) == None

def test_change_subtask_status(project):
	"""
	GIVEN a task with a subtask
	WHEN the change_status method of that subtask is called
	THEN subtask's status should be changed to the target status
	"""
	t = Task(title='new task', project=project)
	t.add_subtask("I'm a subtask of the new task")
	st = t.subtasks.first()
	assert st.status == 'To Do'
	st.change_status('In Progress')
	assert st.status == 'In Progress'
	st.change_status('Done')
	assert st.status == 'Done'
	st.change_status('To Do')
	assert st.status == 'To Do'

def test_first_subtask_in_progress(project):
	"""
	GIVEN a task with subtasks
	WHEN the first subtask changes status to in progress
	THEN the status of the parent task is changed to in progress
	"""
	t = Task(title='new task', project=project, status='To Do')
	t.add_subtask("I'm a subtask of the new task")
	st = t.subtasks.first()
	assert t.status == 'To Do'
	st.change_status('In Progress')
	assert st.status == 'In Progress'
	assert t.status == 'In Progress'

def test_last_subtask_done(project):
	t = Task(title='new task', project=project, status='To Do')
	for i in range(3):
		t.add_subtask(f"I'm subtask number {i} of the new task")
	for st in t.subtasks.all():
		st.change_status('Done')
		if set(subtask.status for subtask in t.subtasks.all()) != {'Done'}:
			assert t.status == 'In Progress'
		else:
			assert t.status == 'Done'
