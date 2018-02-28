#!/usr/bin/python

'''
ttbp: tilde town blogging platform
(also known as the feels engine)
a console-based blogging program developed for tilde.town
copyright (c) 2016 ~endorphant (endorphant@tilde.town)

ttbp.py:
the main console interface

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
from __future__ import absolute_import

import os
import tempfile
import subprocess
import time
import json
from email.mime.text import MIMEText
import datetime
from six.moves import input

import inflect

from . import config
from . import core
from . import chatter
from . import gopher
from . import util

__version__ = "0.11.2"
__author__ = "endorphant <endorphant@tilde.town)"

p = inflect.engine()

## ui globals
BANNER = util.attach_rainbow() + config.BANNER + util.attach_reset()
SPACER = "\n"
INVALID = "please pick a number from the list of options!\n\n"
DUST = "sorry about the dust, but this part is still under construction. check back later!\n\n"
QUITS = ['exit', 'quit', 'q', 'x']
EJECT = "eject button fired! going home now."
RAINBOW = False

## ref
EDITORS = ["nano", "vim", "vi", "emacs", "pico", "ed", "micro"]
SUBJECTS = ["help request", "bug report", "feature suggestion", "general comment"]
DEFAULT_SETTINGS = {
        "editor": "nano",
        "publish dir": None,
        "gopher": False,
        "publishing": False,
        "rainbows": False,
    }

## user globals
SETTINGS = {
        "editor": "nano",
        "publish dir": None,
        "gopher": False,
        "publishing": False,
        "rainbows": False
        }

## ttbp specific utilities

def menu_handler(options, prompt, pagify=10, rainbow=False, top=""):
    '''
    This menu handler takes an incoming list of options, pagifies to a
    pre-set value, and queries via the prompt. Calls print_menu() and
    list_select() as helpers.

    'top' is an optional list topper, to be passed to redraw()
    '''

    optCount = len(options)
    page = 0
    total = optCount / pagify

    # don't display empty pages
    if optCount % pagify == 0:
        total = total - 1

    if total < 1:
        util.print_menu(options, SETTINGS.get("rainbows", False))
        return util.list_select(options, prompt)

    else:
        return page_helper(options, prompt, pagify, rainbow, page, int(total), top)

def page_helper(options, prompt, pagify, rainbow, page, total, top):
    '''
    A helper to process pagination.

    'pagify' is the number of entries per page of display
    'page' is the current page number
    'total' is the total number of pages
    'top' is displyed after the banner redraw
    '''

    ## make short list
    x = 0 + page * pagify
    y = x + pagify
    optPage = options[x:y]

    util.print_menu(optPage, SETTINGS.get("rainbows", False))
    print("\n\t( page {page} of {total}; type 'u' or 'd' to scroll up and down)".format(page=page+1, total=total+1))

    ans = util.list_select(optPage, prompt)

    if ans in util.NAVS:
        error = ""
        if ans == 'u':
            if page == 0:
                error = "can't scroll up anymore!\n\n> "
            else:
                page = page - 1
        else:
            if page == total:
                error = "can't scroll down anymore!\n\n> "
            else:
                page = page + 1
        redraw(error+top)
        return page_helper(options, prompt, pagify, rainbow, page, total, top)

    elif ans is False:
        return ans

    else:
        # shift answer to refer to index from original list
        ans = ans + page * pagify

        return ans

def redraw(leftover=""):
    '''
    screen clearing

    * clears the screen and reprints the banner, plus whatever leftover text to be hilights
    '''

    os.system("clear")
    print(BANNER)
    print(SPACER)
    if leftover:
        print("> {leftover}\n".format(leftover=leftover))

def main():
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
    returns an exit message.
    '''

    return "\n\n\t"+chatter.say("bye")+"\n\n"

