from webapp import db
from webapp.main import bp
from flask import json, request, jsonify
from flask_login import current_user
from webapp.models import Theme, Timebox, Project, User
from sqlalchemy import func

@bp.route('/add_project', methods=['POST'])
def add_project():
    data = json.loads(request.data.decode('utf-8'))
    title = data['title']

    if current_user.is_authenticated == False:
        return 'User not logged in', 401

    if title == None or title == '':
        return 'No title', 400

    project = Project(title=title)
    current_user.add_project(title=title)

    projects = current_user.projects
    resp = {}
    resp['projects'] = [{'project_id': project.id, 'project_title': project.title} for project in projects]
    return jsonify(resp)


@bp.route('/get_projects', methods=['GET'])
def get_projects():
    if current_user.is_authenticated:
        projects = current_user.projects
        resp = {}
        resp['projects'] = [{'project_id': project.id, 'project_title': project.title} for project in projects]
        return resp
    else:
        return 'Not Authorised', 401

@bp.route('/share_project', methods=['POST'])
def share_project():

    if current_user.is_authenticated == False:
        return 'User not logged in', 401

    data = json.loads(request.data.decode('utf-8'))

    if 'project_id' not in data:
        return "No Project Id", 400
    
    if 'username' not in data:
        return "No username", 400

    project_id = data['project_id']
    username = data['username']

    user = User.query.filter_by(username=username).first()

    if user == None:
        return f"No user found with username: {username}", 404
    
    project = Project.query.get(project_id)

    if current_user not in project.users:
        return f"Cannot share project {project_id} with user {username} because {current_user.username} is not owner"

    current_user.share_project(user, project)
    return f"Project succesfully shared with {username}", 200
