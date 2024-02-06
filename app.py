from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

load_dotenv()

app = Flask(__name__)

MYSQL_URL = os.getenv('MYSQL_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URL

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

# view login
login_manager.login_view = 'login'

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'api is running'
    })

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
                login_user(user)
                return jsonify({ 'message': 'Authentication successfully' })

    return jsonify({
        'message': 'Invalid credentials'
    }), 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({ 'message': 'logout successfully' })

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    password = data['password']

    if username and password:
        hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({ 'message': 'User created' }), 201

    return jsonify({
        'message': 'Invalid data'
    }), 400

@app.route('/user/<int:id>')
@login_required
def get_user(id):
    user = User.query.get(id)

    if user:
        return ({ 'username': user.username })

    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    data = request.json
    user = User.query.get(id)

    if id != current_user.id and current_user.role == 'user':
        return ({ 'message': 'Operation not allowed' }), 403

    if user and data.get('password'):
        user.password = data.get('password')
        db.session.commit()
        return ({ 'username': 'User updated', 'id': id })

    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = User.query.get(id)   

    if current_user.role != 'admin':
        return ({ 'message': 'Operation not allowed' }), 403

    if id == current_user.id:
        return jsonify({'message': 'You cannot delete the user logged'}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return ({ 'message': 'User deleted successfully', 'id': id })

    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
