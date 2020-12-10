"""This module starts the flask server"""
# pylint: disable=wrong-import-position,no-member,invalid-name,redefined-outer-name
import os
from os.path import join, dirname
from dotenv import load_dotenv

import flask
import flask_sqlalchemy
import flask_socketio
from flask import request

from chatbot import ChatBot


app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

database_uri = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(
    app
)  # Flask-SQLAlchemy instance used for all database interactions


def init_db(app):
    """Initialize db"""
    db.init_app(app)
    db.app = app
    db.create_all()
    db.session.commit()


init_db(app)

import models

BOT_NAME = "YodaBot"
BOT_EMAIL = "no email"
BOT_AVATAR = "/static/yoda.png"
CONNECTED_USERS = []


def update_user_count():
    """Send number of connected users to the client"""
    socketio.emit("usercount", {"count": len(CONNECTED_USERS)})  # Update user count


def add_user(name, email, avatar):
    """Add new user to database"""

    user_exist = (
        db.session.query(models.Users).filter(models.Users.user_email == email).first()
    )
    if user_exist is None:
        db.session.add(models.Users(name, email, avatar, request.sid))
    else:
        user_exist.session_id = request.sid
    db.session.commit()


def add_bot():
    """Add chat bot to the chat if it doesnt already exist"""
    BOT_EXISTS = (
        db.session.query(models.Users.user_name)
        .filter(models.Users.user_name == BOT_NAME)
        .first()
    )
    if BOT_EXISTS is None:
        db.session.add(models.Users(BOT_NAME, BOT_EMAIL, BOT_AVATAR, "1"))
        db.session.commit()

add_bot()

def emit_all_messages():
    """
    This function will save all of the messages from the database
    into all_messages, and send them to Content.jsx to display them.

    This function is called when a new message is sent, and
    when a user connects to the chat so all messages will be loaded on page load
    """
    all_messages = []
    for db_message in db.session.query(models.Chatlog.message).all():
        all_messages.append(db_message)

    user_names_of_messages = []
    user_avatars = []
    for msg_id in db.session.query(models.Chatlog.user_id).all():
        user_names_of_messages.append(
            db.session.query(models.Users.user_name)
            .filter(models.Users.id == msg_id)
            .one()
        )
        user_avatars.append(
            db.session.query(models.Users.user_avatar)
            .filter(models.Users.id == msg_id)
            .one()
        )

    socketio.emit(
        "new message received",
        {
            "allMessages": all_messages,
            "user_of_message": user_names_of_messages,
            "users_avatar": user_avatars,
        },
    )


def bot_command_called(bot_call):
    """Get the bot response to the user typed command"""
    chat_bot = ChatBot(bot_call)
    bot_response = chat_bot.get_bot_response()
    bot_id = db.session.query(models.Users.id).filter(
        models.Users.user_name == BOT_NAME
    )
    db.session.add(models.Chatlog(bot_response, bot_id))
    db.session.commit()
    emit_all_messages()


@socketio.on("new message sent")
def on_new_message(msg):
    """Handles when a message is submitted from input box"""
    users_id = (
        db.session.query(models.Users.id)
        .filter(models.Users.session_id == request.sid)
        .first()
    )

    if users_id is not None:
        db.session.add(models.Chatlog(msg["message"], users_id))
        db.session.commit()
        emit_all_messages()

    # After the user sends a message, check to see if it was a bot command
    if "!!" in msg["message"][0:2]:
        bot_command_called(msg["message"])


@socketio.on("new google user")
def successful_google_login(user_info):
    """Handle when a user successfully logs in with Google account"""
    name = user_info["name"]
    email = user_info["email"]
    avatar = user_info["avatar"]

    add_user(name, email, avatar)

    if email not in CONNECTED_USERS:
        CONNECTED_USERS.append(email)

    update_user_count()
    emit_all_messages()


@socketio.on("connect")
def on_connect():
    """Update client when new window opened"""
    update_user_count()
    emit_all_messages()


@socketio.on("disconnect")
def on_disconnect():
    """Decrement user count when user disconnects"""
    exists = (
        db.session.query(models.Users)
        .filter(models.Users.session_id == request.sid)
        .first()
    )
    if exists is not None:
        CONNECTED_USERS.remove(exists.user_email)
        update_user_count()


@app.route("/")
def index():
    """Render html page and values when client opened"""
    emit_all_messages()
    update_user_count()
    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
