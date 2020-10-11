import json
import requests


# Still need one more chatbot command
class ChatBot:
    
    def __init__(self, botCall):
        self.botCall = botCall
        
    def get_bot_response(self):
        botResponse = ""
        if(self.botCall == '!!about'):
            botResponse = "A bot created for this project I am... Type !!help, my commands to see. Yes, hrrmmm."
        elif(self.botCall == '!!help'):
            botResponse = "!!about !!help !!funtranslate !!quote, the commands I recognize are"
        elif(self.botCall[0:14] == '!!funtranslate'): # Translate to yoda language https://funtranslations.com/api/yoda
            url = 'https://api.funtranslations.com/translate/yoda.json?text=' + self.botCall[14:]
            response = requests.get(url)
            json_body = response.json()
            yodaTranslate = json_body['contents']['translated']
            botResponse = yodaTranslate
        elif(self.botCall == '!!quote'): # Random quote from yoda
            url = 'http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote'
            response = requests.get(url)
            json_body = response.json()
            botResponse = json_body['starWarsQuote']
        else:
            botResponse = "Recognize that command I do not. All possible commands, type !!help to see"
            
        return botResponse