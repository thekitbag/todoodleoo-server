from datetime import datetime, timedelta

def test_add_project_no_title(logged_in_client):
	"""
	GIVEN a fresh instance of the app
	WHEN add project is called with no title
	THEN a 400 should be returned
	"""
	data = {'title': ''}
	r2 = logged_in_client.post('/add_project', json=data)
	assert r2.status_code == 400

def test_get_tasks_no_project_id(logged_in_client):
	"""
	GIVEN a new project
	WHEN the get_tasks route is called for that project with no project Id
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	response = logged_in_client.get('/get_tasks')
	assert response.status_code == 400

def test_get_tasks_invalid_project_id(logged_in_client):
	"""
	GIVEN a new project
	WHEN the get_tasks route is called with an invalid project Id
	THEN a 404 is returned
	"""
	project_id = 99999
	response = logged_in_client.get(f'/get_tasks?project_id={project_id}')
	assert response.status_code == 404

def test_add_task_no_project_id(logged_in_client):
	"""
	GIVEN a project
	WHEN a task is added with no project Id
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_task', json={'title': 'test task'})
	assert r2.status_code == 400

def add_project_not_logged_in(test_client):
	"""
	GIVEN a non logged in user
	WHEN add project is called with valid data
	THEN a 401 is returned
	"""
	data = {'title': 'my new project'}
	r = test_client.post('/add_project', json=data)
	assert r.status_code == 401

def test_add_task_no_title(logged_in_client):
	"""
	GIVEN a project
	WHEN a task is added with no title
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_task', json={'project_id': project_id})
	assert r2.status_code == 400

def test_add_task_empty_title(logged_in_client):
	"""
	GIVEN a project
	WHEN a task is added with an empty title
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_task', json={'project_id': project_id, 'title': ''})
	assert r2.status_code == 400

def test_add_theme_no_project_id(logged_in_client):
	"""
	GIVEN a project
	WHEN a theme is added with no project ID
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_theme', json={'title': 'test theme'})
	assert r2.status_code == 400

def test_add_theme_no_title(logged_in_client):
	"""
	GIVEN a project
	WHEN a theme is added with no title
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_theme', json={'project_id': project_id})
	assert r2.status_code == 400

def test_add_theme_empty_title(logged_in_client):
	"""
	GIVEN a project
	WHEN a theme is added with an empty title
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_theme', json={'project_id': project_id, 'title': ''})

def test_add_timebox_no_project_id(logged_in_client):
	"""
	GIVEN a project
	WHEN a timebox is added with no project_id
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_timebox', json={'title': 'test timebox'})
	assert r2.status_code == 400

def test_add_timebox_no_title(logged_in_client):
	"""
	GIVEN a project
	WHEN a timebox is added with no title
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_timebox', json={'project_id': project_id})
	assert r2.status_code == 400

def test_add_timebox_empty_title(logged_in_client):
	"""
	GIVEN a project
	WHEN a timebox is added with an empty title
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/add_timebox', json={'project_id': project_id, 'title': ''})
	assert r2.status_code == 400

