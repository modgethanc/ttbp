#!/usr/bin/python

'''
ttbp: tilde town blogging platform
(also known as the feels engine)
a console-based blogging program developed for tilde.town
copyright (c) 2016 ~endorphant (endorphant@tilde.town)

atom.py:
Atom feed generation

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
from . import config
from . import util
from feedgen.feed import FeedGenerator
import os
import mistune
import datetime
import stat
import time

def publish_atom(entry_filenames, settings):
    fg = FeedGenerator()
    url = (config.LIVE + config.USER + '/' +
           str(settings.get("publish dir"))).rstrip('/')
    fg.id(url)
    fg.title("{}'s feels".format(config.USER))
    fg.author(name=config.USER)
    fg.link(href=url+'/', rel='alternate')
    fg.link(href=url+'/atom.xml', rel='self')
    fg.language('en') # TODO: feels language should be configurable

    for filename in sorted(entry_filenames):
        date = util.parse_date(filename)
        title = "-".join(date)
        name = "".join(date)

        path = os.path.join(config.MAIN_FEELS, filename)
        with open(path) as f:
            raw = f.read()
        html = mistune.markdown(raw)

        fe = fg.add_entry(order='prepend')
        fe.id(url+'/'+name)
        fe.link(href=url+'/'+name+'.html', rel="alternate")
        fe.title(title)
        fe.author(name=config.USER)
        fe.content(html, type="html")
        try: # crashing because of an invalid date would be sad
            fe.published("-".join(date)+"T00:00:00Z")
            stats = os.stat(path)
            updated = datetime.datetime.fromtimestamp(stats[stat.ST_MTIME],
                                                      datetime.timezone.utc)
            fe.updated(updated.strftime('%Y-%m-%dT%H:%M:%SZ'))
        except ValueError:
            pass
    outfile = os.path.join(config.WWW, 'atom.xml')
    fg.atom_file(outfile)

def select_atom():
    publish = util.input_yn("""
SETTING UP ATOM

Atom is a syndication format similar to RSS.
it is used so that people can subscribe to blogs and other news sources.

do you want to generate an atom feed for your feels along the HTML?
this setting only has effect if publishing is enabled.

you can change this option any time.
""")
    return publish
