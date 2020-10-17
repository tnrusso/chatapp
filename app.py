from os.path import join, dirname
from dotenv import load_dotenv

import os
import flask
import flask_sqlalchemy
import flask_socketio
from flask import request

from chatbot import ChatBot
import models


app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app) # Flask-SQLAlchemy instance used for all database interactions
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()


botName = 'YodaBot'
botEmail = 'no email'
botAvatar = '/static/yoda.png'
connectedUsers = []

def updateUserCount():
    socketio.emit('usercount', { # Update user count
        'count': len(connectedUsers)
    })

def emit_all_messages():
    # This function will save all of the messages from the database 
    # into all_messages, and send them to Content.jsx to display them. 
    #
    # This function is called when a new message is sent, and 
    # when a user connects to the chat so all messages will be loaded on page load
    all_messages = []
    for db_message in db.session.query(models.Chatlog.message).all():
        all_messages.append(db_message)
        
    userNamesOfMessages = []
    userAvatars = []
    for msg_id in db.session.query(models.Chatlog.userId).all():
        userNamesOfMessages.append(db.session.query(models.Users.userName)\
            .filter(models.Users.id == msg_id).one())
        userAvatars.append(db.session.query(models.Users.userAvatar)\
            .filter(models.Users.id == msg_id).one())
            
    socketio.emit('new message received', {
        'allMessages': all_messages,
        'user_of_message': userNamesOfMessages,
        'users_avatar': userAvatars
    })


def bot_command_called(botCall):
        chatBot = ChatBot(botCall)
        botResponse = chatBot.get_bot_response()
        botId = db.session.query(models.Users.id).\
            filter(models.Users.userName == botName)
        db.session.add(models.Chatlog(botResponse, botId));
        db.session.commit();
        emit_all_messages()
        
        
@socketio.on('new message sent')
def on_new_message(msg):
    usersID = db.session.query(models.Users.id) \
        .filter(models.Users.sessionID == request.sid).first()
        
    if(usersID is not None):    
        db.session.add(models.Chatlog(msg['message'], usersID));
        db.session.commit();
        emit_all_messages()
    
    # After the user sends a message, check to see if it was a bot command
    if('!!' in msg['message'][0:2]):
        bot_command_called(msg['message'])
            
@socketio.on('new google user')
def successful_google_login(userInfo):
    name = userInfo['name']
    email = userInfo['email']
    avatar = userInfo['avatar']
    
    userAlreadyExists = db.session.query(models.Users).\
        filter(models.Users.userEmail == email).first()
    if(userAlreadyExists is None):
        db.session.add(models.Users(name, email, avatar, request.sid));
        db.session.commit();
    else:
        userAlreadyExists.sessionID = request.sid
        db.session.commit()
        
    if(email not in connectedUsers):
        connectedUsers.append(email)
        
    updateUserCount()
    emit_all_messages()

@socketio.on('connect')
def on_connect():
    botExists = db.session.query(models.Users.userName).\
        filter(models.Users.userName == botName).first()
    if (botExists is None):
        db.session.add(models.Users(botName, botEmail, botAvatar, '1'));
        db.session.commit();
    updateUserCount()
    emit_all_messages()
    
@socketio.on('disconnect')
def on_disconnect():
    exists = db.session.query(models.Users).\
        filter(models.Users.sessionID == request.sid).first()
    if(exists is not None):
        connectedUsers.remove(exists.userEmail)
        updateUserCount()

@app.route('/')
def index():
    emit_all_messages()
    updateUserCount()
    return flask.render_template('index.html')

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
        ,debug=True
    )
