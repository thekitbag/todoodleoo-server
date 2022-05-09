from datetime import datetime, timedelta, time
from webapp import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.main.helpers import insert_task_at_priority, prioritise_tasks


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    timebox_id = db.Column(db.Integer, db.ForeignKey('timebox.id'))

    def __repr__(self):
        return f'<Goal {self.id}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(32))
    tasks = db.relationship('Task', backref='project', lazy='dynamic')
    themes = db.relationship('Theme', backref='project', lazy='dynamic')
    timeboxes = db.relationship('Timebox', backref='project', lazy='dynamic')

    def __repr__(self):
        return f'<Project {self.id}  {self.title}>'

class StatusUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    from_status = db.Column(db.String(32))
    to_status = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Status Update {self.id}>'

class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    status = db.Column(db.String(32), index=True)

    def change_status(self, target_status):
        parent_task = self.task
        subtask_statuses = set([st.status for st in parent_task.subtasks.all()])
        if subtask_statuses == {'To Do'}: #if this subtask in the first one to change to in progress
            parent_task.status = 'In Progress'
            self.status = target_status
        else:
            self.status = target_status
            subtask_statuses = set([st.status for st in parent_task.subtasks.all()])
            if subtask_statuses == {'Done'}: #if all subtasks are now done
                parent_task.status = 'Done'
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Subtask {self.id}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(128))
    status = db.Column(db.String(32), index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updates = db.relationship('StatusUpdate', backref='task', lazy='dynamic')
    timebox_id = db.Column(db.Integer, db.ForeignKey('timebox.id'))
    priority = db.Column(db.Integer)
    subtasks = db.relationship('Subtask', backref='task', lazy='dynamic')


    def add(self, project):
        self.priority = 0
        self.project = project
        db.session.add(self)
        db.session.commit()

    def add_to_timebox(self, timebox):
        self.timebox = timebox
        db.session.add(self)
        db.session.commit()

    def add_to_theme(self, project):
        theme = db.session.query(Theme).filter(Theme.project_id == project.id and Theme.title == 'No Theme').first()
        self.theme = theme
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def delete_subtask(self, subtask):
        self.subtasks.remove(subtask)
        db.session.add(self)
        db.session.delete(subtask)
        db.session.commit()

    def update_task(self, project_id, timebox, priority):
        self.add_to_timebox(timebox)
        tb_tasks = db.session.query(Task).filter(Task.project_id==project_id).filter(Task.timebox==timebox).all()
        insert_task_at_priority(task=self, priority=priority, tasks=tb_tasks)
        prioritise_tasks(tb_tasks)
        db.session.add_all(tb_tasks)
        db.session.commit()

    def update_status(self, target_status):
        self.status = target_status
        db.session.add(self)
        db.session.commit()

    def update_theme(self, theme):
        self.theme = theme
        db.session.add(self)
        db.session.commit()

    def edit_task(self, title, priority, theme):
        self.title = title
        self.priority = priority
        self.theme = theme
        db.session.add(self)
        db.session.commit()

    def add_subtask(self, title):
        subtask = Subtask(title=title, status='To Do')
        self.subtasks.append(subtask)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Task {self.id}>'

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(64))
    color = db.Column(db.String(24))
    tasks = db.relationship('Task', backref='theme', lazy='dynamic')

    def __repr__(self):
        return f'<Theme {self.id}>'

class Timebox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.today() + timedelta(hours=8))
    status = db.Column(db.String(32))
    tasks = db.relationship('Task', backref='timebox', lazy='dynamic')
    goals = db.relationship('Goal', backref='timebox', lazy='dynamic')

    def add_goals(self, goals):
        for goal in goals:
            g = Goal(title=goal)
            db.session.add(g)
            self.goals.append(g)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes the timebox and returns all not done tasks
        to the backlog"""
        backlog = db.session.query(Timebox).filter(Timebox.title=='Backlog').filter(Timebox.project_id==self.project_id).first()
        for task in self.tasks.all():
            if task.status != 'Done':
                task.add_to_timebox(backlog)
        db.session.delete(self)
        db.session.commit()

    def change_status(self, target_status):
        """
        changes the timebox to the desired status
        if the target status is Done then all non-done tasks in the timebox
        will be returned to the Backlog
        """
        backlog = db.session.query(Timebox).filter(Timebox.title=='Backlog').filter(Timebox.project_id==self.project_id).first()
        for task in self.tasks.all():
            if task.status != 'Done':
                task.add_to_timebox(backlog)
        self.status = target_status
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Timebox {self.id}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')
    projects = db.relationship('Project', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
