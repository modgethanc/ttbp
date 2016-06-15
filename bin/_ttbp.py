#!/usr/bin/python

'''
ttbp: tilde town blogging platform
(also known as the feels engine)
a console-based blogging program developed for tilde.town
copyright (c) 2016 ~endorphant (endorphant@tilde.town)

_ttbp.py:
the beta version of the main console interface

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

the complete codebase is available at:
https://github.com/modgethanc/ttbp
'''

import os
import random
import tempfile
import subprocess
import time
import json
from email.mime.text import MIMEText;

import core
import chatter
import inflect
import util

__version__ = "0.9.1b"
__author__ = "endorphant <endorphant@tilde.town)"

## system globals
SOURCE = os.path.join("/home", "endorphant", "projects", "ttbp", "bin")
LIVE = "https://tilde.town/~"
FEEDBACK = os.path.join("/home", "endorphant", "ttbp-mail")
FEEDBOX = "endorphant@tilde.town"
USERFILE = os.path.join("/home", "endorphant", "projects", "ttbp", "users.txt")
GRAFF_DIR = os.path.join(SOURCE, "graffiti")
WALL = os.path.join(GRAFF_DIR, "wall.txt")
WALL_LOCK = os.path.join(GRAFF_DIR, ".lock")

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
BANNER = util.attach_rainbow()+open(os.path.join(SOURCE, "config", "banner-beta.txt")).read()+util.rainbow("\t~potentially volatile beta version~")+util.attach_reset()
SPACER = "\n"
INVALID = "please pick a number from the list of options!"
DUST = "sorry about the dust, but this part is still under construction. check back later!"
QUITS = ['exit', 'quit', 'q', 'x']
EJECT = "eject button fired! going home now."
RAINBOW = True

## ref

EDITORS = ["vim", "vi", "emacs", "pico", "nano", "ed"]
SUBJECTS = ["help request", "bug report", "feature suggestion", "general comment"]

##

def redraw(leftover=""):
    '''
    screen clearing

    * clears the screen and reprints the banner, plus whatever leftover text to be hilights
    '''

    os.system("clear")
    print(BANNER)
    print("\t\ttoday is "+ time.strftime("%d %B %Y"))
    print(SPACER)
    if leftover:
        print("> "+leftover+"\n")

def start():
    '''
    main engine head

    * called on program start
    * calls config check
    * proceeds to main menu
    * handles ^c and ^d ejects
    '''

    redraw()
    print("""
if you don't want to be here at any point, press <ctrl-d> and it'll all go away.
just keep in mind that you might lose anything you've started here.\
""")

    try:
        print(check_init())
    except EOFError:
        print(stop())
        return

    ##
    redraw()

    while 1:
        try:
            print(main_menu())
        except EOFError:
            print(stop())
            break
        except KeyboardInterrupt:
            redraw(EJECT)
        else:
            break

def stop():
    '''
    closer

    * prints ending text
    '''

    return "\n\n\t"+chatter.say("bye")+"\n\n"

def check_init():
    '''
    user handler

    * checks for presence of ttbprc
    * checks for last run version
    '''

    global SETTINGS

    print("\n\n")
    if os.path.exists(os.path.join(os.path.expanduser("~"),".ttbp")):
        print(chatter.say("greet")+", "+USER+".\n")

        '''
        ## ttbprc validation
        while not os.path.isfile(TTBPRC):
            setup_repair()
        try:
            SETTINGS = json.load(open(TTBPRC))
        except ValueError:
            setup_repair()
        '''

        ## ttbp env validation
        if not valid_setup():
            setup_repair()

        ## version checker
        mismatch = build_mismatch()
        if mismatch is not False:
            switch_build(mismatch)
        if not updated():
            update_version()

        ## when ready, enter main program and load core engine
        raw_input("press <enter> to explore your feels.\n\n")
        core.load(SETTINGS)

        return ""
    else:
        return init()

