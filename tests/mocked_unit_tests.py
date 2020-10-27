"""Mocked Tests"""
# pylint: disable=wrong-import-position, too-few-public-methods, wrong-import-order, no-self-use, unused-argument, R0902, W0611

import unittest
import unittest.mock as mock

import sys

sys.path.append(".")
from app import (
    app,
    successful_google_login,
    on_connect,
)
from chatbot import ChatBot
import models

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
FUNTRANSLATE_LONG_LENGTH = (
    "Too long, your translation is. Please shorten it and try again. Yrsssss."
)
QUOTE_CORRECT = "The Force will be with you. Always. — Obi-Wan Kenobi"
COMMAND_INCORRECT = (
    "Recognize that command I do not. All possible commands, type !!help to see"
)


class MockedModelUsers:
    """Users"""
    def __init__(self, user_name, user_email, user_avatar, session_id):
        self.user_name = user_name
        self.user_email = user_email
        self.user_avatar = user_avatar
        self.session_id = session_id


class MockedModelChatLog:
    """Chatlog"""
    def __init__(self, message, user_id):
        self.message = message
        self.user_id = user_id


class MockedTestCases(unittest.TestCase):
    """Mocked test cases"""
    def setUp(self):
        """Set up test inputs/expected results"""
        self.success_chatbot_quote = [
            {
                KEY_INPUT: "!!quote",
                KEY_EXPECTED: QUOTE_CORRECT,
            },
            {KEY_INPUT: "!quote", KEY_EXPECTED: COMMAND_INCORRECT},
            {KEY_INPUT: "!! quote", KEY_EXPECTED: COMMAND_INCORRECT},
            {KEY_INPUT: "!!quota", KEY_EXPECTED: COMMAND_INCORRECT},
        ]

        self.failure_chatbot_quote = [
            {
                KEY_INPUT: "!!quote",
                KEY_EXPECTED: COMMAND_INCORRECT,
            },
            {KEY_INPUT: "!quote", KEY_EXPECTED: QUOTE_CORRECT},
            {KEY_INPUT: "!! quote", KEY_EXPECTED: QUOTE_CORRECT},
            {KEY_INPUT: "!!quota", KEY_EXPECTED: QUOTE_CORRECT},
        ]

        self.success_translate_params = [
            {KEY_INPUT: "!!funtranslate text", KEY_EXPECTED: FUNTRANSLATE_CORRECT},
            {KEY_INPUT: "!!translate text", KEY_EXPECTED: COMMAND_INCORRECT},
            {KEY_INPUT: "!! funtranslate text", KEY_EXPECTED: COMMAND_INCORRECT},
        ]

        self.failure_translate_params = [
            {
                KEY_INPUT: "!!funtranslate text",
                KEY_EXPECTED: COMMAND_INCORRECT,
            },
            {KEY_INPUT: "!! funtranslate text", KEY_EXPECTED: FUNTRANSLATE_CORRECT},
            {KEY_INPUT: "!funtranslate", KEY_EXPECTED: FUNTRANSLATE_CORRECT},
        ]

        self.success_translate_length_too_long = [
            {
                KEY_INPUT: "!!funtranslate translated text will be too long to return",
                KEY_EXPECTED: FUNTRANSLATE_LONG_LENGTH,
            }
        ]

        self.failure_translate_length_too_long = [
            {
                KEY_INPUT: "!!funtranslate translated text will be too long to return",
                KEY_EXPECTED: FUNTRANSLATE_CORRECT,
            }
        ]

        self.success_add_user_params = [
            {
                KEY_USER: "My Name",
                KEY_EMAIL: "user_email@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_SESSION_ID: "123",
            },
            {
                KEY_USER: "Users Full Name",
                KEY_EMAIL: "hello@gmail.com",
                KEY_AVATAR: "avatar",
                KEY_SESSION_ID: "123",
            },
        ]

        self.success_add_message_params = [
            {KEY_MESSAGE: "message text", KEY_ID: '1'},
            {KEY_MESSAGE: "some text message", KEY_ID: '2'},
            {KEY_MESSAGE: "qwerrrrewdfasdfasdc", KEY_ID: '8'},
        ]

        self.success_socket_user = [
            {
                KEY_INPUT: "new google user",
                KEY_EXPECTED: {
                    "name": "new google user",
                    "email": "email@email.com",
                    "avatar": "avatar",
                },
            },
            {
                KEY_INPUT: "new google user",
                KEY_EXPECTED: {
                    "name": "full name",
                    "email": "bluesticker22@gmail.com",
                    "avatar": "avatar",
                },
            },
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

    def mocked_api_funtranslate(self, bot_call):
        """Mocked translate API call"""
        return {
            "success": {"total": 1},
            "contents": {"translated": "Text", "text": "text", "translation": "yoda"},
        }

    def mocked_api_funtranslate_length(self, bot_call):
        """Mocked translate API call for long length"""
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
        """Mocked quote API call"""
        return {
            "id": 23,
            "starWarsQuote": "The Force will be with you. Always. — Obi-Wan Kenobi",
            "faction": 0,
        }

    def mocked_add_user(self, name, email, avatar):
        """Add user"""
        return MockedModelUsers(name, email, avatar, '123')

    def mocked_add_new_message(self, message, uid):
        """Add new message"""
        return MockedModelChatLog(message, uid)

    def test_add_user_to_db(self):
        """Test add user"""
        for test in self.success_add_user_params:
            with mock.patch("models.db.session.add", self.mocked_add_user):
                response = models.Users(
                    test[KEY_USER],
                    test[KEY_EMAIL],
                    test[KEY_AVATAR],
                    test[KEY_SESSION_ID],
                )
                expected = self.mocked_add_user(
                    test[KEY_USER], test[KEY_EMAIL], test[KEY_AVATAR]
                )
                self.assertEqual(response.user_name, expected.user_name)
                self.assertEqual(response.user_email, expected.user_email)
                self.assertEqual(response.user_avatar, expected.user_avatar)
                self.assertEqual(response.session_id, expected.session_id)

    def test_add_message_to_db(self):
        """Test add message"""
        for test in self.success_add_message_params:
            with mock.patch("models.db.session.add", self.mocked_add_new_message):
                response = models.Chatlog(test[KEY_MESSAGE], test[KEY_ID])
                expected = self.mocked_add_new_message(test[KEY_MESSAGE], test[KEY_ID])
                self.assertEqual(response.message, expected.message)
                self.assertEqual(response.user_id, expected.user_id)

    def test_chatbot_translate_success(self):
        """Test success chatbot funtranslate"""
        for test in self.success_translate_params:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patch = mock.patch("requests.get")
            translated_text = self.mocked_api_funtranslate("")
            mock_get = mock_get_patch.start()
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patch.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_chatbot_translate_failure(self):
        """Test failure chatbot translate"""
        for test in self.failure_translate_params:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patch = mock.patch("requests.get")
            translated_text = self.mocked_api_funtranslate("")
            mock_get = mock_get_patch.start()
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patch.stop()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    def test_chatbot_quote_success(self):
        """Test success chatbot quote"""
        for test in self.success_chatbot_quote:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patch = mock.patch("requests.get")
            quote = self.mocked_api_quote()
            mock_get = mock_get_patch.start()
            mock_get.return_value.json.return_value = quote
            response = chatbot.get_bot_response()
            mock_get_patch.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_chatbot_quote_failure(self):
        """Test failure chatbot quote"""
        for test in self.failure_chatbot_quote:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patch = mock.patch("requests.get")
            quote = self.mocked_api_quote()
            mock_get = mock_get_patch.start()
            mock_get.return_value.json.return_value = quote
            response = chatbot.get_bot_response()
            mock_get_patch.stop()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    def test_success_chatbot_translate_length(self):
        """Test success chatbot translate long length"""
        for test in self.success_translate_length_too_long:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patch = mock.patch("requests.get")
            translated_text = self.mocked_api_funtranslate_length("")
            mock_get = mock_get_patch.start()
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patch.stop()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_failure_chatbot_translate_length(self):
        """Test failure chatbot translate long length"""
        for test in self.failure_translate_length_too_long:
            chatbot = ChatBot(test[KEY_INPUT])
            mock_get_patch = mock.patch("requests.get")
            translated_text = self.mocked_api_funtranslate_length("")
            mock_get = mock_get_patch.start()
            mock_get.return_value.json.return_value = translated_text
            response = chatbot.get_bot_response()
            mock_get_patch.stop()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    @mock.patch("flask_socketio.SocketIO.emit")
    def test_socket_emit(self, emit_message):
        """Test socket emit"""
        for test in self.success_socket_user:
            with mock.patch("app.add_user", self.mocked_add_user):
                successful_google_login(test[KEY_EXPECTED])
                expected = self.mocked_add_user(
                    test[KEY_EXPECTED]["name"],
                    test[KEY_EXPECTED]["email"],
                    test[KEY_EXPECTED]["avatar"],
                )
                self.assertIsInstance(expected, MockedModelUsers)

    @mock.patch("flask_socketio.SocketIO.emit")
    def test_socket_connect(self, emit_message):
        """Test socket emit"""
        on_connect()
        self.assertEqual(on_connect(), None)


if __name__ == "__main__":
    unittest.main()
