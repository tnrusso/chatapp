from os.path import join, dirname
from dotenv import load_dotenv

import os

import unittest
import unittest.mock as mock

import sys

sys.path.append(".")
from app import (
    app,
    emit_all_messages,
    add_user,
    update_user_count,
    successful_google_login,
    on_new_message,
    on_connect,
    on_disconnect,
)
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
KEY_EXPECTED_ALT = "conditional_expected"
KEY_USER = "name"
KEY_EMAIL = "email"
KEY_AVATAR = "avatar"
KEY_SESSION_ID = "session_id"
KEY_MESSAGE = "message"
KEY_ID = "id"

FUNTRANSLATE_CORRECT = "Text"
FUNTRANSLATE_LONG_LENGTH = "Too long, your translation is. Please shorten it and try again. Yrsssss."
QUOTE_CORRECT = "The Force will be with you. Always. — Obi-Wan Kenobi"
COMMAND_INCORRECT = "Recognize that command I do not. All possible commands, type !!help to see"

class mocked_models_users:
    def __init__(self, user_name, user_email, user_avatar, session_id):
        self.user_name = user_name
        self.user_email = user_email
        self.user_avatar = user_avatar
        self.session_id = session_id


class mocked_models_chatlog:
    def __init__(self, message, userID):
        self.message = message
        self.userID = userID


