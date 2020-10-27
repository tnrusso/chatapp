import unittest
import sys
sys.path.append('.')
import app
from app import app, bot_command_called, add_bot
from chatbot import ChatBot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_EXPECTED_ALT = "conditional_expected"
ABOUT_CORRECT = "A bot created for this project I am... Type !!help, my commands to see. Yes, hrrmmm."
HELP_CORRECT = "!!about !!help !!funtranslate [text] !!quote !!ready, the commands I recognize are"
READY_CORRECT_1 = "What know you of ready? For eight hundred years have I trained Jedi. To start training Jedi, ready you are not."
READY_CORRECT_2 = "This one, a long time have I watched. When gone am I, the last of the Jedi will you be."
COMMAND_INCORRECT = "Recognize that command I do not. All possible commands, type !!help to see"

class UnmockedTestCases(unittest.TestCase):
    def setUp(self):
        self.success_chatbot_about = [
            {
                KEY_INPUT: "!!about",
                KEY_EXPECTED: ABOUT_CORRECT
            },    
            {
                KEY_INPUT: "!about",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!! about",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!!abouts",
                KEY_EXPECTED: COMMAND_INCORRECT
            }
        ]

        self.failure_chatbot_about = [
            {
                KEY_INPUT: "!!about",
                KEY_EXPECTED: COMMAND_INCORRECT
            },    
            {
                KEY_INPUT: "!about",
                KEY_EXPECTED: ABOUT_CORRECT
            },
            {
                KEY_INPUT: "!! about",
                KEY_EXPECTED: ABOUT_CORRECT
            },
            {
                KEY_INPUT: "!!abouts",
                KEY_EXPECTED: ABOUT_CORRECT
            }
        ]

        self.success_chatbot_help = [
            {
                KEY_INPUT: "!!help",
                KEY_EXPECTED: HELP_CORRECT
            },    
            {
                KEY_INPUT: "!help",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!!helpp",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!!help!!!!",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!!help plz",
                KEY_EXPECTED: COMMAND_INCORRECT
            }
        ]

        self.failure_chatbot_help = [
            {
                KEY_INPUT: "!!help",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!!help",
                KEY_EXPECTED: ABOUT_CORRECT
            },
            {
                KEY_INPUT: "!help",
                KEY_EXPECTED: HELP_CORRECT
            },
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: HELP_CORRECT
            },
            {
                KEY_INPUT: "!!helpp",
                KEY_EXPECTED: HELP_CORRECT
            },
            {
                KEY_INPUT: "!!help me plz",
                KEY_EXPECTED: HELP_CORRECT
            }
        ]

        self.success_chatbot_ready = [
            {
                KEY_INPUT: "!!ready",
                KEY_EXPECTED: READY_CORRECT_1,
                KEY_EXPECTED_ALT: READY_CORRECT_2
            },
            {
                KEY_INPUT: "!ready",
                KEY_EXPECTED: COMMAND_INCORRECT,
                KEY_EXPECTED_ALT: COMMAND_INCORRECT 
            }
        ]

        self.failure_chatbot_ready = [
            {
                KEY_INPUT: "!!ready",
                KEY_EXPECTED: COMMAND_INCORRECT,
                KEY_EXPECTED_ALT: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!ready",
                KEY_EXPECTED: READY_CORRECT_1,
                KEY_EXPECTED_ALT: READY_CORRECT_2
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

        self.failure_bot_command_call = [
            {
                KEY_INPUT: "!!about",
                KEY_EXPECTED: ABOUT_CORRECT
            },
            {
                KEY_INPUT: "!!quote",
                KEY_EXPECTED: COMMAND_INCORRECT
            },
            {
                KEY_INPUT: "!!help",
                KEY_EXPECTED: HELP_CORRECT
            }
                
        ]


    def test_success_bot_about(self):
        for test in self.success_chatbot_about:
            response = ChatBot(test[KEY_INPUT]).get_bot_response()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_failure_bot_about(self):
        for test in self.failure_chatbot_about:
            response = ChatBot(test[KEY_INPUT]).get_bot_response()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    def test_success_bot_help(self):
        for test in self.success_chatbot_help:
            response = ChatBot(test[KEY_INPUT]).get_bot_response()
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_failure_bot_help(self):
        for test in self.failure_chatbot_help:
            response = ChatBot(test[KEY_INPUT]).get_bot_response()
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)

    def test_success_bot_ready(self):
        for test in self.success_chatbot_ready:
            response = ChatBot(test[KEY_INPUT]).get_bot_response()
            expected = test[KEY_EXPECTED]
            expected_alt = test[KEY_EXPECTED_ALT]
            self.assertTrue(response == expected or response == expected_alt)

    def test_failure_bot_ready(self):
        for test in self.failure_chatbot_ready:
            response = ChatBot(test[KEY_INPUT]).get_bot_response()
            expected = test[KEY_EXPECTED]
            expected_alt = test[KEY_EXPECTED_ALT]
            self.assertFalse(response == expected or response == expected_alt)

    def test_success_add_bot(self):
        expected = None
        self.assertEqual(add_bot(), expected)

    def test_failure_add_bot(self):
        expected = ""
        self.assertNotEqual(add_bot(), expected)

    def test_success_bot_command_call(self):
        for test in self.success_bot_command_call:
            expected = test[KEY_EXPECTED]
            self.assertEqual(bot_command_called(test[KEY_INPUT]), expected)
            
    def test_bot_failure_command_call(self):
        for test in self.failure_bot_command_call:
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(bot_command_called(test[KEY_INPUT]), expected)

if __name__ == '__main__':
    unittest.main()
