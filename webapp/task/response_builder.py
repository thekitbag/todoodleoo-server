from webapp.main.helpers import prioritise_tasks

def add_project_title_to_response(project, resp):
    resp['project_title'] = project.title

def add_tasks_to_response(all_tasks, timeboxes, resp):
    resp['tasks'] = []
    for tb in timeboxes:
        tasks = [task for task in all_tasks if task.timebox == tb and task.timebox.status != 'Closed']
        prioritise_tasks(tasks)
        tasks.sort(key=lambda x: x.priority)
        for task in tasks:
            resp['tasks'].append( {'id': task.id,
                        'title': task.title,
                        'status': task.status,
                        'priority': task.priority,
                        'theme':task.theme.title,
                        'timebox': task.timebox.title,
                        'theme_color': task.theme.color,
                        'subtasks': [{'id': st.id, 'title': st.title, 'status': st.status} for st in task.subtasks.all()]
                        })

def add_themes_to_response(themes, resp):
    resp['themes'] = [{'id': theme.id, 'title':theme.title, 'color': theme.color} \
                        for theme in themes if theme.title != 'No Theme']

def add_timeboxes_to_response(timeboxes, resp):
    timeboxes_data = []
    for timebox in timeboxes:
        timebox_data = {'id': timebox.id,
            'title': timebox.title,
            'start_time': timebox.start_time,
            'end-time': timebox.end_time,
            'status': timebox.status}
        if timebox.goal:
            timebox_data['goal'] = timebox.goal
        timeboxes_data.append(timebox_data)
    resp['timeboxes'] = timeboxes_data
