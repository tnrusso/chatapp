import unittest
import sys
sys.path.append('.')
import app
from app import app, bot_command_called
from chatbot import ChatBot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_EXPECTED_ALT = "conditional_expected"
class UnmockedTestCases(unittest.TestCase):
    def setUp(self):
        self.success_chatbot_params = [
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
            },
            {
                KEY_INPUT: "!!",
                KEY_EXPECTED: "Recognize that command I do not. All possible commands, type !!help to see"
            },
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: "Recognize that command I do not. All possible commands, type !!help to see"
            }
        ]
        
        self.failure_chatbot_params = [
            {
                KEY_INPUT: "!!about",
                KEY_EXPECTED: "!!about !!help !!funtranslate [text] !!quote !!ready, the commands I recognize are"
            },    
            {
                KEY_INPUT: "!!help",
                KEY_EXPECTED: "the commands I recognize are"
            },
            {
                KEY_INPUT: "!about",
                KEY_EXPECTED: "A bot created for this project I am..."
            },
            {
                KEY_INPUT: "!!",
                KEY_EXPECTED: "!!about !!help !!funtranslate [text] !!quote !!ready, the commands I recognize are"
            },
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: "!!about !!help !!funtranslate [text] !!quote !!ready, the commands I recognize are"
            }
        ]
        
        self.success_ready_params = [
            {
                KEY_INPUT: "!!ready",
                KEY_EXPECTED: "What know you of ready? For eight hundred years have I trained Jedi. To start training Jedi, ready you are not.",
                KEY_EXPECTED_ALT: "This one, a long time have I watched. When gone am I, the last of the Jedi will you be."
            }    
        ]
        
        self.success_bot_command_call = [
            {
                KEY_INPUT: "!!about",
                KEY_EXPECTED: None
            },
            {
                KEY_INPUT: "!!quote",
                KEY_EXPECTED: None
            },
            {
                KEY_INPUT: "!!help",
                KEY_EXPECTED: None
            }
                
        ]

    
    # def test_success_bot_message(self):
    #     for test in self.success_chatbot_params:
    #         response = ChatBot(test[KEY_INPUT]).get_bot_response()
    #         expected = test[KEY_EXPECTED]
    #         self.assertEqual(response, expected)

    # def test_failure_bot_message(self):
    #     for test in self.failure_chatbot_params:
    #         response = ChatBot(test[KEY_INPUT]).get_bot_response()
    #         expected = test[KEY_EXPECTED]
    #         self.assertNotEqual(response, expected)

    # def test_success_ready_params(self):
    #     for test in self.success_ready_params:
    #         response = ChatBot(test[KEY_INPUT]).get_bot_response()
    #         expected = test[KEY_EXPECTED]
    #         expected_alt = test[KEY_EXPECTED_ALT]
    #         self.assertTrue(response == expected or response == expected_alt)

    # def test_bot_command_call(self):
    #     for test in self.success_bot_command_call:
    #         expected = test[KEY_EXPECTED]
    #         self.assertEqual(bot_command_called(test[KEY_INPUT]), expected)

if __name__ == '__main__':
    unittest.main()
