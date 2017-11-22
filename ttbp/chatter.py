import json
import os
import random

DEFAULT_LANG = {
    "greet":[
        "hi",
        "hey",
        "howdy",
        "good morning",
        "good afternoon",
        "good day",
        "good evening",
        "welcome back",
        "nice to see you"
    ],
    "bye":[
        "see you later, space cowboy",
        "bye, townie",
        "until next time, friend",
        "come back whenever"
    ],
    "friend":[
        "friend",
        "pal",
        "buddy",
        "townie"
    ],
    "months":{
        "01":"january",
        "02":"february",
        "03":"march",
        "04":"april",
        "05":"may",
        "06":"june",
        "07":"july",
        "08":"august",
        "09":"september",
        "10":"october",
        "11":"november",
        "12":"december"
  }
}

if os.path.exists("/home/endorphant/lib/python/chatterlib.json"):
    with open("/home/endorphant/lib/python/chatterlib.json", 'r') as f:
        LANG = json.load(f)
else:
    LANG = DEFAULT_LANG

def say(keyword):
    '''
    takes a keyword and randomly returns from language dictionary to match that keyword

    returns None if keyword doesn't exist

    TODO: validate keyword?
    '''

    return random.choice(LANG.get(keyword))

def month(num):
    '''
    takes a MM and returns lovercase full name of that month

    TODO: validate num?
    '''

    return LANG["months"].get(num)
