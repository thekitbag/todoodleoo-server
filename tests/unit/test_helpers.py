from webapp.main.helpers import prioritise_tasks, insert_task_at_priority
from webapp.models import Task

def test_prioritise_tasks(random_data):
	"""
	GIVEN a timebox of tasks
	WHEN prioritise tasks is called on those tasks
	THEN the tasks are ordered first by status and then priority with priorities
	continguous starting from 0
	"""
	project = random_data['projects'][0]
	tb = project.timeboxes[0]
	prioritised_tasks = prioritise_tasks(tb.tasks.all())
	for idx, tsk in enumerate(prioritised_tasks):
		if tsk.status == 'Done':
			for index, task in enumerate(prioritised_tasks):
				if task.status in ['In Progress', 'To Do']:
					assert idx < index
		if tsk.status == 'In Progress':
			for index, task in enumerate(prioritised_tasks):
				if task.status == 'To Do':
					assert idx < index
				elif task.status == 'Done':
					assert idx > index
		if tsk.status == 'To Do':
			for index, task in enumerate(prioritised_tasks):
				if task.status in ['In Progress', 'Done']:
					assert idx > index
		assert tsk.priority == idx



def test_insert_at_top(random_data):
	"""
	GIVEN Some sample data
	WHEN a task is inserted at top spot in priority
	THEN it should be given priority 0 and all tasks underneasth should have contiguos priorities 
	starting at 1 with no duplicates
	"""
	tasks = random_data['tasks']
	prioritised_tasks = prioritise_tasks(tasks)
	sorted_tasks = sorted(prioritised_tasks, key=lambda x: x.priority)

	target_task = sorted_tasks[5]
	usurped_task = sorted_tasks[0]


	insert_task_at_priority(task=target_task, priority=0, tasks=sorted_tasks)
	tasks = sorted(sorted_tasks, key=lambda x: x.priority)
	assert tasks[0] == target_task
	assert tasks[1].priority == 1
	assert tasks[2].priority == 2

def test_insert_in_middle_gets_target_priority(random_data):
	"""
	GIVEN some sample data
	WHEN a task is inserted with middling priority
	THEN the the target task gets the target priority and the previos one gets bumped
	"""
	tasks = random_data['tasks']
	prioritised_tasks = prioritise_tasks(tasks)
	sorted_tasks = sorted(prioritised_tasks, key=lambda x: x.priority)

	target_task = sorted_tasks[6]
	usurped_task = sorted_tasks[3]

	insert_task_at_priority(task=target_task, priority=3, tasks=sorted_tasks)
	resorted_tasks = sorted(sorted_tasks, key=lambda x: x.priority)

	assert resorted_tasks[3] == target_task
	assert resorted_tasks[3] != usurped_task

def test_insert_in_middle_usurped_task_plus_one(random_data):
	"""
	GIVEN some sample data
	WHEN a task is inserted with middling priority
	THEN the previous task is bumped down in priority by 1
	"""
	tasks = random_data['tasks']
	prioritised_tasks = prioritise_tasks(tasks)
	sorted_tasks = sorted(prioritised_tasks, key=lambda x: x.priority)

	target_task = sorted_tasks[6]
	usurped_task = sorted_tasks[3]

	insert_task_at_priority(task=target_task, priority=3, tasks=sorted_tasks)
	resorted_tasks = sorted(sorted_tasks, key=lambda x: x.priority)

	assert usurped_task.priority == 4

def test_insert_in_middle_tasks_above(random_data):
	"""
	GIVEN some sample data
	WHEN a task is inserted with middling priority
	THEN the tasks above it in priority  are unchanged
	"""
	tasks = random_data['tasks']
	prioritised_tasks = prioritise_tasks(tasks)
	sorted_tasks = sorted(prioritised_tasks, key=lambda x: x.priority)

	target_task = sorted_tasks[6]

	insert_task_at_priority(task=target_task, priority=3, tasks=tasks)
	resorted_tasks = sorted(sorted_tasks, key=lambda x: x.priority)
	assert resorted_tasks[0:3] == sorted_tasks[0:3]

def test_insert_in_middle_tasks_below(random_data):
	"""
	GIVEN some sample data
	WHEN a task is inserted with middling priority
	THEN the tasks below it in priority have no dupes, and are contiguous values
	from target priority +1
	"""
	tasks = random_data['tasks']
	prioritised_tasks = prioritise_tasks(tasks)
	sorted_tasks = sorted(prioritised_tasks, key=lambda x: x.priority)

	target_task = sorted_tasks[6]

	insert_task_at_priority(task=target_task, priority=3, tasks=tasks)
	resorted_tasks = sorted(sorted_tasks, key=lambda x: x.priority)
	assert resorted_tasks[4:] != sorted_tasks[4:]
	below_tasks_priorities = [i.priority for i in resorted_tasks[4:]]
	prio = 4
	for i in below_tasks_priorities:
		assert i == prio
		prio += 1


	