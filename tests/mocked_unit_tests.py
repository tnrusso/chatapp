from os.path import join, dirname
from dotenv import load_dotenv

import os

import unittest
import unittest.mock as mock

import sys
sys.path.append('.')
import app
from app import app
from chatbot import ChatBot

import json

KEY_INPUT = "input"
KEY_EXPECTED = "expected"


class MockedFuntranslate:
    def __init__(self, text):
        self.text = text

class MockedTestCases(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "!!funtranslate text",
                KEY_EXPECTED: "Text"
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
        
    def mocked_get_request(self, url):
        return "<Response [200]>"
        
        
    def test_parse_chatbot_message_success(self):
        for test in self.success_test_params:
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

if __name__ == '__main__':
    unittest.main()
