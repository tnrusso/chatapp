from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app) # Flask-SQLAlchemy instance used for all database interactions
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

# This function will save all of the messages from the database into all_messages, and send them to content.jsx to display them. 
# This function is called when a new message is sent, and when a user connects to the chat so all messages will be loaded on page load
def emit_all_messages():
    all_messages = [ \
        db_message.message for db_message in \
        db.session.query(models.Chatlog).all()
    ]
    socketio.emit('new message received', {
        'allMessages': all_messages
    })

@socketio.on('new message sent')
def on_new_message(msg):
    # TODO - add new message to database, then call emit_all_messages to send them
    db.session.add(models.Chatlog(msg['message']));
    db.session.commit();
    emit_all_messages()

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
    emit_all_messages()

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
def index():
    emit_all_messages()
    return flask.render_template('index.html')

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