def init():
    '''
    new user creation

    * introduces user
    * calls setup functinos
    '''

    try:
        raw_input("""
i don't recognize you, stranger. let's make friends.

press <enter> to begin, or <ctrl-c> to get out of here.
        """)
    except KeyboardInterrupt:
        print("\n\nthanks for checking in! i'll always be here.\n\n")
        quit()

    ## record user in source list
    users = open(USERFILE, 'a')
    users.write(USER+"\n")
    users.close()

    ## make .ttbp directory structure
    subprocess.call(["mkdir", PATH])
    subprocess.call(["mkdir", CONFIG])
    subprocess.call(["mkdir", DATA])

    ## create header file
    header = gen_header()
    headerfile = open(os.path.join(CONFIG, "header.txt"), 'w')
    for line in header:
        headerfile.write(line)
    headerfile.close()

    ## copy footer and default stylesheet
    subprocess.call(["cp", os.path.join(SOURCE, "config", "defaults", "footer.txt"), CONFIG])
    subprocess.call(["cp", os.path.join(SOURCE, "config", "defaults", "style.css"), CONFIG])

    ## run user-interactive setup and load core engine
    setup()
    core.load(SETTINGS)

    raw_input("\nyou're all good to go, "+chatter.say("friend")+"! hit <enter> to continue.\n\n")
    return ""

def gen_header():
    '''
    header generator

    builds header to insert username
    '''

    header ="""
<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 3.2//EN\">
<html>
    <head>
        <!--- this header automatically generated by ttbp initialization on """+time.strftime("%Y-%m-%d %h:m")+""" --->
        <title>~"""+USER+""" on TTBP</title>
        <link rel=\"stylesheet\" href=\"style.css\" />
    </head>
    <body>
        <div id=\"meta\">
            <h1><a href=\"index.html#\">~"""+USER+"""</a>@<a href=\"/~endorphant/ttbp\">TTBP</a></h1>
        </div>

        <!---put your custom html here-->



        <!---don't put anything after this line-->
        <div id=\"tlogs\">\
    """
    return header

def valid_setup():
    '''
    Checks to see if user has a sane ttbp environment.
    '''

    global SETTINGS

    if not os.path.isfile(TTBPRC):
        return False

    try:
        SETTINGS = json.load(open(TTBPRC))
    except ValueError:
        return False

    if core.publishing():
        if not SETTINGS.get("publish dir"):
            return False

        if not os.path.exists(WWW):
            return False

        if not os.path.exists(os.path.join(WWW, SETTINGS.get("pubish dir"))):
            return False

    return True

def setup_repair():
    '''
    setup repair function

    * calls setup()
    * handles ^c
    '''

    print("\nyour ttbp configuration doesn't look right. let's make you a fresh copy.\n\n")
    try:
        setup()
    except KeyboardInterrupt:
        print("\n\nsorry, trying again.\n\n")
        setup()

def setup():
    '''
    master setup function

    * editor selection
    * publishing toggle
    * publish/unpublish as needed
    * directory selection

    TODO: break this out better?
    '''

    global SETTINGS

    print("\n\ttext editor:\t" +SETTINGS.get("editor"))
    if core.publishing():
        print("\tpublish dir:\t" +os.path.join(PUBLIC, str(SETTINGS.get("publish dir"))))
    print("\tpubishing:\t"+str(SETTINGS.get("publishing"))+"\n")

    # editor selection
    SETTINGS.update({"editor": select_editor()})
    redraw("text editor set to: "+SETTINGS["editor"])

    # publishing selection
    SETTINGS.update({"publishing":select_publishing()})
    core.reload_ttbprc(SETTINGS)
    update_publishing()
    redraw("blog publishing: "+str(core.publishing()))

    if core.publishing():
        print("publish directory: ~"+USER+"/public_html/"+SETTINGS.get("publish dir"))

    # save settings
    ttbprc = open(TTBPRC, "w")
    ttbprc.write(json.dumps(SETTINGS, sort_keys=True, indent=2, separators=(',',':')))
    ttbprc.close()

    raw_input("\nyou're all good to go, "+chatter.say("friend")+"! hit <enter> to continue.\n\n")
    redraw()

    return SETTINGS

## menus

