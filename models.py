# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
import flask_sqlalchemy
from app import db


class Users(db.Model):
    __tablename__='users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self,n):
        self.userName = n
    def __repr__(self):
        return '<Users userName: %s>' % self.userName 
    
    
class Chatlog(db.Model):
    __tablename__='chatlog'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, m, uid):
        self.message = m
        self.userId = uid
        
    def __repr__(self):
        return '<Chatlog message: %s>' % self.message 