def test_add_task_to_theme_in_different_project(logged_in_client):
	"""
	GIVEN two projects, themes in each project and  a task in one of them
	WHEN update task is called updating the task theme to the theme in the other project
	THEN a 400 is returned
	"""
	data = {'title': 'test project 1'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id_1 = r_body['projects'][0]['project_id']
	data2 = {'title': 'test project 2'}
	r2 = logged_in_client.post('/add_project', json=data2)
	r2_body = r2.json
	project_id_2 = r2_body['projects'][1]['project_id']
	assert project_id_1 == 1
	assert project_id_2 == 2
	theme1_data = {
	'project_id': 1,
	'title': 'test theme 1'
	}
	r3 = logged_in_client.post('/add_theme', json=theme1_data)
	theme2_data = {
	'project_id': 2,
	'title': 'test theme 2'
	}
	r4 = logged_in_client.post('/add_theme', json=theme2_data)
	r5 = logged_in_client.post('/add_task', json={'project_id': project_id_1, 'title': 'test task 1'})
	update_data = {'project_id': project_id_1, 'task_id': 1, 'theme_id': 2}
	r6 = logged_in_client.post('update_task_theme', json=update_data)
	assert r6.status_code == 400

def test_add_task_to_timebox_in_different_project(logged_in_client):
	"""
	GIVEN two projects, timeboxes in each project and  a task in one of them
	WHEN update task is called updating the task timebox to the timebox in the other project
	THEN a 400 is returned
	"""
	data = {'title': 'test project 1'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id_1 = r_body['projects'][0]['project_id']
	data2 = {'title': 'test project 2'}
	r2 = logged_in_client.post('/add_project', json=data2)
	r2_body = r2.json
	project_id_2 = r2_body['projects'][1]['project_id']
	assert project_id_1 == 1
	assert project_id_2 == 2
	timebox1_data = {
	'project_id': project_id_1,
	'title': 'test timebox 1',
	'start_time': datetime.now(),
	'end_time': datetime.now() + timedelta(days=1),
	'goals': []
	}
	r4 = logged_in_client.post('/add_timebox', json=timebox1_data)
	timebox2_data = {
	'project_id': project_id_2,
	'title': 'test timebox 2',
	'start_time': datetime.now(),
	'end_time': datetime.now() + timedelta(days=1),
	'goals': []
	}
	r5 = logged_in_client.post('/add_timebox', json=timebox1_data)
	r6 = logged_in_client.post('/add_task', json={'project_id': project_id_1, 'title': 'test task 1'})
	update_data = {'project_id': project_id_1, 'task_id': 1, 'timebox': 'test timebox 2', 'priority': 4}
	r7 = logged_in_client.post('update_task', json=update_data)
	assert r7.status_code == 404

def test_timebox_shortcut_no_project_id(logged_in_client):
	"""
	GIVEN a project
	WHEN a timebox_shortcut is added with no project_id
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/timebox_shortcuts', json={'shortcut_id': 1})
	assert r2.status_code == 400

def test_timebox_shortcut_no_timebox_id(logged_in_client):
	"""
	GIVEN a project
	WHEN a timebox_shortcut is added with no timebox_id
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/timebox_shortcuts', json={'project_id': project_id})
	assert r2.status_code == 400

def test_timebox_shortcut_invalid_shortcut_id(logged_in_client):
	"""
	GIVEN a project
	WHEN a timebox_shortcut is added with no project_id
	THEN a 400 is returned
	"""
	data = {'title': 'test project'}
	r = logged_in_client.post('/add_project', json=data)
	r_body = r.json
	project_id = r_body['projects'][0]['project_id']
	r2 = logged_in_client.post('/timebox_shortcuts', json={'project_id': project_id, 'timebox_id': 'banana'})
	assert r2.status_code == 400

def test_edit_timebox_no_project_id(logged_in_client):
	"""
	GIVEN a project with a timebox
	WHEN edit timebox is called with no project_id
	THEN a 400 is returned
	"""
	data = {
	'timebox_id': 1,
	'title': 'To do before end of the week',
	'goals': ['feel better', 'sleep more', 'dont drink']
	}
	r = logged_in_client.post('/edit_timebox', json=data)
	assert r.status_code == 400

def test_edit_timebox_incorrect_project_id(logged_in_client, sample_data):
	"""
	GIVEN a project with a timebox
	WHEN edit timebox is called with a project_id that doesn't match
	THEN a 401 is returned
	"""

	r = logged_in_client.get(f"/get_tasks?project_id={1}")
	r_body = r.json

	print(r_body)
	data = {
	'project_id': 2,
	'timebox_id': 1,
	'title': 'To do before end of the week',
	'goals': ['feel better', 'sleep more', 'dont drink']
	}
	r = logged_in_client.post('/edit_timebox', json=data)
	assert r.status_code == 401

def test_close_timebox_missing_data(logged_in_client, sample_data):
	"""
	GIVEN a project with timeboxes
	WHEN close timebox is called with missing data
	THEN a 400 is returned
	"""

	data = {
	'timebox_id': 1,
	'status': 'Closed'
	}

	r2 = logged_in_client.post('/update_timebox_status', json=data)
	assert r2.status_code == 400

def test_close_timebox_incorrect_project_id(logged_in_client, sample_data):
	"""
	GIVEN a project with timeboxes
	WHEN close timebox is called with a project ID that doesnt exist
	THEN a 404 is returned
	"""

	data = {
	'project_id': 9999,
	'timebox_id': 1,
	'status': 'Closed'
	}

	r2 = logged_in_client.post('/update_timebox_status', json=data)
	assert r2.status_code == 404

def test_add_subtask_missing_data(logged_in_client, sample_data):
	"""
	GIVEN a project with tasks
	WHEN add subtask is called with no project_id or task_id
	THEN return a 400
	"""
	data = {
	'task_id': 1,
	'title': "I'm a subtask"
	}
	r = logged_in_client.post('/add_subtask', json=data)
	assert r.status_code == 400

	data = {
	'project_id': 1,
	'title': "I'm a subtask"
	}
	r2 = logged_in_client.post('/add_subtask', json=data)
	assert r2.status_code == 400
