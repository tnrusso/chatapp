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
    
    
    
if __name__ == '__main__':
    unittest.main()
