#!/usr/bin/python

import os
import random
import tempfile
import subprocess
import time
import json

import core
import chatter
import inflect

## system globals
SOURCE = os.path.join("/home", "endorphant", "projects", "ttbp", "bin")
LIVE = "http://tilde.town/~"
FEEDBACK = os.path.join("/home", "endorphant", "ttbp-mail")
USERFILE = os.path.join("/home", "endorphant", "projects", "ttbp", "users.txt")
p = inflect.engine()

## user globals
USER = os.path.basename(os.path.expanduser("~"))
PATH = os.path.join("/home", USER, ".ttbp")
PUBLIC = os.path.join("/home", USER, "public_html")
WWW = os.path.join(PATH, "www")
CONFIG = os.path.join(PATH, "config")
TTBPRC = os.path.join(CONFIG, "ttbprc")
DATA = os.path.join(PATH, "entries")
SETTINGS = {
        "editor": "none",
        "publish dir": False
    }

## ui globals
BANNER = open(os.path.join(SOURCE, "config", "banner.txt")).read()
SPACER = "\n\n\n"
INVALID = "please pick a number from the list of options!\n\n"
DUST = "sorry about the dust, but this part is still under construction. check back later!\n\n"
QUITS = ['exit', 'quit', 'q', 'x']
BACKS = ['back', 'b']
EJECT = "eject button fired! going home now."

## ref

EDITORS = ["vim", "vi", "emacs", "pico", "nano"]
SUBJECTS = ["help request", "bug report", "feature suggestion", "general comment"]

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
  print("if you don't want to be here at any point, press <ctrl-d> and it'll all go away.\njust keep in mind that you might lose anything you've started here.\n")
  print(check_init())
  redraw()

  try:
    print(main_menu())
  #except ValueError or SyntaxError:
  #  redraw("oh no i didn't understand that. let's go home and start over.")
  #  print(main_menu())
  except EOFError:
    print(stop())
  except KeyboardInterrupt:
    redraw(EJECT)
    print(main_menu())

def stop():
  return "\n\n\t"+chatter.say("bye")+"\n\n"

def check_init():
  global SETTINGS
  print("\n\n")
  if os.path.exists(os.path.join(os.path.expanduser("~"),".ttbp")):
      print(chatter.say("greet")+", "+USER+".")
      while not os.path.isfile(TTBPRC):
        setup_handler()
      try:
        SETTINGS = json.load(open(TTBPRC))
      except ValueError:
        setup_handler()

      raw_input("\n\npress <enter> to explore your feels.\n\n")
      core.load()
      return ""
  else:
    return init()

def init():
    try:
        raw_input("i don't recognize you, stranger. let's make friends.\n\npress <enter> to begin, or <ctrl-c> to get out of here. \n\n")
    except KeyboardInterrupt:
        print("\n\nthanks for checking in! i'll always be here.\n\n")
        quit()

    users = open(USERFILE, 'a')
    users.write(USER+"\n")
    users.close()
    subprocess.call(["mkdir", PATH])
    subprocess.call(["mkdir", CONFIG])
    subprocess.call(["mkdir", DATA])
    #subprocess.call(["cp", os.path.join(SOURCE, "config", "defaults", "header.txt"), CONFIG])
    header = gen_header()
    headerfile = open(os.path.join(CONFIG, "header.txt"), 'w')
    for line in header:
        headerfile.write(line)
    headerfile.close()
    subprocess.call(["cp", os.path.join(SOURCE, "config", "defaults", "footer.txt"), CONFIG])

    setup()
    subprocess.call(["cp", os.path.join(SOURCE, "config", "defaults", "style.css"), WWW])
    core.load()

    raw_input("\nyou're all good to go, "+chatter.say("friend")+"! hit <enter> to continue.\n\n")
    return ""

def gen_header():
    header = []

    header.append("<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 3.2//EN\">")
    header.append("\n<html>")
    header.append("\n\t<head>")
    header.append("\n\t\t<title>~"+USER+" on TTBP</title>")
    header.append("\n\t\t<link rel=\"stylesheet\" href=\"style.css\" />")
    header.append("\n\t</head>")
    header.append("\n\t<body>")
    header.append("\n\t\t<div id=\"meta\">")
    header.append("\n\t\t\t<h1><a href=\"index.html#\">~"+USER+"</a>@<a href=\"/~endorphant/ttbp\">TTBP</a></h1>")
    header.append("\n\t\t</div>\n")
    header.append("\n\t\t<!---put your custom html here-->\n\n\n\n")
    header.append("\n\t\t<!---don't put anything after this line-->\n")
    header.append("\n\t\t<div id=\"tlogs\">\n")
    return header

def setup_handler():
    print("\nyour ttbp configuration doesn't look right. let's make you a fresh copy.\n\n")
    try:
        setup()
    except KeyboardInterrupt:
        print("\n\nsorry, trying again.\n\n")
        setup()

