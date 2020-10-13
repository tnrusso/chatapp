import json
import requests
import random


class ChatBot:
    
    def __init__(self, botCall):
        self.botCall = botCall
        
    def get_bot_response(self):
        botResponse = ""
        if(self.botCall == '!!about'):
            botResponse = "A bot created for this project I am... Type !!help, my commands to see. Yes, hrrmmm."
        elif(self.botCall == '!!help'):
            botResponse = "!!about !!help !!funtranslate [text] !!quote !!ready, the commands I recognize are"
        elif(self.botCall[0:14] == '!!funtranslate'): # Translate to yoda language https://funtranslations.com/api/yoda
            url = 'https://api.funtranslations.com/translate/yoda.json?text=' + self.botCall[14:]
            response = requests.get(url)
            json_body = response.json()
            if('contents' not in json_body):
                botResponse = json_body['error']['message']
            else:
                yodaTranslate = json_body['contents']['translated']
                botResponse = yodaTranslate
        elif(self.botCall == '!!quote'): # Random quote from star wars
            url = 'http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote'
            response = requests.get(url)
            json_body = response.json()
            if('starWarsQuote' not in json_body):
                botResponse = "Out of API calls. Try again later"
            else:
                botResponse = json_body['starWarsQuote']
        elif(self.botCall == '!!ready'):
            randomNum = random.randint(0,1000)
            if(randomNum == 1):
                botResponse = "This one, a long time have I watched. When gone am I, the last of the Jedi will you be."
            else:
                botResponse = "What know you of ready? For eight hundred years have I trained Jedi. To start training Jedi, ready you are not."
        else:
            botResponse = "Recognize that command I do not. All possible commands, type !!help to see"
            
        return botResponse