def check_init():
    '''
    user environment validation

    * checks for presence of ttbprc
    * checks for last run version
    '''

    print("\n\n")
    if os.path.exists(os.path.join(os.path.expanduser("~"),".ttbp")):
        if config.USER == "endorphant":
            print("hey boss! :D\n")
        else:
            print("{greeting}, {user}".format(greeting=chatter.say("greet"),
                user=config.USER))

        load_settings = load_user_settings()

        ## ttbp env validation
        if not user_up_to_date():
            update_user_version()

        if not valid_setup(load_settings):
            setup_repair()
        else:
            input("press <enter> to explore your feels.\n\n")

        core.load(SETTINGS)

        return ""
    else:
        return init()

def init():
    """Initializes new user by setting up ~/.ttbp directory and config file.
    """

    try:
        input("""
i don't recognize you, stranger. let's make friends.

press <enter> to begin, or <ctrl-c> to get out of here.""")
    except KeyboardInterrupt:
        print("\n\nthanks for checking in! i'll always be here.\n\n")
        quit()

    print("\nokay! gimme a second to get you set up!")

    time.sleep(1)
    print("...")
    time.sleep(1)

    ## record user in source list
    users = open(config.USERFILE, 'a')
    users.write(config.USER+"\n")
    users.close()

    #subprocess.call(['chmod', 'a+w', config.USERFILE])

    ## make .ttbp directory structure
    print("\ngenerating feels at {path}...".format(path=config.PATH).rstrip())
    subprocess.call(["mkdir", config.PATH])
    subprocess.call(["mkdir", config.USER_CONFIG])
    subprocess.call(["mkdir", config.USER_DATA])

    versionFile = os.path.join(config.PATH, "version")
    open(versionFile, "w").write(__version__)

    ## create header file
    header = gen_header()
    headerfile = open(os.path.join(config.USER_CONFIG, "header.txt"), 'w')
    for line in header:
        headerfile.write(line)
    headerfile.close()

    ## copy footer and default stylesheet
    with open(os.path.join(config.USER_CONFIG, 'footer.txt'), 'w') as f:
        f.write(config.DEFAULT_FOOTER)
    with open(os.path.join(config.USER_CONFIG, 'style.css'), 'w') as f:
        f.write(config.DEFAULT_STYLE)

    ## run user-interactive setup and load core engine
    time.sleep(1)
    print("done setting up feels!")
    print("\nthese are the default settings. you can change any of them now, or change them later at any time!!")
    setup()
    core.load(SETTINGS)

    input("\nyou're all good to go, "+chatter.say("friend")+"! hit <enter> to continue.\n\n")
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
        <title>~"""+config.USER+""" on TTBP</title>
        <link rel=\"stylesheet\" href=\"style.css\" />
    </head>
    <body>
        <div id=\"meta\">
            <h1><a href=\"index.html#\">~"""+config.USER+"""</a>@<a href=\"/~endorphant/ttbp\">TTBP</a></h1>
        </div>

        <!---put your custom html here-->



        <!---don't put anything after this line-->
        <div id=\"tlogs\">\
    """
    return header

def valid_setup(load_settings):
    '''
    Checks to see if user has a valid ttbp environment.
    '''

    if not load_settings:
        return False

    for option in iter(DEFAULT_SETTINGS):
        if option != "publish dir" and SETTINGS.get(option, None) is None:
            return False

    if core.publishing():
        if SETTINGS.get("publish dir", None) is None:
            print("CONFIG ERROR! publishing is enabled but no directory is set")
            return False

        if (not os.path.exists(config.WWW) or 
                not os.path.exists(os.path.join(config.PUBLIC,
                    SETTINGS.get("publish dir")))):
            print("something's weird with your publishing directories. let's try rebuilding them!")

            update_publishing()

    return True

def load_user_settings():
    """attempts to load user's ttbprc; returns settings dict if valie, otherwise
    returns false"""

    global SETTINGS

    if not os.path.isfile(config.TTBPRC):
        return False

    try:
        SETTINGS = json.load(open(config.TTBPRC))
    except ValueError:
        return False

    core.load(SETTINGS)

    return SETTINGS

