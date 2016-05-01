#!/usr/bin/python

#import core

import os
import random
import tempfile
import subprocess
import time

import core
import chatter

SOURCE = os.path.join("/home", "endorphant", "projects", "ttbp", "bin")
USER = os.path.basename(os.path.expanduser("~"))
PATH = os.path.join("/home", USER, ".ttbp")

LIVE = "http://tilde.town/~"
WWW = os.path.join(PATH, "www")
CONFIG = os.path.join(PATH, "config")
DATA = os.path.join(PATH, "entries")

FEEDBACK = os.path.join("/home", "endorphant", "ttbp-mail")
BANNER = open(os.path.join(SOURCE, "banner.txt")).read()
#CLOSER = "\n\tsee you later, space cowboy..."

SPACER = "\n\n\n"
INVALID = "\n\nplease pick a number from the list of options!\n\n"
DUST = "\n\nsorry about the dust, but this part is still under construction. check back later!\n\n"

def start():
  os.system("clear")
  print(BANNER)
  #print(chatter.say("greet")+", "+chatter.say("friend"))
  #print("(remember, you can always press ctrl-c to come home)\n")
  print("if you don't want to be here at any point, press ctrl-d and it'll all go away.\njust keep in mind that you might lose anything you've started here.\n")
  print(check_init())

  try:
    print(main_menu())
  except ValueError or SyntaxError:
    print("\n\noh no i didn't understand that")
    print(main_menu())
  except KeyboardInterrupt:
    print("\n\neject button fired")
    print(main_menu())

def stop():
  return "\n\t"+chatter.say("bye")

def check_init():
  if os.path.exists(os.path.join(os.path.expanduser("~"),".ttbp")):
      raw_input("welcome back, "+USER+".\n\npress enter to explore your feelings.")
      return ""
  else:
    return init()

def init():
    raw_input("i don't recognize you, stranger. let's make friends someday.\n\npress enter to explore some options.")
    return ""

## menus

def print_menu(menu):
    i = 0
    for x in menu:
        line = []
        line.append("\t[ ")
        if i < 10:
            line.append(" ")
        line.append(str(i)+" ] "+x)
        print("".join(line))
        i += 1

def main_menu():
    os.system("clear")
    print(BANNER)
    menuOptions = ["record feelings", "check out neighbors","send feedback"]
    print(SPACER)
    print("you're at ttbp home now. remember, you can always press ctrl-c to come back here.\n\n")
    print_menu(menuOptions)
    #print("how are you feeling today? ")

    choice = raw_input("\ntell me about your feels (enter 'none' to quit): ")

    if choice == '0':
        print(DUST)
    elif choice == '1':
        print(DUST)
    elif choice == '2':
        print(feedback_menu())
    elif choice == "none":
        return stop()
    else:
        print(INVALID)

    return main_menu()

def feedback_menu():
    print("sends mail to ~endorphant about ttbp\n\n")
    menuOptions = ["bug report", "feature suggestion", "general feedback"]

    print(SPACER)
    print_menu(menuOptions)
    choice = raw_input("\npick a category for your feedback: ")

    cat = ""
    if choice in ['0', '1', '2']:
        cat = menuOptions[int(choice)]
        return send_feedback(cat)
    else:
        print(INVALID)

    return feedback_menu()

## handlers

def write_entry(entry=os.path.join(DATA, "test.txt")):

    subprocess.call(["vim", entry])
    return "wrote to "+entry

def send_feedback(subject="none", mailbox=os.path.join(FEEDBACK, USER+"-"+str(int(time.time()))+".msg")):

    mail = ""

    temp = tempfile.NamedTemporaryFile()
    subprocess.call(['vim', temp.name])
    mail = open(temp.name, 'r').read()

    outfile = open(mailbox, 'w')
    outfile.write("from:\t\t~"+USER+"\n")
    outfile.write("subject:\t"+subject+"\n\n")
    outfile.write(mail)
    outfile.close()

    return "mail sent. thanks for writing! i'll try to respond to you soon."

#####

start()
