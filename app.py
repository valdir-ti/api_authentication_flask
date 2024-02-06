from flask import Flask, jsonify, request
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cd6bd383d4886c1345a9a3ed337407c16cddcce2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

# view login
login_manager.login_view = 'login'

@app.route('/')
def hello_world() :
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
        if user and user.password == password:
                login_user(user)
                return jsonify({
                    'message': 'Authentication successfully'
                })

    return jsonify({
        'message': 'Invalid credentials'
    }), 400

if __name__ == '__main__':
    app.run(debug=True)