def main_menu():
    '''
    main navigation menu
    '''

    menuOptions = [
            "record your feels",
            "review your feels",
            "check out your neighbors",
            "browse global feels",
            "scribble some graffiti\t(new!)",
            "change your settings",
            "send some feedback",
            "see credits",
            "read documentation"]

    print("you're at ttbp home. remember, you can always press <ctrl-c> to come back here.\n")
    util.print_menu(menuOptions, RAINBOW)

    try:
        choice = raw_input("\ntell me about your feels (or 'quit' to exit): ")
    except KeyboardInterrupt:
        redraw(EJECT)
        return main_menu()

    if choice == '0':
        redraw()
        today = time.strftime("%Y%m%d")
        write_entry(os.path.join(DATA, today+".txt"))
        core.www_neighbors()
    elif choice == '1':
        if core.publishing():
            intro = "here are some options for reviewing your feels:"
            redraw(intro)
            review_menu(intro)
            core.load_files()
            core.write("index.html")
        else:
            redraw("your recorded feels, listed by date:")
            view_feels(USER)
    elif choice == '2':
        users = core.find_ttbps()
        redraw("the following "+p.no("user", len(users))+" "+p.plural("is", len(users))+" recording feels on ttbp:")
        view_neighbors(users)
    elif choice == '3':
        redraw("most recent global entries")
        view_feed()
    elif choice == '4':
        graffiti_handler()
    elif choice == '5':
        redraw("now changing your settings. press <ctrl-c> if you didn't mean to do this.")
        try:
            core.load(setup()) # reload settings to core
        except KeyboardInterrupt():
            redraw(EJECT)
        redraw()
    elif choice == '6':
        redraw("you're about to send mail to ~endorphant about ttbp")
        feedback_menu()
    elif choice == '7':
        redraw()
        show_credits()
    elif choice == '8':
        subprocess.call(["lynx", os.path.join(SOURCE, "..", "README.html")])
        redraw()
    elif choice in QUITS:
        return stop()
    else:
        redraw(INVALID)

    return main_menu()

def feedback_menu():
    '''
    feedback handling menu

    * selects feedback type
    * calls feedback writing function
    '''

    util.print_menu(SUBJECTS, RAINBOW)
    choice = raw_input("\npick a category for your feedback: ")

    cat = ""
    if choice in ['0', '1', '2', '3']:
        cat = SUBJECTS[int(choice)]
        entered = raw_input("""
composing a """+cat+""" to ~endorphant.

press <enter> to open an external text editor. mail will be sent once you save and quit.

""")
        redraw(send_feedback(entered, cat))
        return
    else:
        redraw(INVALID)

    return feedback_menu()

def review_menu(intro=""):
    '''
    submenu for reviewing feels.
    '''

    menuOptions = [
            "read over feels",
            "modify feels publishing"
            ]

    util.print_menu(menuOptions, RAINBOW)

    choice = util.list_select(menuOptions, "what would you like to do with your feels? (or 'back' to return home) ")

    if choice is not False:
        if choice == 0:
            redraw("your recorded feels, listed by date:")
            view_feels(USER)
        elif choice == 1:
            redraw("here's your current nopub status:")
            set_nopubs()
    else:
        redraw()
        return

    redraw(intro)
    return review_menu()


def view_neighbors(users):
    '''
    generates list of all users on ttbp, sorted by most recent post

    * if user is publishing, list publish directory
    '''

    userList = []

    ## assumes list of users passed in all have valid config files
    for user in users:
        userRC = json.load(open(os.path.join("/home", user, ".ttbp", "config", "ttbprc")))

        ## retrieve publishing url, if it exists
        url="\t\t\t"
        if userRC.get("publish dir"):
            url = LIVE+user+"/"+userRC.get("publish dir")

        ## find last entry
        files = os.listdir(os.path.join("/home", user, ".ttbp", "entries"))
        files.sort()
        lastfile = ""
        for filename in files:
            if core.valid(filename):
                lastfile = os.path.join("/home", user, ".ttbp", "entries", filename)

        ## generate human-friendly timestamp
        ago = "never"
        if lastfile:
            last = os.path.getctime(lastfile)
            since = time.time()-last
            ago = util.pretty_time(int(since)) + " ago"
        else:
            last = 0

        ## some formatting handwavin
        urlpad = ""
        if ago == "never":
            urlpad = "\t"

        userpad = ""
        if len(user) < 7:
            userpad = "\t"

        userList.append(["\t~"+user+userpad+"\t("+ago+")"+urlpad+"\t"+url, last, user])

    # sort user by most recent entry for display
    userList.sort(key = lambda userdata:userdata[1])
    userList.reverse()
    sortedUsers = []
    userIndex = []
    for user in userList:
        sortedUsers.append(user[0])
        userIndex.append(user[2])

    util.print_menu(sortedUsers, RAINBOW)

    #raw_input("\n\npress <enter> to go back home.\n\n")
    choice = util.list_select(sortedUsers, "pick a townie to browse their feels, or type 'back' to go home: ")

    if choice is not False:
        redraw("~"+userIndex[choice]+"'s recorded feels, listed by date: \n")
        view_feels(userIndex[choice])
        view_neighbors(users)
    else:
        redraw()
        return

