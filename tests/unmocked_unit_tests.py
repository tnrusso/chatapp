import unittest
import sys
sys.path.append('.')
import app
from app import app
from chatbot import ChatBot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

class UnmockedTestCases(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "!!about",
                KEY_EXPECTED: "A bot created for this project I am... Type !!help, my commands to see. Yes, hrrmmm."
            },    
            {
                KEY_INPUT: "!!help",
                KEY_EXPECTED: "!!about !!help !!funtranslate [text] !!quote !!ready, the commands I recognize are"
            },
            {
                KEY_INPUT: "!about",
                KEY_EXPECTED: "Recognize that command I do not. All possible commands, type !!help to see"
            }
        ]
        #self.failure_test_params = []

    def test_parse_message_success(self):
        for test in self.success_test_params:
            response = ChatBot(test[KEY_INPUT]).get_bot_response()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
#    def test_parse_message_failure(self):
#        for test in self.failure_test_params:
#            response = chatbot.get_bot_response(test[KEY_INPUT])

if __name__ == '__main__':
    unittest.main()
