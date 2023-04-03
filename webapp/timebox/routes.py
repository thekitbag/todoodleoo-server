from webapp import db
from webapp.main import bp
from flask import json, request, abort
from webapp.models import Timebox, Project
from webapp.timebox.shortcuts import SHORTCUTS

@bp.route('/add_timebox', methods=['POST'])
def add_timebox():
    data = json.loads(request.data.decode('utf-8'))
    if 'project_id' not in data:
        return 'No Project ID', 400
    if 'title' not in data or data['title'] == '':
        return 'Timebox must have a title', 400

    project = Project.query.get(data['project_id'])
    title=data['title']
    goal=data['goal']
    timebox = Timebox(title=title, project=project, status='To Do')
    timebox.add_goal(goal)
    db.session.add(timebox)
    db.session.commit()
    return {'id': timebox.id, 'title': timebox.title, 'start_time': timebox.start_time, 'end-time': timebox.end_time, 'goal': goal}

@bp.route('/delete_timebox', methods=['POST'])
def delete_timebox():
    data = json.loads(request.data.decode('utf-8'))

    if 'project_id' not in data:
        return 'No Project Id', 400
    if 'timebox_id' not in data:
        return 'No timebox ID', 400

    data = json.loads(request.data.decode('utf-8'))
    timebox = Timebox.query.get(data['timebox_id'])
    timebox.delete()
    return 'success', 200

@bp.route('/update_timebox_status', methods=['POST'])
def update_timebox_status():
    data = json.loads(request.data.decode('utf-8'))

    if 'project_id' not in data:
        return 'No Project Id', 400
    if 'timebox_id' not in data:
        return 'No timebox ID', 400
    if data['status'] not in ['To Do', 'In Progress', 'Closed']:
        return 'Invalid status', 400

    project = Project.query.get(data['project_id'])
    timebox = Timebox.query.get(data['timebox_id'])

    if project and timebox:
        timebox.change_status(data['status'])

    else: return 'project or timebox not found', 404
    
    return f'Timebox status changed to to {data["status"]}', 200

@bp.route('/timebox_shortcuts', methods=['POST'])
def timebox_shortcut():
    data = json.loads(request.data.decode('utf-8'))
    if 'project_id' not in data:
        abort(400)
    if 'shortcut_id' not in data or data['shortcut_id'] not in range(0,len(SHORTCUTS)):
        abort(400)
    tbdata = SHORTCUTS[data['shortcut_id']]
    timebox = Timebox(project_id=data['project_id'], title=tbdata['title'], start_time=tbdata['start_time'], end_time=tbdata['end_time'], status='To Do')
    db.session.add(timebox)
    db.session.commit()
    return {'id': timebox.id, 'title': timebox.title, 'start_time': timebox.start_time, 'end_time': timebox.end_time}

@bp.route('/edit_timebox', methods=['POST'])
def edit_timebox():
    data = json.loads(request.data.decode('utf-8'))

    if 'project_id' not in data:
        return 'Request does not contain project ID', 400

    if 'timebox_id' not in data:
        return 'Request does not contain timebox ID', 400

    if 'title' not in data:
        return 'Request does not contain timebox title', 400

    if 'goal' not in data:
        return 'Request does not contain any goals', 400

    project = Project.query.get(data['project_id'])
    timebox = Timebox.query.get(data['timebox_id'])

    if timebox and project:

        if timebox.project_id != project.id:
            return 'Timebox and project ID mismatch', 401

        title=data['title']
        goal=data['goal']

        timebox.title = title
        timebox.goals = []
        timebox.add_goal(goal)

        db.session.add(timebox)
        db.session.commit()

    else:
        return 'Project or timebox not found', 404

    return 'Timebox updated', 200

    return data, 200
