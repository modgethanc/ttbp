a command-line based blogging platform running on tilde.town

to use, run `~endorphant/bin/ttbp` while logged in to tilde.town

you can also try `~endorphant/bin/ttbp-beta` for a more unstable, bleeding-edge
experience.

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


### changing your page layout

you can modify how your blog looks by editing the stylesheet or
header and footer files. the program sets you up with basic
default. if you break your page somehow, you can force the program to
regenerate your configuration by deleting your ~/.ttbp directory entirely. **you might want to back up your ~/.ttbp/entries directory before you do this.**

* to modify your stylesheet, edit your ~/.ttbp/www/style.css
* to modify the page header, edit your ~/.ttbp/config/header.txt
  * you might note that there's a place marked off in the default header where you can safely put custom HTML elements!
* to modify the page footer, edit your ~/.ttbp/config/footer.txt

### general tips

* add `alias ttbp="~endorphant/bin/ttbp"` to your .bash_aliases for fewer keystrokes
