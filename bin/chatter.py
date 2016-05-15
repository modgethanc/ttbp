#!/usr/bin/python

import random
import json
import os

SOURCE = os.path.join("/home", "endorphant", "projects", "ttbp")
langfile = open(os.path.join(SOURCE, "lib", "lang.json"), 'r')
LANG = json.load(langfile)
langfile.close()

def say(keyword):

  return random.choice(LANG.get(keyword))

def month(num):
  return LANG["months"].get(num)
