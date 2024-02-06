from flask import Flask, jsonify, request
from database import db
from models.user import User
from flask_login import LoginManager

app = Flask(__name__)
app.config['MY_SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

# view login

@app.route('/')
def hello_world() :
    return jsonify({
        'message': 'api is running'
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    if username and password:

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
                return jsonify({
                    'message': 'Authentication successfully'
                })

    return jsonify({
        'message': 'Invalid credentials'
    }), 400

if __name__ == '__main__':
    app.run(debug=True)
