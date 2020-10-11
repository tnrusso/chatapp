from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models
from flask import request
from chatbot import ChatBot

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
    # All messages
    all_messages = []
    for db_message in db.session.query(models.Chatlog.message).all():
        all_messages.append(db_message)
        
    # Get the username for each message by filtering by their userId (Users' id)
    userNamesOfMessages = []
    for msg_id in db.session.query(models.Chatlog.userId).all():
        userNamesOfMessages.append(db.session.query(models.Users.userName).filter(models.Users.id == msg_id).one())
        
    socketio.emit('new message received', {
        'allMessages': all_messages,
        'user_of_message': userNamesOfMessages
    })

def bot_command_called(botCall):
        chatBot = ChatBot(botCall)
        botResponse = chatBot.get_bot_response()
        botId = db.session.query(models.Users.id).filter(models.Users.userName == 'YodaBot')
        db.session.add(models.Chatlog(botResponse, botId));
        db.session.commit();
        emit_all_messages()


@socketio.on('new message sent')
def on_new_message(msg):
    # add new message to database, then call emit_all_messages to send them
    usersID = db.session.query(models.Users.id).filter(models.Users.userName == request.sid) # Search for user id based on their username, as username is unnique
    db.session.add(models.Chatlog(msg['message'], usersID)); # userID (Foreign key) is set to the id of the user (Primary key in 'users' model)
    db.session.commit();
    emit_all_messages()
    # After the user sends a message, check to see if it was a bot command, and if so the bot will respond
    if('!!' in msg['message'][0:2]): # bot commands start with '!!', so based on text afterwards determines the bot's response
        bot_command_called(msg['message'])
            
numUsers = 0
@socketio.on('connect')
def on_connect():
    global numUsers
    numUsers += 1
    socketio.emit('connected', {
        'test': 'Connected'
    })
    socketio.emit('usercount', { # Update user count
        'count': numUsers
    })
    # Check if the bot is already in the db, exists returns None if it DNE, and Bot if it does. 
    exists = db.session.query(models.Users.userName).filter(models.Users.userName == 'YodaBot').scalar()
    if (exists is None):
        db.session.add(models.Users('YodaBot')); # The chat bot will take the first row in the users model
        db.session.commit();
    db.session.add(models.Users(request.sid)); # For now, when a user connects to the socket, they are added to the db with their unique session id as their username (until M2)
    db.session.commit();
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
