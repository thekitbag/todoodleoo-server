from datetime import datetime, timedelta, time

def test_get_projects_new_app(logged_in_client):
	"""
	Given a fresh instance of the app
	When the get_boards route is called
	Then the response is valid, content type is JSON and all fields are there but empty
	""" 
	with logged_in_client as c:
		response = logged_in_client.get('/get_projects')
		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = response.json
		assert response_body['projects'] == []

def test_add_project(logged_in_client):
	"""
	GIVEN a fresh instance of the app
	WHEN add project is called
	THEN the project is stored and appears in the response
	"""
	with logged_in_client as c:
		r = logged_in_client.get('/get_projects')
		response_body = r.json
		assert response_body['projects'] == []
		data = {'title': 'test project'}
		r2 = logged_in_client.post('/add_project', json=data)
		assert r2.status_code == 200
		r2_body = r2.json
		assert r2_body['projects'][0]['project_title'] == 'test project'

def test_get_tasks_new_app(logged_in_client):
	"""
	GIVEN a new project
	WHEN the get_tasks route is called for that project
	THEN the response is valid, content type is json and all fields are there but empty
	"""
	with logged_in_client as c:
		data = {'title': 'test project'}
		r = logged_in_client.post('/add_project', json=data)
		r_body = r.json
		project_id = r_body['projects'][0]['project_id']
		response = logged_in_client.get(f'/get_tasks?project_id={project_id}')
		assert response.status_code == 200
		assert response.headers["Content-Type"] == "application/json"
		response_body = response.json
		assert response_body['tasks'] == []
		assert response_body['themes'] == []
		assert 'Backlog' in [tb['title'] for tb in response_body['timeboxes']]

def test_get_tasks_existing_data(sample_data, test_client):
	"""
	GIVEN a project with sample data
	WHEN the get_tasks route is called for that project
	THEN the response is valid, content type is json and all fields are present
	"""
	response = test_client.get(f'/get_tasks?project_id={1}')
	assert response.status_code == 200
	assert response.headers["Content-Type"] == "application/json"
	response_body = response.json
	tasks = response_body['tasks']
	themes = response_body['themes']
	timeboxes = response_body['timeboxes']
	assert tasks[0] == {'id': 1, 
	'priority': 0, 
	'status': 'To Do', 
	'theme': 'No Theme', 
	'theme_color': None, 
	'timebox': 'Backlog', 
	'title': 'test task A'
	}

	assert themes[0]['title'] == 'test theme 11'

def test_add_task(test_client, sample_data):
	"""
	GIVEN a project
	WHEN add task is called with that project's ID
	THEN the task should appear in the get tasks response for that project
	"""
	task_data = {
	'project_id': 1,
	'title': 'test task with very specific name'
	}
	r2 = test_client.post('/add_task', json=task_data)
	r3 = test_client.get(f'/get_tasks?project_id={1}')
	r3_body = r3.json
	tasks = r3_body['tasks']
	matching_tasks = [task for task in tasks if task['title'] == 'test task with very specific name']
	assert len(matching_tasks) == 1

def test_add_theme(test_client, sample_data):
	"""
	GIVEN a project
	WHEN add theme is called
	THEN the theme should appear in the get tasks reponse for that project
	"""
	theme_data = {
	'project_id': 1,
	'title': 'test theme'
	}
	r = test_client.post('/add_theme', json=theme_data)
	r2 = test_client.get(f'/get_tasks?project_id={1}')
	r2_body = r2.json
	assert r2_body['themes'][0]['title'] == 'test theme 11'

def test_add_timebox(test_client, sample_data):
	"""
	GIVEN a project
	WHEN add timebox is called
	THEN the timebox should appear in the get tasks reponse for that project
	"""
	timebox_data = {
	'project_id': 1,
	'title': 'test timebox abc',
	'start_time': datetime.now(),
	'end_time': datetime.now() + timedelta(days=1)
	}
	r = test_client.post('/add_timebox', json=timebox_data)
	r2 = test_client.get(f'/get_tasks?project_id={1}')
	r2_body = r2.json
	assert 'test timebox abc' in [tb['title'] for tb in r2_body['timeboxes']]

def test_add_project_existing(sample_data, logged_in_client):
	"""
	GIVEN an app with test data
	WHEN add project is called
	THEN the number of projects increases by 1 and the new project is in the get projects response
	"""
	r = logged_in_client.get('get_projects')
	r_body = r.json
	assert len(r_body['projects']) == 2
	r2 = logged_in_client.post('add_project', json={'title': 'Shiny New Project'})
	r2_body = r2.json
	assert len(r2_body['projects']) == 3
	assert r2_body['projects'][2]['project_title'] == 'Shiny New Project'

def test_delete_task(sample_data, test_client):
	"""
	GIVEN some test data
	WHEN delete task is called 
	THEN task should be deleted from the test data
	"""
	r = test_client.get('get_tasks?project_id=2')
	r_body = r.json
	assert len(r_body['tasks']) == 4
	r2 = test_client.post('delete_task', json = {'project_id': 2, 'task_id': r_body['tasks'][0]['id']})
	r3 =  test_client.get('get_tasks?project_id=2')
	r3_body = r3.json
	assert len(r3_body['tasks']) == 3

