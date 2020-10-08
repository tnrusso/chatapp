from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
#import models

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']

numUsers = 0

@socketio.on('connect')
def on_connect():
    global numUsers
    numUsers += 1
    print('Someone connected!')
    print(numUsers)
    socketio.emit('connected', {
        'test': 'Connected'
    })
    socketio.emit('usercount', { # Update user count
        'count': numUsers
    })

@socketio.on('disconnect')
def on_disconnect():
    global numUsers
    numUsers -= 1
    print ('Someone disconnected!')
    print(numUsers)
    socketio.emit('usercount', { # Update user count
        'count': numUsers
    })
    


@app.route('/')
def hello():
    return flask.render_template('index.html')

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