def setup_repair():
    '''
    setup repair function

    * calls setup()
    * handles ^c
    '''

    global SETTINGS

    print("\nyour ttbp configuration doesn't look right. let me try to fix it....\n\n")

    time.sleep(1)

    settings_map = {
            "editor": select_editor,
            "publishing": select_publishing,
            "publish dir": select_publish_dir,
            "gopher": gopher.select_gopher,
            "rainbows": toggle_rainbows,
            "post as nopub": toggle_pub_default
            }

    for option in iter(settings_map):
        if SETTINGS.get(option, None) is None:
            SETTINGS.update({option: "NOT SET"})
            SETTINGS.update({option: settings_map[option]()})

    update_publishing()
    core.reload_ttbprc(SETTINGS)
    save_settings()

    print("...")
    time.sleep(1)
    input("\nyou're all good to go, "+chatter.say("friend")+"! hit <enter> to continue.\n\n")

def setup():
    '''
    master setup function

    * editor selection
    * publishing toggle (publish/unpublish as needed)
    * directory selection
    * gopher opt in/out

    TODO: break this out better?
    '''

    global SETTINGS

    menuOptions = []
    settingList = sorted(list(SETTINGS))

    for setting in settingList:
        menuOptions.append(setting + ": \t" + str(SETTINGS.get(setting)))
    util.print_menu(menuOptions, SETTINGS.get("rainbows", False))

    try:
        choice = input("\npick a setting to change (or type 'q' to exit): ")
    except KeyboardInterrupt:
        redraw(EJECT)
        return SETTINGS

    if choice in QUITS:
        redraw()
        return SETTINGS

    # editor selection
    if settingList[int(choice)] == "editor":
        SETTINGS.update({"editor": select_editor()})
        redraw("text editor set to: {editor}".format(editor=SETTINGS["editor"]))
        save_settings()
        return setup()

    # publishing selection
    elif settingList[int(choice)] == "publishing":
        SETTINGS.update({"publishing":select_publishing()})
        core.reload_ttbprc(SETTINGS)
        update_publishing()
        redraw("publishing set to {publishing}".format(publishing=SETTINGS.get("publishing")))
        save_settings()
        return setup()

    # publish dir selection
    elif settingList[int(choice)] == "publish dir":
        publish_dir = select_publish_dir()
        SETTINGS.update({"publish dir": publish_dir})
        #update_publishing()

        if publish_dir is None:
            redraw("sorry, i can't set a publish directory for you if you don't have html publishing enabled. please enable publishing to continue.")
        else:
            redraw("publishing your entries to {url}/index.html".format(
                url="/".join([config.LIVE+config.USER,
                        str(SETTINGS.get("publish dir"))])))
        save_settings()
        return setup()

    # gopher opt-in
    elif settingList[int(choice)] == "gopher":
        SETTINGS.update({'gopher': gopher.select_gopher()})
        redraw('gopher publishing set to: {gopher}'.format(gopher=SETTINGS['gopher']))
        update_gopher()
        save_settings()
        return setup()

    # rainbow menu selection
    elif settingList[int(choice)] == "rainbows":
        SETTINGS.update({"rainbows": toggle_rainbows()})
        redraw("rainbow menus set to {rainbow}".format(rainbow=SETTINGS.get("rainbows")))
        save_settings()
        return setup()

    #nopub toggling
    elif settingList[int(choice)] == "post as nopub":
        SETTINGS.update({"post as nopub": toggle_pub_default()})
        redraw("posting default set to {nopub}".format(nopub=SETTINGS.get("post as nopub")))
        save_settings()
        return setup()

    input("\nyou're all good to go, {friend}! hit <enter> to continue.\n\n".format(friend=chatter.say("friend")))
    redraw()

    return SETTINGS

