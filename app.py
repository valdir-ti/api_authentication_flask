from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MY_SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'api is running'
    })

if __name__ == '__main__':
    app.run(debug=True)