def view_feels(townie):
    '''
    generates a list of all feels by given townie and displays in
    date order

    * calls list_entries() to select feel to read
    '''

    filenames = []
    showpub = False

    if townie == USER:
        entryDir = DATA
        owner = "your"
        if core.publishing():
            showpub = True
    else:
        owner = "~"+townie+"'s"
        entryDir = os.path.join("/home", townie, ".ttbp", "entries")

    for entry in os.listdir(entryDir):
        filenames.append(os.path.join(entryDir, entry))
    metas = core.meta(filenames)

    if len(filenames) > 0:
        entries = []
        for entry in metas:
            pub = ""
            if core.nopub(entry[0]):
                pub = "(nopub)"
            entries.append(""+entry[4]+" ("+p.no("word", entry[2])+") "+"\t"+pub)

        return list_entries(metas, entries, owner+" recorded feels, listed by date: \n")
    else:
        redraw("no feels recorded by ~"+townie)

def show_credits():
    '''
    prints author acknowledgements and commentary
    '''

    print("""
ttbp was written by ~endorphant in python. the codebase is
publicly available on github at https://github.com/modgethanc/ttbp

for the full changelog, see ~endorphant/projects/ttbp/changelog.txt

if you have ideas for ttbp, you are welcome to fork the repo and
work on it. i'm only a neophyte dev, so i apologize for any
bad style and practices of mine; i'm always open to suggestions for
improvement.

i'd love to hear about your ideas and brainstorm about new features!

thanks to everyone who reads, listens, writes, and feels.\
        """)

    raw_input("\n\npress <enter> to go back home.\n\n")
    redraw()

    return

## handlers

def write_entry(entry=os.path.join(DATA, "test.txt")):
    '''
    main feels-recording handler
    '''

    entered = raw_input("""
feels will be recorded for today, """+time.strftime("%d %B %Y")+""".

if you've already started recording feels for this day, you
can pick up where you left off.

you can write your feels in plaintext, markdown, html, or a mixture of
these.

press <enter> to begin recording your feels in your chosen text
editor.

""")

    if entered:
        entryFile = open(entry, "a")
        entryFile.write("\n"+entered+"\n")
        entryFile.close()
    subprocess.call([SETTINGS.get("editor"), entry])

    left = ""

    if core.publishing():
        core.load_files()
        core.write("index.html")
        left = "posted to "+LIVE+USER+"/"+str(SETTINGS.get("publish dir"))+"/index.html\n\n>"
    redraw(left + " thanks for sharing your feels!")

    return

def set_nopubs():
    '''
    handler for toggling nopub on individual entries
    '''

    raw_input(DUST)

def send_feedback(entered, subject="none"):
    '''
    main feedback/bug report handler
    '''

    message = ""

    temp = tempfile.NamedTemporaryFile()
    if entered:
        msgFile = open(temp.name, "a")
        msgFile.write(entered+"\n")
        msgFile.close()
    subprocess.call([SETTINGS["editor"], temp.name])
    message = open(temp.name, 'r').read()

    if message:
        id = "#"+util.genID(3)
        mail = MIMEText(message)
        mail['To'] = FEEDBOX
        mail['From'] = USER+"@tilde.town"
        mail['Subject'] = " ".join(["[ttbp]", subject, id])
        m = os.popen("/usr/sbin/sendmail -t -oi", 'w')
        m.write(mail.as_string())
        m.close()

        exit = """\
thanks for writing! for your reference, it's been recorded
> as """+ " ".join([subject, id])+""". i'll try to respond to you soon.\
        """
    else:
        exit = """\
i didn't send your blank message. if you made a mistake, please try
running through the feedback option again!\
        """

    return exit

def list_entries(metas, entries, prompt):
    '''
    displays a list of entries for reading selection
    '''

    util.print_menu(entries, RAINBOW)

    choice = util.list_select(entries, "pick an entry from the list, or type 'back' to go back: ")

    if choice is not False:

        redraw("now reading ~"+metas[choice][5]+"'s feels on "+metas[choice][4]+"\n> press <q> to return to feels list.\n\n")

        show_entry(metas[choice][0])
        redraw(prompt)

        return list_entries(metas, entries, prompt)

    else:
        redraw()
        return

