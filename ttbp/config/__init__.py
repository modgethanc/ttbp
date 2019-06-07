from __future__ import absolute_import
import os
import sys
import time

from .. import util

## System config

# We refer to some package files (ie .css stuff), so we save a reference to the
# path.
INSTALL_PATH = os.path.dirname(sys.modules['ttbp'].__file__)

# We use this to store any persisted, global state.
VAR = '/var/global/ttbp'
VAR_WWW = os.path.join(VAR, 'www')

if not os.path.isdir('/var/global'):
    raise Exception('bad system state: /var/global does not exist.')

if not os.path.isdir(VAR):
    os.mkdir(VAR)

if not os.path.isdir(VAR_WWW):
    os.mkdir(VAR_WWW)

LIVE = 'https://tilde.town/~'
FEEDBOX = "endorphant@tilde.town"
USERFILE = os.path.join(VAR, "users.txt")
GRAFF_DIR = os.path.join(VAR, "graffiti")
WALL = os.path.join(GRAFF_DIR, "wall.txt")
WALL_LOCK = os.path.join(GRAFF_DIR, ".lock")

if not os.path.isdir(GRAFF_DIR):
    os.mkdir(GRAFF_DIR)

## Defaults

DEFAULT_HEADER = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2//EN">
<html>
  <head>
    <title>$USER on TTBP</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div id="meta">
      <h1><a href="#">~$USER</a>@<a href="/~endorphant/ttbp">TTBP</a></h1>
    </div>

    <div id="tlogs">
'''.lstrip()

DEFAULT_FOOTER = '''
    </div>
  </body>
</html>
'''.lstrip()

with open(os.path.join(INSTALL_PATH, 'config', 'defaults', 'style.css')) as f:
    DEFAULT_STYLE = f.read()


## User config

USER = os.path.basename(os.path.expanduser('~'))
USER_HOME = os.path.expanduser('~')
PATH = os.path.join(USER_HOME, '.ttbp')
PUBLIC = os.path.join(USER_HOME, 'public_html')
WWW = os.path.join(PATH, 'www')
GOPHER_ENTRIES = os.path.join(PATH, 'gopher')
GOPHER_PATH = os.path.join(USER_HOME, 'public_gopher', 'feels')
USER_CONFIG = os.path.join(PATH, 'config')
TTBPRC = os.path.join(USER_CONFIG, 'ttbprc')
MAIN_FEELS = os.path.join(PATH, 'entries')
BURIED_FEELS = os.path.join(PATH, 'buried')
NOPUB = os.path.join(USER_CONFIG, 'nopub')
BACKUPS = os.path.join(PATH, 'backups')
SUBS = os.path.join(USER_CONFIG, 'subs')

## UI

BANNER = '''
___________________________________________________________
|                                                          |
|  the tilde.town                                          |
|  ____ ____ ____ _    ____    ____ _  _ ____ _ _  _ ____  |
|  |___ |___ |___ |    [__     |___ |\ | | __ | |\ | |___  |
|  |    |___ |___ |___ ___]    |___ | \| |__] | | \| |___  |
|                            <gan jue; to feel> ver 0.12.2 |
|__________________________________________________________|
'''.lstrip()
#  ~ u n s t a b l e  e x p e r i m e n t a l  b r a n c h ~
#'''.lstrip()

## page texts

intro_prompt = """
i don't recognize you, stranger. let's make friends.

the feels engine is an internal blogging platform on tilde.town. it assists you
in recording your feels, giving you the option to publish to html or gopher, and
read the feels of other users on tilde.town.

press <enter> to set up an account, or <ctrl-c> to quit.
""".lstrip()

credits = """
ttbp was written for tilde.town by ~endorphant in python. the codebase is
publicly available on github at https://github.com/modgethanc/ttbp

tips for development are accepted at https://liberapay.com/modgethanc/

other contributors:
    ~vilmibm, packaging help and gopher support
    ~sanqui, the bug swatter
    ~sinacutie, for css updates

if you have ideas for ttbp, you are welcome to contact me to discuss them;
please send me tildemail or open a github issue. i am not a very experienced
developer, and ttbp is one of my first public-facing projects, so i appreciate
your patience while i learn how to be a better developer!

i'd love to hear about your ideas and brainstorm about new features!

thanks to everyone who reads, listens, writes, and feels."""

recording = """
feels will be recorded for today, {today}.

if you've already started recording feels for this day, you
can pick up where you left off.

you can write your feels in plaintext, markdown, html, or a mixture of
these.

press <enter> to begin recording your feels in your chosen text
editor.

""".format(today=time.strftime("%d %B %Y"))

bury_feels_prompt = """\
burying a feel removes it from view, including your own. buried feels are
stashed in a private directory at:
   
   {buried_dir}

you can visit your feels there from the command line, but no one else can view
those files.

(a buried feels browser is in the works; for now, you'll have to use the
command line to view your buried feels)

which day's feels do you want to bury?

YYYYMMDD (or 'q' to cancel)> """.format(buried_dir=BURIED_FEELS)

account_wipe_prompt = """\
warning! ! ! this action is irreversible!!!

this tool will remove your entire presence from the feels engine. this includes
all posts, settings, and published html/gopher feels. you will no longer be
listed anywhere as a user here.

there is no way for me to help you recover any part of your feels acccount. i
respect your need to do this from time to time, so please be sure you're ready!

i recommend that you make a backup of your feels and stash them somewhere safe,
just in case a future version of you still wants to look them over."""

