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
    goals=[goal for goal in data['goals'] if goal != None]
    print('goals:',goals)
    timebox = Timebox(title=title, project=project, status='To Do')
    timebox.add_goals(goals)
    db.session.add(timebox)
    db.session.commit()
    return {'id': timebox.id, 'title': timebox.title, 'start_time': timebox.start_time, 'end-time': timebox.end_time, 'goals': [g.title for g in timebox.goals.all()]}

@bp.route('/delete_timebox', methods=['POST'])
def delete_timebox():
    data = json.loads(request.data.decode('utf-8'))
    timebox = Timebox.query.get(data['timebox_id'])
    db.session.delete(timebox)
    db.session.commit()
    timeboxes = db.session.query(Timebox).filter(Timebox.project_id==data['project_id']).all()
    resp = {}
    resp['timeboxes'] = [{'id': timebox.id, 
                    'title': timebox.title
                    } for timebox in timeboxes]
    return resp

@bp.route('/update_timebox_status', methods=['POST'])
def update_timebox_status():
    data = json.loads(request.data.decode('utf-8'))
    timebox = Timebox.query.get(data['timebox_id'])
    timebox.status = data['status']
    db.session.add(timebox)
    db.session.commit()
    return 'success', 200

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

