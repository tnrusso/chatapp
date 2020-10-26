from os.path import join, dirname
from dotenv import load_dotenv

import os

import unittest
import unittest.mock as mock

import sys
sys.path.append('.')
import app
from app import emit_all_messages, add_user, update_user_count, successful_google_login
from app import app
from chatbot import ChatBot
import models
import json

import flask
import flask_sqlalchemy
import flask_socketio
from flask import request, Flask, session

from flask_sqlalchemy import SQLAlchemy

import socketio

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

KEY_USER = "name"
KEY_EMAIL = "email"
KEY_AVATAR = "avatar"
KEY_SESSION_ID = "sessionID"
KEY_MESSAGE = "message"
KEY_ID = "id"

class MockedModelsUsers:
    def __init__(self, userName, userEmail, userAvatar, sessionID):
        self.userName = userName
        self.userEmail = userEmail
        self.userAvatar = userAvatar
        self.sessionID = sessionID

class MockedModelsChatlog:
    def __init__(self, message, userID):
        self.message = message
        self.userID = userID

class MockedTestCases(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.socketio = flask_socketio.SocketIO(app)

        self.success_quote_params = [
            {
                KEY_INPUT: "!!quote",
                KEY_EXPECTED: "The Force will be with you. Always. — Obi-Wan Kenobi"
            }    
        ]
        
        self.success_translate_params = [
            {
                KEY_INPUT: "!!funtranslate text",
                KEY_EXPECTED: "Text"
            }
        ]
        
        self.failure_translate_params = [
            {
                KEY_INPUT: "!!funtranslate text",
                KEY_EXPECTED: "some incorrect translated text"
            }
        ]
        
        self.success_translate_length_too_long = [
            {
                KEY_INPUT: "!!funtranslate translated text will be too long to return",
                KEY_EXPECTED: "Too long, your translation is. Please shorten it and try again. Yrsssss."
            }    
        ]
        
        self.success_add_user_params = [
            {
                KEY_USER:"My Name",
                KEY_EMAIL:"useremail@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_SESSION_ID: "session id"
            },
            {
                KEY_USER: "Users Full Name",
                KEY_EMAIL: "hello@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_SESSION_ID: "session id" 
            }
        ]
        
        self.success_add_message_params = [
            {
                KEY_MESSAGE: "message text",
                KEY_ID: 1
            }    
        ]
        
        self.success_socket_on = [
            {
                KEY_INPUT: "new google user",
                KEY_EXPECTED: {
                    'name': "new google user",
                    'email': 'email@email.com',
                    'avatar': 'avatar'
                }
            }    
        ]
        
        
    
    def mocked_api_funtranslate(self, botCall):
        return (
            {
                "success": {
                    "total": 1
                },
                "contents": {
                    "translated": "Text",
                    "text": "text",
                    "translation": "yoda"
                }
            }    
        )
    
    def mocked_api_funtranslate_length(self, botCall):
        length1000 = "i"
        for i in range(0,1000):
            length1000 += str(i)
        return (
            {
                "success": {
                    "total": 1
                },
                "contents": {
                    "translated": length1000,
                    "text": "translated text will be too long to return",
                    "translation": "yoda"
                }
            }    
        )
    
    def mocked_api_quote(self):
        return (
            {
                "id": 23,
                "starWarsQuote": "The Force will be with you. Always. — Obi-Wan Kenobi",
                "faction": 0
            }    
        )

    def mocked_add_user(self, name, email, avatar):
        return MockedModelsUsers(name, email, avatar, 123)
        
    def mocked_add_new_message(self,message,uid):
        return MockedModelsChatlog(message,uid)
    
    def test_add_user_to_db(self):
        for test in self.success_add_user_params:
            with mock.patch('models.db.session.add', self.mocked_add_user):
                response = models.Users(test[KEY_USER], test[KEY_EMAIL], test[KEY_AVATAR], test[KEY_SESSION_ID])
                
    def test_add_message_to_db(self):
        for test in self.success_add_message_params:
            with mock.patch('models.db.session.add', self.mocked_add_new_message):
                response = models.Chatlog(test[KEY_MESSAGE], test[KEY_ID])
    
    def test_chatbot_translate(self):
        for test in self.success_translate_params:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch('requests.get')
            translated_text = self.mocked_api_funtranslate('')
            mock_get = mock_get_patcher.start()
            mock_get.return_value = mock.Mock(status_code = 200)
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_chatbot_translate_failure(self):
        for test in self.failure_translate_params:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch('requests.get')
            translated_text = self.mocked_api_funtranslate('')
            mock_get = mock_get_patcher.start()
            mock_get.return_value = mock.Mock(status_code = 200)
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    def test_chatbot_quote_success(self):
        for test in self.success_quote_params:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch('requests.get')
            quote = self.mocked_api_quote()
            mock_get = mock_get_patcher.start()
            mock_get.return_value = mock.Mock(status_code = 200)
            mock_get.return_value.json.return_value = quote
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_chatbot_translate_length(self):
        for test in self.success_translate_length_too_long:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch('requests.get')
            translated_text = self.mocked_api_funtranslate_length('')
            mock_get = mock_get_patcher.start()
            mock_get.return_value = mock.Mock(status_code = 200)
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
        
    @mock.patch("flask_socketio.SocketIO.emit")
    def test_socket_emit(self, emit_message):
        for test in self.success_socket_on:
            with mock.patch("app.add_user", self.mocked_add_user):
                self.socketio.emit(test[KEY_INPUT], test[KEY_EXPECTED])
                successful_google_login(test[KEY_EXPECTED])
    
if __name__ == '__main__':
    unittest.main()
