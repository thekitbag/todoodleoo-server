from webapp import db
from webapp.task import bp
from webapp.main.helpers import prioritise_tasks, insert_task_at_priority
import webapp.task.response_builder as response_builder
from flask import request, json, abort
from flask_login import current_user
from webapp.models import Task, StatusUpdate, Theme, Timebox, Project
from sqlalchemy import func


@bp.route('/get_tasks', methods=['GET'])
def get_tasks():
    project_id = request.args.get('project_id')

    if project_id == None:
        return 'No project ID', 400
    project = Project.query.get(project_id)
    if project == None:
        return 'Project not found', 404

    themes = db.session.query(Theme).filter(Theme.project_id==project_id).all()
    timeboxes = db.session.query(Timebox).filter(Timebox.project_id==project_id).filter(Timebox.status!='Closed').all()
    all_tasks = db.session.query(Task).filter(Task.project_id==project_id).all()

    resp = {}

    response_builder.add_tasks_to_response(all_tasks, timeboxes, resp)
    response_builder.add_themes_to_response(themes, resp)
    response_builder.add_timeboxes_to_response(timeboxes, resp)

    return resp, 200


@bp.route('/get_tasks_of_timebox', methods=['GET'])
def get_tasks_of_timebox():
    project_id = request.args.get('project_id')
    timebox_id = request.args.get('timebox_id')
    timebox = Timebox.query.get(timebox_id)
    tasks = db.session.query(Task).filter(Task.project_id==project_id).all()

    resp = {}

    response_builder.add_tasks_to_response(tasks, [timebox], resp)

    return resp, 200


@bp.route('/add_task', methods=['POST'])
def add_task():
    data = json.loads(request.data.decode('utf-8'))

    if 'project_id' not in data:
        return 'No Project Id', 400
    if 'title' not in data or data['title'] == '':
        return 'No Title', 400

    project = Project.query.get(data['project_id'])

    if 'timebox' not in data:
        tb = db.session.query(Timebox).filter(Timebox.project == project).filter(Timebox.title == 'Backlog').first()
    else:
        tb = db.session.query(Timebox).filter(Timebox.project == project).filter(Timebox.title == data['timebox']).first()

    task = Task(title=data['title'], project=project, status='To Do')

    task.add_to_timebox(tb)
    task.add(project)
    task.add_to_theme(project)

    resp = {}

    response_builder.add_tasks_to_response([task], [tb], resp)

    return resp, 200


@bp.route('/delete_task', methods=['POST'])
def delete_task():

    data = json.loads(request.data.decode('utf-8'))
    task = Task.query.get(data['task_id'])
    task.delete()

    return 'Task deleted', 200


@bp.route('/update_task', methods=['POST'])
def update_task():
    data = json.loads(request.data.decode('utf-8'))
    project_id = data['project_id']
    timebox = data['timebox']
    priority = data['priority']

    task = Task.query.get(data['task_id'])

    if int(task.project_id) != int(project_id):
        return 'Project ID mismatch', 400

    timebox = db.session.query(Timebox).filter(Timebox.title==timebox).filter\
            (Timebox.project_id == project_id).filter(Timebox.status=='To Do').first()
    if timebox == None:
        return 'Timebox not found', 404

    task.update_task(project_id, timebox, priority)

    return 'Task updated', 200


@bp.route('/update_task_status', methods=['POST'])
def update_task_status():
    data = json.loads(request.data.decode('utf-8'))
    task = Task.query.get(data['task_id'])
    target_status = data['target_status']

    task.update_status(target_status)

    return 'Task Updated', 200


@bp.route('/update_task_theme', methods=['POST'])
def update_task_theme():
    data = json.loads(request.data.decode('utf-8'))
    task = Task.query.get(data['task_id'])
    theme = Theme.query.get(int(data['theme_id']))

    if task.project_id != theme.project_id:
        abort(400)

    task.update_theme(theme)

    return 'Theme updated', 200


@bp.route('/edit_task', methods=['POST'])
def edit_task():
    data = json.loads(request.data.decode('utf-8'))
    project_id = data['project_id']
    task = Task.query.get(data['id'])
    title = data['title']
    priority = data['priority']
    theme = db.session.query(Theme).filter(Theme.title==data['theme']).first()

    task.edit_task(title, priority, theme)

    return 'success', 200