def save_settings():
    """
    Save current settings.
    """

    ttbprc = open(config.TTBPRC, "w")
    ttbprc.write(json.dumps(SETTINGS, sort_keys=True, indent=2, separators=(',',':')))
    ttbprc.close()

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
            "scribble some graffiti",
            "change your settings",
            "send some feedback",
            "see credits",
            "read documentation"]

    print("you're at ttbp home. remember, you can always press <ctrl-c> to come back here.\n")
    util.print_menu(menuOptions, SETTINGS.get("rainbows", False))

    try:
        choice = input("\ntell me about your feels (or type 'q' to exit): ")
    except KeyboardInterrupt:
        redraw(EJECT)
        return main_menu()

    if choice == '0':
        redraw()
        today = time.strftime("%Y%m%d")
        write_entry(os.path.join(config.USER_DATA, today+".txt"))
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
            view_feels(config.USER)
    elif choice == '2':
        users = core.find_ttbps()
        prompt = "the following {usercount} {are} recording feels on ttbp:".format(
                usercount=p.no("user", len(users)),
                are=p.plural("is", len(users)))
        redraw(prompt)
        view_neighbors(users, prompt)
    elif choice == '3':
        redraw("most recent global entries")
        view_feed()
    elif choice == '4':
        graffiti_handler()
    elif choice == '5':
        redraw("now changing your settings. press <ctrl-c> if you didn't mean to do this.")
        core.load(setup()) # reload settings to core
    elif choice == '6':
        redraw("you're about to send mail to ~endorphant about ttbp")
        feedback_menu()
    elif choice == '7':
        redraw()
        show_credits()
    elif choice == '8':
        subprocess.call(["lynx", os.path.join(config.INSTALL_PATH, "..", "README.html")])
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

    util.print_menu(SUBJECTS, SETTINGS.get("rainbows", False))
    choice = input("\npick a category for your feedback: ")

    cat = ""
    if choice in ['0', '1', '2', '3']:
        cat = SUBJECTS[int(choice)]
        entered = input("""
composing a {mail_category} to ~endorphant.

press <enter> to open an external text editor. mail will be sent once you save and quit.

""".format(mail_category=cat))
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

    util.print_menu(menuOptions, SETTINGS.get("rainbows", False))

    choice = util.list_select(menuOptions, "what would you like to do with your feels? (or 'back' to return home) ")

    if choice is not False:
        if choice == 0:
            redraw("your recorded feels, listed by date:")
            view_feels(config.USER)
        elif choice == 1:
            redraw("publishing status of your feels:")
            list_nopubs(config.USER)
    else:
        redraw()
        return

    redraw(intro)
    return review_menu()

def view_neighbors(users, prompt):
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
            url = config.LIVE+user+"/"+userRC.get("publish dir")

        ## find last entry
        try:
            files = os.listdir(os.path.join("/home", user, ".ttbp", "entries"))
        except OSError:
            files = []
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

        userList.append(["\t~{user}{userpad}\t({ago}){urlpad}\t{url}".format(user=user,
            userpad=userpad, ago=ago, urlpad=urlpad, url=url), last, user])

    # sort user by most recent entry for display
    userList.sort(key = lambda userdata:userdata[1])
    userList.reverse()
    sortedUsers = []
    userIndex = []
    for user in userList:
        sortedUsers.append(user[0])
        userIndex.append(user[2])

    choice = menu_handler(sortedUsers, "pick a townie to browse their feels, or type 'back' or 'q' to go home: ", 15, SETTINGS.get("rainbows", False), prompt)

    if choice is not False:
        redraw("~{user}'s recorded feels, listed by date: \n".format(user=userIndex[choice]))
        view_feels(userIndex[choice])
        view_neighbors(users, prompt)
    else:
        redraw()
        return

