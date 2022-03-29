from webapp import db
from webapp.main import bp
from flask import json, request, jsonify
from flask_login import current_user
from webapp.models import Theme, Timebox, Project
from sqlalchemy import func

@bp.route('/add_project', methods=['POST'])
def add_project():
    data = json.loads(request.data.decode('utf-8'))
    title = data['title']

    if current_user.is_authenticated == False:
        return 'User not logged in', 401

    if title == None or title == '':
        return 'No title', 400

    project = Project(title=title, user=current_user)
    tb1 = Timebox(title='Backlog', project=project, status='To Do')
    th1 = Theme(title='No Theme', project=project)

    db.session.add_all([project, tb1, th1])
    db.session.commit()

    projects = current_user.projects.all()
    resp = {}
    resp['projects'] = [{'project_id': project.id, 'project_title': project.title} for project in projects]

    return jsonify(resp)


@bp.route('/get_projects', methods=['GET'])
def get_projects():
    if current_user.is_authenticated:
        projects = current_user.projects.all()
        resp = {}
        resp['projects'] = [{'project_id': project.id, 'project_title': project.title} for project in projects]
        return resp
    else:
        return 'Not Authorised', 401
