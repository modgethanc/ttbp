#!/usr/bin/python

'''
util.py: frequently used terminal and text processing utilities
copyright (c) 2016 ~endorphant (endorphant@tilde.town)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import random
import time
from six.moves import input
import os

import colorama
import inflect

## misc globals
BACKS = ['back', 'b', 'q', '<q>']
NAVS = ['u', 'd']

## color stuff
colorama.init()
textcolors = [ colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.WHITE, colorama.Fore.CYAN]
lastcolor = colorama.Fore.RESET

p = inflect.engine()

def set_rainbow():
    '''
    prints a random terminal color code
    '''

    global lastcolor

    color = lastcolor
    while color == lastcolor:
        color = random.choice(textcolors)

    lastcolor = color

    print(color)

def reset_color():
    '''
    prints terminal color code reset
    '''

    print(colorama.Fore.RESET)

def attach_rainbow():
    '''
    returns a random terminal color code, presumably to be 'attached' to a string
    '''

    global lastcolor

    color = lastcolor
    while color == lastcolor:
        color = random.choice(textcolors)

    lastcolor = color
    return color

def attach_reset():
    '''
    returns terminal color code reset, presumably to be 'attached' to a string
    '''

    return colorama.Style.RESET_ALL

def hilight(text):
    '''
    takes a string and highlights it on return
    '''

    return colorama.Style.BRIGHT+text+colorama.Style.NORMAL

def rainbow(txt):
    '''
    Takes a string and makes every letter a different color.
    '''

    rainbow = ""
    for letter in txt:
        rainbow += attach_rainbow() + letter

    rainbow += attach_reset()

    return rainbow

def pretty_time(time):
    '''
    human-friendly time formatter

    takes an integer number of seconds and returns a phrase that describes it,
    using the largest possible figure, rounded down (ie, time=604 returns '10
    minutes', not '10 minutes, 4 seconds' or '604 seconds')
    '''

    m, s = divmod(time, 60)
    if m > 0:
        h, m = divmod(m, 60)
        if h > 0:
            d, h = divmod(h, 24)
            if d > 0:
                w, d = divmod(d, 7)
                if w > 0:
                    mo, w = divmod(w, 4)
                    if mo > 0:
                        return p.no("month", mo)
                    else:
                        return p.no("week", w)
                else:
                    return p.no("day", d)
            else:
                return p.no("hour", h)
        else:
            return p.no("minute", m)
    else:
        return p.no("second", s)

def genID(digits=5):
    '''
    returns a string-friendly string of digits, which can start with 0
    '''

    id = ""
    x  = 0
    while x < digits:
        id += str(random.randint(0,9))
        x += 1

    return id

def print_menu(menu, rainbow=False):
    '''
    A pretty menu handler that takes an incoming lists of
    options and prints them nicely.

    Set rainbow=True for colorized menus.
    '''

    i = 0
    for x in menu:
        line = []
        if rainbow is not False:
            line.append(attach_rainbow())
        line.append("\t[ ")
        if i < 10:
            line.append(" ")
        line.append(str(i)+" ] "+x)
        line.append(attach_reset())
        print("".join(line))
        i += 1

def list_select(options, prompt):
    '''
    Given a list and query prompt, returns either False as an
    eject flag, or an integer index of the list Catches cancel
    option from list defined by BACKS; otherwise, retries on
    ValueError or IndexError.
    '''

    ans = ""
    invalid = True

    choice = input("\n"+prompt)

    if choice in BACKS:
        return False

    if choice in NAVS:
        return choice

    try:
        ans = int(choice)
    except ValueError:
        return list_select(options, prompt)

    try:
        options[ans]
    except IndexError:
        return list_select(options, prompt)

    return ans

def input_yn(query):
    '''
    Given a query, returns boolean True or False by processing y/n input
    '''

    try:
        ans = input(query+" [y/n] ")
    except KeyboardInterrupt:
        input_yn(query)

    while ans not in ["y", "n"]:
        ans = input("'y' or 'n' please: ")

    return ans == "y"

def parse_date(file):
    '''
    parses date out of pre-validated filename

    * assumes a filename of YYYYMMDD.txt
    * returns a list:
      [0] 'YYYY'
      [1] 'MM'
      [2] 'DD'
    '''

    rawdate = os.path.splitext(os.path.basename(file))[0]

    date = [rawdate[0:4], rawdate[4:6], rawdate[6:]]

    return date