def view_feels(townie):
    '''
    generates a list of all feels by given townie and displays in
    date order; allows selection of one feel to read.

    '''

    metas, owner = generate_feels_list(townie)

    if len(metas) > 0:
        entries = []
        for entry in metas:
            pub = ""
            if core.nopub(entry[0]):
                pub = "(nopub)"
            entries.append(""+entry[4]+" ("+p.no("word", entry[2])+") "+"\t"+pub)

        return list_entries(metas, entries, owner+" recorded feels, listed by date: ")
    else:
        redraw("no feels recorded by ~"+townie)

def generate_feels_list(user):
    """create a list of feels for display from the named user.
    """

    filenames = []
    showpub = False

    if user == config.USER:
        entryDir = config.USER_DATA
        owner = "your"
        if core.publishing():
            showpub = True
    else:
        owner = "~"+user+"'s"
        entryDir = os.path.join("/home", user, ".ttbp", "entries")

    for entry in os.listdir(entryDir):
        filenames.append(os.path.join(entryDir, entry))
    metas = core.meta(filenames)
    metas.sort(key = lambda entry:entry[4])
    metas.reverse()

    return metas, owner

def show_credits():
    '''
    prints author acknowledgements and commentary
    '''

    print("""
ttbp was written for tilde.town by ~endorphant in python. the codebase is
publicly available on github at https://github.com/modgethanc/ttbp

other contributors:
    ~vilmibm, packaging help and gopher support
    ~sanqui, the bug swatter

if you have ideas for ttbp, you are welcome to contact me to discuss them;
please send me tildemail or open a github issue. i am not a very experienced
developer, and ttbp is one of my first public-facing projects, so i appreciate
your patience while i learn how to be a better developer!

i'd love to hear about your ideas and brainstorm about new features!

thanks to everyone who reads, listens, writes, and feels.\
        """)

    input("\n\npress <enter> to go back home.\n\n")
    redraw()

    return

## handlers

def write_entry(entry=os.path.join(config.USER_DATA, "test.txt")):
    '''
    main feels-recording handler
    '''

    entered = input("""
feels will be recorded for today, {today}.

if you've already started recording feels for this day, you
can pick up where you left off.

you can write your feels in plaintext, markdown, html, or a mixture of
these.

press <enter> to begin recording your feels in your chosen text
editor.

""".format(today=time.strftime("%d %B %Y")))

    if entered:
        entryFile = open(entry, "a")
        entryFile.write("\n"+entered+"\n")
        entryFile.close()
    subprocess.call([SETTINGS.get("editor"), entry])

    left = ""

    if SETTINGS.get("post as nopub"):
        core.toggle_nopub(os.path.basename(entry))
    else:
        if core.publishing():
            core.write("index.html")
            left = "posted to {url}/index.html\n\n>".format(
                url="/".join(
                    [config.LIVE+config.USER,
                        str(SETTINGS.get("publish dir"))]))

        if SETTINGS.get('gopher'):
            gopher.publish_gopher('feels', core.get_files())
            left += " also posted to your ~/public_gopher!\n"

    core.load_files()
    redraw(left + " thanks for sharing your feels!")

    return

def list_nopubs(user):
    '''
    handler for toggling nopub on individual entries
    '''

    metas, owner = generate_feels_list(user)

    if len(metas) > 0:
        return set_nopubs(metas, user, "publishing status of your feels:")
    else:
        redraw("no feels recorded by ~"+user)