def test_timebox_shortcuts_1(test_client, random_data):
	"""
	GIVEN a project
	WHEN timebox shortcut is called with valid projectId and timebox short cut one
	THEN timebox is returned in response with title 'To Do Today', start time of now
	and end time of midnight tonight
	"""
	project_id = random_data['projects'][0].id
	r = test_client.post('/timebox_shortcuts', json={'project_id': project_id, 'shortcut_id': 1 })
	r_body = r.json
	assert r_body['title'] == 'To Do Today'
	assert datetime.strptime(r_body['start_time'], '%a, %d %b %Y %H:%M:%S GMT') < datetime.now() + timedelta(seconds=1)
	assert datetime.strptime(r_body['end_time'], '%a, %d %b %Y %H:%M:%S GMT') > datetime.now()
	assert datetime.strptime(r_body['end_time'], '%a, %d %b %Y %H:%M:%S GMT') < datetime.now() + timedelta(days=1)

def test_update_task_priority(random_data, test_client):
	"""
	GIVEN some sample data
	WHEN update task is called with updated priority on one of those tasks
	THEN when get tasks is called, that tasks priority has been updated
	"""
	r = test_client.get('/get_tasks?project_id=1')
	r_body = r.json
	t = [task for task in r_body['tasks'] if task['timebox'] == 'Backlog' and task['priority'] == 5][0]
	data = {
	'project_id': 1,
	'task_id': t['id'],
	'timebox': 'Backlog',
	'priority': 0
	}
	r2 = test_client.post('/update_task', json=data)
	r2_body = r2.json
	r3 = test_client.get('/get_tasks?project_id=1')
	r3_body = r3.json
	print(t['id'])
	print(r3_body)
	task = [task for task in r3_body['tasks'] if task['id'] == t['id']][0]
	assert task['priority'] <  t['priority']

def test_update_task_timebox(sample_data, logged_in_client):
	"""
	GIVEN some sample data
	WHEN update task is called with updated timebox
	THEN when get tasks is called, that tasks timebox has been updated
	"""
	r = logged_in_client.get(f"/get_tasks?project_id={1}")
	r_body = r.json
	t = [task for task in r_body['tasks'] if task['timebox'] == 'Backlog' and task['priority'] == 0][0]
	data = {
	'project_id': 1,
	'task_id': t['id'],
	'timebox': r_body['timeboxes'][1]['title'],
	'priority': 0
	}
	r2 = logged_in_client.post('/update_task', json=data)
	r2_body = r2.json
	r3 = logged_in_client.get(f"/get_tasks?project_id={1}")
	r3_body = r3.json
	task = [task for task in r3_body['tasks'] if task['id'] == t['id']]
	assert task[0]['timebox'] != 'Backlog'
	assert task[0]['timebox'] == data['timebox']

def test_add_task_to_theme(logged_in_client, sample_data):
	"""
	GIVEN a project with tasks and themes
	WHEN update_task_theme is called for one of those tasks with one of those themes
	THEN task theme should be updated
	"""
	r = logged_in_client.get(f"/get_tasks?project_id={1}")
	r_body = r.json
	tasks = r_body['tasks']
	themes = r_body['themes']
	t = tasks[0]
	th = themes[0]
	assert t['theme'] == 'No Theme'
	assert [task for task in tasks if task['theme'] == th] == []
	r2 = logged_in_client.post('update_task_theme', json={'task_id': t['id'], 'theme_id': th['id'] })
	r3 = logged_in_client.get(f"/get_tasks?project_id={1}")
	r3_body = r3.json
	t2 = [task for task in r3_body['tasks'] if task['id'] == t['id']][0]
	th2 = [theme for theme in r3_body['themes'] if theme['id'] == th['id']][0]
	assert t2['theme'] == th2['title']

def test_delete_theme(logged_in_client, sample_data):
	"""
	GIVEN a theme with tasks 
	WHEN that theme is deleted
	THEN theme should not exist, tasks within it should go back to no theme, and get tasks
	should return a 200"""
	r = logged_in_client.get(f"/get_tasks?project_id={1}")
	r_body = r.json
	tasks = r_body['tasks']
	themes = r_body['themes']
	t = tasks[0]
	th = themes[0]
	assert t['theme'] == 'No Theme'
	assert [task for task in tasks if task['theme'] == th] == []
	r2 = logged_in_client.post('update_task_theme', json={'task_id': t['id'], 'theme_id': th['id'] })

	r3 = logged_in_client.post('delete_theme', json={'project_id': 1, 'theme_id': th['id']})
	assert r3.status_code == 200
	r4 = logged_in_client.get(f"/get_tasks?project_id={1}")
	assert r4.status_code == 200
	r4_body = r4.json
	tasks = r4_body['tasks']
	themes = r4_body['themes']
	assert th['title'] not in [theme['title'] for theme in themes]
	assert [task for task in tasks if task['theme'] == th] == [] 



#get tasks of timebox
#delete theme
#delete timebox
#edit task
