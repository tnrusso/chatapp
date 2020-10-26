'''This module contains the chat bot responses'''
#pylint: disable=too-few-public-methods, superfluous-parens
import random
import requests


class ChatBot:
    '''Chatbot Class'''
    def __init__(self, bot_call):
        self.bot_call = bot_call

    def get_bot_response(self):
        '''Determines the chat bot response depending on user input command'''
        bot_response = ""
        if(self.bot_call == '!!about'):
            bot_response = (
                "A bot created for this project I am... "+ \
                "Type !!help, my commands to see. Yes, hrrmmm.")
        elif(self.bot_call == '!!help'):
            bot_response = \
                "!!about !!help !!funtranslate [text] !!quote !!ready, the commands I recognize are"
        elif(self.bot_call[0:14] == '!!funtranslate'):
            # Translate to yoda language https://funtranslations.com/api/yoda
            url = 'https://api.funtranslations.com/translate/yoda.json?text=' + self.bot_call[14:]
            response = requests.get(url)
            json_body = response.json()
            if('contents' not in json_body):
                bot_response = json_body['error']['message']
            elif(len(json_body['contents']['translated']) > 1000):
                bot_response = (
                    "Too long, your translation is. "+\
                    "Please shorten it and try again. Yrsssss.")
            else:
                yoda_translate = json_body['contents']['translated']
                bot_response = yoda_translate
        elif(self.bot_call == '!!quote'): # Random quote from star wars
            url = 'http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote'
            response = requests.get(url)
            json_body = response.json()
            bot_response = "Out of API calls. Try again later"
            if('starWarsQuote' in json_body):
                bot_response = json_body['starWarsQuote']
        elif(self.bot_call == '!!ready'):
            random_num = random.randint(0, 1000)
            if(random_num == 1):
                bot_response = (
                    "This one, a long time have I watched. "+\
                    "When gone am I, the last of the Jedi will you be.")
            else:
                bot_response = (
                    "What know you of ready? "+\
                    "For eight hundred years have I trained Jedi. "+\
                    "To start training Jedi, ready you are not.")
        else:
            bot_response = (
                "Recognize that command I do not. "+\
                "All possible commands, type !!help to see")

        return bot_response