def setup():
    global SETTINGS

    # editor selection
    print_menu(EDITORS)
    choice = raw_input("\npick your favorite text editor: ")
    while choice  not in ['0', '1', '2', '3', '4']:
        choice = raw_input("\nplease pick a number from the list: ")

    SETTINGS["editor"] = EDITORS[int(choice)]
    redraw("text editor set to: "+SETTINGS["editor"])

    # publish directory selection
    if SETTINGS["publish dir"]:
        print("\tcurrent publish dir:\t"+os.path.join(PUBLIC, SETTINGS["publish dir"])+"\n\n")
    choice = raw_input("\nwhere do you want your blog published? (leave blank to use default \"blog\") ")
    if not choice:
        choice = "blog"

    publishing = os.path.join(PUBLIC, choice)
    while os.path.exists(publishing):
        second = raw_input("\n"+publishing+" already exists!\nif you're sure you want to use it, hit <enter> to confirm. otherwise, pick another location: ")
        if second == "":
            break
        choice = second
        publishing = os.path.join(PUBLIC, choice)

    SETTINGS["publish dir"] = choice

    # set up publish directory
    if not os.path.exists(publishing):
        subprocess.call(["mkdir", publishing])
        subprocess.call(["touch", os.path.join(publishing, "index.html")])
        index = open(os.path.join(publishing, "index.html"), "w")
        index.write("<h1>ttbp blog placeholder</h1>")
        index.close()
    if os.path.exists(WWW):
        subprocess.call(["rm", WWW])
    subprocess.call(["ln", "-s", publishing, WWW])
    print("\n\tpublishing to "+LIVE+USER+"/"+SETTINGS["publish dir"]+"/\n\n")

    # save settings
    ttbprc = open(TTBPRC, "w")
    ttbprc.write(json.dumps(SETTINGS, sort_keys=True, indent=2, separators=(',',':')))
    ttbprc.close()

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
            "record your feels",
            "review your feels",
            "check out your neighbors",
            "browse global feels",
            "change your settings",
            "send some feedback",
            "(wip) see credits"]
    #print(SPACER)
    print("you're at ttbp home. remember, you can always press <ctrl-c> to come back here.\n\n")
    print_menu(menuOptions)
    #print("how are you feeling today? ")

    #try:
    #    choice = raw_input("\ntell me about your feels (or 'quit' to exit): ")
    #except KeyboardInterrupt:
    #    redraw(EJECT)
    #    return main_menu()
    try:
        choice = raw_input("\ntell me about your feels (or 'quit' to exit): ")
    except KeyboardInterrupt:
        redraw(EJECT)
        return main_menu()

    if choice == '0':
        redraw()
        today = time.strftime("%Y%m%d")
        write_entry(os.path.join(DATA, today+".txt"))
    elif choice == '1':
        redraw("here are your recorded feels, listed by date:\n\n")
        view_own()
    elif choice == '2':
        users = find_ttbps()
        redraw("the following "+p.no("user", len(users))+" "+p.plural("is", len(users))+" recording feels on ttbp, listed by most recently updated first:\n\n")
        view_neighbors(users)
    elif choice == '3':
        redraw("now viewing most recent entries\n\n")
        view_feed()
    elif choice == '4':
        pretty_settings = "\n\ttext editor:\t" +SETTINGS["editor"]
        pretty_settings += "\n\tpublish dir:\t" +os.path.join(PUBLIC, SETTINGS["publish dir"])

        redraw("now changing your settings. press <ctrl-c> if you didn't mean to do this.\n\ncurrent settings "+pretty_settings+"\n")
        try:
            setup()
        except KeyboardInterrupt():
            redraw(EJECT)
        raw_input("\nyou're all good to go, "+chatter.say("friend")+"! hit <enter> to continue.\n\n")
        redraw()
    elif choice == '5':
        redraw()
        feedback_menu()
    elif choice == '6':
        redraw(DUST)
    elif choice in QUITS:
        return stop()
    else:
        redraw(INVALID)

    return main_menu()

def feedback_menu():
    print("you're about to send mail to ~endorphant about ttbp\n\n")

    print_menu(SUBJECTS)
    choice = raw_input("\npick a category for your feedback: ")

    cat = ""
    if choice in ['0', '1', '2', '3']:
        cat = SUBJECTS[int(choice)]
        raw_input("\ncomposing a "+cat+" to ~endorphant.\n\npress <enter> to open an external text editor. mail will be sent once you save and quit.\n")
        redraw(send_feedback(cat))
        return
    else:
        redraw(INVALID)

    return feedback_menu()

## handlers

def write_entry(entry=os.path.join(DATA, "test.txt")):

    entered = raw_input("\nfeels will be recorded for today, "+time.strftime("%d %B %Y")+".\n\nif you've already started recording feels for this day, you \ncan pick up where you left off.\n\npress <enter> to begin recording your feels.\n\n")
    if entered:
        entryFile = open(entry, "a")
        entryFile.write("\n"+entered+"\n")
        entryFile.close()
    subprocess.call([SETTINGS["editor"], entry])
    core.load_files()
    core.write("index.html")
    redraw("posted to "+LIVE+USER+"/"+SETTINGS["publish dir"]+"/index.html\n\nthanks for sharing your feels!")
    return

