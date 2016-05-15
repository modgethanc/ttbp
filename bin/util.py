#!/usr/bin/python

import inflect
import time
import random
import colorama

colorama.init()

textcolors = [ colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.WHITE, colorama.Fore.CYAN]

lastcolor = colorama.Fore.RESET

p = inflect.engine()

def set_rainbow():
    global lastcolor

    color = lastcolor
    while color == lastcolor:
        color = random.choice(textcolors)

    lastcolor = color

    print(color)

def reset_color():
    print(colorama.Fore.RESET)

def attach_rainbow():
    global lastcolor

    color = lastcolor
    while color == lastcolor:
        color = random.choice(textcolors)

    lastcolor = color
    return color

def attach_reset():
    return colorama.Style.RESET_ALL

def hilight(text):
    return colorama.Style.BRIGHT+text+colorama.Style.NORMAL

def pretty_time(time):
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
    # makes a string of digits

    id = ""
    x  = 0
    while x < digits:
        id += str(random.randint(0,9))
        x += 1

    return id