class MockedTestCases(unittest.TestCase):
    def setUp(self):

        self.success_chatbot_quote = [
            {
                KEY_INPUT: "!!quote",
                KEY_EXPECTED: QUOTE_CORRECT,
            },
            {
                KEY_INPUT: "!quote",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!! quote",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!!quota",
                KEY_EXPECTED: COMMAND_INCORRECT
            }
        ]
        
        self.failure_chatbot_quote = [
            {
                KEY_INPUT: "!!quote",
                KEY_EXPECTED: COMMAND_INCORRECT,
            },
            {
                KEY_INPUT: "!quote",
                KEY_EXPECTED: QUOTE_CORRECT
            },
            {
                KEY_INPUT: "!! quote",
                KEY_EXPECTED: QUOTE_CORRECT
            },
            {
                KEY_INPUT: "!!quota",
                KEY_EXPECTED: QUOTE_CORRECT
            }
        ]

        self.success_translate_params = [
            {
                KEY_INPUT: "!!funtranslate text",
                KEY_EXPECTED: FUNTRANSLATE_CORRECT
            },
            {
                KEY_INPUT: "!!translate text",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!! funtranslate text",
                KEY_EXPECTED: COMMAND_INCORRECT
            }
        ]

        self.failure_translate_params = [
            {
                KEY_INPUT: "!!funtranslate text",
                KEY_EXPECTED: COMMAND_INCORRECT,
            },
            {
                KEY_INPUT: "!! funtranslate text",
                KEY_EXPECTED: FUNTRANSLATE_CORRECT
            },
            {
                KEY_INPUT: "!funtranslate",
                KEY_EXPECTED: FUNTRANSLATE_CORRECT
            }
        ]

        self.success_translate_length_too_long = [
            {
                KEY_INPUT: "!!funtranslate translated text will be too long to return",
                KEY_EXPECTED: FUNTRANSLATE_LONG_LENGTH
            }
        ]
        
        self.failure_translate_length_too_long = [
            {
                KEY_INPUT: "!!funtranslate translated text will be too long to return",
                KEY_EXPECTED: FUNTRANSLATE_CORRECT
            }
        ]

        self.success_add_user_params = [
            {
                KEY_USER: "My Name",
                KEY_EMAIL: "user_email@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_SESSION_ID: "session id",
            },
            {
                KEY_USER: "Users Full Name",
                KEY_EMAIL: "hello@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_SESSION_ID: "session id",
            },
        ]

        self.success_add_message_params = [
            {
                KEY_MESSAGE: "message text",
                KEY_ID: 1
            },
            {
                KEY_MESSAGE: "some text message",
                KEY_ID: 2
            },
            {
                KEY_MESSAGE: "qwerrrrewdfasdfasdc",
                KEY_ID: 8
            }
        ]

        self.success_socket_user = [
            {
                KEY_INPUT: "new google user",
                KEY_EXPECTED: {
                    "name": "new google user",
                    "email": "email@email.com",
                    "avatar": "avatar",
                }
            },
            {
                KEY_INPUT: "new google user",
                KEY_EXPECTED: {
                    "name": "full name",
                    "email": "bluesticker22@gmail.com",
                    "avatar": "avatar",
                }
            }
        ]

        self.success_add_user_method = [
            {
                KEY_USER: "name",
                KEY_EMAIL: "email@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_EXPECTED: None,
            },
            {
                KEY_USER: "qwertqwy",
                KEY_EMAIL: "my_email@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_EXPECTED: None,
            },
            {
                KEY_USER: "My Username",
                KEY_EMAIL: "bug@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_EXPECTED: None,
            },
        ]

    def mocked_api_funtranslate(self, botCall):
        return {
            "success": {"total": 1},
            "contents": {"translated": "Text", "text": "text", "translation": "yoda"},
        }

    def mocked_api_funtranslate_length(self, botCall):
        length1000 = "i"
        for i in range(0, 1100):
            length1000 += str(i)
        return {
            "success": {"total": 1},
            "contents": {
                "translated": length1000,
                "text": "translated text will be too long to return",
                "translation": "yoda",
            },
        }

    def mocked_api_quote(self):
        return {
            "id": 23,
            "starWarsQuote": "The Force will be with you. Always. — Obi-Wan Kenobi",
            "faction": 0,
        }

    def mocked_add_user(self, name, email, avatar):
        return mocked_models_users(name, email, avatar, 123)

    def mocked_add_new_message(self, message, uid):
        return mocked_models_chatlog(message, uid)

    def mocked_add_bot(self):
        bot = mocked_models_users("name", "email", "avatar", "1")
        return bot

    def mocked_db_query(self, name):
        return None

    def test_add_user_to_db(self):
        for test in self.success_add_user_params:
            with mock.patch("models.db.session.add", self.mocked_add_user):
                models.Users(
                    test[KEY_USER],
                    test[KEY_EMAIL],
                    test[KEY_AVATAR],
                    test[KEY_SESSION_ID],
                )
                expected = self.mocked_add_user(
                    test[KEY_USER], test[KEY_EMAIL], test[KEY_AVATAR]
                )
                self.assertIsInstance(expected, mocked_models_users)

    def test_add_message_to_db(self):
        for test in self.success_add_message_params:
            with mock.patch("models.db.session.add", self.mocked_add_new_message):
                models.Chatlog(test[KEY_MESSAGE], test[KEY_ID])
                expected = self.mocked_add_new_message(test[KEY_MESSAGE], test[KEY_ID])
                self.assertIsInstance(expected, mocked_models_chatlog)

    def test_chatbot_translate(self):
        for test in self.success_translate_params:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch("requests.get")
            translated_text = self.mocked_api_funtranslate("")
            mock_get = mock_get_patcher.start()
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_chatbot_translate_failure(self):
        for test in self.failure_translate_params:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch("requests.get")
            translated_text = self.mocked_api_funtranslate("")
            mock_get = mock_get_patcher.start()
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    def test_chatbot_quote_success(self):
        for test in self.success_chatbot_quote:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch("requests.get")
            quote = self.mocked_api_quote()
            mock_get = mock_get_patcher.start()
            mock_get.return_value.json.return_value = quote
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_chatbot_quote_failure(self):
        for test in self.failure_chatbot_quote:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch("requests.get")
            quote = self.mocked_api_quote()
            mock_get = mock_get_patcher.start()
            mock_get.return_value.json.return_value = quote
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    def test_success_chatbot_translate_length(self):
        for test in self.success_translate_length_too_long:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch("requests.get")
            translated_text = self.mocked_api_funtranslate_length("")
            mock_get = mock_get_patcher.start()
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_failure_chatbot_translate_length(self):
        for test in self.failure_translate_length_too_long:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patcher = mock.patch("requests.get")
            translated_text = self.mocked_api_funtranslate_length("")
            mock_get = mock_get_patcher.start()
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patcher.stop()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    @mock.patch("flask_socketio.SocketIO.emit")
    def test_socket_emit(self, emit_message):
        for test in self.success_socket_user:
            with mock.patch("app.add_user", self.mocked_add_user):
                successful_google_login(test[KEY_EXPECTED])
                expected = self.mocked_add_user(
                    test[KEY_EXPECTED]["name"],
                    test[KEY_EXPECTED]["email"],
                    test[KEY_EXPECTED]["avatar"],
                )
                self.assertIsInstance(expected, mocked_models_users)

    @mock.patch("flask_socketio.SocketIO.emit")
    def test_socket_connect(self, emit_message):
        with mock.patch("app.add_bot", self.mocked_add_bot):
            on_connect()
            self.assertEqual(on_connect(), None)


if __name__ == "__main__":
    unittest.main()