feels_purge_prompt = """\
warning! ! ! this action is irreversible!!!

there is no way for me to help you recover your feels if you purge them all. i
respect your need to do this from time to time, so please be sure you're ready!

i recommend that you make a backup of your feels and stash them somewhere safe,
just in case a future version of you still wants to look them over.
"""

mystery_error = """\
sorry, something went wrong! please try to address the error and try again.
if you need help, ask in IRC or send mail to ~endorphant and we'll try to
figure it out!
""".lstrip()

## update announcements

UPDATES = {
        "0.9.0": """
ver. 0.9.0 features:
    * browsing other people's feels from neighbor view
    * documentation browser""",
        "0.9.1": """
ver 0.9.1 features:
    * graffiti wall """,
        "0.9.2": """
ver 0.9.2 features:
    * paginated entry view
    * improved entry listing performance so it should
      be less sluggish (for now)
    * expanded menu for viewing your own feels (further features to be implemented) """,
        "0.9.3": """
version 0.9.3 features:
        * ttbp is now packaged, making it easier to contribute to.
        * things should otherwise be the same!
        * check out https://github.com/modgethanc/ttbp if you'd like to contribute.
        * takes advantage of new /var/global """,
        "0.10.1": """
~[version 0.10.1 features]~
        * thanks to help from ~vilmibm, ttbp now supports publishing to gopher!
        * if you enable gopher publishing, feels will automatically publish to
            gopher://tilde.town/1/~{user}/feels
        * if you don't know what gopher is, it's fine to opt-out; ask around on
            irc if you'd like to learn more!
        * the settings menu has been reworked to be less clunky""",
        "0.11.0": """
~[version 0.11.0 update]~

    * rainbow menus are now an option! please message ~endorphant (with
        screencaps, if possible) if rainbow menus are unreadable with your
        terminal settings, so adjustments can be made for future updates
    * you can now set individual posts to be published or not published; this
        option is listed under 'review your feels' as 'modify feels publishing',
        and is only available if you have publishing turned on. if you toggle
        your publishing state, this list will persist. unpublished posts will
        be removed from html/gopher, but will still be accessible from within
        the feels engine.
    * some errors in selecting and validating settings and creating publishing
        directories have been corrected
    * please send mail to ~endorphant or ask for help on IRC if you're still
        having issues with getting your settings sorted out!

    general PSA:
        * join #ttbp on the local irc network for help and discussion about the
            feels engine!
        * ~login created centralfeels, which is an opt-in collection of
            html-published feels; create a blank file called '.centralfeels' in
            your home directory if you'd like to be included!""",
        "0.11.1": """
~[version 0.11.1 update]~

    * a quick patch to correct a directory listing error, nothing too
      exciting
    * general PSA: feel free to use the github repo for bugs/feature requests:
            https://github.com/modgethanc/ttbp/issues""",
        "0.11.2": """
~[version 0.11.2 update]~

    * added a new option to allow setting entries to default to either public or
      non-public on posting; this option only really makes sense if you're
      already publishing to html/gopher, but is available either way!

      you can find this option under 'settings' as 'post as nopub'.""",
        "0.11.3": """
~[version 0.11.3 update]~

    * thanks to ~sinacutie, you can now set custom css for the permalink text
      styling on your html page. the default permalink style has been added to
      your current css file, and shouldn't change the appearance of your page.

      if you're not using custom css, don't worry about this!""",
        "0.12.0": """
~[version 0.12.0 update]~

    a lot of new stuff this time! from the main menu, option (1) is now called
    "manage your feels", which contains an expanded set of tools for organizing
    your feels:
        * read over feels (a list of all your entries)
        * modify feels publishing (toggle privacy on individual entries)
        * backup your feels (makes a .tar.gz of all your entries)
        * import a feels backup (unpacks a backup into your feels)
        * bury some feels (hide individual entries from view)
        * delete feels by day (permanently remove individual entries)
        * purge all feels (permanently remove all entries)
        * wipe feels account (permanently remove everything associated with
          ttbp)

    each of these tools has expanded descriptions and instructions from the
    menu, so check them out if you're curious! all of the irreversibl data
    management actions have confirmation actions, so it's easy to cancel if you
    accidentally access a tool.

    also, i've updated the documentation file to reflect recent feature changes,
    including some more details about how things work under the hood, and some
    clarifications on how existing features work. please give it a read through
    if you have a chance, and let me know if there's anything else i can
    improve!

    lastly, i just wanted to mention that i do accept tips for my dev work at
    https://liberapay.com/modgethanc/ but there's no pressure to donate at all,
    i'm just making this option available for anyone whose financially stable
    and wants to kick some spare change my way; this is a labor of love, and i'm
    happy to work on it regardless :)
""",
        "0.12.1":"""
~[version 0.12.1 update]~

    new feature: "visit your subscriptions"
        * view recent entries from a list of townies you've subscribed to
        * subscription list is private; no one else can see who you're following
        * add/remove users from the subscription menu

    minor changes:
        * global feed now shows 50 most recent entries, which you can scroll through
        * documentation page updated to reflect new feature
        * graffiti wall lock releases after 3 days

    thanks for those of your who've written me with feedback!

    keep feelin' together <3
""",
        "0.12.2":"""
~[version 0.12.2 update]~

    bug fix: ~epicmorphism helped out with fixing the pagination bug! now, when
    you scroll through a list of entries, it'll correctly return you to the
    page you were on if you open and close an item. thanks so much, friend <3

    thanks to everyone writing me with feedback; i've been real busy lately,
    and i might not get to making improvements or responding to mail for a
    while :(

    feel on!
    ~endo
"""
}
