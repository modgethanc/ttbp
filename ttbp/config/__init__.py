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
USER_CONFIG = os.path.join(PATH, 'config')
TTBPRC = os.path.join(USER_CONFIG, 'ttbprc')
USER_DATA = os.path.join(PATH, 'entries')
NOPUB = os.path.join(USER_CONFIG, "nopub")

## UI

BANNER = '''
__________________________________________________________
|                                                          |
|  the tilde.town                                          |
|  ____ ____ ____ _    ____    ____ _  _ ____ _ _  _ ____  |
|  |___ |___ |___ |    [__     |___ |\ | | __ | |\ | |___  |
|  |    |___ |___ |___ ___]    |___ | \| |__] | | \| |___  |
|                            ver 0.10.0 (now with gophers) |
|__________________________________________________________|
'''.lstrip()
