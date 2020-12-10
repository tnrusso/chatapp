'''This module creates the user and chatlog database models'''
# pylint: disable=no-member, too-few-public-methods
import flask_sqlalchemy
from app import db


class Users(db.Model):
    '''Model for registered users'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(1000), unique=True, nullable=False)
    user_avatar = db.Column(db.String(1000), nullable=False)
    session_id = db.Column(db.String(100))

    def __init__(self, name, email, avatar, sid):
        self.user_name = name
        self.user_email = email
        self.user_avatar = avatar
        self.session_id = sid

    def __repr__(self):
        return '<Users userName: %s>' % self.user_name


class Chatlog(db.Model):
    '''Model of chat messages'''
    __tablename__ = 'chatlog'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, message, uid):
        self.message = message
        self.user_id = uid

    def __repr__(self):
        return '<Chatlog message: %s>' % self.message
    