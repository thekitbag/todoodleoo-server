from flask import request, json, session, jsonify, make_response
from flask_login import current_user, login_user, logout_user
from webapp.auth import bp
from webapp.models import User
from webapp import db


@bp.route('/me', methods=['GET', 'POST'])
def me():
	if current_user.is_authenticated:
		userdata = {'username': current_user.username, 'user_id': current_user.id}
		return userdata, 200
	else:
		userdata = {'username': '', 'user_id': -1}
		return userdata, 200

@bp.route('/test', methods=['GET', 'POST'])
def test():
	print(request.headers)
	return {'authenticated:': current_user.is_authenticated}

@bp.route('/login', methods=['POST'])
def login():

	if current_user.is_authenticated:
		return 'Already logged in', 409

	req = request.get_json(force=True)
	username = req.get('username', None)
	password = req.get('password', None)

	user = User.query.filter_by(username=username).first()

	if user is None or not user.check_password(password):
			return "Incorrect username/password combo", 200

	login_user(user)
	userdata = {'username': current_user.username, 'user_id': current_user.id}
	resp = make_response(userdata)
	print(request.cookies.get("sessionToken"))
	return resp, 200

@bp.route('/register', methods=['POST'])
def register():
	if current_user.is_authenticated:
		return 'Already logged in', 409

	data = json.loads(request.data.decode('utf-8'))
	username = data['username']
	user = User(username=username, roles='user')
	user.set_password(data['password'])
	db.session.add(user)
	db.session.commit()
	userdata = {'username': username, 'user_id': user.id}
	return userdata, 200

@bp.route('/logout', methods=['POST', 'GET'])
def logout():
	logout_user()
	return 'Logged out', 200
