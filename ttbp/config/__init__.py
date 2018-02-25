from __future__ import absolute_import
import os
import sys

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
GOPHER_PATH = os.path.join(USER_HOME, 'public_gopher', 'feels')
USER_CONFIG = os.path.join(PATH, 'config')
TTBPRC = os.path.join(USER_CONFIG, 'ttbprc')
USER_DATA = os.path.join(PATH, 'entries')
NOPUB = os.path.join(USER_CONFIG, "nopub")

## UI

BANNER = '''
___________________________________________________________
|                                                          |
|  the tilde.town                                          |
|  ____ ____ ____ _    ____    ____ _  _ ____ _ _  _ ____  |
|  |___ |___ |___ |    [__     |___ |\ | | __ | |\ | |___  |
|  |    |___ |___ |___ ___]    |___ | \| |__] | | \| |___  |
|                                    ver 0.11.1 (rainbows) |
|__________________________________________________________|
'''.lstrip()

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
        }