def show_entry(filename):
    '''
    call less on passed in filename
    '''

    subprocess.call(["less", filename])

    return

def view_feed():
    '''
    generate and display list of most recent global entries
    '''

    feedList = []

    for townie in core.find_ttbps():
        entryDir = os.path.join("/home", townie, ".ttbp", "entries")
        filenames = os.listdir(entryDir)

        for entry in filenames:
            if core.valid(entry):
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

    list_entries(metas, entries, "most recent global entries:")

    redraw()

    return

def graffiti_handler():
    '''
    Main graffiti handler.
    '''

    if os.path.isfile(WALL_LOCK):
        redraw("sorry, "+chatter.say("friend")+", but someone's there right now. try again in a few!")
    else:
        subprocess.call(["touch", WALL_LOCK])
        redraw()
        print("""\
the graffiti wall is a world-writeable text file. anyone can
scribble on it; anyone can move or delete things. please be
considerate of your neighbors when writing on it.

no one will be able to visit the wall while you are here, so don't
worry about overwriting someone else's work. anything you do to the
wall will be recorded if you save the file, and you can cancel
your changes by exiting without saving.

""")
        raw_input("press <enter> to visit the wall\n\n")
        subprocess.call([SETTINGS.get("editor"), WALL])
        subprocess.call(["rm", WALL_LOCK])
        redraw("thanks for visiting the graffiti wall!")


## misc helpers


def select_editor():
    '''
    setup helper for editor selection
    '''

    util.print_menu(EDITORS, RAINBOW)
    
    choice = util.list_select(EDITORS, "pick your favorite text editor: ")
    #choice = raw_input("\npick your favorite text editor: ")
    #while choice  not in ['0', '1', '2', '3', '4', '5']:
    #    choice = raw_input("\nplease pick a number from the list: ")

    if choice is False:
        redraw("please pick a text editor!")
        select_editor()

    return EDITORS[int(choice)]

def select_publish_dir():
    '''
    setup helper for publish directory selection
    '''

    current = SETTINGS.get("publish dir")
    republish = False

    if current:
        print("\ncurrent publish dir:\t"+os.path.join(PUBLIC, SETTINGS["publish dir"]))
        republish = True

    choice = raw_input("\nwhere do you want your blog published? (leave blank to use default \"blog\") ")
    if not choice:
        choice = "blog"

    publishDir = os.path.join(PUBLIC, choice)
    while os.path.exists(publishDir):
        second = raw_input("\n"+publishDir+"""\
 already exists!

setting this as your publishing directory means this program may
delete or overwrite file there!

if you're sure you want to use it, hit <enter> to confirm.
otherwise, pick another location: """)

        if second == "":
            break
        choice = second
        publishDir = os.path.join(PUBLIC, choice)

    return choice

def select_publishing():
    '''
    setup helper for toggling publishing
    '''

    publish = util.input_yn("""\
do you want to publish your feels online?

if yes, your feels will be published to a directory of your choice in
your public_html. i'll confirm the location of that directory in a
moment.

if not, your feels will only be readable from within the tilde.town
network. if you already have a publishing directory, i'll remove it for
you (don't worry, your written entries will still be saved!)

you can change this option any time.

please enter\
""")

    return publish

def unpublish():
    '''
    remove user's published directory, if it exists. this should only remove the symlink in public_html.
    '''

    dir = SETTINGS.get("publish dir")
    if dir:
        publishDir = os.path.join(PUBLIC, dir)
        subprocess.call(["rm", publishDir])

def update_publishing():
    '''
    updates publishing directory if user is publishing. otherwise, wipe it.
    '''

    global SETTINGS

    if core.publishing():
        oldDir = SETTINGS.get("publish dir")
        newDir = select_publish_dir()
        SETTINGS.update({"publish dir": newDir})
        if oldDir:
            subprocess.call(["rm", os.path.join(PUBLIC, oldDir)])
        make_publish_dir(newDir)
        core.load_files()
        core.write("index.html")
    else:
        unpublish()
        SETTINGS.update({"publish dir": None})

    core.load(SETTINGS)

