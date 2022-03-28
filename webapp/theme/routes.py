import random
from webapp import db
from webapp.main import bp
from flask import request, json
from webapp.models import Theme, Project, Task
from webapp.theme.helpers import rgb_number


@bp.route('/add_theme', methods=['POST'])
def add_theme():
    data = json.loads(request.data.decode('utf-8'))

    if 'project_id' not in data:
        return 'no project id', 400
    if 'title' not in data or data['title'] == '':
        return 'no title', 400

    project = Project.query.get(data['project_id'])
    theme = Theme(title=data['title'], project=project)
    theme.color = rgb_number()
    db.session.add(theme)
    db.session.commit()

    return {'id': theme.id, 'title':theme.title, 'color': theme.color}

@bp.route('/delete_theme', methods=['POST'])
def delete_theme():
    data = json.loads(request.data.decode('utf-8'))
    theme = Theme.query.get(data['theme_id'])

    tasks = db.session.query(Task).filter(Task.theme==theme).all()
    no_theme = db.session.query(Theme).filter(Theme.title == 'No Theme').first()

    for task in tasks:
        task.theme = no_theme

    db.session.add_all(tasks)
    db.session.delete(theme)
    db.session.commit()
    
    themes = db.session.query(Theme).filter(Theme.project_id==data['project_id']).all()
    resp = {}
    resp['themes'] = [{'id': theme.id, 
                    'title': theme.title,
                    'color': theme.color
                    } for theme in themes if theme.title != 'No Theme']
    return resp


