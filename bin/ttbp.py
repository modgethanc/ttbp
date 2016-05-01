#!/usr/bin/python

import os
import random
import tempfile
import subprocess
import time

#import core
import chatter

## system globals
SOURCE = os.path.join("/home", "endorphant", "projects", "ttbp", "bin")
LIVE = "http://tilde.town/~"
FEEDBACK = os.path.join("/home", "endorphant", "ttbp-mail")

## user globals
USER = os.path.basename(os.path.expanduser("~"))
PATH = os.path.join("/home", USER, ".ttbp")
WWW = os.path.join(PATH, "www")
CONFIG = os.path.join(PATH, "config")
DATA = os.path.join(PATH, "entries")
SETTINGS = {
        "editor":"vim",
        "publish dir":"blog"
    }

## ui globals
BANNER = open(os.path.join(SOURCE, "config", "banner.txt")).read()
SPACER = "\n\n\n"
INVALID = "please pick a number from the list of options!\n\n"
DUST = "sorry about the dust, but this part is still under construction. check back later!\n\n"

## ref

EDITORS = ["vim", "vi", "emacs", "pico", "nano"]
SUBJECTS = ["bug report", "feature suggestion", "general comment"]

##

def redraw(leftover=""):
    os.system("clear")
    print(BANNER)
    print(SPACER)
    if leftover:
        print("> "+leftover+"\n")

def start():
  redraw()
  #print(chatter.say("greet")+", "+chatter.say("friend"))
  #print("(remember, you can always press ctrl-c to come home)\n")
  print("if you don't want to be here at any point, press ctrl-d and it'll all go away.\njust keep in mind that you might lose anything you've started here.\n")
  print(check_init())

  try:
    redraw()
    print(main_menu())
  except ValueError or SyntaxError:
    redraw("oh no i didn't understand that. let's go home and start over.")
    print(main_menu())
  except KeyboardInterrupt:
    redraw("eject button fired! going home now.")
    print(main_menu())

def stop():
  return "\n\t"+chatter.say("bye")

def check_init():
  if os.path.exists(os.path.join(os.path.expanduser("~"),".ttbp")):
      print("welcome back, "+USER+".")
      if not os.path.isfile(os.path.join(CONFIG, "ttbprc")):
          print("\nyour ttbp configuration doesn't look right. let's make you a fresh copy.\n\n")
          try:
              setup()
          except KeyboardInterrupt:
              print("\n\nsorry, trying again.\n\n")
              setup()
      raw_input("\n\npress enter to explore your feelings.\n\n")
      return ""
  else:
    return init()

def init():
    raw_input("i don't recognize you, stranger. let's make friends someday.\n\npress enter to explore some options.\n\n")
    return ""

def setup():
    global SETTINGS

    # editor selection
    print_menu(EDITORS)
    choice = raw_input("\npick your favorite text editor: ")
    while choice  not in ['0', '1', '2', '3', '4']:
        choice = raw_input("\nplease pick a number from the list: ")

    SETTINGS["editor"] = EDITORS[int(choice)]
    print("\ntext editor set to >"+SETTINGS["editor"])

    # publish directory selection
    choice = raw_input("\n\nwhere do you want your blog published? (leave blank to use default \"blog\") ")
    if not choice:
        choice = "blog"

    publishing = os.path.join("/home", USER, "public_html", choice)
    while os.path.exists(publishing):
        second = raw_input("\n"+publishing+" already exists!\nif you're sure you want to use it, hit <enter> to confirm. otherwise, pick another location: ")
        if second == "":
            break
        choice = second
        publishing = os.path.join("/home", USER, "public_html", choice)

    SETTINGS["publish dir"] = choice
    
    # set up publish directory
    if not os.path.exists(publishing):
        subprocess.call(["mkdir", publishing])
        subprocess.call(["touch", os.path.join(publishing, "index.html")])
        index = open(os.path.join(publishing, "index.html"), "w")
        index.write("<h1>ttbp blog placeholder</h1>")
        index.close()
    subprocess.call(["rm", WWW])
    subprocess.call(["ln", "-s", publishing, WWW])
    print("\npublishing to "+LIVE+USER+"/"+SETTINGS["publish dir"]+"/\n\n")

    return SETTINGS

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
    #os.system("clear")
    #print(BANNER)
    #redraw()
    menuOptions = [
            "record feelings", 
            "check out neighbors",
            "change settings",
            "send feedback",
            "see credits"]
    #print(SPACER)
    print("you're at ttbp home now. remember, you can always press ctrl-c to come back here.\n\n")
    print_menu(menuOptions)
    #print("how are you feeling today? ")

    try:
        choice = raw_input("\ntell me about your feels (enter 'none' to quit): ")
    except KeyboardInterrupt:
        redraw("eject button fired! going home now.")
        return main_menu()

    if choice == '0':
        redraw(DUST)
    elif choice == '1':
        redraw(DUST)
    elif choice == '2':
        redraw(DUST)
    elif choice == '3':
        redraw()
        feedback_menu()
    elif choice == '4':
        redraw(DUST)
    elif choice == "none":
        return stop()
    else:
        redraw(INVALID)

    return main_menu()

def feedback_menu():
    print("you're about to send mail to ~endorphant about ttbp\n\n")

    print_menu(SUBJECTS)
    choice = raw_input("\npick a category for your feedback: ")

    cat = ""
    if choice in ['0', '1', '2']:
        cat = SUBJECTS[int(choice)]
        raw_input("\ncomposing a "+cat+" to ~endorphant.\n\npress enter to open an external text editor. mail will be sent once you save and quit.\n")
        redraw(send_feedback(cat))
        return
    else:
        redraw(INVALID)

    return feedback_menu()

## handlers

def write_entry(entry=os.path.join(DATA, "test.txt")):

    subprocess.call([SETTINGS["editor"], entry])
    return "wrote to "+entry

def send_feedback(subject="none", mailbox=os.path.join(FEEDBACK, USER+"-"+str(int(time.time()))+".msg")):

    mail = ""

    temp = tempfile.NamedTemporaryFile()
    subprocess.call([SETTINGS["editor"], temp.name])
    mail = open(temp.name, 'r').read()

    outfile = open(mailbox, 'w')
    outfile.write("from:\t\t~"+USER+"\n")
    outfile.write("subject:\t"+subject+"\n\n")
    outfile.write(mail)
    outfile.close()

    return "mail sent. thanks for writing! i'll try to respond to you soon."

#####

start()