def make_publish_dir(dir):
    '''
    setup helper to create publishing directory
    '''

    if not os.path.exists(WWW):
        subprocess.call(["mkdir", WWW])
        subprocess.call(["ln", "-s", os.path.join(CONFIG, "style.css"), os.path.join(WWW, "style.css")])
        subprocess.call(["touch", os.path.join(WWW, "index.html")])
        index = open(os.path.join(WWW, "index.html"), "w")
        index.write("<h1>ttbp blog placeholder</h1>")
        index.close()

    publishDir = os.path.join(PUBLIC, dir)
    if os.path.exists(publishDir):
        subprocess.call(["rm", publishDir])

    subprocess.call(["ln", "-s", WWW, publishDir])

    print("\n\tpublishing to "+LIVE+USER+"/"+SETTINGS.get("publish dir")+"/\n\n")

##### PATCHING UTILITIES

def build_mismatch():
    '''
    checks to see if user's last run build is the same as this session
    '''

    versionFile = os.path.join(PATH, "version")
    if not os.path.exists(versionFile):
        return False

    ver = open(versionFile, "r").read().rstrip()
    if ver[-1] == __version__[-1]:
        return False

    return ver

def switch_build(ver):
    '''
    switches user between beta and stable builds
    '''

    if __version__[-1] == 'b':
        build = "beta"
        ver += "b"
    else:
        build = "stable"
        ver = ver[0:-1]

    # write user versionfile
    print("\nswitching you over to the "+build+" version...\n")
    time.sleep(1)
    print("...")
    versionFile = os.path.join(PATH, "version")
    open(versionFile, "w").write(ver)
    time.sleep(1)
    #print("\nall good!\n")

def updated():
    '''
    checks to see if current user is up to the same version as system
    '''

    versionFile = os.path.join(PATH, "version")
    if not os.path.exists(versionFile):
        return False

    ver = open(versionFile, "r").read()

    if ver == __version__:
        return True

    return False

def update_version():
    '''
    updates user to current version
    '''

    global SETTINGS

    versionFile = os.path.join(PATH, "version")

    print("ttbp had some updates!")

    print("\ngive me a second to update you to version "+__version__+"...\n")

    time.sleep(1)
    print("...")
    time.sleep(2)

    userVersion = ""

    if not os.path.isfile(versionFile):
        # from 0.8.5 to 0.8.6:

        # change style.css location
        if os.path.isfile(os.path.join(WWW, "style.css")):
            subprocess.call(["mv", os.path.join(WWW, "style.css"), CONFIG])

        # change www symlink
        if os.path.exists(WWW):
            subprocess.call(["rm", WWW])
        
        subprocess.call(["mkdir", WWW])

        subprocess.call(["ln", "-s", os.path.join(CONFIG, "style.css"), os.path.join(WWW, "style.css")])

        publishDir = os.path.join(PUBLIC, SETTINGS.get("publish dir"))
        if os.path.exists(publishDir):
            subprocess.call(["rm", "-rf", publishDir])

        subprocess.call(["ln", "-s", WWW, os.path.join(PUBLIC, SETTINGS.get("publish dir"))])

        # repopulate html files
        core.load_files()
        core.write("index.html")

        # add publishing setting
        print("\nnew feature!\n")
        SETTINGS.update({"publishing":select_publishing()})
        update_publishing()
        ttbprc = open(TTBPRC, "w")
        ttbprc.write(json.dumps(SETTINGS, sort_keys=True, indent=2, separators=(',',':')))
        ttbprc.close()

    else: # version at least 0.8.6
        userVersion = open(versionFile, "r").read().rstrip()

        # from 0.8.6
        if userVersion == "0.8.6":
            print("\nresetting your publishing settings...\n")
            SETTINGS.update({"publishing":select_publishing()})
            update_publishing()
            ttbprc = open(TTBPRC, "w")
            ttbprc.write(json.dumps(SETTINGS, sort_keys=True, indent=2, separators=(',',':')))
            ttbprc.close()

    # increment user versionfile
    open(versionFile, "w").write(__version__)
    print("""
you're all good to go, """+chatter.say("friend")+"""! please contact ~endorphant if
somehing strange happened to you during this update.
""")

    # show patch notes
    #if userVersion != "0.9.0" and userVersion != "0.9.0b":
    if userVersion[0:5] < "0.9.0":
        # version 0.9.0 patch notes:
        print("""
ver. 0.9.0 features:
    * browsing other people's feels from neighbor view
    * documentation browser
        """)

    if userVersion[0:5] < "0.9.1":
        # version 0.9.1 patch notes
        print("""
ver 0.9.1 features:
    * graffiti wall
        """)

#####

if __name__ == '__main__':
    start()
    #print("ttbp beta is out to lunch. bbl.")
