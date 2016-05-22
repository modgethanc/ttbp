#!/usr/bin/python

'''
ttbp: tilde town blogging platform
(also known as the feels engine)
a console-based blogging program developed for tilde.town
copyright (c) 2016 ~endorphant (endorphant@tilde.town)

chatter.py:
some text processing utilities

GNU GPL BOILERPLATE:
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

the complete codebase is available at:
https://github.com/modgethanc/ttbp
'''

import os

import random
import json
import os

SOURCE = os.path.join("/home", "endorphant", "projects", "ttbp")
langfile = open(os.path.join(SOURCE, "lib", "lang.json"), 'r')
LANG = json.load(langfile)
langfile.close()

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
