from webapp.main.helpers import prioritise_tasks

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
                        'theme_color': task.theme.color
                        })
    
def add_themes_to_response(themes, resp):
    resp['themes'] = [{'id': theme.id, 'title':theme.title, 'color': theme.color} \
                        for theme in themes if theme.title != 'No Theme']

def add_timeboxes_to_response(timeboxes, resp):
    resp['timeboxes'] = [{'id': timebox.id, 'title': timebox.title, 'goals': [goal.title for goal in timebox.goals.all()], 'start_time': timebox.start_time, \
                        'end-time': timebox.end_time, 'status': timebox.status} for timebox in timeboxes]
    