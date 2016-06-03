*a command-line based blogging platform running on tilde.town*

`ttbp` stands for "tilde.town blogging platform", the original working name for
this project.

to use, run `~endorphant/bin/ttbp` while logged in to tilde.town

you can also try `~endorphant/bin/ttbp-beta` for a more colorful, but
potentially volatile experience; i sometimes announce in irc or on twitter when
i'm testing a new feature.

### writing entries

entries are recorded as plaintext files in your ~/.ttbp/entries
directory. you can edit them there directly, or fix old entries, or
delete entries.

*warning*: changing old entries might cause strange things to
happen with timestamps. the main program looks at the filename
first for setting the date, then the last modified time to sort
recent posts. it expects YYYMMDD.txt as the filename; anything else
won't show up as a valid entry. yes, this means you can post things out
of date order by creating files with any date you want.

#### general entry-writing notes

* you can use [markdown](https://daringfireball.net/projects/markdown/syntax)
* you can use html
* you can also put things between `<!-- comments -->` to have them show up
in the feed but not render in a browser (but people can still read
them with view-source)

### privacy

when you start your ttbp, you have the option of publishing or not publishing
your blog.

if you opt to publish, the program creates a directory `~/.ttbp/www`
where it stores all html files it generates, and symlinks this from your
`~/public_html` with your chosen blog directory. your blog will also be listed
on the [main ttbp page](https://tilde.town/~endorphant/ttbp).

if you opt to not publish, your entires will never be accessible from outside
of the tilde.town network; other tilde.town users will still be able to read
your entries through the ttbp interface, or by directly accessing your
`~/.ttbp/entries` directory.

if you want to further protect your entries, you can `chmod 700` your entries
directory.

### changing your page layout

you can modify how your blog looks by editing the stylesheet or
header and footer files. the program sets you up with basic
default. if you break your page somehow, you can force the program to
regenerate your configuration by deleting your ~/.ttbp directory entirely.
**you might want to back up your ~/.ttbp/entries directory before you do
this.**

* to modify your stylesheet, edit your ~/.ttbp/config/style.css
  * (future feature: having multiple stylesheets you can select)
* to modify the page header, edit your ~/.ttbp/config/header.txt
  * you might note that there's a place marked off in the default header where
    you can safely put custom HTML elements!
* to modify the page footer, edit your ~/.ttbp/config/footer.txt

### general tips/troubleshooting

* add `alias ttbp="~endorphant/bin/ttbp"` to your .bash_aliases for fewer keystrokes
* (similarly, `alias ttbp-beta="~endorphant/bin/ttbp-beta"`)
* if the date looks like it's ahead or behind, it's because you haven't set
  your local timezone yet.  here are some
  [timezone setting instructions](http://www.cyberciti.biz/faq/linux-unix-set-tz-environment-variable/)

### dependencies

* [mistune](https://pypi.python.org/pypi/mistune)
* [inflect](https://pypi.python.org/pypi/inflect)

### future features

these are a few ideas being kicked around, or under active development:

* better entry privacy/publish control options
* stylesheet/theme selector
* responding to entries
* paginated list view
* better entry display within ttbp