def set_nopubs(metas, user, prompt):
    """displays a list of entries for pub/nopub toggling.
    """

    entries = []
    for entry in metas:
        pub = ""
        if core.nopub(entry[0]):
            pub = "(nopub)"
        entries.append(""+entry[4]+" ("+p.no("word", entry[2])+") "+"\t"+pub)

    choice = menu_handler(entries, "pick an entry from the list, or type 'q' to go back: ", 10, SETTINGS.get("rainbows", False), prompt)

    if choice is not False:
        target = os.path.basename(metas[choice][0])
        action = core.toggle_nopub(target)
        redraw(prompt)

        core.write("index.html")
        if SETTINGS["gopher"]:
            gopher.publish_gopher('feels', core.get_files())

        return set_nopubs(metas, user, prompt)

    else:
        redraw()
        return

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
        mail['To'] = config.FEEDBOX
        mail['From'] = config.USER+"@tilde.town"
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
    displays a list of entries for reading selection, allowing user to select
    one for display.
    '''

    choice = menu_handler(entries, "pick an entry from the list, or type 'q' to go back: ", 10, SETTINGS.get("rainbows", False), prompt)

    if choice is not False:

        redraw("now reading ~{user}'s feels on {date}\n> press <q> to return to feels list.\n\n".format(user=metas[choice][5],
                    date=metas[choice][4]))

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
        try:
            filenames = os.listdir(entryDir)
        except OSError:
            filenames = []

        for entry in filenames:
            ## hardcoded display cutoff at 30 days
            if core.valid(entry):
                year = int(entry[0:4])
                month = int(entry[4:6])
                day = int(entry[6:8])
                datecheck = datetime.date(year, month, day)
                displayCutoff = datetime.date.today() - datetime.timedelta(days=30)

                if datecheck > displayCutoff:
                    feedList.append(os.path.join(entryDir, entry))

    metas = core.meta(feedList)
    metas.sort(key = lambda entry:entry[3])
    metas.reverse()

    entries = []
    for entry in metas[0:10]:
        pad = ""
        if len(entry[5]) < 8:
            pad = "\t"

        entries.append("~{user}{pad}\ton {date} ({wordcount})".format(
                user=entry[5], pad=pad, date=entry[3], 
                wordcount=p.no("word", entry[2])))

    list_entries(metas, entries, "most recent global entries:")

    redraw()

    return

def graffiti_handler():
    '''
    Main graffiti handler.
    '''

    if os.path.isfile(config.WALL_LOCK):
        redraw("sorry, {friend}, but someone's there right now. try again in a few!".format(friend=chatter.say("friend")))
    else:
        subprocess.call(["touch", config.WALL_LOCK])
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
        input("press <enter> to visit the wall\n\n")
        subprocess.call([SETTINGS.get("editor"), config.WALL])
        subprocess.call(["rm", config.WALL_LOCK])
        redraw("thanks for visiting the graffiti wall!")


## misc helpers

def toggle_pub_default():
    """setup helper for setting default publish privacy (does not apply
    retroactively).  """

    if SETTINGS.get("post as nopub", False) is True:
        (nopub, will) = ("(nopub)", "won't")
    else:
        (nopub, will) = ("public", "will")

    if SETTINGS.get("publishing", False) is True:
        publishing = ""
    else:
        publishing = """\
since you're currently not publishing your posts to html/gopher, this setting
won't affect the visibility of your posts.  however, the option is still here if
you'd like to change it.
"""

    print("""

DEFAULT POST PRIVACY

your entries are set to automatically post as {nopub}. this means they {will} be
posted to your world-visible pages at first (which you can always change after
the fact.)

this setting only affects subsequent posts; it does not apply retroactively.

{publishing}""".format(nopub=nopub, will=will, publishing=publishing))

    ans = util.input_yn("""\
would you like to change this behavior?

please enter""")

    if ans:
        return not SETTINGS.get("post as nopub")
    else:
        return SETTINGS.get("post as nopub")

def toggle_rainbows():
    """setup helper for rainbow toggling
    """

    if SETTINGS.get("rainbows", False) is True:
        status = "enabled"
    else:
        status = "disabled"

    print("\nRAINBOW MENU TOGGLING")
    print("rainbow menus are currently {status}".format(status=status))

    publish = util.input_yn("""\

would you like to have rainbow menus?

please enter\
""")

    return publish

def select_editor():
    '''
    setup helper for editor selection
    '''

    print("\nTEXT EDITOR SELECTION")
    print("your current editor is: "+SETTINGS.get("editor"))
    util.print_menu(EDITORS, SETTINGS.get("rainbows", False))
    choice = util.list_select(EDITORS, "pick your favorite text editor, or type 'q' to go back: ")

    if choice is False:
        # if selection is canceled, return either previously set editor or default
        return SETTINGS.get("editor", EDITORS[0])
    return EDITORS[int(choice)]

def select_publish_dir():
    '''
    setup helper for publish directory selection
    '''

    if not core.publishing():
        return None

    current = SETTINGS.get("publish dir")
    republish = False

    print("\nUPDATING HTML PATH")

    if current:
        print("\ncurrent publish dir:\t"+os.path.join(config.PUBLIC, SETTINGS["publish dir"]))
        republish = True

    choice = input("\nwhere do you want your blog published? (leave blank to use default \"blog\") ")
    if not choice:
        choice = "blog"

    publishDir = os.path.join(config.PUBLIC, choice)
    while os.path.exists(publishDir):
        second = input("\n"+publishDir+"""\
 already exists!

setting this as your publishing directory means this program may
delete or overwrite file there!

if you're sure you want to use it, hit <enter> to confirm.
otherwise, pick another location: """)

        if second == "":
            break
        choice = second
        publishDir = os.path.join(config.PUBLIC, choice)

    return choice

def select_publishing():
    '''
    setup helper for toggling publishing
    '''

    publish = util.input_yn("""\

SETTING UP PUBLISHING

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
    '''remove all published entries in html and gopher.
    '''

    global SETTINGS

    directory = SETTINGS.get("publish dir")

    if directory:
        publishDir = os.path.join(config.PUBLIC, directory)
        subprocess.call(["rm", publishDir])

    if SETTINGS.get("gopher"):
        SETTINGS.update({"gopher": False})
        subprocess.call(["rm", config.GOPHER_PATH])

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
            subprocess.call(["rm", os.path.join(config.PUBLIC, oldDir)])
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

    if not os.path.exists(config.WWW):
        subprocess.call(["mkdir", config.WWW])
        subprocess.call(["ln", "-s", os.path.join(config.USER_CONFIG, "style.css"), os.path.join(config.WWW, "style.css")])
        subprocess.call(["touch", os.path.join(config.WWW, "index.html")])
        index = open(os.path.join(config.WWW, "index.html"), "w")
        index.write("<h1>ttbp blog placeholder</h1>")
        index.close()

    publishDir = os.path.join(config.PUBLIC, dir)
    if os.path.exists(publishDir):
        subprocess.call(["rm", publishDir])

    subprocess.call(["ln", "-s", config.WWW, publishDir])

    print("\n\tpublishing to "+config.LIVE+config.USER+"/"+SETTINGS.get("publish dir")+"/\n\n")

def update_gopher():
    '''
    helper for toggling gopher settings
    '''
    # TODO for now i'm hardcoding where people's gopher stuff is generated. if
    # there is demand for this to be configurable we can expose that.
    if SETTINGS.get("gopher"):
        gopher.setup_gopher('feels')
        gopher.publish_gopher("feels", core.get_files())
    else:
        subprocess.call(["rm", config.GOPHER_PATH])
    redraw("gopher publishing set to {gopher}".format(gopher=SETTINGS.get("gopher")))

##### PATCHING UTILITIES

def user_up_to_date():
    '''
    checks to see if current user is up to the same version as system
    '''

    versionFile = os.path.join(config.PATH, "version")
    if not os.path.exists(versionFile):
        return False

    ver = open(versionFile, "r").read()

    if ver == __version__:
        return True

    return False

def update_user_version():
    '''
    updates user to current version, printing relevant release notes and
    stepping through new features.
    '''

    global SETTINGS

    versionFile = os.path.join(config.PATH, "version")

    print("ttbp had some updates!")

    print("\ngive me a second to update you to version "+__version__+"...\n")

    time.sleep(1)
    print("...")
    time.sleep(1)

    userVersion = ""
    (x, y, z) = [0, 0, 0]

    if not os.path.isfile(versionFile):
        # updates from 0.8.5 to 0.8.6, before versionfile existed

        # change style.css location
        if core.publishing():
            if os.path.isfile(os.path.join(config.WWW, "style.css")):
                subprocess.call(["mv", os.path.join(config.WWW, "style.css"), config.USER_CONFIG])

            # change www symlink
            if os.path.exists(config.WWW):
                subprocess.call(["rm", config.WWW])

            subprocess.call(["mkdir", config.WWW])

            subprocess.call(["ln", "-s", os.path.join(config.USER_CONFIG, "style.css"), os.path.join(config.WWW, "style.css")])

            publishDir = os.path.join(config.PUBLIC, SETTINGS.get("publish dir"))
            if os.path.exists(publishDir):
                subprocess.call(["rm", "-rf", publishDir])

            subprocess.call(["ln", "-s", config.WWW, os.path.join(config.PUBLIC, SETTINGS.get("publish dir"))])

            # repopulate html files
            core.load_files()
            core.write("index.html")

        # add publishing setting
        print("\nnew feature!\n")
        SETTINGS.update({"publishing":select_publishing()})
        update_publishing()
        ttbprc = open(config.TTBPRC, "w")
        ttbprc.write(json.dumps(SETTINGS, sort_keys=True, indent=2, separators=(',',':')))
        ttbprc.close()

    else: # version at least 0.8.6
        userVersion = open(versionFile, "r").read().rstrip()
        x, y, z = [int(num) for num in userVersion.split(".")]

        # from 0.8.6
        if userVersion == "0.8.6":
            print("\nresetting your publishing settings...\n")
            SETTINGS.update({"publishing":select_publishing()})
            update_publishing()
            ttbprc = open(config.TTBPRC, "w")
            ttbprc.write(json.dumps(SETTINGS, sort_keys=True, indent=2, separators=(',',':')))
            ttbprc.close()

        # from earlier than 0.10.1
        if y < 10:
            #  select gopher
            print("[ NEW FEATURE ]")
            print("""
    * thanks to help from ~vilmibm, ttbp now supports publishing to gopher!
    * if you enable gopher publishing, feels will automatically publish to
        gopher://tilde.town/1/~"""+config.USER+"""/feels

            """)
            SETTINGS.update({'gopher': gopher.select_gopher()})
            if SETTINGS.get('gopher'):
                print("opting into gopher: " + str(SETTINGS['gopher']))
                gopher.setup_gopher('feels')
            else:
                print("okay, passing on gopher for now. this option is available in settings if you change\nyour mind!")

        if y < 11:
            # set rainbow menu for 0.11.0
            print("[ NEW FEATURE ]")
            SETTINGS.update({"rainbows": toggle_rainbows()})

        if z < 2:
            # set default option for 0.11.2
            # print("default nopub: false")
            SETTINGS.update({"post as nopub": False})
            save_settings()

    print("""
you're all good to go, """+chatter.say("friend")+"""! please contact ~endorphant if
something strange happened to you during this update.
""")

    if y < 10:
        # version 0.10.1 patch notes
        print(config.UPDATES["0.10.1"])

    if y < 11:
        # version 0.11.0 patch notes
        print(config.UPDATES["0.11.0"])

    if y < 11 or z < 1:
        # version 0.11.1 patch notes
        print(config.UPDATES["0.11.1"])

    if y < 11 or z < 2:
        # version 0.11.2 patch notes
        print(config.UPDATES["0.11.2"])

    confirm = ""

    while confirm not in ("x", "<x>", "X", "<X>"):
        confirm = input("\nplease type <x> when you've finished reading about the updates! ")

    print("\n\n")

    open(versionFile, "w").write(__version__)

#####

if __name__ == '__main__':
    sys.exit(main())