def send_feedback(subject="none", mailbox=os.path.join(FEEDBACK, USER+"-"+time.strftime("%Y%m%d-%H%M")+".msg")):

    mail = ""

    temp = tempfile.NamedTemporaryFile()
    subprocess.call([SETTINGS["editor"], temp.name])
    mail = open(temp.name, 'r').read()

    outfile = open(mailbox, 'w')
    outfile.write("from:\t\t~"+USER+"\n")
    outfile.write("subject:\t"+subject+"\n")
    outfile.write("date:\t"+time.strftime("%d %B %y")+"\n")
    outfile.write(mail)
    outfile.close()

    return "mail sent. thanks for writing! i'll try to respond to you soon."

def view_neighbors(users):

    userList = []

    for user in users:
        userRC = json.load(open(os.path.join("/home", user, ".ttbp", "config", "ttbprc")))
        url = LIVE+user+"/"+userRC["publish dir"]
        count = 0
        lastfile = ""
        files = os.listdir(os.path.join("/home", user, ".ttbp", "entries"))
        files.sort()
        #for filename in os.listdir(os.path.join("/home", user, ".ttbp", "entries")).sort():
        for filename in files:
            if os.path.splitext(filename)[1] == ".txt" and len(os.path.splitext(filename)[0]) == 8:
                count += 1
                lastfile = os.path.join("/home", user, ".ttbp", "entries", filename)

        date = ""
        if lastfile:
            last = os.path.getctime(lastfile)
            date = time.strftime("%Y%m%d %H%M", time.localtime(last))
        else:
            last = 0

        pad = ""
        if len(user) < 8:
            pad = "\t"
        user = "~"+user
        if len(user) < 8:
            user += "\t"

        userList.append(["\t"+user+"\t"+url+pad+"\t("+p.no("feel", count)+")", last])
        #userList.append(["\t"+user+"\t"+url+pad+"\t("+p.no("feel", count)+") "+date, last])

    # sort user by most recent entry
    userList.sort(key = lambda userdata:userdata[1])
    userList.reverse()
    sortedUsers = []
    for user in userList:
        sortedUsers.append(user[0])

    print_menu(sortedUsers)

    raw_input("\n\npress <enter> to go back home.\n\n")
    redraw()

    return

def view_own():

    filenames = []

    for entry in os.listdir(DATA):
        filenames.append(os.path.join(DATA, entry))
    metas = core.meta(filenames)

    entries = []
    for entry in metas:
        #print(entry)
        entries.append(""+entry[4]+" ("+p.no("word", entry[2])+") ")


    #view_entries(metas, entries, "here are your recorded feels, listed by date: \n\n")
    return view_entries(metas, entries, "here are your recorded feels, listed by date: \n\n")

def view_entries(metas, entries, prompt):

    print_menu(entries)

    choice = list_select(entries, "pick an entry from the list, or type 'back' to go home: ")

    if choice is not False:

        redraw("now reading ~"+metas[choice][5]+"'s feels on "+metas[choice][4]+"\n> press <q> to return to feels list.\n\n")

        show_entry(metas[choice][0])
        #redraw("here are your recorded feels, listed by date:\n\n")
        redraw(prompt)

        return view_entries(metas, entries, prompt)

    else:
        redraw()
        return

def show_entry(filename):

    subprocess.call(["less", filename])

    return

def view_feed():

    feedList = []

    for townie in find_ttbps():
        entryDir = os.path.join("/home", townie, ".ttbp", "entries")
        filenames = os.listdir(entryDir)
        for entry in filenames:
            ### REALLY MAKE A REAL FILENAME VALIDATOR
            fileSplit = os.path.splitext(entry)
            if len(fileSplit[0]) == 8 and fileSplit[1] == ".txt":
                feedList.append(os.path.join(entryDir, entry))

    metas = core.meta(feedList)
    metas.sort(key = lambda entry:entry[3])
    metas.reverse()

    entries = []
    for entry in metas[0:10]:
        pad = ""
        if len(entry[5]) < 8:
            pad = "\t"

        entries.append("~"+entry[5]+pad+"\ton "+entry[3]+" ("+p.no("word", entry[2])+") ")

    #print_menu(entries)
    view_entries(metas, entries, "most recent ten entries: \n\n")

    redraw()

    return
#####

def find_ttbps():
    # looks for users with a valid ttbp config and returns a list of them
    users = []

    for townie in os.listdir("/home"):
        if os.path.exists(os.path.join("/home", townie, ".ttbp", "config", "ttbprc")):
            users.append(townie)

    return users

def list_select(options, prompt):
    # runs the prompt for the list until a valid index is imputted

    ans = ""
    invalid = True

    while invalid:
        #try:
        #    choice = raw_input("\n\n"+prompt)
        #except KeyboardInterrupt:
        #    redraw()
        #    main_menu()

        choice = raw_input("\n\n"+prompt)
        if choice in BACKS:
            return False

        try:
            ans = int(choice)
        except ValueError:
            choice = raw_input("\n\n"+prompt+"\n\n")

        invalid = False

    if ans >= len(options):
        return list_select(options, prompt)

    return ans

#####

start()
